"use strict";
// Public-fixture harness. The production runner receives NO buyer private key.
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const M = require("../../vault/src/ordinal-pair"),
  { bsv, output, pay } = M;
const { startNode } = require("./regtest-node");
const { runCanary, spend, durable } = require("../funded-runner");
const { preflight, configuration } = require("./canary-preflight");
async function main(evidence) {
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
        "funded-rehearsal",
        linux(path.join(__dirname, "canary-run.js")),
        "--owner-authorized",
        "--regtest-rehearsal",
        linux(path.resolve(evidence)),
      ],
      { stdio: "inherit", timeout: 360000 }
    );
    assert.equal(r.status, 0, "WSL rehearsal failed");
    return;
  }
  assert.ok(path.isAbsolute(evidence));
  assert.ok(!fs.existsSync(evidence));
  fs.mkdirSync(evidence, { recursive: true });
  const node = await startNode(path.join(evidence, "node"));
  const rpc = node.rpc;
  const key = (n) =>
    new bsv.PrivateKey(new bsv.crypto.BN(n), bsv.Networks.testnet);
  const owner = key(101),
    sponsor = key(102),
    buyer = key(104),
    miner = key(109);
  const config = {
    inventoryKeyPath: path.join(node.data, "inventory.wif"),
    sponsorKeyPath: path.join(node.data, "sponsor.wif"),
    buyerPubkey: buyer.publicKey.toString(),
    paymentXpub: bsv.HDPrivateKey.fromSeed(
      Buffer.alloc(32, 103),
      bsv.Networks.testnet
    ).hdPublicKey.toString(),
  };
  const buyerPath = path.join(node.data, "offline-buyer.wif");
  const log = (name, v) => durable(path.join(evidence, name), v);
  let outcomes = [];
  try {
    for (const [p, k] of [
      [config.inventoryKeyPath, owner],
      [config.sponsorKeyPath, sponsor],
      [buyerPath, buyer],
    ])
      fs.writeFileSync(p, k.toWIF(), { mode: 0o600, flag: "wx" });
    const tick = async () => {
      await new Promise((r) => setTimeout(r, 200));
      await rpc("generatetoaddress", [1, miner.toAddress().toString()]);
    };
    async function admit(name, tx) {
      assert.equal(
        await rpc("sendrawtransaction", [tx.uncheckedSerialize()]),
        tx.id
      );
      for (let i = 0; i < 10; i++) {
        await tick();
        const d = await rpc("getrawtransaction", [tx.id, true]);
        if (d.confirmations > 0) {
          log(name + ".hex", tx.uncheckedSerialize() + "\n");
          outcomes.push({
            name,
            txid: tx.id,
            confirmations: d.confirmations,
            blockhash: d.blockhash,
          });
          return tx;
        }
      }
      throw Error("Not included");
    }
    const blocks = await rpc("generatetoaddress", [
      110,
      miner.toAddress().toString(),
    ]);
    const first = await rpc("getblock", [blocks[0]]),
      coinbase = new bsv.Transaction(
        await rpc("getrawtransaction", [first.tx[0]])
      );
    const outs = [
      ...Array.from({ length: 2 }, () =>
        output(pay(owner.publicKey.toString()), 60000)
      ),
      ...Array.from({ length: 3 }, () =>
        output(pay(sponsor.publicKey.toString()), 50500)
      ),
      output(pay(buyer.publicKey.toString()), 20000),
      output(pay(buyer.publicKey.toString()), 1500),
      output(pay(buyer.publicKey.toString()), 1500),
    ];
    outs.push(
      output(
        pay(miner.publicKey.toString()),
        coinbase.outputs[0].satoshis -
          outs.reduce((a, o) => a + o.satoshis, 0) -
          500
      )
    );
    const root = await admit("funding", spend(coinbase, 0, outs, miner));
    const transport = {
      async json(route) {
        if (route === "chain/info") return rpc("getblockchaininfo");
        const match = /^address\/([^/]+)\/unspent$/.exec(route);
        assert.ok(match, "Unsupported local read");
        const script = bsv.Script.buildPublicKeyHashOut(match[1]).toHex(),
          rows = [];
        const info = await rpc("getblockchaininfo");
        const seen = new Set();
        const inspect = async (id, height) => {
          if (seen.has(id)) return;
          seen.add(id);
          const tx = new bsv.Transaction(await rpc("getrawtransaction", [id]));
          if (tx.isCoinbase()) return;
          for (let index = 0; index < tx.outputs.length; index++) {
            const o = tx.outputs[index];
            if (o.script.toHex() !== script) continue;
            const u = await rpc("gettxout", [id, index]);
            if (u)
              rows.push({
                tx_hash: id,
                tx_pos: index,
                value: o.satoshis,
                height,
              });
          }
        };
        for (let h = 111; h <= info.blocks; h++) {
          const block = await rpc("getblock", [await rpc("getblockhash", [h])]);
          for (const id of block.tx) await inspect(id, h);
        }
        for (const id of await rpc("getrawmempool")) await inspect(id, 0);
        return rows.sort(
          (a, b) => a.tx_hash.localeCompare(b.tx_hash) || a.tx_pos - b.tx_pos
        );
      },
      async transactionEvidence(id) {
        const d = await rpc("getrawtransaction", [id, true]);
        assert.ok(d.confirmations >= 1);
        const block = await rpc("getblock", [d.blockhash]);
        assert.ok(block.tx.includes(id));
        return { raw: d.hex, detail: d, block, confirmations: d.confirmations };
      },
    };
    await assert.rejects(
      preflight(config, {
        chain: "regtest",
        stage: "startup",
        localTransport: transport,
      }),
      /Incorrect funding shape/
    );
    log("onchain-funding-refusal.json", {
      status: "PASS",
      source: root.id,
      observedSponsorSats: [50500, 50500, 50500],
      requiredSponsorSats: [50000, 50000, 50000],
      runnerBroadcasts: 0,
    });
    // Correct only disposable local fixture funding; never an automatic runner repair.
    for (let i = 2; i < 5; i++)
      await admit(
        "funding-correction-" + i,
        spend(
          root,
          i,
          [output(pay(sponsor.publicKey.toString()), 50000)],
          sponsor
        )
      );
    const report = await preflight(config, {
      chain: "regtest",
      stage: "startup",
      localTransport: transport,
    });
    log("preflight.json", report);
    let paymentSent = false;
    const local = {
      rpc,
      transport,
      tick,
      onReservation: async (r) => {
        assert.ok(!paymentSent);
        paymentSent = true;
        await admit(
          "payment",
          spend(
            root,
            5,
            [
              output(bsv.Script.buildPublicKeyHashOut(r.payAddress), 10000),
              output(pay(buyer.publicKey.toString()), 9500),
            ],
            buyer
          )
        );
      },
    };
    let refusedCalls = 0;
    const refusingLocal = {
      ...local,
      rpc: async (...args) => {
        refusedCalls++;
        return rpc(...args);
      },
      transport: {
        json: async (...args) => {
          refusedCalls++;
          return transport.json(...args);
        },
        transactionEvidence: async (...args) => {
          refusedCalls++;
          return transport.transactionEvidence(...args);
        },
      },
    };
    await assert.rejects(
      runCanary({
        config,
        report,
        evidence: path.join(evidence, "absent-gate"),
        chain: "regtest",
        local: refusingLocal,
      }),
      /Owner authorization/
    );
    assert.equal(refusedCalls, 0);
    log("owner-gate-refusal.json", {
      status: "PASS",
      networkCallsBeforeRefusal: refusedCalls,
      reason: "Absent explicit authorization",
    });
    const wrong = structuredClone(report);
    wrong.funding.sponsor.expectedSatoshis = [150000];
    await assert.rejects(
      runCanary({
        config,
        report: wrong,
        evidence: path.join(evidence, "wrong-funding"),
        chain: "regtest",
        local,
        ownerAuthorized: true,
        rehearsal: true,
      })
    );
    assert.ok(!fs.existsSync(path.join(evidence, "wrong-funding")));
    log("funding-gate-refusal.json", {
      status: "PASS",
      reason: "Nonexact sponsor shape; no runner evidence or broadcasts",
    });
    const bundle = await runCanary({
      config,
      report,
      evidence: path.join(evidence, "runner"),
      chain: "regtest",
      local,
      ownerAuthorized: true,
      rehearsal: true,
    });
    // Separate offline wallet process; only signed transactions return.
    const sources = [
      { raw: root.uncheckedSerialize(), index: 6 },
      { raw: root.uncheckedSerialize(), index: 7 },
    ];
    log("buyer-fee-sources.json", sources);
    const signedPath = path.join(evidence, "buyer-signed.json");
    const child = spawnSync(
      process.execPath,
      [
        path.join(__dirname, "canary-buyer.js"),
        path.join(evidence, "runner/buyer-bundle.json"),
        buyerPath,
        path.join(evidence, "buyer-fee-sources.json"),
        signedPath,
      ],
      { encoding: "utf8" }
    );
    assert.equal(child.status, 0, child.stderr);
    log("offline-wallet.txt", child.stdout);
    const signed = JSON.parse(fs.readFileSync(signedPath, "utf8"));
    for (const row of signed)
      await admit(row.name, new bsv.Transaction(row.raw));
    const withdrawal = new bsv.Transaction(signed.at(-1).raw),
      final = [];
    for (let i = 0; i < 2; i++) {
      const u = await rpc("gettxout", [withdrawal.id, i]);
      assert.equal(u.value, 0.00000001);
      assert.equal(u.scriptPubKey.hex, pay(buyer.publicKey.toString()).toHex());
      final.push(u);
    }
    const history = [
      ...bundle.history.map((r) => new bsv.Transaction(r)),
      new bsv.Transaction(signed[1].raw),
      withdrawal,
    ];
    const parents = [
      ...bundle.fundingParents.map((r) => new bsv.Transaction(r)),
      new bsv.Transaction(signed[0].raw),
      new bsv.Transaction(signed[2].raw),
    ];
    assert.ok(
      M.verifyHistory(
        {
          foreign: new bsv.Transaction(bundle.foreign),
          box: new bsv.Transaction(bundle.box),
        },
        history,
        parents
      ).valid
    );
    assert.equal(await rpc("verifychain", [4, 0]), true);
    assert.equal(await rpc("getconnectioncount"), 0);
    log("result.json", {
      status: "PASS",
      throughSameRunner: true,
      runnerEnds: "TRANSFER_CONFIRMED",
      buyerCompletion: "separate offline-wallet process",
      mainnetWrites: 0,
      outcomes,
      finalUTXOs: final,
      historyValid: true,
    });
    console.log(
      JSON.stringify({
        status: "PASS",
        evidence,
        runner: "TRANSFER_CONFIRMED",
        offlineBuyer: "WITHDRAWN",
      })
    );
  } finally {
    for (const p of [config.inventoryKeyPath, config.sponsorKeyPath, buyerPath])
      if (fs.existsSync(p)) fs.unlinkSync(p);
    await node.stop();
  }
}
module.exports = { main };
