"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const M = require("../../vault/src/ordinal-pair");
const { SaleStore } = require("../sale");
const { TransferWorker } = require("../transfer");
const Canary = require("../canary");
const f = M.fixture(),
  opts = { sponsor: f.bob };
const packed = M.transition(f, null, 0, f.alice, null, null, undefined, opts);
const sealed = M.transition(
  f,
  packed.tx,
  1,
  f.alice,
  null,
  null,
  undefined,
  opts
);
const sent = M.transition(
  f,
  sealed.tx,
  2,
  f.alice,
  f.bob.publicKey.toString(),
  null,
  undefined,
  opts
);
const xpub = M.bsv.HDPrivateKey.fromSeed(
  Buffer.alloc(32, 7),
  M.bsv.Networks.testnet
).hdPublicKey.toString();
function setup(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "finality-")),
    file = path.join(dir, "sale.jsonl");
  let s = new SaleStore({ file, xpub });
  const b = s.list({ priceSats: 1000, inventoryId: "sealed" });
  s.reserve(b.id, f.bob.publicKey.toString(), Date.now() + 60000);
  s.payment(b.id, { satoshis: 1000, confirmations: 3, refs: ["fixture:0"] });
  s.update(b.id, {
    transfer: {
      stage: "SUBMITTED",
      raw: sent.tx.uncheckedSerialize(),
      txid: sent.tx.id,
      sourceRaw: sealed.tx.uncheckedSerialize(),
      fundingRaw: sent.funding.uncheckedSerialize(),
      attempts: 1,
    },
  });
  // Ordinary worker methods against a real durable store; constructor deliberately
  // bypassed for observation-only tests, so no key file is loaded or generated.
  const w = Object.create(TransferWorker.prototype);
  Canary.bind(w, {});
  Object.assign(w, {
    store: s,
    depth: 2,
    fee: 500,
    maxAttempts: 3,
    retryMs: 0,
    pool: {
      dispense() {
        throw Error("replacement dispense");
      },
    },
    paymentTransport: {
      read: async () => ({ satoshis: 1000, confirmations: 3 }),
    },
  });
  let included = true,
    readError = false,
    sends = 0,
    reads = 0;
  w.rpc = async (m) => {
    if (m === "getblockchaininfo") return { chain: "regtest" };
    if (m === "sendrawtransaction") {
      sends++;
      throw Error("replacement send");
    }
    if (readError) throw Error("offline");
    if (m === "getrawtransaction") {
      reads++;
      return {
        hex: sent.tx.uncheckedSerialize(),
        confirmations: included ? 3 : 0,
        blockhash: "ab".repeat(32),
      };
    }
    if (m === "getblock") return { hash: "ab".repeat(32), confirmations: 3, tx: [sent.tx.id] };
    throw Error(m);
  };
  t.after(() => {
    s.close();
    fs.rmSync(dir, { recursive: true, force: true });
  });
  return {
    w,
    id: b.id,
    get: () => s.get(b.id),
    sends: () => sends,
    reads: () => reads,
    setIncluded: (v) => (included = v),
    setError: (v) => (readError = v),
    restart() {
      s.close();
      s = new SaleStore({ file, xpub });
      w.store = s;
      return s;
    },
  };
}
test("included transfer revalidates missing payment, preserves buyer history and durable hold", async (t) => {
  const h = setup(t);
  h.w.paymentTransport.read = async () => ({ satoshis: 0, confirmations: 0 });
  await h.w.run(h.id);
  const b = h.get();
  assert.equal(b.state, "TRANSFERRED");
  assert.equal(b.reconciliationRequired, true);
  assert.ok(b.reconciliationReasons.includes("PAYMENT_FINALITY_LOST"));
  assert.equal(b.buyerPubkey, f.bob.publicKey.toString());
  h.restart();
  assert.equal(h.get().reconciliationRequired, true);
  await h.w.run(h.id);
  assert.equal(h.sends(), 0);
  assert.equal(h.get().transfer.raw, sent.tx.uncheckedSerialize());
});
test("terminal transfer inclusion loss is monitored and never demotes OPENED ownership", async (t) => {
  const h = setup(t);
  await h.w.run(h.id);
  h.w.store.update(h.id, { state: "OPENED", openTxid: "historical-open" });
  h.setIncluded(false);
  await h.w.run(h.id);
  assert.equal(h.get().state, "OPENED");
  assert.ok(h.get().reconciliationReasons.includes("TRANSFER_FINALITY_LOST"));
  assert.equal(h.get().openTxid, "historical-open");
  h.restart();
  await h.w.run(h.id);
  assert.equal(h.sends(), 0);
  assert.ok(h.reads() >= 3);
});
test("read failures are uncertainty not proven loss and holds remain after healthy observation", async (t) => {
  const h = setup(t);
  await h.w.run(h.id);
  h.setError(true);
  h.w.paymentTransport.read = async () => {
    throw Error("network");
  };
  await h.w.run(h.id);
  assert.deepEqual(h.get().reconciliationReasons.sort(), [
    "PAYMENT_OBSERVATION_UNAVAILABLE",
    "TRANSFER_OBSERVATION_UNAVAILABLE",
  ]);
  h.setError(false);
  h.w.paymentTransport.read = async () => ({
    satoshis: 1000,
    confirmations: 3,
  });
  await h.w.run(h.id);
  assert.equal(h.get().reconciliationRequired, true);
  assert.equal(h.sends(), 0);
});
test("submitted payment loss is observed without replacement and read-only observation is idempotent", async (t) => {
  const h = setup(t);
  h.setIncluded(false);
  h.w.paymentTransport.read = async () => ({ satoshis: 0, confirmations: 0 });
  await h.w.run(h.id);
  assert.equal(h.get().state, "PAID_PENDING");
  assert.ok(h.get().reconciliationReasons.includes("PAYMENT_FINALITY_LOST"));
  const before = h.get();
  await h.w.run(h.id);
  assert.deepEqual(h.get(), before);
  assert.equal(h.sends(), 0);
});
test("chain-info outage durably records uncertainty without bypassing policy caps", async (t) => {
  const h = setup(t);
  await h.w.run(h.id);
  const rpc = h.w.rpc;
  h.w.rpc = async (m, p) => {
    if (m === "getblockchaininfo") throw Error("offline");
    return rpc(m, p);
  };
  await h.w.run(h.id);
  assert.ok(
    h.get().reconciliationReasons.includes("TRANSFER_OBSERVATION_UNAVAILABLE")
  );
  assert.equal(h.get().state, "TRANSFERRED");
  h.restart();
  assert.equal(h.get().reconciliationRequired, true);
  assert.equal(h.sends(), 0);
  h.w.fee = 10001;
  await assert.rejects(h.w.run(h.id), /fee/);
});
test('asynchronous finality observation retains the single-flight lock until durable write', async t => {
  const h = setup(t);
  let release, reads = 0;
  h.w.paymentTransport.read = () => { reads++; return new Promise(resolve => { release = resolve; }); };
  const first = h.w.run(h.id);
  while (!release) await new Promise(resolve => setImmediate(resolve));
  const second = h.w.run(h.id);
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(reads, 1);
  release({satoshis:1000,confirmations:3});
  await Promise.all([first, second]);
  assert.equal(h.get().state, 'TRANSFERRED');
});
for (const state of ["TRANSFERRED", "OPENED"])
  test(
    "late overpayment preserves " + state + " with durable refund hold",
    async (t) => {
      const h = setup(t);
      await h.w.run(h.id);
      h.w.store.update(h.id, { state });
      h.w.paymentTransport.read = async () => ({
        satoshis: 1001,
        confirmations: 3,
        refs: ["late:0"],
      });
      await h.w.run(h.id);
      assert.equal(h.get().state, state);
      assert.equal(h.get().refundRequired, true);
      assert.ok(h.get().reconciliationReasons.includes("PAYMENT_EXCESS"));
      h.restart();
      assert.equal(h.get().refundRequired, true);
      assert.equal(h.sends(), 0);
    }
  );
