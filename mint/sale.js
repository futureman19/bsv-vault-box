"use strict";
const fs = require("node:fs"),
  path = require("node:path");
const { bsv } = require("../vault/src/ordinal-pair");
const copy = (x) => JSON.parse(JSON.stringify(x));
function positive(n) {
  if (!Number.isSafeInteger(n) || n < 1)
    throw Error("Positive integer required");
  return n;
}
function publicKey(pub) {
  if (
    typeof pub !== "string" ||
    !/^0[23][0-9a-f]{64}$/.test(pub) ||
    !bsv.PublicKey.isValid(pub)
  )
    throw Error("Compressed buyer public key required");
  return pub;
}
// Crash locks require manual reconciliation; allocations are never recycled.
class SaleStore {
  constructor({ file, xpub }) {
    if (!path.isAbsolute(file)) throw Error("Absolute journal path required");
    this.hd = new bsv.HDPublicKey(xpub);
    if (this.hd.network.name !== "testnet")
      throw Error("Testnet xpub required");
    this.file = file;
    this.xpub = xpub;
    this.boxes = new Map();
    this.closed = false;
    this.lock = fs.openSync(file + ".lock", "wx", 0o600);
    try {
      this.fd = fs.openSync(file, "a+", 0o600);
      const text = fs.readFileSync(this.fd, "utf8");
      if (text && !text.endsWith("\n")) throw Error("Truncated journal");
      for (const line of text.split("\n").filter(Boolean)) {
        const e = JSON.parse(line);
        if (e.xpub !== xpub || !e.box || typeof e.box.id !== "string")
          throw Error("Invalid journal");
        this.boxes.set(e.box.id, e.box);
      }
    } catch (e) {
      this.close();
      throw e;
    }
  }
  assertOpen() {
    if (this.closed) throw Error("Sale store closed");
  }
  append(box) {
    this.assertOpen();
    const buf = Buffer.from(JSON.stringify({ xpub: this.xpub, box }) + "\n");
    try {
      let n = 0;
      while (n < buf.length) {
        const wrote = fs.writeSync(this.fd, buf, n, buf.length - n);
        if (!wrote) throw Error("Journal short write");
        n += wrote;
      }
      fs.fsyncSync(this.fd);
    } catch (e) {
      this.close();
      throw e;
    }
    this.boxes.set(box.id, copy(box));
    return copy(box);
  }
  all() {
    this.assertOpen();
    return [...this.boxes.values()].map(copy);
  }
  get(id) {
    this.assertOpen();
    const b = this.boxes.get(id);
    if (!b) throw Error("Box not found");
    return copy(b);
  }
  list({ priceSats, inventoryId }) {
    this.assertOpen();
    positive(priceSats);
    if (
      typeof inventoryId !== "string" ||
      !inventoryId.length ||
      inventoryId.length > 128
    )
      throw Error("Inventory id required");
    if (this.all().some((b) => b.inventoryId === inventoryId))
      throw Error("Duplicate inventory");
    const index = this.boxes.size;
    if (index >= 0x80000000) throw Error("HD index exhausted");
    const payAddress = this.hd
      .deriveChild(index)
      .publicKey.toAddress(bsv.Networks.testnet)
      .toString();
    return this.append({
      id: "box-" + (index + 1),
      state: "LISTED",
      payAddress,
      buyerPubkey: null,
      priceSats,
      inventoryId,
      index,
      expiresAt: null,
      refundRequired: false,
      transfer: null,
    });
  }
  reserve(id, buyerPubkey, expiresAt) {
    const b = this.get(id);
    if (b.state !== "LISTED" || b.buyerPubkey || b.refundRequired)
      throw Error("Box already reserved");
    publicKey(buyerPubkey);
    positive(expiresAt);
    return this.append({ ...b, buyerPubkey, expiresAt });
  }
  expire(now = Date.now()) {
    positive(now);
    for (const b of this.all())
      if (b.state === "LISTED" && b.expiresAt !== null && now >= b.expiresAt)
        this.append({
          ...b,
          state: "EXPIRED",
          refundRequired: b.refundRequired || Boolean(b.payment?.satoshis),
        });
  }
  payment(id, p, now = Date.now()) {
    positive(now);
    if (
      !Number.isSafeInteger(p.satoshis) ||
      p.satoshis < 0 ||
      !Number.isSafeInteger(p.confirmations) ||
      p.confirmations < 0 ||
      !Array.isArray(p.refs)
    )
      throw Error("Invalid payment");
    this.expire(now);
    const b = this.get(id);
    if (b.state === "EXPIRED" || !b.buyerPubkey) {
      if (p.satoshis > 0)
        return this.append({ ...b, refundRequired: true, payment: p });
      return b;
    }
    if (b.state !== "LISTED") return b;
    if (p.satoshis >= b.priceSats && p.confirmations >= 1)
      return this.append({ ...b, state: "PAID_PENDING", payment: p });
    return this.append({ ...b, payment: p });
  }
  // Trusted worker interface; HTTP never accepts state patches.
  update(id, patch) {
    return this.append({ ...this.get(id), ...copy(patch) });
  }
  close() {
    if (this.closed) return;
    this.closed = true;
    if (this.fd !== undefined) fs.closeSync(this.fd);
    if (this.lock !== undefined) {
      fs.closeSync(this.lock);
      fs.unlinkSync(this.file + ".lock");
    }
  }
}
module.exports = { SaleStore };
