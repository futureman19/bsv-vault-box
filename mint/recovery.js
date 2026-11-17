"use strict";
// No store/pool construction, key access or RPC: captured evidence only.
const M = require("../vault/src/ordinal-pair");
const { parsePrep } = require("./pool");
function journal(text) {
  if (typeof text !== "string" || (text && !text.endsWith("\n")))
    throw Error("Truncated journal");
  return text
    ? text
        .slice(0, -1)
        .split("\n")
        .map((line) => JSON.parse(line))
    : [];
}
function transaction(raw) {
  if (typeof raw !== "string" || !/^(?:[0-9a-f]{2})+$/.test(raw))
    throw Error("Invalid transaction encoding");
  const tx = new M.bsv.Transaction(raw);
  if (tx.uncheckedSerialize() !== raw) throw Error("Noncanonical transaction");
  return tx;
}
function classify({
  id,
  saleText,
  poolText,
  sponsorPubkey,
  observations = [],
  depth = 1,
} = {}) {
  const base = {
    quarantined: true,
    mayResume: false,
    txid: null,
    fundingOutpoint: null,
  };
  try {
    if (
      !Number.isSafeInteger(depth) ||
      depth < 1 ||
      typeof id !== "string" ||
      !Array.isArray(observations)
    )
      throw Error("Invalid input");
    const pool = new Map(),
      sources = new Set();
    for (const row of journal(poolText)) {
      if (row.type === "prepared") {
        const tx = transaction(row.raw),
          parsed = parsePrep(tx.toBuffer(), sponsorPubkey);
        const source =
          tx.inputs[0].prevTxId.toString("hex") +
          ":" +
          tx.inputs[0].outputIndex;
        if (
          pool.has(tx.id) ||
          sources.has(source) ||
          row.txid !== tx.id ||
          row.source !== source ||
          row.amount !== parsed.amount ||
          !Number.isSafeInteger(row.inputSats) ||
          !Number.isSafeInteger(row.prepFee) ||
          row.prepFee < 1 ||
          row.prepFee > 10000 ||
          row.inputSats !== row.amount + row.prepFee
        )
          throw Error("Invalid pool mapping");
        sources.add(source);
        pool.set(tx.id, { raw: row.raw, dispensed: false });
      } else if (row.type === "dispensed") {
        const entry = pool.get(row.txid);
        if (!entry || entry.dispensed) throw Error("Invalid dispense");
        entry.dispensed = true;
      } else throw Error("Invalid pool event");
    }
    const sales = new Map();
    let xpub;
    for (const row of journal(saleText)) {
      if (
        !row.box ||
        typeof row.box.id !== "string" ||
        typeof row.xpub !== "string" ||
        (xpub && row.xpub !== xpub)
      )
        throw Error("Invalid sale journal");
      xpub = row.xpub;
      const b = row.box,
        prior = sales.get(b.id);
      if (
        prior &&
        (prior.inventoryId !== b.inventoryId ||
          (prior.buyerPubkey && prior.buyerPubkey !== b.buyerPubkey) ||
          (prior.transfer?.raw && prior.transfer.raw !== b.transfer?.raw))
      )
        throw Error("Changed durable intent");
      // Snapshots may advance retries, but must never erase custody history or
      // operator holds. Reject contradictions rather than guessing a safe merge.
      if (
        (b.reconciliationReasons !== undefined &&
          (!Array.isArray(b.reconciliationReasons) ||
            b.reconciliationReasons.some((r) => typeof r !== "string"))) ||
        (prior &&
          ((prior.transfer?.stage === "INCLUDED" &&
            b.transfer?.stage !== "INCLUDED") ||
            (prior.state === "TRANSFERRED" &&
              !["TRANSFERRED", "OPENED"].includes(b.state)) ||
            (prior.state === "OPENED" && b.state !== "OPENED") ||
            (prior.openTxid && prior.openTxid !== b.openTxid) ||
            (prior.reconciliationRequired && !b.reconciliationRequired) ||
            (prior.reconciliationReasons || []).some(
              (r) => !(b.reconciliationReasons || []).includes(r)
            )))
      )
        throw Error("Regressed durable history");
      sales.set(b.id, b);
    }
    const claims = new Map();
    for (const sale of sales.values()) {
      if (!sale.transfer?.raw) continue;
      const tx = transaction(sale.transfer.raw);
      const refs = [
        "tx:" + tx.id,
        ...tx.inputs.map(
          (i) => "outpoint:" + i.prevTxId.toString("hex") + ":" + i.outputIndex
        ),
      ];
      for (const ref of refs) {
        if (claims.has(ref) && claims.get(ref) !== sale.id)
          throw Error("Ambiguous cross-sale assignment");
        claims.set(ref, sale.id);
      }
    }
    const b = sales.get(id);
    if (!b) throw Error("Sale absent");
    const tr = b.transfer;
    if (!tr)
      return {
        ...base,
        classification: "NO_TRANSFER_INTENT",
        persistedStage: null,
      };
    if (tr.stage === "RESERVING") {
      if (tr.raw || tr.txid) throw Error("Invalid reservation");
      return {
        ...base,
        classification: "RESERVING",
        persistedStage: "RESERVING",
        reason:
          "Funding assignment unresolved even if exactly one pool dispense exists",
      };
    }
    if (!["BUILT", "SUBMITTED", "INCLUDED", "UNCERTAIN"].includes(tr.stage))
      throw Error("Invalid transfer stage");
    const tx = transaction(tr.raw),
      source = transaction(tr.sourceRaw),
      funding = transaction(tr.fundingRaw);
    if (
      tr.txid !== tx.id ||
      tx.inputs.length !== 3 ||
      tx.inputs[0].prevTxId.toString("hex") !== source.id ||
      tx.inputs[0].outputIndex !== 0 ||
      tx.inputs[1].prevTxId.toString("hex") !== source.id ||
      tx.inputs[1].outputIndex !== 1 ||
      tx.inputs[2].prevTxId.toString("hex") !== funding.id ||
      tx.inputs[2].outputIndex !== 0
    )
      throw Error("Transfer outpoint mismatch");
    const entry = pool.get(funding.id);
    if (!entry?.dispensed || entry.raw !== tr.fundingRaw)
      throw Error("Funding not durably assigned");
    const from = M.C.fromHex(source.outputs[0].script.toHex()),
      to = M.C.fromHex(tx.outputs[0].script.toHex());
    if (
      from.phase !== 2n ||
      to.phase !== 2n ||
      to.owner !== b.buyerPubkey ||
      !M.verify(tx, [source, funding]).success
    )
      throw Error("Invalid serialized transfer");
    const matches = observations.filter((o) => o.txid === tx.id);
    if (matches.length > 1) throw Error("Ambiguous observations");
    let included = false,
      observed = "NOT_CAPTURED";
    if (matches.length) {
      const o = matches[0];
      if (
        o.raw !== tr.raw ||
        !Number.isSafeInteger(o.confirmations) ||
        o.confirmations < 0
      )
        throw Error("Invalid captured transaction");
      observed = "BELOW_DEPTH";
      if (o.confirmations >= depth) {
        if (
          !/^[0-9a-f]{64}$/.test(o.blockhash) ||
          o.block?.hash !== o.blockhash ||
          !Number.isSafeInteger(o.block.confirmations) ||
          o.block.confirmations < depth ||
          !Array.isArray(o.block.tx) ||
          !o.block.tx.includes(tx.id)
        )
          throw Error("Invalid captured block membership");
        included = true;
        observed = "INCLUDED";
      }
    }
    const lost = tr.stage === "INCLUDED" && observed === "BELOW_DEPTH";
    return {
      ...base,
      classification: lost
        ? "FINALITY_LOST"
        : included
        ? "INCLUDED"
        : tr.stage === "UNCERTAIN"
        ? "UNCERTAIN_SEND"
        : tr.stage,
      persistedStage: tr.stage,
      txid: tx.id,
      fundingOutpoint: funding.id + ":0",
      capturedObservation: observed,
      reconciliationRequired: lost || !!b.reconciliationRequired,
      reconciliationReasons: [...(b.reconciliationReasons || [])],
    };
  } catch {
    return {
      ...base,
      classification: "INCONSISTENT",
      reason:
        "Invalid, truncated, contradictory or unmapped evidence; manual reconciliation required",
    };
  }
}
module.exports = { classify };
