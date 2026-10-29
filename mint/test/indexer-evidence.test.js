"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const { bsv, output, pay } = require("../../vault/src/ordinal-pair");
const { HttpTransport } = require("../watcher");
function fixture(change = () => {}) {
  const key = new bsv.PrivateKey(new bsv.crypto.BN(1), bsv.Networks.testnet);
  const tx = new bsv.Transaction()
    .addInput(
      new bsv.Transaction.Input({
        prevTxId: "01".repeat(32),
        outputIndex: 0,
        script: "",
        output: output(bsv.Script.empty()),
      })
    )
    .addOutput(output(pay(key.publicKey.toString()), 1));
  const hash = "02".repeat(32),
    tip = { chain: "main", blocks: 105, bestblockhash: "03".repeat(32) };
  const detail = {
    txid: tx.id,
    blockhash: hash,
    blockheight: 100,
    confirmations: 6,
    vout: [
      {
        n: 0,
        value: 1e-8,
        scriptPubKey: { hex: tx.outputs[0].script.toHex() },
      },
    ],
  };
  const block = { hash, height: 100, confirmations: 6, tx: [tx.id] };
  const state = {
    tip,
    detail,
    block,
    raw: tx.uncheckedSerialize(),
    after: structuredClone(tip),
  };
  change(state);
  let tips = 0;
  const transport = new HttpTransport({
    baseUrl: "https://fixture.invalid",
    chain: "mainnet",
    canary: true,
    apiPrefix: "/v1/bsv",
    fetchImpl: async (u, o) => {
      assert.equal(o.method, "GET");
      const route = new URL(u).pathname.split("/main/")[1];
      const data =
        route === "chain/info"
          ? tips++
            ? state.after
            : state.tip
          : route.startsWith("block/")
          ? state.block
          : route.endsWith("/hex")
          ? state.raw
          : state.detail;
      return {
        ok: true,
        json: async () => structuredClone(data),
        text: async () => data,
      };
    },
  });
  return () => transport.transactionEvidence(tx.id);
}
test("transaction evidence matches raw bytes, outputs and exact confirmation arithmetic", async () => {
  const e = await fixture()();
  assert.equal(e.confirmations, 6);
});
for (const [name, mutate] of [
  ["script", (s) => (s.detail.vout[0].scriptPubKey.hex = "00")],
  ["value", (s) => (s.detail.vout[0].value = 2e-8)],
  ["txid", (s) => (s.detail.txid = "00".repeat(32))],
  ["confirmation", (s) => (s.detail.confirmations = 5)],
  ["height", (s) => (s.detail.blockheight = 99)],
  ["membership", (s) => (s.block.tx = [])],
  ["reorg", (s) => (s.after.bestblockhash = "04".repeat(32))],
  ["raw", (s) => (s.raw = "00")],
  ["block identity", (s) => (s.block.hash = "04".repeat(32))],
  ["block confirmation", (s) => (s.block.confirmations = 0)],
])
  test("transaction evidence fails closed: " + name, async () => {
    await assert.rejects(fixture(mutate)());
  });
