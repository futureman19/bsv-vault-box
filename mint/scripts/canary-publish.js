"use strict";
// Separate owner action for the four offline buyer-signed transactions. No keys.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict"),
  crypto = require("node:crypto");
const Canary = require("../canary"),
  M = require("../../vault/src/ordinal-pair");
const { createMainnetAdapter } = require("../broadcast");
const { durable } = require("../funded-runner");
const delay = (ms) => new Promise((r) => setTimeout(r, ms));
async function main(args = process.argv.slice(2)) {
  assert.equal(args[0], "--owner-authorized", "Owner authorization required");
  assert.equal(args.length, 3, "Expected ABS_SIGNED_JSON ABS_NEW_EVIDENCE");
  assert.ok(args.slice(1).every((p) => path.isAbsolute(p)));
  const bytes = fs.readFileSync(args[1]);
  const authorization = await Canary.authorizeRunner({
    chain: "mainnet",
    ownerAuthorized: true,
    binding: crypto.createHash("sha256").update(bytes).digest("hex"),
  });
  const rows = JSON.parse(bytes);
  assert.deepEqual(
    rows.map((r) => r.name),
    ["buyer-open-prep", "buyer-open", "buyer-withdraw-prep", "buyer-withdraw"]
  );
  fs.mkdirSync(args[2], { mode: 0o700 });
  const requests = [];
  const { rpc } = createMainnetAdapter({
    authorization,
    requests,
    fetchImpl: async (url, opts) => {
      await delay(1500);
      return fetch(url, opts);
    },
  });
  const log = (name, value) => durable(path.join(args[2], name), value);
  try {
    for (const [i, row] of rows.entries()) {
      const tx = new M.bsv.Transaction(row.raw);
      assert.equal(tx.id, row.txid);
      assert.equal(tx.inputs.length, i % 2 === 0 ? 1 : 3);
      const parents = [];
      let total = 0;
      for (const input of tx.inputs) {
        const id = input.prevTxId.toString("hex"),
          u = await rpc("gettxout", [id, input.outputIndex]);
        assert.ok(u && u.confirmations >= 1, "Input missing or spent");
        const p = new M.bsv.Transaction(await rpc("getrawtransaction", [id]));
        assert.equal(
          u.scriptPubKey.hex,
          p.outputs[input.outputIndex].script.toHex()
        );
        assert.equal(
          Math.round(u.value * 1e8),
          p.outputs[input.outputIndex].satoshis
        );
        total += p.outputs[input.outputIndex].satoshis;
        parents.push(p);
      }
      assert.equal(
        total - tx.outputs.reduce((n, o) => n + o.satoshis, 0),
        i % 2 === 0 ? 500 : 1000
      );
      assert.ok(M.verify(tx, parents).success);
      if (i % 2 === 1) {
        assert.equal(tx.inputs[2].prevTxId.toString("hex"), rows[i - 1].txid);
        assert.equal(tx.inputs[2].outputIndex, 0);
      }
      if (i === 3) {
        assert.equal(tx.inputs[0].prevTxId.toString("hex"), rows[1].txid);
        assert.equal(tx.inputs[1].prevTxId.toString("hex"), rows[1].txid);
      }
      log(row.name + "-intent.json", row);
      assert.equal(await rpc("sendrawtransaction", [row.raw]), tx.id);
      let included = false;
      for (let n = 0; n < 240; n++) {
        let d;
        try {
          d = await rpc("getrawtransaction", [tx.id, true]);
        } catch (e) {
          if (e.code !== -5) throw e;
        }
        if (d?.confirmations >= 1) {
          assert.equal(d.hex, row.raw);
          const block = await rpc("getblock", [d.blockhash]);
          assert.ok(block.confirmations >= 1 && block.tx.includes(tx.id));
          log(row.name + "-included.json", {
            txid: tx.id,
            blockhash: d.blockhash,
            confirmations: d.confirmations,
          });
          included = true;
          break;
        }
        await delay(15000);
      }
      assert.ok(included, "Inclusion deadline; reconcile, no retry");
    }
    log("result.json", { status: "BUYER_WITHDRAW_CONFIRMED" });
  } finally {
    log("requests.json", requests);
  }
}
module.exports = { main };
if (require.main === module)
  main().catch(() => {
    console.error(
      "Owner authorization required or publication halted; preserve intents and reconcile. No automatic retry."
    );
    process.exitCode = 1;
  });
