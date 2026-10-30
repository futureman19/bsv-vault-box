"use strict";
// One fixed WoC origin; no ARC fallback: ambiguous submissions must be reconciled.
const assert = require("node:assert/strict");
const { bsv } = require("../vault/src/ordinal-pair");
const Canary = require("./canary");
const { HttpTransport } = require("./watcher");
const ORIGIN = "https://api.whatsonchain.com";
const PREFIX = "/v1/bsv/main/";
function createMainnetAdapter({
  authorization,
  fetchImpl = fetch,
  requests = [],
} = {}) {
  const options = { chain: "mainnet", canary: true, authorization };
  const policy = Canary.policy(options);
  const transport = new HttpTransport({
    ...options,
    baseUrl: ORIGIN,
    apiPrefix: "/v1/bsv",
    timeoutMs: 15000,
    fetchImpl: async (url, opts) => {
      const u = new URL(url);
      assert.equal(u.origin, ORIGIN);
      assert.ok(!u.search && !u.hash && !u.username && !u.password);
      assert.equal(opts.method, "GET");
      assert.equal(opts.redirect, "error");
      assert.ok(!opts.body);
      assert.match(
        u.pathname,
        /^\/v1\/bsv\/main\/(?:chain\/info|address\/[1-9A-HJ-NP-Za-km-z]+\/unspent(?:\/all)?|script\/[0-9a-f]{64}\/unspent\/all|tx\/[0-9a-f]{64}(?:\/hex)?|block\/hash\/[0-9a-f]{64})$/
      );
      const r = await fetchImpl(url, opts);
      requests.push({ method: "GET", url, status: r.status });
      assert.ok(!r.headers?.get("next-page"), "Paginated UTXO set");
      if (r.status === 404) {
        const e = Error("Not indexed");
        e.code = -5;
        throw e;
      }
      return r;
    },
  });
  async function rpc(method, args = []) {
    if (method === "sendrawtransaction") {
      Canary.broadcast(policy); // before parsing, signing, fetch or any side effect
      assert.equal(args.length, 1);
      const raw = args[0];
      assert.match(raw, /^(?:[0-9a-f]{2})+$/);
      const tx = new bsv.Transaction(raw);
      assert.equal(tx.uncheckedSerialize(), raw);
      const url = ORIGIN + PREFIX + "tx/raw";
      const r = await fetchImpl(url, {
        method: "POST",
        redirect: "error",
        signal: AbortSignal.timeout(15000),
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ txhex: raw }),
      });
      requests.push({ method: "POST", url, status: r.status, txid: tx.id });
      assert.ok(
        r.ok,
        "Broadcast outcome unknown; reconcile, never retry automatically"
      );
      const text = (await r.text()).trim();
      // WoC returns a JSON string txid; accept a plain-text txid too, never objects.
      const id = text.startsWith('"') ? JSON.parse(text) : text;
      assert.equal(id, tx.id, "Broadcast txid mismatch; reconcile");
      return id;
    }
    if (method === "getblockchaininfo") return transport.json("chain/info");
    if (method === "getblock") {
      assert.match(args[0], /^[0-9a-f]{64}$/);
      return transport.json("block/hash/" + args[0]);
    }
    if (method === "getrawtransaction") {
      assert.match(args[0], /^[0-9a-f]{64}$/);
      const d = await transport.json("tx/" + args[0]);
      if (d.blockhash) {
        const e = await transport.transactionEvidence(args[0]);
        return args[1] ? { ...e.detail, hex: e.raw } : e.raw;
      }
      const raw = (await transport.json("tx/" + args[0] + "/hex", true)).trim();
      assert.equal(new bsv.Transaction(raw).id, args[0]);
      return args[1] ? { txid: args[0], hex: raw, confirmations: 0 } : raw;
    }
    if (method === "gettxout") {
      const e = await transport.transactionEvidence(args[0]);
      assert.ok(Number.isSafeInteger(args[1]) && args[1] >= 0);
      const out = new bsv.Transaction(e.raw).outputs[args[1]];
      assert.ok(out);
      const hash = bsv.crypto.Hash.sha256(out.script.toBuffer())
        .reverse()
        .toString("hex");
      const rows = await transport.json("script/" + hash + "/unspent/all");
      assert.ok(
        rows &&
          rows.error === "" &&
          Array.isArray(rows.result) &&
          !rows["next-page"] &&
          rows.result.length < 1000,
        "Incomplete UTXO evidence"
      );
      const matches = rows.result.filter(
        (r) => r.tx_hash === args[0] && r.tx_pos === args[1]
      );
      assert.ok(matches.length <= 1, "Duplicate outpoint");
      const row = matches[0];
      if (!row || row.isSpentInMempoolTx === true) return null;
      assert.equal(row.isSpentInMempoolTx, false);
      assert.equal(row.status, "confirmed");
      assert.equal(row.value, out.satoshis);
      assert.equal(row.height, e.block.height);
      const tip = await transport.json("chain/info");
      assert.equal(tip.bestblockhash, e.tip.bestblockhash);
      return {
        value: out.satoshis / 1e8,
        scriptPubKey: { hex: out.script.toHex() },
        confirmations: e.confirmations,
      };
    }
    throw Error("Unsupported canary RPC method");
  }
  return Object.freeze({ rpc, transport, policy, requests });
}
module.exports = { createMainnetAdapter };
