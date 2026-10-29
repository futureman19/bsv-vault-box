"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const { bsv, S, pay, output, verify } = require("../../vault/src/ordinal-pair");
const P = require("../pool"),
  { loadKey } = require("../keys");
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), "mint-test-"));
const key = new bsv.PrivateKey(new bsv.crypto.BN(1), bsv.Networks.testnet);
function root(n = 1) {
  return new bsv.Transaction()
    .addInput(
      new bsv.Transaction.Input({
        prevTxId: n.toString(16).padStart(64, "0"),
        outputIndex: 0,
        script: "",
        output: output(bsv.Script.empty()),
      })
    )
    .addOutput(output(pay(key.publicKey.toString()), 100000));
}
function setup(t) {
  const dir = tmp();
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const keyPath = path.join(dir, "key");
  fs.writeFileSync(keyPath, key.toWIF(), { mode: 0o600 });
  return { dir, keyPath };
}
test("builds byte-exact bounded parents and valid signatures", () => {
  for (let n = 1; n <= 30; n++) {
    const r = root(n),
      tx = P.buildPrep(r, 0, key, 500),
      raw = tx.toBuffer();
    const parsed = P.parsePrep(raw, key.publicKey.toString());
    assert.equal(parsed.amount, 99500);
    assert.equal(raw[4], 1);
    assert.ok(raw[41] <= 108);
    assert.equal(raw[46 + raw[41]], 1);
    assert.equal(raw.length, 85 + raw[41]);
    assert.equal(new bsv.Transaction(raw).outputs.length, 1);
    assert.equal(verify(tx, [r]).success, true);
  }
});
test("rejects invalid fees, wrong source and malformed grammar", () => {
  for (const fee of [0, -1, 10001, 1.5, NaN])
    assert.throws(() => P.buildPrep(root(), 0, key, fee));
  for (const fee of [1, 500, 10000])
    assert.equal(
      P.parsePrep(
        P.buildPrep(root(), 0, key, fee).toBuffer(),
        key.publicKey.toString()
      ).amount,
      100000 - fee
    );
  const raw = P.buildPrep(root(), 0, key, 500).toBuffer();
  for (const offset of [4, 41, 46 + raw[41], 55 + raw[41]]) {
    const b = Buffer.from(raw);
    b[offset] = 253;
    assert.throws(() => P.parsePrep(b, key.publicKey.toString()));
  }
  assert.throws(() =>
    P.parsePrep(
      Buffer.concat([raw, Buffer.from([0])]),
      key.publicKey.toString()
    )
  );
  assert.throws(() =>
    P.parsePrep(raw, key.publicKey.toString().replace(/^02/, "03"))
  );
  const bad = root();
  bad.outputs[0].setScript(bsv.Script.empty());
  assert.throws(() => P.buildPrep(bad, 0, key, 500));
});
test("key custody rejects mainnet WIF and insecure files without echoing input", (t) => {
  const { keyPath } = setup(t);
  if (process.platform === "win32") {
    assert.throws(() => loadKey(keyPath), /POSIX/);
    return;
  }
  assert.equal(loadKey(keyPath).publicKey.toString(), key.publicKey.toString());
  fs.chmodSync(keyPath, 0o644);
  assert.throws(() => loadKey(keyPath), /0600/);
  fs.chmodSync(keyPath, 0o600);
  fs.writeFileSync(
    keyPath,
    new bsv.PrivateKey(new bsv.crypto.BN(1), bsv.Networks.livenet).toWIF()
  );
  assert.throws(() => loadKey(keyPath), /testnet/);
  fs.writeFileSync(keyPath, "not-a-key");
  assert.throws(() => loadKey(keyPath), /Invalid/);
});
test("pool waits five confirmations, rechecks unspentness, FIFO and durable ledger", async (t) => {
  if (process.platform === "win32")
    return t.skip("POSIX file modes required; exercised under WSL");
  let pool;
  t.after(() => pool?.close());
  const { dir, keyPath } = setup(t),
    known = new Map();
  let depth = 0,
    chain = "regtest",
    spent = false;
  const rpc = async (method, args = []) => {
    if (method === "getblockchaininfo") return { chain };
    if (method === "sendrawtransaction") {
      const tx = new bsv.Transaction(args[0]);
      known.set(tx.id, tx);
      return tx.id;
    }
    if (method === "gettxout") {
      if ([1, 2, 3].some((n) => root(n).id === args[0]))
        return {
          value: 0.001,
          confirmations: 5,
          scriptPubKey: { hex: pay(key.publicKey.toString()).toHex() },
        };
      const tx = known.get(args[0]);
      return tx && !spent
        ? {
            confirmations: depth,
            value: tx.outputs[0].satoshis / 1e8,
            scriptPubKey: { hex: tx.outputs[0].script.toHex() },
          }
        : null;
    }
    throw Error(method);
  };
  const options = {
    keyPath,
    ledgerPath: path.join(dir, "ledger.jsonl"),
    rpc,
    capSats: 200000,
  };
  pool = new P.SponsorPool(options);
  const a = await pool.prepare(root(1), 0),
    b = await pool.prepare(root(2), 0);
  assert.throws(() => new P.SponsorPool(options), /locked/);
  await assert.rejects(pool.prepare(root(1), 0), /duplicate/);
  await assert.rejects(pool.prepare(root(3), 0), /cap/);
  assert.equal(await pool.dispense(), null);
  depth = 4;
  assert.equal(await pool.dispense(), null);
  depth = 5;
  spent = true;
  assert.equal(await pool.dispense(), null);
  spent = false;
  assert.equal((await pool.dispense()).id, a.id);
  pool.close();
  pool = new P.SponsorPool(options);
  assert.equal((await pool.dispense()).id, b.id);
  assert.equal(await pool.dispense(), null);
  assert.deepEqual(pool.totals(), {
    inputSats: 200000,
    prepFeeSats: 1000,
    preparedSats: 199000,
    dispensedSats: 199000,
    heldSats: 0,
  });
  chain = "main";
  await assert.rejects(pool.prepare(root(3), 0), /regtest/);
});
test("broadcast uncertainty stays reserved across restart and corrupt ledgers fail closed", async (t) => {
  if (process.platform === "win32") return t.skip("POSIX file modes required");
  let pool;
  t.after(() => pool?.close());
  const { dir, keyPath } = setup(t);
  const ledgerPath = path.join(dir, "ledger.jsonl");
  let fail = true,
    depth = 5;
  const rpc = async (method, args) => {
    if (method === "getblockchaininfo") return { chain: "regtest" };
    if (method === "sendrawtransaction") {
      if (fail) throw Error("timeout");
      return new bsv.Transaction(args[0]).id;
    }
    if (method === "gettxout")
      return {
        value: [1, 2].some((n) => root(n).id === args[0]) ? 0.001 : 0.000995,
        confirmations: depth,
        scriptPubKey: { hex: pay(key.publicKey.toString()).toHex() },
      };
  };
  const opts = { keyPath, ledgerPath, rpc, capSats: 100000 };
  pool = new P.SponsorPool(opts);
  await assert.rejects(pool.prepare(root(), 0), /timeout/);
  assert.equal(pool.totals().heldSats, 99500);
  pool.close();
  pool = new P.SponsorPool(opts);
  await assert.rejects(pool.prepare(root(), 0), /duplicate/);
  await assert.rejects(pool.prepare(root(2), 0), /cap/);
  assert.equal((await pool.refresh())[0].ready, true);
  depth = 4;
  assert.equal(await pool.dispense(), null);
  depth = 5;
  const results = await Promise.allSettled([pool.dispense(), pool.dispense()]);
  assert.equal(results.filter((r) => r.status === "fulfilled").length, 1);
  assert.equal(results.filter((r) => r.status === "rejected").length, 1);
  pool.close();
  fs.appendFileSync(ledgerPath, "{");
  assert.throws(() => new P.SponsorPool(opts), /Truncated/);
});
test("missing or mismatched chain source is rejected before signing or ledger writes", async (t) => {
  if (process.platform === "win32") return t.skip("POSIX file modes required");
  let pool;
  t.after(() => pool?.close());
  const { dir, keyPath } = setup(t);
  let value = null,
    broadcasts = 0;
  const rpc = async (method) => {
    if (method === "getblockchaininfo") return { chain: "regtest" };
    if (method === "gettxout") return value;
    if (method === "sendrawtransaction") broadcasts++;
  };
  pool = new P.SponsorPool({
    keyPath,
    ledgerPath: path.join(dir, "ledger"),
    rpc,
  });
  await assert.rejects(pool.prepare(root(), 0), /Source UTXO/);
  value = {
    value: 0.002,
    scriptPubKey: { hex: pay(key.publicKey.toString()).toHex() },
  };
  await assert.rejects(pool.prepare(root(), 0), /Source UTXO/);
  assert.equal(broadcasts, 0);
  assert.equal(pool.totals().inputSats, 0);
});
test("short ledger writes are completed before broadcasting", async (t) => {
  if (process.platform === "win32") return t.skip("POSIX file modes required");
  let pool;
  t.after(() => pool?.close());
  const { dir, keyPath } = setup(t);
  const ledgerPath = path.join(dir, "short.jsonl");
  const rpc = async (method, args) => {
    if (method === "getblockchaininfo") return { chain: "regtest" };
    if (method === "gettxout")
      return {
        value: 0.001,
        scriptPubKey: { hex: pay(key.publicKey.toString()).toHex() },
      };
    if (method === "sendrawtransaction") {
      assert.doesNotThrow(() =>
        JSON.parse(fs.readFileSync(ledgerPath, "utf8"))
      );
      return new bsv.Transaction(args[0]).id;
    }
  };
  pool = new P.SponsorPool({ keyPath, ledgerPath, rpc });
  const original = fs.writeSync;
  let shortened = false;
  fs.writeSync = function (fd, data, ...args) {
    if (fd === pool.fd && !shortened) {
      shortened = true;
      return original.call(fs, fd, Buffer.from(data).subarray(0, 10));
    }
    return original.call(fs, fd, data, ...args);
  };
  try {
    await pool.prepare(root(), 0);
  } finally {
    fs.writeSync = original;
  }
  assert.equal(shortened, true);
});
test("grammar accepts N=108 and rejects 109, extra inputs/outputs and huge amounts", () => {
  const raw = P.buildPrep(root(), 0, key, 500).toBuffer(),
    n = raw[41];
  const resize = (size) => {
    const b = Buffer.concat([
      raw.subarray(0, 41),
      Buffer.from([size]),
      Buffer.alloc(size),
      raw.subarray(42 + n),
    ]);
    return b;
  };
  assert.equal(
    P.parsePrep(resize(108), key.publicKey.toString()).amount,
    99500
  );
  assert.throws(
    () => P.parsePrep(resize(109), key.publicKey.toString()),
    /grammar/
  );
  for (const offset of [4, 46 + n]) {
    const bad = Buffer.from(raw);
    bad[offset] = 2;
    assert.throws(() => P.parsePrep(bad, key.publicKey.toString()), /grammar/);
  }
  const bad = Buffer.from(raw);
  bad.writeBigUInt64LE(2100000000000001n, 47 + n);
  assert.throws(() => P.parsePrep(bad, key.publicKey.toString()), /sat amount/);
});
