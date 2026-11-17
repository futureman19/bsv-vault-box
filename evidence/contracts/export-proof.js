"use strict";
// Local deterministic fixture only. Never run a funded/key/network entrypoint.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const { fixture, sha } = require("../../vault/tests/launch-fixture");
const M = require("../../vault/src/ordinal-pair");
const p = fixture();
const raw = (t) => t.uncheckedSerialize();
const phases = ["pack", "seal", "transfer", "open", "withdraw"];
const artifact = fs.readFileSync(
  path.resolve(__dirname, "../../vault/artifacts/ordinalPair.json")
);
const packet = {
  scope:
    "synthetic local VM proof; no live chain unspentness, no issuance, no media storage",
  metadata: p.metadata,
  envelope: p.envelope,
  mediaHashes: p.mediaHashes,
  foreign: raw(p.f.foreign),
  box: raw(p.f.box),
  origin: p.f.origin,
  artifact: {
    fileSha256: sha(artifact),
    normalizedSha256: sha(JSON.stringify(JSON.parse(artifact))),
    sourceSha256: sha(
      fs.readFileSync(
        path.resolve(__dirname, "../../vault/src/contracts/ordinalPair.ts")
      )
    ),
  },
  steps: p.entries.map((tx, i) => ({
    stage: phases[i],
    txid: tx.id,
    raw: raw(tx),
    fundingRaw: raw(p.fundingParents[i]),
    fundingRootRaw: raw(p.fundingRoots[i]),
    inputs: tx.inputs.map(
      (x) => x.prevTxId.toString("hex") + ":" + x.outputIndex
    ),
    outputs: tx.outputs.map((x) => ({
      satoshis: x.satoshis,
      script: x.script.toHex(),
    })),
  })),
};
assert.equal(new Set(packet.steps.map((s) => s.inputs[2])).size, 5);
for (const step of packet.steps) assert.equal(step.outputs[0].satoshis, 1);
fs.writeFileSync(
  path.join(__dirname, "proof.json"),
  JSON.stringify(packet, null, 2) + "\n"
);
// This is an explicitly PUBLIC TEST trust policy, not production issuer trust.
fs.writeFileSync(
  path.join(__dirname, "fixture-trusted-policy.json"),
  JSON.stringify(p.policy, null, 2) + "\n"
);
const tx = p.entries[2],
  funding = p.fundingParents[2];
const box = {
  id: "box-1",
  state: "PAID_PENDING",
  buyerPubkey: p.f.bob.publicKey.toString(),
  inventoryId: "iceland",
  transfer: {
    stage: "UNCERTAIN",
    raw: raw(tx),
    txid: tx.id,
    sourceRaw: raw(p.entries[1]),
    fundingRaw: raw(funding),
    attempts: 1,
  },
};
fs.writeFileSync(
  path.join(__dirname, "fixture-sales.jsonl"),
  JSON.stringify({ xpub: "public-fixture-policy-only", box }) + "\n"
);
const prep = {
  type: "prepared",
  txid: funding.id,
  source: funding.inputs[0].prevTxId.toString("hex") + ":0",
  inputSats: p.fundingRoots[2].outputs[0].satoshis,
  amount: funding.outputs[0].satoshis,
  prepFee: 500,
  raw: raw(funding),
};
fs.writeFileSync(
  path.join(__dirname, "fixture-pool.jsonl"),
  [prep, { type: "dispensed", txid: funding.id }]
    .map(JSON.stringify)
    .join("\n") + "\n"
);
fs.writeFileSync(path.join(__dirname, "fixture-observations.json"), "[]\n");
console.log(
  JSON.stringify(
    {
      origin: packet.origin,
      steps: packet.steps.map((s) => ({ stage: s.stage, txid: s.txid })),
      artifact: packet.artifact,
    },
    null,
    2
  )
);
