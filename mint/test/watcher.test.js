"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const {
  PaymentWatcher,
  HttpTransport,
  RegtestTransport,
} = require("../watcher");
test("confirmed threshold and dedup; overlapping polls do not emit twice", async () => {
  let confirmations = 0;
  const w = new PaymentWatcher({
    transport: {
      read: async () => ({ satoshis: 1000, confirmations, refs: ["a:0"] }),
    },
    depth: 2,
  });
  w.watch({ id: "a", payAddress: "addr", priceSats: 1000 });
  const got = [];
  await w.poll((e) => got.push(e));
  assert.equal(got.length, 0);
  confirmations = 2;
  await Promise.all([w.poll((e) => got.push(e)), w.poll((e) => got.push(e))]);
  assert.equal(got.length, 1);
  assert.equal(got[0].confirmations, 2);
});
test("failed event handling can be retried", async () => {
  const w = new PaymentWatcher({
    transport: {
      read: async () => ({ satoshis: 1, confirmations: 1, refs: ["a:0"] }),
    },
  });
  w.watch({ id: "a", payAddress: "addr", priceSats: 1 });
  await assert.rejects(
    w.poll(() => {
      throw Error("disk");
    }),
    /disk/
  );
  let n = 0;
  await w.poll(() => n++);
  assert.equal(n, 1);
});
test("HTTP balance alone is never finality evidence", async () => {
  const calls = [];
  const h = new HttpTransport({
    baseUrl: "http://127.0.0.1:1",
    fetchImpl: async (url) => {
      calls.push(url);
      return {
        ok: true,
        json: async () => ({ confirmed: 10, unconfirmed: 0 }),
      };
    },
  });
  await assert.rejects(h.read("addr"), /evidence/);
  assert.match(calls[0], /\/api\/v1\/bsv\/main\/address\/addr\/balance$/);
});
test("partial confirmed late funds still emit for refund accounting", async () => {
  const w = new PaymentWatcher({
    transport: {
      read: async () => ({ satoshis: 1, confirmations: 1, refs: ["a:0"] }),
    },
  });
  w.watch({ id: "a", payAddress: "addr", priceSats: 100 });
  let n = 0;
  await w.poll(() => n++);
  assert.equal(n, 1);
});
test("HTTP detail transport validates output amount, address and block height", async () => {
  const { fixture, bsv } = require("../../vault/src/ordinal-pair");
  const address = fixture().alice.toAddress().toString();
  const script = bsv.Script.buildPublicKeyHashOut(address).toHex();
  const hash = "a".repeat(64);
  const fetchImpl = async (url) => ({
    ok: true,
    json: async () =>
      url.endsWith("/balance")
        ? { confirmed: 42 }
        : url.endsWith("/unspent")
        ? [{ tx_hash: hash, tx_pos: 0, value: 42, height: 9 }]
        : url.endsWith("/chain/info")
        ? { blocks: 10 }
        : url.endsWith("/hex")
        ? null
        : {
            txid: hash,
            confirmations: 2,
            vout: [{ value: 0.00000042, scriptPubKey: { hex: script } }],
          },
  });
  const h = new HttpTransport({ baseUrl: "http://127.0.0.1:1", fetchImpl });
  assert.deepEqual(await h.read(address, 2), {
    satoshis: 42,
    confirmations: 2,
    refs: [hash + ":0"],
  });
});
test("regtest transport refuses other chains", async () => {
  const r = new RegtestTransport({ rpc: async () => ({ chain: "main" }) });
  await assert.rejects(r.read("addr"), /regtest/);
});
