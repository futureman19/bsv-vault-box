"use strict";
const M = require("../vault/src/ordinal-pair");
const { loadKey } = require("./keys"),
  { parsePrep } = require("./pool");
const Canary = require("./canary");
const active = new WeakSet();
class TransferWorker {
  #inventoryKey;
  #sponsorKey;
  constructor({
    store,
    chain,
    canary,
    authorization,
    rpc,
    pool,
    inventory,
    inventoryKeyPath,
    sponsorKeyPath,
    paymentTransport,
    depth = 1,
    fee = 500,
    maxAttempts = 3,
    retryMs = 1000,
  } = {}) {
    Canary.bind(this, { chain, canary, authorization });
    if (!Number.isSafeInteger(fee) || fee < 1 || fee > Canary.CAPS.fee)
      throw Error("Invalid fee cap");
    if (
      !Number.isSafeInteger(depth) ||
      depth < 1 ||
      !Number.isSafeInteger(maxAttempts) ||
      maxAttempts < 1 ||
      maxAttempts > 10 ||
      !Number.isSafeInteger(retryMs) ||
      retryMs < 0
    )
      throw Error("Invalid retry/finality policy");
    this.store = store;
    this.rpc = rpc;
    this.pool = pool;
    this.inventory = inventory;
    this.paymentTransport = paymentTransport;
    this.depth = depth;
    this.fee = fee;
    this.maxAttempts = maxAttempts;
    this.retryMs = retryMs;
    this.checkCaps();
    this.#inventoryKey = loadKey(inventoryKeyPath, this.policy);
    this.#sponsorKey = loadKey(sponsorKeyPath, this.policy);
  }
  checkCaps() {
    if (
      !Number.isSafeInteger(this.fee) ||
      this.fee < 1 ||
      this.fee > Canary.CAPS.fee
    )
      throw Error("Invalid fee cap");
    for (const c of [this.store, this.pool, this.paymentTransport])
      Canary.match(this.policy, c);
    if (this.policy.canary) Canary.inventory(this.policy, this.store.all());
  }
  async checkPayment(b) {
    this.checkCaps();
    Canary.box(this.policy, b);
    const p = await this.paymentTransport.read(b.payAddress, this.depth);
    if (p && Canary.overpaid(this.policy, p.satoshis, b.priceSats))
      throw Error("Canary payment cap exceeded");
    if (
      !p ||
      !Number.isSafeInteger(p.satoshis) ||
      !Number.isSafeInteger(p.confirmations) ||
      p.satoshis < b.priceSats ||
      p.confirmations < this.depth
    )
      throw Error("Payment no longer confirmed");
  }
  async guard() {
    this.checkCaps();
    let info;
    try {
      info = await this.rpc("getblockchaininfo");
    } catch {
      const e = Error("Chain observation unavailable");
      e.code = "CHAIN_OBSERVATION_UNAVAILABLE";
      throw e;
    }
    Canary.chain(this.policy, info.chain);
    this.checkCaps();
  }
  async unspent(tx, index) {
    const o = tx.outputs[index],
      u = await this.rpc("gettxout", [tx.id, index]);
    if (
      !u ||
      u.confirmations < 1 ||
      Math.round(u.value * 1e8) !== o.satoshis ||
      u.scriptPubKey.hex !== o.script.toHex()
    )
      throw Error("Chain UTXO missing or mismatched");
  }
  async included(txid, raw) {
    let detail;
    try {
      detail = await this.rpc("getrawtransaction", [txid, true]);
    } catch (e) {
      if (e.code === -5) return false;
      throw e;
    }
    if (
      !detail ||
      typeof detail !== "object" ||
      Array.isArray(detail) ||
      detail.hex !== raw
    )
      throw Error("Transaction bytes mismatch");
    if (!Number.isSafeInteger(detail.confirmations) || detail.confirmations < 0)
      throw Error("Invalid transaction depth");
    if (detail.confirmations < this.depth) return false;
    if (
      typeof detail.blockhash !== "string" ||
      !/^[0-9a-f]{64}$/.test(detail.blockhash)
    )
      throw Error("Invalid transaction block identity");
    const block = await this.rpc("getblock", [detail.blockhash]);
    // Contradictory/malformed evidence is unavailable, not permission to retry.
    if (
      !block ||
      typeof block !== "object" ||
      Array.isArray(block) ||
      block.hash !== detail.blockhash ||
      !Number.isSafeInteger(block.confirmations) ||
      block.confirmations < this.depth ||
      !Array.isArray(block.tx) ||
      block.tx.some(
        (id) => typeof id !== "string" || !/^[0-9a-f]{64}$/.test(id)
      )
    )
      throw Error("Invalid block finality evidence");
    return block.tx.includes(txid);
  }
  // Observation is independent of custody history. Holds are monotonic and
  // require operator reconciliation; a healthy later read never clears one.
  async observeFinality(id, b, included, unavailable = false) {
    const reasons = new Set(b.reconciliationReasons || []);
    if (unavailable) reasons.add("TRANSFER_OBSERVATION_UNAVAILABLE");
    else if (!included && ["TRANSFERRED", "OPENED"].includes(b.state))
      reasons.add("TRANSFER_FINALITY_LOST");
    let excess = false;
    try {
      const p = await this.paymentTransport.read(b.payAddress, this.depth);
      if (
        !p ||
        !Number.isSafeInteger(p.satoshis) ||
        p.satoshis < 0 ||
        !Number.isSafeInteger(p.confirmations) ||
        p.confirmations < 0
      ) {
        reasons.add("PAYMENT_OBSERVATION_UNAVAILABLE");
      } else {
        if (p.satoshis < b.priceSats || p.confirmations < this.depth)
          reasons.add("PAYMENT_FINALITY_LOST");
        if (p.satoshis > b.priceSats) {
          reasons.add("PAYMENT_EXCESS");
          excess = true;
        }
      }
    } catch {
      reasons.add("PAYMENT_OBSERVATION_UNAVAILABLE");
    }
    const patch = {};
    if (included && b.state === "PAID_PENDING") {
      patch.state = "TRANSFERRED";
      patch.transfer = { ...b.transfer, stage: "INCLUDED" };
    }
    const all = [...reasons].sort();
    if (
      all.length &&
      (!b.reconciliationRequired ||
        JSON.stringify(all) !== JSON.stringify(b.reconciliationReasons))
    ) {
      patch.reconciliationRequired = true;
      patch.reconciliationReasons = all;
    }
    if (excess && !b.refundRequired) patch.refundRequired = true;
    return Object.keys(patch).length ? this.store.update(id, patch) : b;
  }
  async run(id) {
    if (active.has(this.store)) return;
    active.add(this.store);
    try {
      let b;
      try {
        await this.guard();
      } catch (e) {
        if (e.code !== "CHAIN_OBSERVATION_UNAVAILABLE") throw e;
        this.checkCaps();
        b = this.store.get(id);
        if (
          !b.transfer?.raw ||
          !["PAID_PENDING", "TRANSFERRED", "OPENED"].includes(b.state)
        )
          throw e;
        return await this.observeFinality(id, b, false, true);
      }
      b = this.store.get(id);
      if (["TRANSFERRED", "OPENED"].includes(b.state) && b.transfer?.raw) {
        let included = false,
          unavailable = false;
        try {
          included = await this.included(b.transfer.txid, b.transfer.raw);
        } catch {
          unavailable = true;
        }
        return await this.observeFinality(id, b, included, unavailable);
      }
      if (b.state !== "PAID_PENDING") return b;
      if (b.transfer?.stage === "RESERVING")
        throw Error(
          "Ambiguous funding reservation; manual reconciliation required"
        );
      // No reservation, signing or broadcast on mainnet in the read-only phase.
      Canary.box(this.policy, b);
      Canary.broadcast(this.policy);
      if (!b.transfer) {
        await this.checkPayment(b);
        const { f, source } = await this.inventory(b.inventoryId);
        const c = M.C.fromHex(source.outputs[0].script.toHex());
        if (
          c.phase !== 2n ||
          c.owner !== this.#inventoryKey.publicKey.toString() ||
          source.outputs[0].satoshis !== 1 ||
          source.outputs[1].satoshis !== 1 ||
          source.outputs[0].script.toHex() !== source.outputs[1].script.toHex()
        )
          throw Error("Invalid sealed inventory");
        await this.unspent(source, 0);
        await this.unspent(source, 1);
        this.store.update(id, { transfer: { stage: "RESERVING" } });
        const funding = await this.pool.dispense();
        if (!funding) {
          this.store.update(id, { transfer: null });
          return this.store.get(id);
        }
        // Once dispensed, any error stays RESERVING: never allocate another parent.
        const parsed = parsePrep(
          funding.toBuffer(),
          this.#sponsorKey.publicKey.toString()
        );
        Canary.cap(this.policy, "prep", parsed.amount);
        await this.unspent(funding, 0);
        this.checkCaps();
        const result = M.transition(
          f,
          source,
          2,
          this.#inventoryKey,
          b.buyerPubkey,
          null,
          undefined,
          {
            sponsor: this.#sponsorKey,
            funding: parsed.amount,
            fee: this.fee,
            fundingTx: funding,
          }
        );
        if (!result.result.success)
          throw Error("Transition verification failed");
        const tx = result.tx;
        if (
          tx.inputs.length !== 3 ||
          tx.outputs[0].satoshis !== 1 ||
          tx.outputs[1].satoshis !== 1
        )
          throw Error("Transition shape mismatch");
        this.store.update(id, {
          transfer: {
            stage: "BUILT",
            txid: tx.id,
            raw: tx.uncheckedSerialize(),
            fundingRaw: funding.uncheckedSerialize(),
            sourceRaw: source.uncheckedSerialize(),
            attempts: 0,
            nextAttemptAt: 0,
          },
        });
      }
      b = this.store.get(id);
      let tr = b.transfer;
      let included = false,
        unavailable = false;
      try {
        included = await this.included(tr.txid, tr.raw);
      } catch {
        unavailable = true;
      }
      if (
        included ||
        unavailable ||
        tr.stage === "SUBMITTED" ||
        b.reconciliationRequired
      )
        return await this.observeFinality(id, b, included, unavailable);
      if (
        tr.stage === "SUBMITTED" ||
        tr.attempts >= this.maxAttempts ||
        Date.now() < tr.nextAttemptAt
      )
        return b;
      await this.guard();
      await this.checkPayment(b);
      tr = {
        ...tr,
        attempts: tr.attempts + 1,
        nextAttemptAt: Date.now() + this.retryMs * 2 ** tr.attempts,
      };
      this.store.update(id, { transfer: tr });
      try {
        this.checkCaps();
        Canary.broadcast(this.policy);
        const txid = await this.rpc("sendrawtransaction", [tr.raw]);
        if (txid !== tr.txid) throw Error("Broadcast id mismatch");
        this.store.update(id, { transfer: { ...tr, stage: "SUBMITTED" } });
      } catch {
        this.store.update(id, { transfer: { ...tr, stage: "UNCERTAIN" } });
      }
      return this.store.get(id);
    } finally {
      active.delete(this.store);
    }
  }
  // Buyer key never enters this worker. Observe a mined buyer-authored OPEN.
  async observeOpen(id, raw, fundingRaw) {
    await this.guard();
    const b = this.store.get(id);
    if (b.state !== "TRANSFERRED") throw Error("Not transferred");
    const tx = new M.bsv.Transaction(raw),
      parent = new M.bsv.Transaction(b.transfer.raw),
      funding = new M.bsv.Transaction(fundingRaw);
    if (
      tx.inputs.length !== 3 ||
      tx.inputs[0].prevTxId.toString("hex") !== parent.id ||
      tx.inputs[0].outputIndex !== 0 ||
      tx.inputs[1].prevTxId.toString("hex") !== parent.id ||
      tx.inputs[1].outputIndex !== 1
    )
      throw Error("Not a direct open");
    const c = M.C.fromHex(tx.outputs[0].script.toHex());
    if (
      c.phase !== 3n ||
      c.owner !== b.buyerPubkey ||
      !M.verify(tx, [parent, funding]).success
    )
      throw Error("Invalid open");
    if (!(await this.included(tx.id, raw))) throw Error("Open not confirmed");
    return this.store.update(id, { state: "OPENED", openTxid: tx.id });
  }
}
module.exports = { TransferWorker };
