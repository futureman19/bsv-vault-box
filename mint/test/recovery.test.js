"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const { classify } = require("../recovery"),
  { fixture } = require("../../vault/tests/launch-fixture");
const p = fixture(),
  tx = p.entries[2],
  funding = p.fundingParents[2];
const lines = (xs) => xs.map(JSON.stringify).join("\n") + "\n";
function evidence(stage = "BUILT") {
  const row = {
    id: "box-1",
    state: "PAID_PENDING",
    buyerPubkey: p.f.bob.publicKey.toString(),
    inventoryId: "iceland",
    transfer: {
      stage,
      raw: tx.uncheckedSerialize(),
      txid: tx.id,
      sourceRaw: p.entries[1].uncheckedSerialize(),
      fundingRaw: funding.uncheckedSerialize(),
      attempts: 1,
    },
  };
  if (stage === "RESERVING") row.transfer = { stage };
  if (stage === "INCLUDED") row.state = "TRANSFERRED";
  const prep = {
    type: "prepared",
    txid: funding.id,
    raw: funding.uncheckedSerialize(),
    source: funding.inputs[0].prevTxId.toString("hex") + ":0",
    amount: funding.outputs[0].satoshis,
    inputSats: p.fundingRoots[2].outputs[0].satoshis,
    prepFee: 500,
  };
  return {
    id: row.id,
    saleText: lines([{ xpub: "fixture-public-policy", box: row }]),
    poolText: lines([prep, { type: "dispensed", txid: funding.id }]),
    sponsorPubkey: p.f.bob.publicKey.toString(),
    observations: [],
    depth: 2,
  };
}
for (const stage of [
  "RESERVING",
  "BUILT",
  "SUBMITTED",
  "INCLUDED",
  "UNCERTAIN",
])
  test(
    "read-only recovery identifies " +
      stage +
      " and exact persisted transaction",
    () => {
      const e = evidence(stage),
        r = classify(e);
      assert.equal(
        r.classification,
        stage === "UNCERTAIN" ? "UNCERTAIN_SEND" : stage
      );
      assert.equal(r.quarantined, true);
      assert.equal(r.txid, stage === "RESERVING" ? null : tx.id);
      assert.equal(r.mayResume, false);
      assert.deepEqual(classify(e), r);
    }
  );
test("RESERVING before and after dispense never guesses funding assignment", () => {
  for (const poolText of ["", evidence().poolText]) {
    const r = classify({ ...evidence("RESERVING"), poolText });
    assert.equal(r.classification, "RESERVING");
    assert.equal(r.fundingOutpoint, null);
    assert.equal(r.quarantined, true);
  }
});
test("send succeeded before stage persistence: matching captured inclusion resolves observation not auto-resume", () => {
  const e = evidence();
  e.observations = [
    {
      txid: tx.id,
      raw: tx.uncheckedSerialize(),
      confirmations: 3,
      blockhash: "ab".repeat(32),
      block: { hash: "ab".repeat(32), confirmations: 3, tx: [tx.id] },
    },
  ];
  const r = classify(e);
  assert.equal(r.classification, "INCLUDED");
  assert.equal(r.persistedStage, "BUILT");
  assert.equal(r.txid, tx.id);
  assert.equal(r.mayResume, false);
});
for (const [name, mutate] of [
  ["truncated sale write", (e) => (e.saleText = e.saleText.slice(0, -1))],
  ["short pool write", (e) => (e.poolText += '{"type":')],
  [
    "missing dispense",
    (e) => (e.poolText = lines([JSON.parse(e.poolText.split("\n")[0])])),
  ],
  [
    "wrong txid",
    (e) => {
      const r = JSON.parse(e.saleText);
      r.box.transfer.txid = "00".repeat(32);
      e.saleText = lines([r]);
    },
  ],
  [
    "wrong source bytes",
    (e) => {
      const r = JSON.parse(e.saleText);
      r.box.transfer.sourceRaw = p.entries[0].uncheckedSerialize();
      e.saleText = lines([r]);
    },
  ],
  [
    "duplicate dispense",
    (e) => (e.poolText += e.poolText.split("\n")[1] + "\n"),
  ],
  [
    "ambiguous pool mapping",
    (e) => (e.poolText = e.poolText.replace(funding.id, "00".repeat(32))),
  ],
  [
    "changed buyer on replay",
    (e) => {
      const r = JSON.parse(e.saleText);
      r.box.buyerPubkey = p.f.alice.publicKey.toString();
      e.saleText += lines([r]);
    },
  ],
  [
    "contradictory captured bytes",
    (e) =>
      (e.observations = [
        {
          txid: tx.id,
          raw: p.entries[1].uncheckedSerialize(),
          confirmations: 3,
        },
      ]),
  ],
  [
    "false captured block membership",
    (e) =>
      (e.observations = [
        {
          txid: tx.id,
          raw: tx.uncheckedSerialize(),
          confirmations: 3,
          blockhash: "ab".repeat(32),
          block: { hash: "ab".repeat(32), confirmations: 3, tx: [] },
        },
      ]),
  ],
])
  test("inconsistent evidence stays quarantined: " + name, () => {
    const e = evidence();
    mutate(e);
    assert.equal(classify(e).classification, "INCONSISTENT");
    assert.equal(classify(e).mayResume, false);
  });
test("cross-sale claims on identical transfer and funding are inconsistent", () => {
  const e = evidence();
  const second = JSON.parse(e.saleText);
  second.box.id = "box-2";
  e.saleText += lines([second]);
  assert.equal(classify(e).classification, "INCONSISTENT");
});
test("captured inclusion loss is distinct from historical INCLUDED", () => {
  const e = evidence("INCLUDED");
  e.observations = [
    { txid: tx.id, raw: tx.uncheckedSerialize(), confirmations: 0 },
  ];
  const r = classify(e);
  assert.equal(r.classification, "FINALITY_LOST");
  assert.equal(r.persistedStage, "INCLUDED");
  assert.equal(r.reconciliationRequired, true);
});
for (const [name, mutate] of [
  [
    "inclusion regression",
    (b) => {
      b.transfer.stage = "BUILT";
    },
  ],
  [
    "ownership regression",
    (b) => {
      b.state = "PAID_PENDING";
    },
  ],
  [
    "open regression",
    (b) => {
      b.state = "TRANSFERRED";
    },
  ],
  [
    "changed open identity",
    (b) => {
      b.openTxid = "changed";
    },
  ],
  [
    "cleared hold",
    (b) => {
      b.reconciliationRequired = false;
    },
  ],
  [
    "cleared reason with hold retained",
    (b) => {
      b.reconciliationReasons = [];
    },
  ],
])
  test("replay rejects historical " + name, () => {
    const e = evidence("INCLUDED"),
      prior = JSON.parse(e.saleText);
    Object.assign(prior.box, {
      state: "OPENED",
      openTxid: "historical",
      reconciliationRequired: true,
      reconciliationReasons: ["PAYMENT_FINALITY_LOST"],
    });
    const later = structuredClone(prior);
    mutate(later.box);
    const r = classify({ ...e, saleText: lines([prior, later]) });
    assert.equal(r.classification, "INCONSISTENT");
    assert.equal(r.quarantined, true);
    assert.equal(r.mayResume, false);
  });
test("legitimate retry progression and accumulated reasons remain quarantined", () => {
  const e = evidence(),
    rows = [],
    row = JSON.parse(e.saleText);
  for (const stage of [
    "BUILT",
    "UNCERTAIN",
    "UNCERTAIN",
    "SUBMITTED",
    "INCLUDED",
  ]) {
    row.box.transfer.stage = stage;
    if (stage === "INCLUDED") row.box.state = "TRANSFERRED";
    rows.push(structuredClone(row));
  }
  Object.assign(row.box, {
    state: "OPENED",
    openTxid: "historical",
    reconciliationRequired: true,
    reconciliationReasons: ["PAYMENT_FINALITY_LOST"],
  });
  rows.push(structuredClone(row));
  row.box.reconciliationReasons.push("TRANSFER_FINALITY_LOST");
  rows.push(row);
  const r = classify({ ...e, saleText: lines(rows) });
  assert.equal(r.classification, "INCLUDED");
  assert.equal(r.reconciliationRequired, true);
  assert.deepEqual(r.reconciliationReasons, [
    "PAYMENT_FINALITY_LOST",
    "TRANSFER_FINALITY_LOST",
  ]);
  assert.equal(r.quarantined, true);
  assert.equal(r.mayResume, false);
});
module.exports = { evidence };
