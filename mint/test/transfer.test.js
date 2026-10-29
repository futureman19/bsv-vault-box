"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const M = require("../../vault/src/ordinal-pair");
const { TransferWorker } = require("../transfer");
function harness(t, { chain = "regtest", ambiguous = false } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "transfer-"));
  const f = M.fixture();
  const opts = { sponsor: f.bob };
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
  const prep = M.transition(
    f,
    sealed.tx,
    2,
    f.alice,
    f.bob.publicKey.toString(),
    null,
    undefined,
    opts
  ).funding;
  for (const [n, k] of [
    ["inventory", f.alice],
    ["sponsor", f.bob],
  ])
    fs.writeFileSync(path.join(dir, n), k.toWIF(), { mode: 0o600 });
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  let row = {
    id: "a",
    state: "PAID_PENDING",
    buyerPubkey: f.bob.publicKey.toString(),
    inventoryId: "sealed",
    payment: { satoshis: 1000, confirmations: 1, refs: ["p:0"] },
    priceSats: 1000,
    transfer: null,
  };
  let calls = 0,
    dispenses = 0;
  const store = {
    get: () => structuredClone(row),
    update: (id, p) => {
      row = { ...row, ...structuredClone(p) };
      return structuredClone(row);
    },
  };
  const rpc = async (m, p) => {
    if (m === "getblockchaininfo") return { chain };
    if (m === "gettxout") {
      const tx = p[0] === sealed.tx.id ? sealed.tx : prep;
      return {
        value: tx.outputs[p[1]].satoshis / 1e8,
        scriptPubKey: { hex: tx.outputs[p[1]].script.toHex() },
        confirmations: 5,
      };
    }
    if (m === "getrawtransaction") {
      const e = Error("missing");
      e.code = -5;
      throw e;
    }
    if (m === "sendrawtransaction") {
      calls++;
      if (ambiguous) throw Error("timeout");
      return new M.bsv.Transaction(p[0]).id;
    }
    throw Error(m);
  };
  const w = new TransferWorker({
    store,
    rpc,
    pool: {
      dispense: async () => {
        dispenses++;
        return prep;
      },
    },
    inventory: () => ({ f, source: sealed.tx }),
    inventoryKeyPath: path.join(dir, "inventory"),
    sponsorKeyPath: path.join(dir, "sponsor"),
    retryMs: 0,
    maxAttempts: 2,
    paymentTransport: { read: async () => row.payment },
  });
  return { w, store, calls: () => calls, dispenses: () => dispenses };
}
test(
  "invalid payment evidence never dispenses",
  { skip: process.platform === "win32" },
  async (t) => {
    const h = harness(t);
    h.w.paymentTransport = { read: async () => ({}) };
    await assert.rejects(h.w.run("a"), /Payment/);
    assert.equal(h.dispenses(), 0);
  }
);
test(
  "retry revalidates payment finality",
  { skip: process.platform === "win32" },
  async (t) => {
    const h = harness(t, { ambiguous: true });
    await h.w.run("a");
    h.w.paymentTransport = {
      read: async () => ({ satoshis: 0, confirmations: 0 }),
    };
    await assert.rejects(h.w.run("a"), /Payment/);
    assert.equal(h.calls(), 1);
  }
);
test(
  "ambiguous reservation is held without second dispense",
  { skip: process.platform === "win32" },
  async (t) => {
    const h = harness(t);
    h.store.update("a", { transfer: { stage: "RESERVING" } });
    await assert.rejects(h.w.run("a"), /manual reconciliation/);
    assert.equal(h.dispenses(), 0);
  }
);
test("fee cap rejected before key loading", () =>
  assert.throws(() => new TransferWorker({ fee: 10001 }), /fee/i));
test(
  "network gate prevents dispense and broadcast",
  { skip: process.platform === "win32" },
  async (t) => {
    const h = harness(t, { chain: "main" });
    await assert.rejects(h.w.run("a"), /regtest/);
    assert.equal(h.dispenses(), 0);
    assert.equal(h.calls(), 0);
  }
);
test(
  "parallel transfer calls dispense once; pending does not mean included",
  { skip: process.platform === "win32" },
  async (t) => {
    const h = harness(t);
    await Promise.all([h.w.run("a"), h.w.run("a")]);
    assert.equal(h.dispenses(), 1);
    assert.equal(h.calls(), 1);
    assert.equal(h.store.get().state, "PAID_PENDING");
    assert.equal(
      new M.bsv.Transaction(h.store.get().transfer.raw).inputs.length,
      3
    );
  }
);
test(
  "ambiguous broadcasts keep same bytes and stop at durable retry budget",
  { skip: process.platform === "win32" },
  async (t) => {
    const h = harness(t, { ambiguous: true });
    await h.w.run("a");
    const raw = h.store.get().transfer.raw;
    await h.w.run("a");
    await h.w.run("a");
    assert.equal(h.calls(), 2);
    assert.equal(h.dispenses(), 1);
    assert.equal(h.store.get().transfer.raw, raw);
    assert.equal(h.store.get().state, "PAID_PENDING");
  }
);
