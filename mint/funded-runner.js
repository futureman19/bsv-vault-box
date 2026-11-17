"use strict";
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict"),
  crypto = require("node:crypto");
const M = require("../vault/src/ordinal-pair");
const { bsv, S, C, pay, output, outpoint, transition } = M;
const Canary = require("./canary");
const { loadKey } = require("./keys");
const { SponsorPool } = require("./pool");
const { SaleStore } = require("./sale");
const { createService } = require("./service");
const { TransferWorker } = require("./transfer");
const {
  preflight,
  configuration,
  fundingRows,
} = require("./scripts/canary-preflight");
const { createMainnetAdapter } = require("./broadcast");
const delay = (ms) => new Promise((r) => setTimeout(r, ms));
const PLAN = Object.freeze({
  inventory: [60000, 60000],
  sponsor: [50000, 50000, 50000],
  payment: [10000],
});
function validateReport(
  r,
  { chain, addresses, buyerPubkey, now = Date.now() }
) {
  assert.equal(r.status, "READ_ONLY_PREFLIGHT_PASS");
  assert.equal(r.stage, "startup");
  assert.equal(r.policy.chain, chain);
  assert.ok(
    Number.isSafeInteger(r.createdAt) &&
      now >= r.createdAt &&
      now - r.createdAt <= 300000,
    "Preflight older than five minutes or future dated"
  );
  assert.equal(r.composition.buyerPubkey, buyerPubkey);
  for (const role of Object.keys(PLAN)) {
    const f = r.funding[role];
    assert.equal(f.address, addresses[role]);
    assert.deepEqual(f.expectedSatoshis, PLAN[role]);
    assert.equal(
      f.status,
      role === "payment" ? "UNFUNDED" : "EXACT_CONFIRMED_UNSPENT",
      role + " funding gate"
    );
    assert.equal(
      f.outpoints.length,
      role === "payment" ? 0 : PLAN[role].length
    );
    assert.equal(new Set(f.outpoints).size, f.outpoints.length);
  }
}
function spend(parent, index, outs, key) {
  const source = parent.outputs[index];
  assert.ok(source);
  const tx = new bsv.Transaction().addInput(
    new bsv.Transaction.Input({
      prevTxId: parent.id,
      outputIndex: index,
      script: "",
      output: source,
    })
  );
  for (const o of outs) tx.addOutput(o);
  tx.inputs[0].setScript(
    bsv.Script.fromASM(
      S.signTx(tx, key, source.script, source.satoshis, 0) + " " + key.publicKey
    )
  );
  assert.ok(M.verify(tx, [parent]).success);
  return tx;
}
function durable(file, value) {
  const fd = fs.openSync(file, "wx", 0o600);
  try {
    const bytes = Buffer.from(
      typeof value === "string" ? value : JSON.stringify(value, null, 2) + "\n"
    );
    let offset = 0;
    while (offset < bytes.length) {
      const n = fs.writeSync(fd, bytes, offset, bytes.length - offset);
      assert.ok(n > 0);
      offset += n;
    }
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
}
async function runCanary({
  config,
  report,
  evidence,
  chain = "mainnet",
  ownerAuthorized = false,
  rehearsal = false,
  local,
  print = console.log,
}) {
  // First operation: no key loading, chain reads or file creation without gate.
  const authorization = await Canary.authorizeRunner({
    chain,
    ownerAuthorized,
    rehearsal,
    binding: crypto
      .createHash("sha256")
      .update(JSON.stringify({ config, report, evidence }))
      .digest("hex"),
  });
  const options = { chain, canary: chain === "mainnet", authorization },
    policy = Canary.policy(options);
  assert.deepEqual(
    Canary.CAPS,
    {
      pool: 250000,
      prep: 100000,
      fee: 10000,
      price: 10000,
      paymentMultiple: 2,
      inventory: 2,
    },
    "Frozen caps changed"
  );
  assert.ok(!local || chain === "regtest", "Local hooks forbidden on mainnet");
  assert.ok(
    path.isAbsolute(evidence) && !fs.existsSync(evidence),
    "New absolute evidence directory required"
  );
  const { addresses } = configuration(config, chain);
  validateReport(report, { chain, addresses, buyerPubkey: config.buyerPubkey });
  const requests = [];
  const adapter =
    local ||
    createMainnetAdapter({
      authorization,
      requests,
      fetchImpl: async (url, opts) => {
        await delay(1500);
        return fetch(url, opts);
      },
    });
  const rpc = async (method, args = []) => {
    if (method === "sendrawtransaction") Canary.broadcast(policy);
    return adapter.rpc(method, args);
  };
  Canary.chain(policy, (await rpc("getblockchaininfo")).chain);
  if (chain === "regtest") assert.equal(await rpc("getconnectioncount"), 0);
  const checks = {
    chain,
    localTransport: chain === "regtest" ? adapter.transport : undefined,
    fetchImpl: async (url, opts) => {
      await delay(1500);
      return fetch(url, opts);
    },
  };
  // Never trust a stale or edited local PASS: independently rerun the exact stage.
  const fresh = await preflight(config, { ...checks, stage: "startup" });
  validateReport(fresh, { chain, addresses, buyerPubkey: config.buyerPubkey });
  assert.deepEqual(
    fresh.funding,
    report.funding,
    "Funding changed since preflight"
  );
  fs.mkdirSync(evidence, { mode: 0o700 });
  const log = (name, v) => durable(path.join(evidence, name), v);
  log("startup.json", fresh);
  log("composition.json", {
    chain,
    caps: Canary.CAPS,
    inventoryFunding: 120000,
    sponsorFunding: 150000,
    prepFee: 500,
    transitionFee: 1000,
    price: 10000,
    buyerPubkey: config.buyerPubkey,
    addresses,
  });
  print(
    JSON.stringify({
      composition: "one box; three preps; no replenishment",
      chain,
      addresses,
      priceSats: 10000,
    })
  );
  const owner = loadKey(config.inventoryKeyPath, policy),
    sponsor = loadKey(config.sponsorKeyPath, policy);
  let pool, store, api;
  const parents = [],
    history = [],
    outcomes = [];
  const wait = async () => {
    if (chain === "regtest") await adapter.tick();
    else await delay(15000);
  };
  async function included(name, tx, depth = 1) {
    for (let n = 0; n < 240; n++) {
      let d;
      try {
        d = await rpc("getrawtransaction", [tx.id, true]);
      } catch (e) {
        if (e.code !== -5) throw e;
      }
      if (d) {
        assert.equal(d.hex, tx.uncheckedSerialize(), "Inclusion bytes differ");
        if (d.confirmations >= depth && d.blockhash) {
          const block = await rpc("getblock", [d.blockhash]);
          assert.ok(block.confirmations >= depth && block.tx.includes(tx.id));
          const result = {
            name,
            txid: tx.id,
            bytes: tx.toBuffer().length,
            confirmations: d.confirmations,
            blockhash: d.blockhash,
          };
          outcomes.push(result);
          log(name + "-included.json", result);
          return tx;
        }
      }
      await wait();
    }
    throw Error("Inclusion deadline; reconcile without retry");
  }
  async function admit(name, tx) {
    const inputs = [];
    for (const i of tx.inputs) {
      const u = await rpc("gettxout", [
        i.prevTxId.toString("hex"),
        i.outputIndex,
      ]);
      assert.ok(u && u.confirmations >= 1, "Spend input missing");
      assert.equal(u.scriptPubKey.hex, i.output.script.toHex());
      assert.equal(Math.round(u.value * 1e8), i.output.satoshis);
      inputs.push(i.output.satoshis);
    }
    const fee =
      inputs.reduce((a, b) => a + b, 0) -
      tx.outputs.reduce((a, o) => a + o.satoshis, 0);
    assert.ok(Number.isSafeInteger(fee) && fee > 0 && fee <= Canary.CAPS.fee);
    log(name + ".hex", tx.uncheckedSerialize() + "\n");
    log(name + "-intent.json", {
      txid: tx.id,
      inputs,
      outputs: tx.outputs.map((o) => o.satoshis),
      fee,
      attempts: 1,
    });
    assert.equal(
      await rpc("sendrawtransaction", [tx.uncheckedSerialize()]),
      tx.id
    );
    return included(name, tx);
  }
  async function source(ref) {
    const [id, n] = ref.split(":");
    return {
      tx: new bsv.Transaction(await rpc("getrawtransaction", [id])),
      index: Number(n),
    };
  }
  try {
    pool = new SponsorPool({
      ...options,
      rpc,
      keyPath: config.sponsorKeyPath,
      ledgerPath: path.join(evidence, "pool.jsonl"),
      capSats: 150000,
      prepFee: 500,
      depth: 5,
    });
    for (const [i, ref] of fresh.funding.sponsor.outpoints.entries()) {
      const p = await source(ref),
        tx = await pool.prepare(p.tx, p.index);
      parents.push(tx);
      log("prep-" + i + ".hex", tx.uncheckedSerialize() + "\n");
      await included("prep-" + i, tx, 5);
    }
    const a = await source(fresh.funding.inventory.outpoints[0]);
    const inscription =
      pay(owner.publicKey.toString()).toHex() +
      "0063036f7264510a746578742f706c61696e000b426f7853562d746573746168";
    const foreign = await admit(
      "inscription",
      spend(
        a.tx,
        a.index,
        [
          output(bsv.Script.fromHex(inscription)),
          output(pay(owner.publicKey.toString()), 59499),
        ],
        owner
      )
    );
    const c = new C(outpoint(foreign, 0), 0n, owner.publicKey.toString());
    c.phase = 0n;
    c.owner = owner.publicKey.toString();
    const b = await source(fresh.funding.inventory.outpoints[1]);
    const box = await admit(
      "empty-box",
      spend(
        b.tx,
        b.index,
        [
          output(c.lockingScript),
          output(pay(owner.publicKey.toString()), 59499),
        ],
        owner
      )
    );
    const f = { foreign, box, origin: foreign.id + "_0" };
    async function move(name, prior, action) {
      const funding = await pool.dispense();
      assert.ok(funding, "No prepared funding");
      const r = transition(
        f,
        prior,
        action,
        owner,
        config.buyerPubkey,
        null,
        undefined,
        {
          sponsor,
          funding: funding.outputs[0].satoshis,
          fee: 1000,
          fundingTx: funding,
        }
      );
      assert.ok(r.result.success);
      await admit(name, r.tx);
      history.push(r.tx);
      return r.tx;
    }
    const deposit = await move("deposit", null, 0),
      seal = await move("seal", deposit, 1);
    assert.ok(M.verifyHistory(f, history, parents).valid);
    const manifest = {
      origin: f.origin,
      foreign: foreign.uncheckedSerialize(),
      box: box.uncheckedSerialize(),
      history: history.map((t) => t.uncheckedSerialize()),
      fundingParents: parents.map((t) => t.uncheckedSerialize()),
      buyerPubkey: config.buyerPubkey,
    };
    log("sealed-manifest.json", manifest);
    log("seal-commit.json", {
      sealTxid: seal.id,
      sha256: crypto
        .createHash("sha256")
        .update(JSON.stringify(manifest))
        .digest("hex"),
      meaning:
        "Local evidence commitment; not an extra on-chain root transaction",
    });
    store = new SaleStore({
      ...options,
      file: path.join(evidence, "sales.jsonl"),
      xpub: config.paymentXpub,
    });
    const listed = store.list({ inventoryId: seal.id, priceSats: 10000 });
    const reservation = store.reserve(
      listed.id,
      config.buyerPubkey,
      Date.now() + 3600000
    );
    assert.equal(reservation.payAddress, addresses.payment);
    api = createService({ ...options, store, inventory: [] });
    await api.listen(chain === "mainnet" ? 8090 : 0);
    log("reservation.json", reservation);
    print(
      JSON.stringify({
        PAY_ONLY_NOW: reservation.payAddress,
        satoshis: 10000,
        reservation: reservation.id,
      })
    );
    if (chain === "regtest" && adapter.onReservation)
      await adapter.onReservation(reservation);
    async function exactPayment() {
      const rows = await fundingRows(
        adapter.transport,
        addresses.payment,
        chain === "mainnet"
      );
      assert.ok(Array.isArray(rows));
      if (!rows.length) return null;
      assert.equal(
        rows.length,
        1,
        "Payment shape mismatch; halt and reconcile"
      );
      assert.equal(
        rows[0].value,
        10000,
        "Payment amount mismatch; halt and reconcile"
      );
      if (rows[0].height === 0) return null;
      const report = await preflight(config, { ...checks, stage: "payment" });
      const f = report.funding.payment;
      return { report, satoshis: 10000, confirmations: 1, refs: f.outpoints };
    }
    let payment;
    for (let n = 0; n < 240; n++) {
      store.expire();
      assert.equal(
        store.get(listed.id).state,
        "LISTED",
        "Reservation expired; reconcile"
      );
      payment = await exactPayment();
      if (payment) break;
      await wait();
    }
    assert.ok(payment, "Payment deadline; reconcile");
    log("payment.json", payment.report);
    store.payment(listed.id, payment);
    const paymentTransport = {
      policy,
      read: async (address) => {
        assert.equal(address, addresses.payment);
        const p = await exactPayment();
        assert.ok(p, "Payment no longer exact confirmed unspent");
        return p;
      },
    };
    const worker = new TransferWorker({
      ...options,
      store,
      rpc,
      pool,
      inventory: () => ({ f, source: seal }),
      inventoryKeyPath: config.inventoryKeyPath,
      sponsorKeyPath: config.sponsorKeyPath,
      paymentTransport,
      fee: 1000,
      maxAttempts: 1,
    });
    await worker.run(listed.id);
    let sold = store.get(listed.id);
    assert.equal(
      sold.transfer?.stage,
      "SUBMITTED",
      "Uncertain transfer; halt and reconcile"
    );
    const transfer = new bsv.Transaction(sold.transfer.raw);
    log("transfer.hex", sold.transfer.raw + "\n");
    const funding = new bsv.Transaction(sold.transfer.fundingRaw),
      inputSats =
        seal.outputs[0].satoshis +
        seal.outputs[1].satoshis +
        funding.outputs[0].satoshis;
    const outputSats = transfer.outputs.reduce((n, o) => n + o.satoshis, 0);
    assert.equal(inputSats - outputSats, 1000);
    log("transfer-accounting.json", {
      inputSats,
      outputSats,
      fee: inputSats - outputSats,
      outputs: transfer.outputs.map((o) => o.satoshis),
    });
    await included("transfer", transfer);
    await worker.run(listed.id);
    sold = store.get(listed.id);
    assert.equal(sold.state, "TRANSFERRED");
    history.push(transfer);
    assert.equal(transfer.inputs.length, 3);
    assert.ok(M.verifyHistory(f, history, parents).valid);
    const bundle = {
      ...manifest,
      history: history.map((t) => t.uncheckedSerialize()),
      transfer: transfer.uncheckedSerialize(),
      chain,
      buyerFeeSources: [1500, 1500],
      buyerPrepFee: 500,
      buyerTransitionFee: 1000,
    };
    log("buyer-bundle.json", bundle);
    print(
      "TRANSFER CONFIRMED. Service stops here. Copy buyer-bundle.json to offline owner wallet; build open/withdraw with mint/scripts/canary-buyer.js and two separate 1500-sat buyer fee UTXOs. Buyer key NEVER enters this runner."
    );
    log("result.json", {
      status: "TRANSFER_CONFIRMED",
      outcomes,
      pool: pool.totals(),
      buyerKeyCustody: false,
      historyValid: true,
    });
    return bundle;
  } catch (e) {
    log("halt.json", {
      status: "HALT_RECONCILE",
      message:
        "Preserve all intents/journals. No automatic resume, replacement or refund.",
    });
    throw e;
  } finally {
    if (api) await api.close();
    store?.close();
    pool?.close();
    log("http-requests.json", requests);
    log("runner-shutdown.json", {
      serviceClosed: true,
      storeClosed: !store || store.closed,
      poolClosed: !pool || pool.closed,
    });
  }
}
module.exports = { runCanary, validateReport, spend, durable };
