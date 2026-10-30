"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const path = require("node:path");
test("runner refuses absent gate before opening config or chain", () => {
  const r = spawnSync(
    process.execPath,
    [
      path.join(__dirname, "../scripts/canary-run.js"),
      "missing",
      "missing",
      "missing",
    ],
    { encoding: "utf8" }
  );
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /Owner authorization required/);
});
test("fresh report validation rejects shape, age, chain and address drift", () => {
  const { validateReport } = require("../funded-runner");
  const now = Date.now(),
    addresses = { inventory: "a", sponsor: "b", payment: "c" };
  const report = {
    status: "READ_ONLY_PREFLIGHT_PASS",
    stage: "startup",
    createdAt: now,
    policy: { chain: "regtest" },
    composition: { buyerPubkey: "pub" },
    funding: {
      inventory: {
        address: "a",
        status: "EXACT_CONFIRMED_UNSPENT",
        expectedSatoshis: [60000, 60000],
        outpoints: ["a:0", "a:1"],
      },
      sponsor: {
        address: "b",
        status: "EXACT_CONFIRMED_UNSPENT",
        expectedSatoshis: [50000, 50000, 50000],
        outpoints: ["b:0", "b:1", "b:2"],
      },
      payment: {
        address: "c",
        status: "UNFUNDED",
        expectedSatoshis: [10000],
        outpoints: [],
      },
    },
  };
  assert.doesNotThrow(() =>
    validateReport(report, {
      chain: "regtest",
      addresses,
      buyerPubkey: "pub",
      now,
    })
  );
  for (const change of [
    { createdAt: now - 300001 },
    { createdAt: now + 1 },
    { stage: "inspect" },
    { policy: { chain: "mainnet" } },
    { status: "FAIL" },
  ])
    assert.throws(() =>
      validateReport(
        { ...report, ...change },
        { chain: "regtest", addresses, buyerPubkey: "pub", now }
      )
    );
  const wrong = structuredClone(report);
  wrong.funding.payment.status = "EXACT_CONFIRMED_UNSPENT";
  assert.throws(() =>
    validateReport(wrong, {
      chain: "regtest",
      addresses,
      buyerPubkey: "pub",
      now,
    })
  );
  assert.throws(() =>
    validateReport(report, {
      chain: "regtest",
      addresses: { ...addresses, inventory: "other" },
      buyerPubkey: "pub",
      now,
    })
  );
});
