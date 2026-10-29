"use strict";
// Owns only a fresh regtest instance, public fixture key, and fresh evidence dir.
const fs = require("node:fs"),
  path = require("node:path"),
  os = require("node:os"),
  assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
if (process.platform === "win32") {
  const linux = (p) =>
    p
      .replaceAll("\\", "/")
      .replace(/^([A-Za-z]):/, (_, d) => "/mnt/" + d.toLowerCase());
  const result = spawnSync(
    "wsl.exe",
    [
      "-e",
      "bash",
      "-lc",
      'exec node "$@"',
      "mint-regtest",
      linux(__filename),
      ...process.argv.slice(2).map((p) => linux(path.resolve(p))),
    ],
    { stdio: "inherit", timeout: 360000 }
  );
  process.exit(result.status ?? 1);
}
const { S, bsv, pay, output } = require("../../vault/src/ordinal-pair");
const { SponsorPool, parsePrep } = require("../pool");
const { startNode } = require("./regtest-node");
async function main() {
  const evidence = path.resolve(
    process.argv[2] || path.join(__dirname, "../../evidence/mint-pool-regtest")
  );
  const node = await startNode(evidence);
  const { rpc, data } = node;
  let pool;
  const log = (name, value) =>
    fs.writeFileSync(
      path.join(evidence, name),
      JSON.stringify(value, null, 2) + "\n"
    );
  try {
    assert.equal((await rpc("getblockchaininfo")).chain, "regtest");
    assert.equal(await rpc("getconnectioncount"), 0);
    // Public scalar 1 fixture. NEVER FUND on a real network. WIF never leaves file.
    const key = new bsv.PrivateKey(new bsv.crypto.BN(1), bsv.Networks.testnet),
      script = pay(key.publicKey.toString()),
      address = key.toAddress().toString();
    const keyPath = path.join(data, "fixture.key");
    fs.writeFileSync(keyPath, key.toWIF(), { mode: 0o600 });
    const blocks = await rpc("generatetoaddress", [110, address]);
    const block = await rpc("getblock", [blocks[0]]);
    const coinbase = new bsv.Transaction(
      await rpc("getrawtransaction", [block.tx[0]])
    );
    assert.ok((await rpc("gettxout", [coinbase.id, 0])).confirmations >= 100);
    const root = new bsv.Transaction().addInput(
      new bsv.Transaction.Input({
        prevTxId: coinbase.id,
        outputIndex: 0,
        script: "",
        output: coinbase.outputs[0],
      })
    );
    for (let i = 0; i < 3; i++) root.addOutput(output(script, 100000));
    root.addOutput(output(script, coinbase.outputs[0].satoshis - 300000 - 500));
    root.inputs[0].setScript(
      bsv.Script.fromASM(
        S.signTx(
          root,
          key,
          coinbase.outputs[0].script,
          coinbase.outputs[0].satoshis,
          0
        ) +
          " " +
          key.publicKey
      )
    );
    assert.equal(
      await rpc("sendrawtransaction", [root.uncheckedSerialize()]),
      root.id
    );
    const mine = async () => {
      await new Promise((r) => setTimeout(r, 200));
      return rpc("generatetoaddress", [1, address]);
    };
    for (let i = 0; i < 5; i++) {
      await mine();
      if ((await rpc("getrawtransaction", [root.id, true])).confirmations > 0)
        break;
    }
    assert.ok(
      (await rpc("getrawtransaction", [root.id, true])).confirmations > 0
    );
    pool = new SponsorPool({
      keyPath,
      ledgerPath: path.join(evidence, "ledger.jsonl"),
      rpc,
      capSats: 300000,
    });
    const prepared = [];
    for (let i = 0; i < 3; i++) {
      const tx = await pool.prepare(root, i);
      prepared.push(tx);
      assert.ok((await rpc("getrawmempool")).includes(tx.id));
      assert.equal(
        parsePrep(tx.toBuffer(), key.publicKey.toString()).amount,
        99500
      );
    }
    assert.equal(await pool.dispense(), null);
    // Mine until all are included; depth must still gate them before K.
    for (let i = 0; i < 5; i++) {
      await mine();
      if ((await pool.refresh()).every((s) => s.confirmations > 0)) break;
    }
    const initial = await pool.refresh();
    assert.ok(initial.every((s) => s.confirmations > 0 && s.confirmations < 5));
    assert.equal(await pool.dispense(), null);
    while ((await pool.refresh()).some((s) => s.confirmations < 5))
      await mine();
    const outcomes = [];
    let actualInput = 0,
      actualOutput = 0;
    for (const tx of prepared) {
      const detail = await rpc("getrawtransaction", [tx.id, true]),
        mined = await rpc("getblock", [detail.blockhash]);
      assert.ok(detail.confirmations >= 5);
      assert.ok(mined.tx.includes(tx.id));
      assert.equal(detail.hex, tx.uncheckedSerialize());
      const previous = await rpc("getrawtransaction", [
        detail.vin[0].txid,
        true,
      ]);
      actualInput += Math.round(previous.vout[detail.vin[0].vout].value * 1e8);
      actualOutput += Math.round(detail.vout[0].value * 1e8);
      assert.equal(
        await rpc("gettxout", [root.id, tx.inputs[0].outputIndex]),
        null
      );
      const dispensed = await pool.dispense();
      assert.equal(dispensed.id, tx.id);
      parsePrep(dispensed.toBuffer(), key.publicKey.toString());
      outcomes.push({
        txid: tx.id,
        bytes: tx.toBuffer().length,
        confirmations: detail.confirmations,
        block: detail.blockhash,
        admitted: true,
        mined: true,
        grammar: true,
      });
    }
    assert.equal(await pool.dispense(), null);
    assert.deepEqual(pool.totals(), {
      inputSats: actualInput,
      prepFeeSats: actualInput - actualOutput,
      preparedSats: actualOutput,
      dispensedSats: actualOutput,
      heldSats: 0,
    });
    assert.equal(await rpc("verifychain", [4, 0]), true);
    assert.equal(await rpc("getconnectioncount"), 0);
    log("result.json", {
      status: "PASS",
      depth: 5,
      prepFee: 500,
      rootTxid: root.id,
      rootFee: 500,
      coinbaseTxid: coinbase.id,
      outcomes,
      ledger: pool.totals(),
      chainAccounting: {
        inputSats: actualInput,
        outputSats: actualOutput,
        prepFeeSats: actualInput - actualOutput,
      },
      boundary:
        "Isolated regtest only; public fixture key; no mainnet/miner policy or production-readiness claim.",
    });
    console.log(
      JSON.stringify({
        status: "PASS",
        preparations: prepared.length,
        depth: 5,
        ledger: pool.totals(),
        evidence,
      })
    );
  } catch (e) {
    log("failure.json", { error: e.message });
    throw e;
  } finally {
    pool?.close();
    await node.stop();
  }
}
main().catch((e) => {
  console.error(e.message);
  process.exitCode = 1;
});
