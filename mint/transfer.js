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
    Canary.bind(this, { chain, canary });
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
    Canary.chain(this.policy, (await this.rpc("getblockchaininfo")).chain);
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
    if (detail.hex !== raw) throw Error("Transaction bytes mismatch");
    if (
      !Number.isSafeInteger(detail.confirmations) ||
      detail.confirmations < this.depth ||
      !detail.blockhash
    )
      return false;
    const block = await this.rpc("getblock", [detail.blockhash]);
    return block.confirmations > 0 && block.tx.includes(txid);
  }
  async run(id) {
    if (active.has(this.store)) return;
    active.add(this.store);
    try {
      await this.guard();
      let b = this.store.get(id);
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
      if (await this.included(tr.txid, tr.raw)) {
        return this.store.update(id, {
          state: "TRANSFERRED",
          transfer: { ...tr, stage: "INCLUDED" },
        });
      }
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
