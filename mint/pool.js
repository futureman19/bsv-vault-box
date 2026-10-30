"use strict";
const fs = require("node:fs"),
  path = require("node:path");
const { S, bsv, pay, output } = require("../vault/src/ordinal-pair");
const { loadKey } = require("./keys");
const Canary = require("./canary");
const MAX_SATS = 2100000000000000;
function sats(n) {
  if (!Number.isSafeInteger(n) || n < 1 || n > MAX_SATS)
    throw Error("Invalid sat amount");
  return n;
}
function fee(n) {
  sats(n);
  if (n > Canary.CAPS.fee) throw Error("Fee exceeds 10000 sat cap");
  return n;
}
function parsePrep(raw, pubkey) {
  if (!Buffer.isBuffer(raw)) throw Error("Raw Buffer required");
  const n = raw[41],
    prefix = 47 + n;
  if (
    raw.length < 85 ||
    raw[4] !== 1 ||
    n > 108 ||
    raw.length !== 85 + n ||
    raw[46 + n] !== 1 ||
    raw[prefix + 8] !== 25
  )
    throw Error("Noncanonical funding grammar");
  const script = pay(pubkey).toBuffer();
  if (!raw.subarray(prefix + 9, prefix + 34).equals(script))
    throw Error("Wrong sponsor P2PKH");
  const amount = sats(Number(raw.readBigUInt64LE(prefix)));
  const tx = new bsv.Transaction(raw);
  if (!tx.toBuffer().equals(raw)) throw Error("Noncanonical encoding");
  return {
    amount,
    txid: tx.id,
    prefix: raw.subarray(0, prefix).toString("hex"),
    locktime: raw.subarray(-4).toString("hex"),
  };
}
function buildPrep(parent, index, key, prepFee = 500, options = {}) {
  const policy = Canary.policy(options);
  fee(prepFee);
  if (key.network !== bsv.Networks[policy.network] || !key.compressed)
    throw Error("Compressed " + policy.chain + " key required");
  const source = parent.outputs[index],
    script = pay(key.publicKey.toString());
  if (!source || !source.script.toBuffer().equals(script.toBuffer()))
    throw Error("Source must be sponsor P2PKH");
  sats(source.satoshis);
  Canary.cap(policy, "prep", source.satoshis);
  const amount = sats(source.satoshis - prepFee);
  const tx = new bsv.Transaction()
    .addInput(
      new bsv.Transaction.Input({
        prevTxId: parent.id,
        outputIndex: index,
        script: "",
        output: source,
      })
    )
    .addOutput(output(script, amount));
  tx.inputs[0].setScript(
    bsv.Script.fromASM(
      S.signTx(tx, key, source.script, source.satoshis, 0) + " " + key.publicKey
    )
  );
  parsePrep(tx.toBuffer(), key.publicKey.toString());
  return tx;
}
// Single writer with durable write-ahead reservations. A failed/ambiguous broadcast
// remains held and counts against the cap until operator reconciliation.
class SponsorPool {
  #key;
  constructor({
    keyPath,
    ledgerPath,
    rpc,
    depth = 5,
    capSats,
    chain,
    canary,
    authorization,
    prepFee = 500,
  }) {
    Canary.bind(this, { chain, canary, authorization });
    if (capSats === undefined)
      capSats = this.policy.canary ? Canary.CAPS.pool : 1000000;
    Canary.cap(this.policy, "pool", capSats);
    this.#key = loadKey(keyPath, this.policy);
    if (!path.isAbsolute(ledgerPath) || typeof rpc !== "function")
      throw Error("Absolute ledger path and RPC required");
    if (!Number.isSafeInteger(depth) || depth < 1) throw Error("Invalid depth");
    this.depth = depth;
    this.capSats = sats(capSats);
    this.prepFee = fee(prepFee);
    this.rpc = rpc;
    this.ledgerPath = ledgerPath;
    this.pubkey = this.#key.publicKey.toString();
    this.entries = [];
    this.busy = false;
    this.closed = false;
    this.lock = ledgerPath + ".lock";
    try {
      this.lockFd = fs.openSync(this.lock, "wx", 0o600);
    } catch {
      throw Error("Pool locked; reconcile stale lock manually");
    }
    try {
      const text = fs.existsSync(ledgerPath)
        ? fs.readFileSync(ledgerPath, "utf8")
        : "";
      if (text && !text.endsWith("\n"))
        throw Error("Truncated ledger; reconcile manually");
      for (const line of text.split("\n").filter(Boolean))
        this.apply(JSON.parse(line));
      this.checkCaps();
      this.fd = fs.openSync(
        ledgerPath,
        fs.constants.O_WRONLY |
          fs.constants.O_CREAT |
          fs.constants.O_APPEND |
          fs.constants.O_NOFOLLOW,
        0o600
      );
    } catch (e) {
      this.close();
      throw e;
    }
  }
  checkCaps() {
    Canary.cap(this.policy, "pool", this.capSats);
    fee(this.prepFee);
    if (this.policy.canary) {
      for (const e of this.entries) {
        Canary.cap(this.policy, "prep", e.inputSats);
        Canary.cap(this.policy, "prep", e.amount);
        fee(e.prepFee);
      }
      Canary.cap(this.policy, "pool", this.totals().heldSats);
    }
  }
  apply(row) {
    if (row.type === "prepared") {
      const parsed = parsePrep(Buffer.from(row.raw, "hex"), this.pubkey),
        tx = new bsv.Transaction(row.raw);
      const source =
        tx.inputs[0].prevTxId.toString("hex") + ":" + tx.inputs[0].outputIndex;
      if (
        row.txid !== parsed.txid ||
        row.source !== source ||
        row.amount !== parsed.amount ||
        sats(row.inputSats) !== row.amount + fee(row.prepFee) ||
        this.entries.some((e) => e.source === source)
      )
        throw Error("Invalid prepared ledger entry");
      this.entries.push({ ...row, dispensed: false });
    } else if (row.type === "dispensed") {
      const entry = this.entries.find((e) => e.txid === row.txid);
      if (!entry || entry.dispensed)
        throw Error("Invalid dispense ledger entry");
      entry.dispensed = true;
    } else throw Error("Unknown ledger event");
  }
  append(row) {
    if (this.closed) throw Error("Pool closed");
    try {
      const bytes = Buffer.from(JSON.stringify(row) + "\n");
      let offset = 0;
      while (offset < bytes.length) {
        const written = fs.writeSync(
          this.fd,
          bytes,
          offset,
          bytes.length - offset
        );
        if (written <= 0) throw Error("Ledger write made no progress");
        offset += written;
      }
      fs.fsyncSync(this.fd);
      this.apply(row);
    } catch (e) {
      // This synchronous failure aborts the operation before any further RPC.
      // Unlike public close(), it must poison the writer even while busy.
      this.#close();
      throw e;
    }
  }
  async exclusive(fn) {
    if (this.closed) throw Error("Pool closed");
    if (this.busy) throw Error("Pool busy");
    this.checkCaps();
    this.busy = true;
    try {
      Canary.chain(this.policy, (await this.rpc("getblockchaininfo")).chain);
      this.checkCaps();
      return await fn();
    } finally {
      this.busy = false;
    }
  }
  async prepare(parent, index) {
    return this.exclusive(async () => {
      Canary.cap(this.policy, "prep", parent.outputs[index]?.satoshis);
      Canary.broadcast(this.policy);
      const source = parent.id + ":" + index;
      if (this.entries.some((e) => e.source === source))
        throw Error("duplicate source");
      const actual = await this.rpc("gettxout", [parent.id, index, true]),
        claimed = parent.outputs[index];
      if (
        !actual ||
        !claimed ||
        Math.round(actual.value * 1e8) !== claimed.satoshis ||
        actual.scriptPubKey.hex !== claimed.script.toHex()
      )
        throw Error("Source UTXO absent or mismatched");
      this.checkCaps();
      const tx = buildPrep(parent, index, this.#key, this.prepFee, this.policy);
      if (
        this.totals().heldSats + parent.outputs[index].satoshis >
        this.capSats
      )
        throw Error("Pool cap exceeded");
      this.append({
        type: "prepared",
        txid: tx.id,
        source,
        inputSats: parent.outputs[index].satoshis,
        amount: tx.outputs[0].satoshis,
        prepFee: this.prepFee,
        raw: tx.uncheckedSerialize(),
      });
      if (
        (await this.rpc("sendrawtransaction", [tx.uncheckedSerialize()])) !==
        tx.id
      )
        throw Error("Broadcast txid mismatch");
      return tx;
    });
  }
  async refreshUnlocked() {
    this.checkCaps();
    const states = [];
    for (const e of this.entries.filter((e) => !e.dispensed)) {
      const utxo = await this.rpc("gettxout", [e.txid, 0, true]);
      const valid =
        utxo &&
        Math.round(utxo.value * 1e8) === e.amount &&
        utxo.scriptPubKey.hex === pay(this.pubkey).toHex();
      states.push({
        txid: e.txid,
        confirmations: valid ? utxo.confirmations : 0,
        ready: !!valid && utxo.confirmations >= this.depth,
      });
    }
    return states;
  }
  refresh() {
    return this.exclusive(() => this.refreshUnlocked());
  }
  dispense() {
    return this.exclusive(async () => {
      const first = (await this.refreshUnlocked()).find((s) => s.ready);
      if (!first) return null;
      this.checkCaps();
      const e = this.entries.find((e) => e.txid === first.txid);
      this.append({ type: "dispensed", txid: e.txid });
      return new bsv.Transaction(e.raw);
    });
  }
  totals() {
    const r = {
      inputSats: 0,
      prepFeeSats: 0,
      preparedSats: 0,
      dispensedSats: 0,
      heldSats: 0,
    };
    for (const e of this.entries) {
      r.inputSats += e.inputSats;
      r.prepFeeSats += e.prepFee;
      r.preparedSats += e.amount;
      r[e.dispensed ? "dispensedSats" : "heldSats"] += e.amount;
    }
    for (const n of Object.values(r))
      if (!Number.isSafeInteger(n)) throw Error("Ledger sum overflow");
    return r;
  }
  close() {
    if (this.busy)
      throw Error("Pool busy; await active operation before close");
    this.#close();
  }
  #close() {
    if (this.closed) return;
    this.closed = true;
    if (this.fd !== undefined) fs.closeSync(this.fd);
    if (this.lockFd !== undefined) {
      fs.closeSync(this.lockFd);
      fs.unlinkSync(this.lock);
    }
  }
}
module.exports = { SponsorPool, buildPrep, parsePrep };
