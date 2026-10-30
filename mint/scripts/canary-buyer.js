"use strict";
// Offline owner wallet ONLY. No HTTP/RPC imports. Never invoked by funded-runner.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const M = require("../../vault/src/ordinal-pair"),
  Canary = require("../canary");
const { loadKey } = require("../keys"),
  { buildPrep } = require("../pool");
function buildBuyer(bundle, key, sources) {
  const policy = Canary.policy({
    chain: bundle.chain,
    canary: bundle.chain === "mainnet",
  });
  assert.equal(key.publicKey.toString(), bundle.buyerPubkey, "Wrong buyer");
  assert.equal(sources.length, 2);
  assert.equal(
    new Set(sources.map((s) => new M.bsv.Transaction(s.raw).id + ":" + s.index))
      .size,
    2,
    "Buyer fee sources must be distinct"
  );
  const f = {
    foreign: new M.bsv.Transaction(bundle.foreign),
    box: new M.bsv.Transaction(bundle.box),
  };
  const history = bundle.history.map((r) => new M.bsv.Transaction(r)),
    parents = bundle.fundingParents.map((r) => new M.bsv.Transaction(r));
  assert.ok(M.verifyHistory(f, history, parents).valid);
  let prior = new M.bsv.Transaction(bundle.transfer);
  assert.equal(prior.id, history.at(-1).id);
  assert.equal(
    M.C.fromHex(prior.outputs[0].script.toHex()).owner,
    bundle.buyerPubkey
  );
  const signed = [];
  for (const [i, source] of sources.entries()) {
    const parent = new M.bsv.Transaction(source.raw);
    assert.equal(parent.outputs[source.index].satoshis, 1500);
    const prep = buildPrep(parent, source.index, key, 500, policy);
    parents.push(prep);
    const result = M.transition(
      f,
      prior,
      i === 0 ? 3 : 4,
      key,
      bundle.buyerPubkey,
      null,
      undefined,
      { sponsor: key, funding: 1000, fee: 1000, fundingTx: prep }
    );
    assert.ok(result.result.success);
    history.push(result.tx);
    signed.push({
      name: i === 0 ? "buyer-open-prep" : "buyer-withdraw-prep",
      raw: prep.uncheckedSerialize(),
      txid: prep.id,
      fee: 500,
    });
    signed.push({
      name: i === 0 ? "buyer-open" : "buyer-withdraw",
      raw: result.tx.uncheckedSerialize(),
      txid: result.tx.id,
      fee: 1000,
    });
    prior = result.tx;
  }
  assert.ok(M.verifyHistory(f, history, parents).valid);
  return signed;
}
function main(args = process.argv.slice(2)) {
  assert.equal(
    args.length,
    4,
    "Offline: ABS_BUYER_BUNDLE ABS_BUYER_WIF ABS_FEE_SOURCES_JSON ABS_NEW_SIGNED_JSON"
  );
  assert.ok(args.every((p) => path.isAbsolute(p)));
  const bundle = JSON.parse(fs.readFileSync(args[0], "utf8")),
    policy = Canary.policy({
      chain: bundle.chain,
      canary: bundle.chain === "mainnet",
    });
  const signed = buildBuyer(
    bundle,
    loadKey(args[1], policy),
    JSON.parse(fs.readFileSync(args[2], "utf8"))
  );
  fs.writeFileSync(args[3], JSON.stringify(signed, null, 2) + "\n", {
    flag: "wx",
    mode: 0o600,
  });
  console.log(
    "Offline signed only. Independently verify all inputs/fees. Publish each in order and wait for confirmation; do not hand buyer keys to service."
  );
}
module.exports = { buildBuyer, main };
if (require.main === module) {
  try {
    main();
  } catch {
    console.error("Offline buyer build refused");
    process.exitCode = 1;
  }
}
