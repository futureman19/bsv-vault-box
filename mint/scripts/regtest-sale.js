"use strict";
// Only public fixture keys; fresh guarded official-node regtest, never live coins.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
if (process.platform === "win32") {
  const linux = (p) =>
    p
      .replaceAll("\\", "/")
      .replace(/^([A-Za-z]):/, (_, d) => "/mnt/" + d.toLowerCase());
  const r = spawnSync(
    "wsl.exe",
    [
      "-e",
      "bash",
      "-lc",
      'exec node "$@"',
      "sale-regtest",
      linux(__filename),
      ...process.argv.slice(2).map((p) => linux(path.resolve(p))),
    ],
    { stdio: "inherit", timeout: 360000 }
  );
  process.exit(r.status ?? 1);
}
const M = require("../../vault/src/ordinal-pair"),
  { bsv, S, C, pay, output, outpoint, transition } = M;
const { SponsorPool } = require("../pool"),
  { startNode } = require("./regtest-node");
const { SaleStore } = require("../sale"),
  { PaymentWatcher, RegtestTransport } = require("../watcher");
const { TransferWorker } = require("../transfer"),
  { createService } = require("../service");
async function main() {
  const evidence = path.resolve(
    process.argv[2] || path.join(__dirname, "../../evidence/mint-sale-regtest")
  );
  const node = await startNode(evidence),
    { rpc, data } = node;
  let pool, store, api;
  const log = (name, value) =>
    fs.writeFileSync(
      path.join(evidence, name),
      typeof value === "string" ? value : JSON.stringify(value, null, 2) + "\n"
    );
  const outcomes = [],
    chain = [],
    fundingParents = [];
  const f = M.fixture(),
    sponsor = new bsv.PrivateKey(new bsv.crypto.BN(3), bsv.Networks.testnet),
    buyer = f.bob,
    owner = f.alice;
  const keyPaths = ["inventory.key", "sponsor.key"].map((n) =>
    path.join(data, n)
  );
  try {
    for (const [i, key] of [owner, sponsor].entries())
      fs.writeFileSync(keyPaths[i], key.toWIF(), { mode: 0o600 });
    const address = owner.toAddress().toString();
    const mine = async () => {
      await new Promise((r) => setTimeout(r, 200));
      await rpc("generatetoaddress", [1, address]);
    };
    async function included(name, tx) {
      log(name + ".hex", tx.uncheckedSerialize() + "\n");
      let detail;
      for (let n = 0; n < 8; n++) {
        await mine();
        detail = await rpc("getrawtransaction", [tx.id, true]);
        if (detail.confirmations > 0) break;
      }
      assert.ok(detail.confirmations > 0);
      assert.equal(detail.hex, tx.uncheckedSerialize());
      assert.ok((await rpc("getblock", [detail.blockhash])).tx.includes(tx.id));
      outcomes.push({
        name,
        txid: tx.id,
        confirmations: detail.confirmations,
        block: detail.blockhash,
        bytes: tx.toBuffer().length,
      });
      return tx;
    }
    async function admit(name, tx) {
      assert.equal(
        await rpc("sendrawtransaction", [tx.uncheckedSerialize()]),
        tx.id
      );
      return included(name, tx);
    }
    function spend(parent, index, outs, key) {
      const tx = new bsv.Transaction().addInput(
        new bsv.Transaction.Input({
          prevTxId: parent.id,
          outputIndex: index,
          script: "",
          output: parent.outputs[index],
        })
      );
      for (const o of outs) tx.addOutput(o);
      tx.inputs[0].setScript(
        bsv.Script.fromASM(
          S.signTx(
            tx,
            key,
            parent.outputs[index].script,
            parent.outputs[index].satoshis,
            0
          ) +
            " " +
            key.publicKey
        )
      );
      return tx;
    }
    const blocks = await rpc("generatetoaddress", [110, address]),
      first = await rpc("getblock", [blocks[0]]),
      coinbase = new bsv.Transaction(
        await rpc("getrawtransaction", [first.tx[0]])
      );
    const root = await admit(
      "root",
      spend(
        coinbase,
        0,
        [
          output(pay(owner.publicKey.toString()), 1000000),
          output(pay(owner.publicKey.toString()), 1000000),
          ...Array.from({ length: 6 }, () =>
            output(pay(sponsor.publicKey.toString()), 100000)
          ),
          output(pay(buyer.publicKey.toString()), 100000),
          output(
            pay(owner.publicKey.toString()),
            coinbase.outputs[0].satoshis - 2700000 - 500
          ),
        ],
        owner
      )
    );
    f.foreign = await admit(
      "inscription",
      spend(
        root,
        0,
        [
          output(f.foreign.outputs[0].script),
          output(pay(owner.publicKey.toString()), 999499),
        ],
        owner
      )
    );
    const c = new C(outpoint(f.foreign, 0), 0n, owner.publicKey.toString());
    c.phase = 0n;
    c.owner = owner.publicKey.toString();
    f.box = await admit(
      "empty-box",
      spend(
        root,
        1,
        [
          output(c.lockingScript),
          output(pay(owner.publicKey.toString()), 999499),
        ],
        owner
      )
    );
    f.origin = f.foreign.id + "_0";
    pool = new SponsorPool({
      rpc,
      keyPath: keyPaths[1],
      ledgerPath: path.join(evidence, "pool.jsonl"),
      capSats: 600000,
      depth: 5,
    });
    for (let i = 2; i < 8; i++) {
      const p = await pool.prepare(root, i);
      fundingParents.push(p);
      log("prep-" + i + ".hex", p.uncheckedSerialize() + "\n");
    }
    for (let n = 0; n < 12; n++) {
      await mine();
      if ((await pool.refresh()).every((e) => e.confirmations >= 5)) break;
    }
    async function build(source, action, signer) {
      const funding = await pool.dispense();
      assert.ok(funding);
      const result = transition(
        f,
        source,
        action,
        signer,
        buyer.publicKey.toString(),
        null,
        undefined,
        {
          sponsor,
          funding: funding.outputs[0].satoshis,
          fee: 500,
          fundingTx: funding,
        }
      );
      return { ...result, funding };
    }
    const deposit = await build(null, 0, owner);
    await admit("deposit", deposit.tx);
    chain.push(deposit.tx);
    const seal = await build(deposit.tx, 1, owner);
    await admit("seal", seal.tx);
    chain.push(seal.tx);
    const hd = bsv.HDPrivateKey.fromSeed(
      Buffer.alloc(32, 7),
      bsv.Networks.testnet
    );
    store = new SaleStore({
      file: path.join(evidence, "sales.jsonl"),
      xpub: hd.hdPublicKey.toString(),
    });
    api = createService({
      store,
      inventory: [{ inventoryId: seal.tx.id, priceSats: 10000 }],
    });
    await api.listen(0);
    const base = "http://127.0.0.1:" + api.address().port;
    assert.equal(
      (await (await fetch(base + "/health")).json()).service,
      "boxsv-mint"
    );
    let response = await fetch(base + "/v1/boxes", { method: "POST" });
    assert.equal(response.status, 201);
    const listing = await response.json();
    response = await fetch(base + "/v1/boxes", {
      method: "POST",
      body: JSON.stringify({
        id: listing.id,
        buyerPubkey: buyer.publicKey.toString(),
      }),
    });
    assert.equal(response.status, 201);
    const transport = new RegtestTransport({
      rpc,
      startHeight: (await rpc("getblockchaininfo")).blocks + 1,
    });
    const watcher = new PaymentWatcher({ transport, depth: 1 });
    watcher.watch(store.get(listing.id));
    const payment = spend(
      root,
      8,
      [
        output(bsv.Script.buildPublicKeyHashOut(listing.payAddress), 10000),
        output(pay(buyer.publicKey.toString()), 89500),
      ],
      buyer
    );
    await rpc("sendrawtransaction", [payment.uncheckedSerialize()]);
    await watcher.poll((e) => store.payment(e.id, e));
    assert.equal(store.get(listing.id).state, "LISTED");
    await included("buyer-payment", payment);
    const events = [];
    await watcher.poll((e) => {
      events.push(e);
      store.payment(e.id, e);
    });
    assert.equal(events.length, 1);
    assert.equal(store.get(listing.id).state, "PAID_PENDING");
    log("payment-events.json", events);
    const worker = new TransferWorker({
      store,
      rpc,
      pool,
      inventory: () => ({ f, source: seal.tx }),
      inventoryKeyPath: keyPaths[0],
      sponsorKeyPath: keyPaths[1],
      paymentTransport: transport,
    });
    await worker.run(listing.id);
    assert.equal(store.get(listing.id).state, "PAID_PENDING");
    const transfer = new bsv.Transaction(store.get(listing.id).transfer.raw);
    await included("transfer", transfer);
    await worker.run(listing.id);
    assert.equal(store.get(listing.id).state, "TRANSFERRED");
    chain.push(transfer);
    // Attack against UNSPENT pair, so rejection proves Script authorization, not conflict.
    const attack = await build(transfer, 3, owner);
    assert.equal(attack.result.success, false);
    for (let i = 0; i < 2; i++)
      assert.ok(await rpc("gettxout", [transfer.id, i]));
    let rejection;
    try {
      await rpc("sendrawtransaction", [attack.tx.uncheckedSerialize()]);
    } catch (e) {
      rejection = { code: e.code, message: e.message };
    }
    assert.equal(rejection?.code, -26);
    assert.ok(!(await rpc("getrawmempool")).includes(attack.tx.id));
    for (let i = 0; i < 2; i++)
      assert.ok(await rpc("gettxout", [transfer.id, i]));
    log("old-owner-open.hex", attack.tx.uncheckedSerialize() + "\n");
    log("old-owner-rejection.json", rejection);
    const opened = await build(transfer, 3, buyer);
    assert.ok(opened.result.success);
    await admit("buyer-open", opened.tx);
    chain.push(opened.tx);
    await worker.observeOpen(
      listing.id,
      opened.tx.uncheckedSerialize(),
      opened.funding.uncheckedSerialize()
    );
    assert.equal(store.get(listing.id).state, "OPENED");
    const withdrawal = await build(opened.tx, 4, buyer);
    assert.ok(withdrawal.result.success);
    await admit("buyer-withdraw", withdrawal.tx);
    chain.push(withdrawal.tx);
    const final = [];
    for (let i = 0; i < 2; i++) {
      const u = await rpc("gettxout", [withdrawal.tx.id, i]);
      assert.equal(u.value, 0.00000001);
      assert.equal(u.scriptPubKey.hex, pay(buyer.publicKey.toString()).toHex());
      final.push(u);
    }
    assert.equal(M.verifyHistory(f, chain, fundingParents).valid, true);
    assert.equal(await rpc("verifychain", [4, 0]), true);
    assert.equal(await rpc("getconnectioncount"), 0);
    const status = await (await fetch(base + "/v1/boxes/" + listing.id)).json();
    assert.equal(status.state, "OPENED");
    log("api-status.json", status);
    log("result.json", {
      status: "PASS",
      origin: f.origin,
      outcomes,
      oldOwnerRejected: rejection,
      finalUTXOs: final,
      pool: pool.totals(),
      saleState: status.state,
      boundary:
        "Official guarded v1.2.3 isolated regtest only; public fixture keys; no miner-policy or production-readiness claim.",
    });
    console.log(
      JSON.stringify({
        status: "PASS",
        saleState: status.state,
        evidence,
        transitions: chain.length,
        oldOwnerRejected: true,
      })
    );
  } catch (e) {
    log("failure.json", { error: e.stack, outcomes });
    throw e;
  } finally {
    if (api) await api.close();
    store?.close();
    pool?.close();
    for (const p of keyPaths) if (fs.existsSync(p)) fs.unlinkSync(p);
    await node.stop();
  }
}
main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
