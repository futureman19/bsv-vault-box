"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const { bsv, fixture } = require("../../vault/src/ordinal-pair");
const { SaleStore } = require("../sale");
const xpub = bsv.HDPrivateKey.fromSeed(
  Buffer.alloc(32, 7),
  bsv.Networks.testnet
).hdPublicKey.toString();
function setup(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "sale-"));
  const file = path.join(dir, "sales.jsonl");
  const s = new SaleStore({ file, xpub });
  t.after(() => {
    s.close();
    fs.rmSync(dir, { recursive: true, force: true });
  });
  return { s, file };
}
const buyer = fixture().bob.publicKey.toString();
test("allocations survive restart, keep buyer immutable and never recycle addresses", (t) => {
  const { s, file } = setup(t);
  const a = s.list({ priceSats: 1000, inventoryId: "aa" });
  s.reserve(a.id, buyer, 100);
  assert.throws(
    () => s.reserve(a.id, fixture().alice.publicKey.toString(), 100),
    /reserved/
  );
  s.close();
  const restored = new SaleStore({ file, xpub });
  assert.equal(restored.get(a.id).buyerPubkey, buyer);
  const b = restored.list({ priceSats: 1000, inventoryId: "bb" });
  assert.notEqual(a.payAddress, b.payAddress);
  assert.equal(bsv.Address.fromString(b.payAddress).network.name, "testnet");
  assert.throws(
    () => restored.list({ priceSats: 1000, inventoryId: "aa" }),
    /inventory/
  );
  restored.close();
});
test("expiry flags late funds and underpayment never authorizes transfer", (t) => {
  const { s } = setup(t);
  const a = s.list({ priceSats: 1000, inventoryId: "aa" });
  s.reserve(a.id, buyer, 100);
  s.payment(a.id, { satoshis: 999, confirmations: 1, refs: ["x"] }, 50);
  assert.equal(s.get(a.id).state, "LISTED");
  s.expire(101);
  assert.equal(s.get(a.id).refundRequired, true);
  s.payment(a.id, { satoshis: 1000, confirmations: 1, refs: ["y"] }, 102);
  assert.equal(s.get(a.id).state, "EXPIRED");
  assert.equal(s.get(a.id).refundRequired, true);
});
test("payment binds reservation; durable transfer intent is immutable", (t) => {
  const { s } = setup(t);
  const a = s.list({ priceSats: 1000, inventoryId: "aa" });
  s.reserve(a.id, buyer, 100);
  s.payment(a.id, { satoshis: 1000, confirmations: 1, refs: ["x"] }, 50);
  assert.equal(s.get(a.id).state, "PAID_PENDING");
  s.update(a.id, { transfer: { stage: "RESERVING" } });
  assert.throws(() => s.reserve(a.id, buyer, 200), /reserved/);
  assert.equal(s.get(a.id).transfer.stage, "RESERVING");
});
test("unassigned payments quarantine the address before any reservation", (t) => {
  const { s } = setup(t);
  const b = s.list({ priceSats: 1000, inventoryId: "prepaid" });
  s.payment(b.id, { satoshis: 1000, confirmations: 1, refs: ["p"] }, 50);
  assert.throws(() => s.reserve(b.id, buyer, 100), /reserved/);
});
test("exclusive writer, truncated journal and closed store fail closed", (t) => {
  const { s, file } = setup(t);
  assert.throws(() => new SaleStore({ file, xpub }), /exist/);
  s.close();
  assert.throws(() => s.list({ priceSats: 1, inventoryId: "a" }), /closed/);
  fs.appendFileSync(file, '{"broken":');
  assert.throws(() => new SaleStore({ file, xpub }), /journal/);
});
