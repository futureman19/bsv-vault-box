"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const { bsv, output } = require("../../vault/src/ordinal-pair");
const {
  configuration,
  getOnly,
  preflight,
  main,
} = require("../scripts/canary-preflight");
function fixture(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "preflight-"));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  // Public disposable scalars; never random keys or real funds.
  const key = (n) =>
    new bsv.PrivateKey(new bsv.crypto.BN(n), bsv.Networks.livenet);
  const c = {
    inventoryKeyPath: path.join(dir, "inventory.wif"),
    sponsorKeyPath: path.join(dir, "sponsor.wif"),
    paymentXpub: bsv.HDPrivateKey.fromSeed(
      Buffer.alloc(32, 7),
      bsv.Networks.livenet
    ).hdPublicKey.toString(),
    buyerPubkey: key(3).publicKey.toString(),
  };
  fs.writeFileSync(c.inventoryKeyPath, key(1).toWIF(), { mode: 0o600 });
  fs.writeFileSync(c.sponsorKeyPath, key(2).toWIF(), { mode: 0o600 });
  return { c, dir };
}
function network(
  c,
  {
    funded = false,
    wrongShape = false,
    duplicate = false,
    changed = false,
  } = {}
) {
  const { addresses } = configuration(c),
    txs = {},
    rows = {};
  const hash = "ab".repeat(32);
  for (const [role, address] of Object.entries(addresses)) {
    const amounts =
      role === "inventory"
        ? [60000, 60000]
        : role === "sponsor"
        ? wrongShape
          ? [150000]
          : [50000, 50000, 50000]
        : [10000];
    const tx = new bsv.Transaction().addInput(
      new bsv.Transaction.Input({
        prevTxId: "cd".repeat(32),
        outputIndex: 0,
        script: "",
        output: output(bsv.Script.empty()),
      })
    );
    for (const amount of amounts)
      tx.addOutput(output(bsv.Script.buildPublicKeyHashOut(address), amount));
    txs[tx.id] = tx;
    rows[address] = funded
      ? amounts.map((value, tx_pos) => ({
          tx_hash: tx.id,
          tx_pos,
          height: 10,
          value,
        }))
      : [];
    if (duplicate && role === "inventory" && funded)
      rows[address][1] = rows[address][0];
  }
  let calls = 0,
    tips = 0;
  return {
    calls: () => calls,
    fetch: async (url, opts) => {
      calls++;
      assert.equal(opts.method, "GET");
      assert.equal(opts.redirect, "error");
      const route = new URL(url).pathname.replace("/v1/bsv/main/", "");
      let data;
      if (route === "chain/info")
        data = {
          chain: "main",
          blocks: 10,
          bestblockhash: changed && ++tips > 1 ? "ef".repeat(32) : hash,
        };
      else if (route.startsWith("address/")) {
        const address = route.split("/")[1];
        data = rows[address];
        if (route.endsWith("/unspent/all"))
          data = {
            address,
            error: "",
            result: data.map((r) => ({
              ...r,
              status: "confirmed",
              isSpentInMempoolTx: false,
            })),
          };
      } else if (route.startsWith("block/hash/"))
        data = { hash, height: 10, confirmations: 1, tx: Object.keys(txs) };
      else if (route.startsWith("tx/")) {
        const tx = txs[route.split("/")[1]];
        data = route.endsWith("/hex")
          ? tx.uncheckedSerialize()
          : {
              txid: tx.id,
              blockhash: hash,
              blockheight: 10,
              confirmations: 1,
              vout: tx.outputs.map((o, n) => ({
                n,
                value: o.satoshis / 1e8,
                scriptPubKey: { hex: o.script.toHex() },
              })),
            };
      } else throw Error("Unexpected route " + route);
      return {
        status: 200,
        ok: true,
        json: async () => structuredClone(data),
        text: async () => data,
      };
    },
  };
}
test("staged preflight includes mempool and rejects spent or incomplete UTXO sets", async (t) => {
  const { c } = fixture(t),
    n = network(c, { funded: true });
  const address = configuration(c).addresses.payment;
  for (const fault of ["spent", "pagination", "pending-payment"]) {
    const fetchImpl = async (url, opts) => {
      const r = await n.fetch(url.replace("/unspent/all", "/unspent"), opts);
      if (!url.endsWith("/unspent/all")) return r;
      const rows = await r.json();
      const payment = url.includes("/" + address + "/");
      const data = {
        address: new URL(url).pathname.split("/")[5],
        error: "",
        result: payment
          ? fault === "pending-payment"
            ? [
                {
                  ...rows[0],
                  height: 0,
                  status: "unconfirmed",
                  isSpentInMempoolTx: false,
                },
              ]
            : []
          : rows.map((v) => ({
              ...v,
              status: "confirmed",
              isSpentInMempoolTx: fault === "spent",
            })),
      };
      if (fault === "pagination") data["next-page"] = "more";
      return { ok: true, status: 200, json: async () => data };
    };
    await assert.rejects(preflight(c, { stage: "startup", fetchImpl }));
  }
});
test("startup stage refuses early payment and unfunded service roles", async (t) => {
  const { c } = fixture(t);
  await assert.rejects(
    preflight(c, {
      fetchImpl: network(c, { funded: true }).fetch,
      stage: "startup",
    }),
    /payment.*UNFUNDED/
  );
  await assert.rejects(
    preflight(c, { fetchImpl: network(c).fetch, stage: "startup" }),
    /inventory.*EXACT/
  );
});
test("startup and payment stages enforce disjoint exact shapes", async (t) => {
  const { c } = fixture(t),
    n = network(c, { funded: true });
  const address = configuration(c).addresses.payment;
  const fetchImpl = async (url, opts) =>
    url.includes("/address/" + address + "/")
      ? {
          ok: true,
          status: 200,
          json: async () => ({ address, error: "", result: [] }),
        }
      : n.fetch(url, opts);
  const r = await preflight(c, { fetchImpl, stage: "startup" });
  assert.equal(r.stage, "startup");
  assert.ok(Number.isSafeInteger(r.createdAt));
  const payment = await preflight(c, { fetchImpl: n.fetch, stage: "payment" });
  assert.equal(payment.stage, "payment");
  assert.deepEqual(Object.keys(payment.funding), ["payment"]);
});
test("preflight executes full confirmed funding shape using GETs only; never signs", async (t) => {
  const { c } = fixture(t),
    n = network(c, { funded: true });
  const original = bsv.Transaction.prototype.sign;
  bsv.Transaction.prototype.sign = () => {
    throw Error("must not sign");
  };
  try {
    const r = await preflight(c, { fetchImpl: n.fetch });
    assert.equal(r.status, "READ_ONLY_PREFLIGHT_PASS");
    assert.equal(r.broadcastAuthorized, false);
    assert.ok(
      Object.values(r.funding).every(
        (v) => v.status === "EXACT_CONFIRMED_UNSPENT"
      )
    );
    assert.ok(r.requests.length > 6);
    assert.ok(r.requests.every((v) => v.method === "GET"));
    assert.deepEqual(r.composition.preparedSats, [49500, 49500, 49500]);
    assert.ok(
      !JSON.stringify(r).includes(fs.readFileSync(c.sponsorKeyPath, "utf8"))
    );
  } finally {
    bsv.Transaction.prototype.sign = original;
  }
});
test("unfunded dry run labels absence honestly and cannot authorize payment", async (t) => {
  const { c } = fixture(t),
    n = network(c);
  const r = await preflight(c, { fetchImpl: n.fetch });
  assert.ok(Object.values(r.funding).every((v) => v.status === "UNFUNDED"));
  assert.equal(r.broadcastAuthorized, false);
});
for (const mutation of ["wrongShape", "duplicate", "changed"])
  test("preflight rejects " + mutation, async (t) => {
    const { c } = fixture(t),
      n = network(c, { funded: true, [mutation]: true });
    await assert.rejects(preflight(c, { fetchImpl: n.fetch }));
  });
for (const fault of [
  "partial",
  "extra",
  "unconfirmed",
  "wrong-value",
  "wrong-script",
  "http429",
  "wrong-chain",
])
  test("funding evidence fails closed: " + fault, async (t) => {
    const { c } = fixture(t),
      n = network(c, { funded: true });
    const fetchImpl = async (url, opts) => {
      const response = await n.fetch(url, opts);
      if (fault === "http429") return { status: 429, ok: false };
      if (url.endsWith("/hex")) return response;
      const data = await response.json();
      if (url.endsWith("/unspent")) {
        if (fault === "partial") data.pop();
        if (fault === "extra") data.push(data[0]);
        if (fault === "unconfirmed") data[0].height = 0;
        if (fault === "wrong-value") data[0].value++;
      }
      if (fault === "wrong-script" && data.vout)
        data.vout[0].scriptPubKey.hex = "51";
      if (fault === "wrong-chain" && data.chain) data.chain = "test";
      return { ...response, json: async () => data };
    };
    await assert.rejects(preflight(c, { fetchImpl }));
  });
test("custody, network and unsupported options fail before HTTP", async (t) => {
  const { c } = fixture(t);
  let calls = 0;
  const fetchImpl = async () => {
    calls++;
    throw Error("unexpected");
  };
  fs.chmodSync(c.inventoryKeyPath, 0o644);
  await assert.rejects(preflight(c, { fetchImpl }), /0600/);
  fs.chmodSync(c.inventoryKeyPath, 0o600);
  await assert.rejects(
    preflight({ ...c, broadcast: true }, { fetchImpl }),
    /config fields/
  );
  await assert.rejects(
    preflight(
      {
        ...c,
        paymentXpub: bsv.HDPrivateKey.fromSeed(
          Buffer.alloc(32, 7),
          bsv.Networks.testnet
        ).hdPublicKey.toString(),
      },
      { fetchImpl }
    ),
    /Mainnet/
  );
  await assert.rejects(
    preflight({ ...c, sponsorKeyPath: c.inventoryKeyPath }, { fetchImpl }),
    /distinct/
  );
  assert.equal(calls, 0);
});
test("GET firewall rejects writes, redirects, alien origins, unexpected routes before fetch", async () => {
  let calls = 0;
  const f = getOnly(async () => {
    calls++;
  });
  const url = "https://api.whatsonchain.com/v1/bsv/main/chain/info";
  for (const opts of [
    { method: "POST", redirect: "error" },
    { method: "GET", redirect: "follow" },
    { method: "GET", redirect: "error", body: "x" },
  ])
    await assert.rejects(f(url, opts));
  for (const u of [
    url.replace("api.whatsonchain.com", "example.com"),
    url.replace("chain/info", "tx/raw"),
    url + "?x=1",
  ])
    await assert.rejects(f(u, { method: "GET", redirect: "error" }));
  assert.equal(calls, 0);
});
test("CLI writes new report and keeps secrets out of it; failures are redacted", async (t) => {
  const { dir, c } = fixture(t),
    n = network(c, { funded: true });
  const config = path.join(dir, "config.json"),
    report = path.join(dir, "report.json");
  fs.writeFileSync(config, JSON.stringify(c));
  const oldFetch = global.fetch,
    oldTimeout = global.setTimeout;
  global.fetch = n.fetch;
  global.setTimeout = (fn) => {
    fn();
    return 0;
  };
  try {
    await main([config, report]);
    assert.equal(
      JSON.parse(fs.readFileSync(report)).status,
      "READ_ONLY_PREFLIGHT_PASS"
    );
    assert.equal(fs.statSync(report).mode & 0o777, 0o600);
    global.fetch = async () => ({ ok: false, status: 429 });
    const failed = path.join(dir, "failed.json");
    await assert.rejects(main([config, failed]), /failed closed/);
    const failure = JSON.parse(fs.readFileSync(failed));
    assert.equal(failure.status, "FAIL_CLOSED");
    assert.equal(failure.broadcastAuthorized, false);
    assert.equal(failure.requests[0].status, 429);
  } finally {
    global.fetch = oldFetch;
    global.setTimeout = oldTimeout;
  }
});
test("CLI help runs, refuses unsupported mode, never overwrites existing file", async (t) => {
  const { dir, c } = fixture(t);
  await main(["--help"]);
  await assert.rejects(main(["--broadcast"]));
  const p = path.join(dir, "config.json");
  fs.writeFileSync(p, JSON.stringify(c));
  const before = fs.readFileSync(p);
  await assert.rejects(main([p, p]), /EEXIST/);
  assert.deepEqual(fs.readFileSync(p), before);
});
