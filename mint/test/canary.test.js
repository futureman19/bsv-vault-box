"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const { bsv, pay, output } = require("../../vault/src/ordinal-pair");
const { SaleStore } = require("../sale");
const { SponsorPool, buildPrep } = require("../pool");
const { TransferWorker } = require("../transfer");
const { createService } = require("../service");
const { HttpTransport, PaymentWatcher } = require("../watcher");
const { loadKey } = require("../keys");
const main = { chain: "mainnet", canary: true };
// PUBLIC, DISPOSABLE FIXTURE SCALARS ONLY. Never fund these keys.
const key = (net) =>
  new bsv.PrivateKey(new bsv.crypto.BN(1), bsv.Networks[net]);
const hd = (net) =>
  bsv.HDPrivateKey.fromSeed(
    Buffer.alloc(32, 7),
    bsv.Networks[net]
  ).hdPublicKey.toString();
function dir(t) {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), "canary-"));
  t.after(() => fs.rmSync(d, { recursive: true, force: true }));
  return d;
}
function store(t, opts = main) {
  let s;
  t.after(() => s?.close());
  s = new SaleStore({
    file: path.join(dir(t), "sales"),
    xpub: hd(opts.chain === "mainnet" ? "livenet" : "testnet"),
    ...opts,
  });
  return s;
}
function pool(t, opts = {}) {
  let p;
  t.after(() => p?.close());
  const d = dir(t),
    k = key("livenet");
  fs.writeFileSync(path.join(d, "key"), k.toWIF(), { mode: 0o600 });
  p = new SponsorPool({
    keyPath: path.join(d, "key"),
    ledgerPath: path.join(d, "ledger"),
    rpc: async (m) => {
      if (m === "getblockchaininfo") return { chain: "main" };
      throw Error("unexpected RPC " + m);
    },
    ...main,
    ...opts,
  });
  return p;
}
function root(amount, k = key("livenet")) {
  return new bsv.Transaction()
    .addInput(
      new bsv.Transaction.Input({
        prevTxId: "01".repeat(32),
        outputIndex: 0,
        script: "",
        output: output(bsv.Script.empty()),
      })
    )
    .addOutput(output(pay(k.publicKey.toString()), amount));
}
test("all mainnet constructors reject without literal canary true before resources", () => {
  for (const canary of [undefined, false, 1, "true"])
    for (const make of [
      (o) => new SaleStore(o),
      (o) => new SponsorPool(o),
      (o) => new TransferWorker(o),
      (o) => createService(o),
      (o) => new HttpTransport(o),
      (o) => new PaymentWatcher(o),
    ])
      assert.throws(() => make({ chain: "mainnet", canary }), /canary/i);
  for (const chain of ["main", "test", "unknown", null])
    assert.throws(() => new SaleStore({ chain }), /chain/i);
});
test("WIF gates both directions, defaults unchanged, custody remains enforced", (t) => {
  const p = path.join(dir(t), "key");
  for (const net of ["testnet", "livenet"]) {
    fs.writeFileSync(p, key(net).toWIF(), { mode: 0o600 });
    for (const opts of [{}, { chain: "testnet" }, main]) {
      if ((net === "livenet") === (opts.chain === "mainnet"))
        assert.equal(
          loadKey(p, opts).publicKey.toString(),
          key(net).publicKey.toString()
        );
      else assert.throws(() => loadKey(p, opts), /network|testnet|mainnet/i);
    }
  }
  fs.chmodSync(p, 0o644);
  assert.throws(() => loadKey(p, main), /0600/);
});
test("xpub gates both directions and derived address network", (t) => {
  for (const opts of [{}, { chain: "testnet" }, main]) {
    const s = store(t, opts);
    const b = s.list({ priceSats: 10000, inventoryId: "a" });
    assert.equal(
      new bsv.Address(b.payAddress).network.name,
      opts.chain === "mainnet" ? "livenet" : "testnet"
    );
    assert.throws(
      () =>
        new SaleStore({
          file: path.join(dir(t), "bad"),
          xpub: hd(opts.chain === "mainnet" ? "testnet" : "livenet"),
          ...opts,
        }),
      /xpub/
    );
  }
});
test("sale caps apply to listing, updates, reads, inventory and replay", (t) => {
  const s = store(t);
  assert.throws(() => s.list({ priceSats: 10001, inventoryId: "a" }), /price/i);
  const a = s.list({ priceSats: 10000, inventoryId: "a" });
  s.list({ priceSats: 1, inventoryId: "b" });
  assert.throws(() => s.list({ priceSats: 1, inventoryId: "c" }), /inventory/i);
  assert.throws(() => s.update(a.id, { priceSats: 10001 }), /price/i);
  s.boxes.get(a.id).priceSats = 10001;
  assert.throws(() => s.get(a.id), /price/i);
  s.boxes.get(a.id).priceSats = 10000;
  const file = s.file;
  s.close();
  const rows = fs.readFileSync(file, "utf8").trim().split("\n").map(JSON.parse);
  rows[0].box.priceSats = 10001;
  fs.writeFileSync(file, rows.map(JSON.stringify).join("\n") + "\n");
  assert.throws(
    () => new SaleStore({ file, xpub: hd("livenet"), ...main }),
    /price/i
  );
});
test("overpayments are durably quarantined, boundary 2x accepted", (t) => {
  const s = store(t),
    a = s.list({ priceSats: 10000, inventoryId: "a" }),
    b = s.list({ priceSats: 10000, inventoryId: "b" });
  for (const x of [a, b])
    s.reserve(x.id, key("livenet").publicKey.toString(), Date.now() + 60000);
  assert.equal(
    s.payment(a.id, { satoshis: 20000, confirmations: 1, refs: ["a:0"] }).state,
    "PAID_PENDING"
  );
  const rejected = s.payment(b.id, {
    satoshis: 20001,
    confirmations: 1,
    refs: ["b:0"],
  });
  assert.equal(rejected.state, "EXPIRED");
  assert.equal(rejected.refundRequired, true);
  assert.equal(
    s.payment(b.id, { satoshis: 10000, confirmations: 1, refs: ["b:0"] }).state,
    "EXPIRED"
  );
});
test("late excess receipts cannot erase recorded ownership transfer", (t) => {
  const s = store(t),
    b = s.list({ priceSats: 10000, inventoryId: "a" });
  s.update(b.id, {
    state: "TRANSFERRED",
    transfer: { stage: "INCLUDED", txid: "aa".repeat(32) },
  });
  const result = s.payment(b.id, {
    satoshis: 20001,
    confirmations: 1,
    refs: ["p:0"],
  });
  assert.equal(result.state, "TRANSFERRED");
  assert.equal(result.refundRequired, true);
});
test("pool construction and each operation recheck immutable hard caps", async (t) => {
  assert.throws(() => pool(t, { capSats: 250001 }), /cap/i);
  const p = pool(t);
  assert.equal(p.capSats, 250000);
  assert.throws(() => {
    p.policy = { chain: "regtest" };
  }, TypeError);
  p.capSats = 250001;
  for (const f of [
    () => p.prepare(root(100000), 0),
    () => p.refresh(),
    () => p.dispense(),
  ])
    await assert.rejects(f(), /cap/i);
  p.capSats = 250000;
  p.prepFee = 10001;
  await assert.rejects(p.refresh(), /fee/i);
});
test("prep amount bounded on pure builder; regtest bytes unchanged by explicit policy", () => {
  assert.throws(
    () => buildPrep(root(100001), 0, key("livenet"), 500, main),
    /prep/i
  );
  assert.equal(
    buildPrep(root(100000), 0, key("livenet"), 500, main).outputs[0].satoshis,
    99500
  );
  const k = key("testnet"),
    r = root(100000, k);
  assert.equal(
    buildPrep(r, 0, k).uncheckedSerialize(),
    buildPrep(r, 0, k, 500, { chain: "regtest" }).uncheckedSerialize()
  );
  assert.throws(() => buildPrep(r, 0, k, 500, main), /key|network/i);
});
test("service validates inventory at construction and on requests", async (t) => {
  const s = store(t);
  assert.throws(
    () =>
      createService({ store: s, inventory: [{ priceSats: 10001 }], ...main }),
    /price/i
  );
  assert.throws(
    () => createService({ store: s, inventory: [1, 2, 3], ...main }),
    /inventory/i
  );
  const inv = [{ inventoryId: "a", priceSats: 10000 }],
    api = createService({ store: s, inventory: inv, ...main });
  await api.listen(0);
  t.after(() => api.close());
  inv[0].priceSats = 10001;
  assert.equal(
    (
      await fetch("http://127.0.0.1:" + api.address().port + "/v1/boxes", {
        method: "POST",
      })
    ).status,
    400
  );
});
test("mainnet pool prepare and worker run never sign, reserve or broadcast", async (t) => {
  const p = pool(t),
    s = store(t);
  await assert.rejects(p.prepare(root(100001), 0), /prep/);
  await assert.rejects(p.prepare(root(100000), 0), /broadcasts disabled/);
  assert.equal(p.entries.length, 0);
  const b = s.list({ priceSats: 10000, inventoryId: "a" });
  s.reserve(b.id, key("livenet").publicKey.toString(), Date.now() + 60000);
  s.payment(b.id, { satoshis: 10000, confirmations: 1, refs: ["p:0"] });
  const d = dir(t),
    kp = path.join(d, "key");
  fs.writeFileSync(kp, key("livenet").toWIF(), { mode: 0o600 });
  const transport = new HttpTransport({
    baseUrl: "https://example.invalid",
    ...main,
  });
  let rpcCalls = 0;
  const w = new TransferWorker({
    store: s,
    pool: p,
    paymentTransport: transport,
    inventory: () => {
      throw Error("must not load inventory");
    },
    inventoryKeyPath: kp,
    sponsorKeyPath: kp,
    rpc: async (m) => {
      rpcCalls++;
      assert.equal(m, "getblockchaininfo");
      return { chain: "main" };
    },
    ...main,
  });
  await assert.rejects(w.run(b.id), /broadcasts disabled/);
  assert.equal(s.get(b.id).transfer, null);
  w.fee = 10001;
  await assert.rejects(w.run(b.id), /fee/i);
  await assert.rejects(w.observeOpen(b.id, "", ""), /fee/i);
  assert.equal(rpcCalls, 1);
  w.fee = 500;
  transport.read = async () => ({
    satoshis: 20001,
    confirmations: 1,
    refs: ["p:0"],
  });
  await assert.rejects(w.checkPayment(s.get(b.id)), /payment cap/);
  s.boxes.get(b.id).priceSats = 10001;
  await assert.rejects(w.run(b.id), /price/i);
  s.boxes.get(b.id).priceSats = 10000;
  assert.throws(
    () =>
      new TransferWorker({ store: s, pool: p, paymentTransport: {}, ...main }),
    /component/
  );
});
test("watcher caps rechecked on every watch and poll; overpay still delivered for refund", async (t) => {
  const s = store(t),
    transport = new HttpTransport({
      baseUrl: "https://example.invalid",
      ...main,
    });
  transport.read = async () => ({
    satoshis: 20001,
    confirmations: 1,
    refs: ["p:0"],
  });
  const w = new PaymentWatcher({ transport, ...main });
  const a = s.list({ priceSats: 10000, inventoryId: "a" });
  w.watch(a);
  w.watch({ ...a, id: "b" });
  assert.throws(() => w.watch({ ...a, id: "c" }), /inventory/);
  w.entries.get(a.id).priceSats = 10001;
  await assert.rejects(
    w.poll(() => {}),
    /price/
  );
  w.entries.get(a.id).priceSats = 10000;
  const events = [];
  await w.poll((e) => events.push(e));
  assert.equal(events.length, 2);
  assert.equal(events[0].satoshis, 20001);
});
test("pool replay rejects over-cap held sum and prep rows", (t) => {
  const p = pool(t),
    raw = buildPrep(root(100000), 0, key("livenet"), 500, main),
    file = p.ledgerPath;
  p.close();
  fs.writeFileSync(
    file,
    JSON.stringify({
      type: "prepared",
      txid: raw.id,
      source: root(100000).id + ":0",
      inputSats: 100001,
      amount: 99500,
      prepFee: 501,
      raw: raw.uncheckedSerialize(),
    }) + "\n"
  );
  const d = dir(t),
    kp = path.join(d, "key");
  fs.writeFileSync(kp, key("livenet").toWIF(), { mode: 0o600 });
  assert.throws(
    () =>
      new SponsorPool({
        keyPath: kp,
        ledgerPath: file,
        rpc: async () => {},
        ...main,
      }),
    /prep/
  );
});
test("aggregate pool replay cannot exceed hard cap; constants cannot be configured", (t) => {
  const Canary = require("../canary");
  assert.ok(Object.isFrozen(Canary.CAPS));
  assert.throws(() => {
    Canary.CAPS.pool = 999999;
  }, TypeError);
  const p = pool(t),
    file = p.ledgerPath;
  p.close();
  const rows = [1, 2, 3].map((n) => {
    const r = root(100000);
    r.inputs[0].prevTxId = Buffer.alloc(32, n);
    const tx = buildPrep(r, 0, key("livenet"), 500, main);
    return {
      type: "prepared",
      txid: tx.id,
      source: r.id + ":0",
      inputSats: 100000,
      amount: 99500,
      prepFee: 500,
      raw: tx.uncheckedSerialize(),
    };
  });
  fs.writeFileSync(file, rows.map(JSON.stringify).join("\n") + "\n");
  const kp = path.join(dir(t), "key");
  fs.writeFileSync(kp, key("livenet").toWIF(), { mode: 0o600 });
  assert.throws(
    () =>
      new SponsorPool({
        keyPath: kp,
        ledgerPath: file,
        rpc: async () => {},
        ...main,
      }),
    /pool cap/
  );
});
test("HTTP chain route is explicit, no non-GET requests", async () => {
  let url;
  const h = new HttpTransport({
    baseUrl: "https://example.invalid",
    chain: "testnet",
    fetchImpl: async (u, o) => {
      url = u;
      assert.equal(o.method, "GET");
      return { ok: true, json: async () => ({}) };
    },
  });
  await h.json("chain/info");
  assert.match(url, /bsv\/test\/chain/);
});
