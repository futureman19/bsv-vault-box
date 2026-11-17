"use strict";
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict"),
  crypto = require("node:crypto");
const M = require("../../vault/src/ordinal-pair"),
  { verifyLaunch } = require("../../vault/src/launch-record");
if (process.argv.length !== 4)
  throw Error("Pass proof JSON and separately chosen trusted policy JSON");
const p = JSON.parse(fs.readFileSync(process.argv[2])),
  policy = JSON.parse(fs.readFileSync(process.argv[3]));
const parse = (raw) => {
  const tx = new M.bsv.Transaction(raw);
  assert.equal(tx.uncheckedSerialize(), raw);
  return tx;
};
const f = { foreign: parse(p.foreign), box: parse(p.box) };
const entries = p.steps.map((s) => parse(s.raw)),
  fundingParents = p.steps.map((s) => parse(s.fundingRaw));
const artifact = fs.readFileSync(
  path.join(__dirname, "../../vault/artifacts/ordinalPair.json")
);
const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
assert.equal(sha(artifact), p.artifact.fileSha256);
assert.equal(
  sha(JSON.stringify(JSON.parse(artifact))),
  p.artifact.normalizedSha256
);
assert.equal(
  sha(
    fs.readFileSync(
      path.join(__dirname, "../../vault/src/contracts/ordinalPair.ts")
    )
  ),
  p.artifact.sourceSha256
);
assert.equal(p.origin, f.foreign.id + "_0");
assert.deepEqual(
  p.steps.map((s) => s.stage),
  ["pack", "seal", "transfer", "open", "withdraw"]
);
const parents = [f.foreign, f.box, ...fundingParents],
  ledger = new M.Ledger(parents);
for (let i = 0; i < entries.length; i++) {
  const tx = entries[i],
    step = p.steps[i];
  assert.equal(tx.id, step.txid);
  assert.deepEqual(
    tx.inputs.map((x) => x.prevTxId.toString("hex") + ":" + x.outputIndex),
    step.inputs
  );
  assert.deepEqual(
    tx.outputs.map((x) => ({ satoshis: x.satoshis, script: x.script.toHex() })),
    step.outputs
  );
  assert.equal(tx.outputs[0].satoshis, 1);
  assert.equal(tx.outputs[1].satoshis, 1);
  assert.equal(
    M.verify(fundingParents[i], [parse(step.fundingRootRaw)]).success,
    true
  );
  ledger.accept(tx);
  const r = M.verifyHistory(f, entries.slice(0, i + 1), fundingParents);
  assert.equal(r.valid, true);
  assert.equal(r.origin, p.origin);
  assert.equal(r.ordinalInput, 0);
  assert.equal(r.ordinalOutput, 0);
}
assert.throws(() => ledger.accept(entries[2]), /conflicting/);
const result = verifyLaunch({ ...p, f, entries, fundingParents, policy });
assert.deepEqual(result, {
  originalIssuanceProvenance: true,
  originalManifestComplete: true,
  currentCustodyIntegrity: true,
});
console.log(
  JSON.stringify(
    {
      result,
      serializedTransactionsReplayed: entries.length,
      sponsorPreparationsReplayed: fundingParents.length,
      origin: p.origin,
      conflictingSpendRejected: true,
      liveChainChecked: false,
    },
    null,
    2
  )
);
