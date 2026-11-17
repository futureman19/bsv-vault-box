"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { TransferWorker } = require("../transfer");
const { SaleStore } = require("../sale");
const Canary = require("../canary");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const { fixture } = require("../../vault/tests/launch-fixture");
const { verifyLaunch } = require("../../vault/src/launch-record");
const p = fixture(),
  hash = "ab".repeat(32);
const mutations = [
  ["shallow block", (b) => ({ ...b, confirmations: 1 })],
  ["wrong hash", (b) => ({ ...b, hash: "cd".repeat(32) })],
  ["fractional depth", (b) => ({ ...b, confirmations: 0.5 })],
  [
    "unsafe depth",
    (b) => ({ ...b, confirmations: Number.MAX_SAFE_INTEGER + 1 }),
  ],
  ["missing membership", (b) => ({ ...b, tx: [] })],
  ["malformed membership", (b) => ({ ...b, tx: "not-an-array" })],
  ["missing block", () => null],
];
function setup(t, state, stage) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "security-fix-"));
  const file = path.join(dir, "sales.jsonl");
  const M = require("../../vault/src/ordinal-pair");
  const xpub = M.bsv.HDPrivateKey.fromSeed(
    Buffer.alloc(32, 7),
    M.bsv.Networks.testnet
  ).hdPublicKey.toString();
  const store = new SaleStore({ file, xpub });
  t.after(() => {
    store.close();
    fs.rmSync(dir, { recursive: true, force: true });
  });
  const b = store.list({ priceSats: 1000, inventoryId: "sealed" });
  store.reserve(b.id, p.f.bob.publicKey.toString(), Date.now() + 60000);
  store.payment(b.id, {
    satoshis: 1000,
    confirmations: 3,
    refs: ["fixture:0"],
  });
  const tx = p.entries[2];
  store.update(b.id, {
    state,
    transfer: {
      stage,
      raw: tx.uncheckedSerialize(),
      txid: tx.id,
      attempts: 0,
      nextAttemptAt: 0,
    },
    ...(state === "OPENED" ? { openTxid: p.entries[3].id } : {}),
  });
  const w = Object.create(TransferWorker.prototype);
  Canary.bind(w, {});
  let sends = 0,
    dispenses = 0;
  Object.assign(w, {
    store,
    depth: 2,
    fee: 500,
    maxAttempts: 3,
    retryMs: 0,
    pool: {
      dispense() {
        dispenses++;
        throw Error("unexpected funding");
      },
    },
    paymentTransport: {
      read: async () => ({ satoshis: 1000, confirmations: 3 }),
    },
  });
  return {
    w,
    id: b.id,
    store,
    assertNoSpend() {
      assert.equal(sends, 0);
      assert.equal(dispenses, 0);
    },
    rpcFor(tx, mutate) {
      w.rpc = async (method) => {
        if (method === "getblockchaininfo") return { chain: "regtest" };
        if (method === "sendrawtransaction") {
          sends++;
          throw Error("unexpected broadcast");
        }
        if (method === "getrawtransaction")
          return {
            hex: tx.uncheckedSerialize(),
            confirmations: 3,
            blockhash: hash,
          };
        if (method === "getblock")
          return mutate({ hash, confirmations: 3, tx: [tx.id] });
        throw Error(method);
      };
    },
  };
}
for (const [name, mutate] of mutations) {
  for (const [state, stage] of [
    ["PAID_PENDING", "SUBMITTED"],
    ["TRANSFERRED", "INCLUDED"],
    ["OPENED", "INCLUDED"],
  ])
    test(`${state} rejects ${name} without spend`, async (t) => {
      const h = setup(t, state, stage);
      h.rpcFor(p.entries[2], mutate);
      await h.w.run(h.id);
      const b = h.store.get(h.id);
      assert.equal(b.state, state);
      assert.equal(b.transfer.stage, stage);
      assert.equal(b.buyerPubkey, p.f.bob.publicKey.toString());
      if (state !== "PAID_PENDING")
        assert.equal(b.reconciliationRequired, true);
      if (state === "OPENED") assert.equal(b.openTxid, p.entries[3].id);
      h.assertNoSpend();
    });
  test(`observeOpen rejects ${name} without spend`, async (t) => {
    const h = setup(t, "TRANSFERRED", "INCLUDED");
    h.rpcFor(p.entries[3], mutate);
    await assert.rejects(
      h.w.observeOpen(
        h.id,
        p.entries[3].uncheckedSerialize(),
        p.fundingParents[3].uncheckedSerialize()
      )
    );
    assert.equal(h.store.get(h.id).state, "TRANSFERRED");
    h.assertNoSpend();
  });
}
test("BUILT contradictory block evidence quarantines rather than retrying broadcast", async (t) => {
  const h = setup(t, "PAID_PENDING", "BUILT");
  h.rpcFor(p.entries[2], mutations[0][1]);
  await h.w.run(h.id);
  assert.equal(h.store.get(h.id).state, "PAID_PENDING");
  assert.equal(h.store.get(h.id).reconciliationRequired, true);
  h.assertNoSpend();
});
test("observeOpen accepts consistent deep block membership", async (t) => {
  const h = setup(t, "TRANSFERRED", "INCLUDED");
  h.rpcFor(p.entries[3], (b) => b);
  await h.w.observeOpen(
    h.id,
    p.entries[3].uncheckedSerialize(),
    p.fundingParents[3].uncheckedSerialize()
  );
  assert.equal(h.store.get(h.id).state, "OPENED");
  h.assertNoSpend();
});
for (const [field, result] of [
  ["envelope", "originalIssuanceProvenance"],
  ["policy", "originalIssuanceProvenance"],
  ["mediaHashes", "originalManifestComplete"],
])
  for (const key of Object.keys(p[field]))
    test(`${field} rejects inherited ${key}`, () => {
      const obj = { ...p[field] };
      delete obj[key];
      obj.extra = "unexpected";
      Object.setPrototypeOf(obj, { [key]: p[field][key] });
      assert.equal(verifyLaunch({ ...p, [field]: obj })[result], false);
    });
