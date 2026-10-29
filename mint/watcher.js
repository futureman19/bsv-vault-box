"use strict";
const { bsv } = require("../vault/src/ordinal-pair");
const Canary = require("./canary");
function valid(p) {
  if (
    !p ||
    !Number.isSafeInteger(p.satoshis) ||
    p.satoshis < 0 ||
    !Number.isSafeInteger(p.confirmations) ||
    p.confirmations < 0 ||
    !Array.isArray(p.refs) ||
    new Set(p.refs).size !== p.refs.length
  )
    throw Error("Invalid payment evidence");
  return p;
}
class PaymentWatcher {
  constructor({ transport, depth = 1, chain, canary } = {}) {
    Canary.bind(this, { chain, canary });
    Canary.match(this.policy, transport);
    if (!Number.isSafeInteger(depth) || depth < 1) throw Error("Invalid depth");
    this.transport = transport;
    this.depth = depth;
    this.entries = new Map();
    this.seen = new Map();
  }
  watch(entry) {
    Canary.box(this.policy, entry);
    Canary.cap(
      this.policy,
      "inventory",
      this.entries.size + (this.entries.has(entry.id) ? 0 : 1)
    );
    if (
      this.entries.has(entry.id) &&
      this.entries.get(entry.id).payAddress !== entry.payAddress
    )
      throw Error("Address cannot change");
    this.entries.set(entry.id, { ...entry });
  }
  async poll(onPayment) {
    Canary.match(this.policy, this.transport);
    Canary.inventory(this.policy, [...this.entries.values()]);
    if (this.busy) return;
    this.busy = true;
    try {
      for (const e of this.entries.values()) {
        const p = valid(await this.transport.read(e.payAddress, this.depth));
        if (p.satoshis < 1 || p.confirmations < this.depth) continue;
        const fingerprint = JSON.stringify([p.satoshis, [...p.refs].sort()]);
        if (this.seen.get(e.id) === fingerprint) continue;
        await onPayment({ ...p, id: e.id, payAddress: e.payAddress });
        this.seen.set(e.id, fingerprint);
      }
    } finally {
      this.busy = false;
    }
  }
}
// Read-only production-shaped adapter. Balance is only a polling hint, never a
// confirmation count. Deployments must supply independently verified tx evidence.
class HttpTransport {
  constructor({
    baseUrl,
    apiPrefix = "/api/v1/bsv",
    chain,
    canary,
    fetchImpl = fetch,
    evidenceReader,
    timeoutMs = 5000,
  }) {
    Canary.bind(this, { chain, canary });
    const u = new URL(baseUrl);
    if (u.username || u.password || !["http:", "https:"].includes(u.protocol))
      throw Error("Invalid indexer URL");
    if (!["/api/v1/bsv", "/v1/bsv"].includes(apiPrefix))
      throw Error("Invalid API prefix");
    this.apiPrefix = apiPrefix;
    this.base = baseUrl.replace(/\/$/, "");
    this.fetch = fetchImpl;
    this.evidenceReader = evidenceReader;
    this.timeoutMs = timeoutMs;
  }
  async json(route, text = false) {
    const r = await this.fetch(
      this.base +
        this.apiPrefix +
        "/" +
        (this.policy.chain === "testnet" ? "test" : "main") +
        "/" +
        route,
      {
        method: "GET",
        redirect: "error",
        signal: AbortSignal.timeout(this.timeoutMs),
      }
    );
    if (!r.ok) throw Error("Indexer evidence unavailable");
    return text ? r.text() : r.json();
  }
  // Immutable transaction evidence anchored to serialized bytes and an active block.
  // No SPV claim: block membership/active status still trusts the indexer.
  async transactionEvidence(txid) {
    if (!/^[0-9a-f]{64}$/.test(txid)) throw Error("Invalid txid");
    const tip = await this.json("chain/info");
    if (this.policy.chain !== "regtest") Canary.chain(this.policy, tip.chain);
    const detail = await this.json("tx/" + txid);
    const raw = (await this.json("tx/" + txid + "/hex", true)).trim();
    if (!/^(?:[0-9a-f]{2})+$/.test(raw))
      throw Error("Invalid transaction bytes");
    const tx = new bsv.Transaction(raw);
    if (
      tx.id !== txid ||
      detail.txid !== txid ||
      !tx.toBuffer().equals(Buffer.from(raw, "hex"))
    )
      throw Error("Transaction identity mismatch");
    if (!Array.isArray(detail.vout) || detail.vout.length !== tx.outputs.length)
      throw Error("Output mismatch");
    tx.outputs.forEach((o, i) => {
      if (
        detail.vout[i].n !== i ||
        detail.vout[i].scriptPubKey?.hex !== o.script.toHex() ||
        Math.round(detail.vout[i].value * 1e8) !== o.satoshis
      )
        throw Error("Output evidence mismatch");
    });
    if (!/^[0-9a-f]{64}$/.test(detail.blockhash))
      throw Error("Unconfirmed transaction");
    const block = await this.json("block/hash/" + detail.blockhash);
    const after = await this.json("chain/info");
    if (
      after.bestblockhash !== tip.bestblockhash ||
      after.blocks !== tip.blocks
    )
      throw Error("Chain changed during evidence read");
    const count = tip.blocks - block.height + 1;
    if (
      !Number.isSafeInteger(tip.blocks) ||
      !Number.isSafeInteger(block.height) ||
      block.height < 0 ||
      count < 1 ||
      block.hash !== detail.blockhash ||
      detail.blockheight !== block.height ||
      detail.confirmations !== count ||
      block.confirmations !== count ||
      !block.tx?.includes(txid)
    )
      throw Error("Inconsistent confirmation evidence");
    return { txid, raw, detail, block, tip, confirmations: count };
  }
  async details(address, depth) {
    const rows = await this.json(
      "address/" + encodeURIComponent(address) + "/unspent"
    );
    const tip = await this.json("chain/info");
    if (
      !Array.isArray(rows) ||
      rows.length > 1000 ||
      !Number.isSafeInteger(tip.blocks)
    )
      throw Error("Invalid transaction evidence");
    const script = bsv.Script.buildPublicKeyHashOut(address).toHex();
    let satoshis = 0,
      confirmations = Infinity;
    const refs = [];
    for (const row of rows) {
      if (
        !/^[0-9a-f]{64}$/.test(row.tx_hash) ||
        !Number.isSafeInteger(row.tx_pos) ||
        row.tx_pos < 0 ||
        !Number.isSafeInteger(row.height) ||
        row.height < 0 ||
        !Number.isSafeInteger(row.value) ||
        row.value < 1
      )
        throw Error("Invalid transaction evidence");
      if (row.height === 0) continue;
      const count = tip.blocks - row.height + 1;
      if (count < depth) continue;
      const tx = await this.json("tx/" + row.tx_hash);
      const out = tx.vout?.[row.tx_pos];
      if (
        tx.txid !== row.tx_hash ||
        !Number.isSafeInteger(tx.confirmations) ||
        tx.confirmations < count ||
        !out ||
        out.scriptPubKey?.hex !== script ||
        Math.round(out.value * 1e8) !== row.value
      )
        throw Error("Inconsistent transaction evidence");
      satoshis += row.value;
      confirmations = Math.min(confirmations, count);
      refs.push(row.tx_hash + ":" + row.tx_pos);
    }
    return { satoshis, confirmations: refs.length ? confirmations : 0, refs };
  }
  async read(address, depth = 1) {
    const r = await this.fetch(
      `${this.base}${this.apiPrefix}/${
        this.policy.chain === "testnet" ? "test" : "main"
      }/address/${encodeURIComponent(address)}/balance`,
      {
        method: "GET",
        redirect: "error",
        signal: AbortSignal.timeout(this.timeoutMs),
      }
    );
    if (!r.ok) throw Error("Indexer HTTP failure");
    const balance = await r.json();
    if (!Number.isSafeInteger(balance.confirmed) || balance.confirmed < 0)
      throw Error("Invalid balance");
    const p = valid(
      await (this.evidenceReader
        ? this.evidenceReader(address, depth)
        : this.details(address, depth))
    );
    if (p.satoshis > balance.confirmed)
      throw Error("Inconsistent balance evidence");
    return p;
  }
}
// Bounded local chain scan, not wallet RPC. Re-scan at each poll to handle reorgs.
// Payment outputs are counted even if later spent, since receipt != balance.
class RegtestTransport {
  constructor({ rpc, startHeight = 1, maxBlocks = 10000, chain, canary }) {
    Canary.bind(this, { chain, canary });
    if (this.policy.chain !== "regtest")
      throw Error("Regtest transport requires regtest chain");
    this.rpc = rpc;
    this.startHeight = startHeight;
    this.maxBlocks = maxBlocks;
  }
  async read(address, depth = 1) {
    const info = await this.rpc("getblockchaininfo");
    if (info.chain !== "regtest") throw Error("regtest only");
    if (info.blocks - this.startHeight + 1 > this.maxBlocks)
      throw Error("Scan bound exceeded");
    const script = bsv.Script.buildPublicKeyHashOut(address).toHex();
    let satoshis = 0,
      confirmations = Infinity;
    const refs = [];
    for (let height = this.startHeight; height <= info.blocks; height++) {
      const count = info.blocks - height + 1;
      if (count < depth) continue;
      const hash = await this.rpc("getblockhash", [height]);
      const block = await this.rpc("getblock", [hash]);
      for (const id of block.tx) {
        const tx = new bsv.Transaction(
          await this.rpc("getrawtransaction", [id])
        );
        if (tx.isCoinbase()) continue;
        for (let i = 0; i < tx.outputs.length; i++) {
          const o = tx.outputs[i];
          if (o.script.toHex() === script) {
            satoshis += o.satoshis;
            confirmations = Math.min(confirmations, count);
            refs.push(id + ":" + i);
          }
        }
      }
    }
    if (
      (await this.rpc("getblockchaininfo")).bestblockhash !== info.bestblockhash
    )
      throw Error("Chain changed during scan");
    return valid({
      satoshis,
      confirmations: refs.length ? confirmations : 0,
      refs,
    });
  }
}
module.exports = { PaymentWatcher, HttpTransport, RegtestTransport };
