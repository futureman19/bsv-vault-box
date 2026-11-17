"use strict";
// No RPC, signing, transaction builders, service listener or broadcast adapter.
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const { bsv } = require("../../vault/src/ordinal-pair");
const { loadKey } = require("../keys");
const Canary = require("../canary");
const { HttpTransport } = require("../watcher");
const POLICY = Object.freeze({ chain: "mainnet", canary: true });
const PLAN = Object.freeze({
  inventory: Object.freeze([60000, 60000]),
  sponsor: Object.freeze([50000, 50000, 50000]),
  payment: Object.freeze([10000]),
});
function configuration(c, chain = "mainnet") {
  assert.deepEqual(
    Object.keys(c).sort(),
    ["buyerPubkey", "inventoryKeyPath", "paymentXpub", "sponsorKeyPath"],
    "Unexpected/missing config fields"
  );
  const policy = Canary.policy({ chain, canary: chain === "mainnet" });
  const inventory = loadKey(c.inventoryKeyPath, policy);
  const sponsor = loadKey(c.sponsorKeyPath, policy);
  const hd = new bsv.HDPublicKey(c.paymentXpub);
  assert.equal(
    hd.network.name,
    policy.network,
    "Mainnet xpub / matching network required"
  );
  assert.match(c.buyerPubkey, /^0[23][0-9a-f]{64}$/);
  assert.ok(bsv.PublicKey.isValid(c.buyerPubkey), "Invalid buyer public key");
  const addresses = {
    inventory: inventory.toAddress().toString(),
    sponsor: sponsor.toAddress().toString(),
    payment: hd
      .deriveChild(0)
      .publicKey.toAddress(bsv.Networks[policy.network])
      .toString(),
  };
  assert.equal(
    new Set(Object.values(addresses)).size,
    3,
    "Roles must have distinct addresses"
  );
  assert.ok(
    ![inventory.publicKey.toString(), sponsor.publicKey.toString()].includes(
      c.buyerPubkey
    ),
    "Buyer key must stay separate"
  );
  Canary.cap(
    policy,
    "pool",
    PLAN.sponsor.reduce((a, b) => a + b, 0)
  );
  for (const amount of PLAN.sponsor) Canary.cap(policy, "prep", amount);
  Canary.cap(policy, "fee", 500);
  Canary.cap(policy, "fee", 1000);
  Canary.inventory(policy, [{ priceSats: PLAN.payment[0] }]);
  if (policy.canary)
    assert.throws(() => Canary.broadcast(policy), /broadcasts disabled/);
  return { policy, addresses };
}
function getOnly(fetchImpl = fetch, requests = []) {
  return async (url, options) => {
    const u = new URL(url);
    assert.equal(u.origin, "https://api.whatsonchain.com");
    assert.ok(!u.search && !u.hash && !u.username && !u.password);
    assert.match(
      u.pathname,
      /^\/v1\/bsv\/main\/(?:chain\/info|address\/[1-9A-HJ-NP-Za-km-z]+\/(?:balance|unspent(?:\/all)?)|tx\/[0-9a-f]{64}(?:\/hex)?|block\/hash\/[0-9a-f]{64})$/
    );
    assert.equal(options.method, "GET");
    assert.equal(options.redirect, "error");
    assert.ok(!options.body);
    const r = await fetchImpl(url, options);
    requests.push({ method: "GET", url, status: r.status });
    assert.ok(!r.headers?.get("next-page"), "Paginated UTXO response");
    return r;
  };
}
async function fundingRows(transport, address, complete = false) {
  const data = await transport.json(
    "address/" + address + "/unspent" + (complete ? "/all" : "")
  );
  if (!complete) return data;
  assert.ok(
    data &&
      data.address === address &&
      data.error === "" &&
      Array.isArray(data.result) &&
      data.result.length < 1000 &&
      !data["next-page"],
    "Incomplete address UTXO set"
  );
  for (const row of data.result) {
    assert.equal(row.isSpentInMempoolTx, false, "Funding spent in mempool");
    assert.ok(["confirmed", "unconfirmed"].includes(row.status));
  }
  return data.result;
}
async function preflight(
  config,
  {
    fetchImpl = fetch,
    stage = "inspect",
    chain = "mainnet",
    localTransport,
  } = {}
) {
  assert.ok(["inspect", "startup", "payment"].includes(stage), "Invalid stage");
  assert.ok(
    !localTransport || chain === "regtest",
    "Local transport only for regtest"
  );
  const { policy, addresses } = configuration(config, chain);
  const requests = [];
  const transport =
    localTransport ||
    new HttpTransport({
      ...policy,
      baseUrl: "https://api.whatsonchain.com",
      apiPrefix: "/v1/bsv",
      timeoutMs: 15000,
      fetchImpl: getOnly(fetchImpl, requests),
    });
  try {
    const start = await transport.json("chain/info");
    Canary.chain(policy, start.chain);
    const funding = {};
    for (const [role, address] of Object.entries(addresses)) {
      if (stage === "payment" && role !== "payment") continue;
      const rows = await fundingRows(
        transport,
        address,
        chain === "mainnet" && stage !== "inspect"
      );
      assert.ok(
        Array.isArray(rows) && rows.length <= PLAN[role].length,
        "Unexpected funding output count: " + role
      );
      const refs = new Set();
      if (stage === "startup" && role === "payment")
        assert.equal(rows.length, 0, "payment must be UNFUNDED");
      const script = bsv.Script.buildPublicKeyHashOut(address).toHex();
      for (const row of rows) {
        assert.match(row.tx_hash, /^[0-9a-f]{64}$/);
        assert.ok(Number.isSafeInteger(row.tx_pos) && row.tx_pos >= 0);
        const ref = row.tx_hash + ":" + row.tx_pos;
        assert.ok(!refs.has(ref), "Duplicate outpoint");
        refs.add(ref);
        const e = await transport.transactionEvidence(row.tx_hash);
        assert.equal(row.height, e.block.height);
        const out = new bsv.Transaction(e.raw).outputs[row.tx_pos];
        assert.ok(
          out && out.script.toHex() === script,
          "Funding script mismatch"
        );
        assert.equal(row.value, out.satoshis);
      }
      const after = await fundingRows(
        transport,
        address,
        chain === "mainnet" && stage !== "inspect"
      );
      assert.deepEqual(after, rows, "UTXOs changed during read");
      const amounts = rows.map((r) => r.value).sort((a, b) => a - b);
      if (rows.length)
        assert.deepEqual(
          amounts,
          [...PLAN[role]],
          "Incorrect funding shape: " + role
        );
      if ((stage === "startup" && role !== "payment") || stage === "payment")
        assert.ok(rows.length, role + " must be EXACT_CONFIRMED_UNSPENT");
      funding[role] = {
        address,
        expectedSatoshis: PLAN[role],
        status: rows.length ? "EXACT_CONFIRMED_UNSPENT" : "UNFUNDED",
        outpoints: [...refs],
      };
    }
    const end = await transport.json("chain/info");
    Canary.chain(policy, end.chain);
    assert.equal(end.bestblockhash, start.bestblockhash, "Tip changed; rerun");
    assert.equal(end.blocks, start.blocks, "Tip changed; rerun");
    return {
      status: "READ_ONLY_PREFLIGHT_PASS",
      broadcastAuthorized: false,
      policy,
      stage,
      createdAt: Date.now(),
      funding,
      requests,
      composition: {
        listen: "127.0.0.1:8090 (future service; not started)",
        paymentDerivation: "xpub/0; fresh single-box journal only",
        buyerPubkey: config.buyerPubkey,
        priceSats: 10000,
        prepFeeSats: 500,
        preparedSats: [49500, 49500, 49500],
        transitionFeeSats: 1000,
        sponsorChangeSats: [48500, 48500, 48500],
      },
      limitations: [
        "Budget composition only: no inventory minted, reservation created, transaction built or signed.",
        "Payment must only be made after a durable buyer reservation in the later funded release; this command does not reserve.",
        "No mainnet writes; broadcast remains hard locked. PASS is not funding authorization or miner acceptance.",
        "Indexer evidence is not SPV. Revalidate before any later spend; no automatic retries or refunds.",
      ],
    };
  } catch (e) {
    e.publicRequests = requests;
    throw e;
  }
}
async function main(args = process.argv.slice(2)) {
  if (args.length === 1 && args[0] === "--help") {
    console.log(
      "Usage: node mint/scripts/canary-preflight.js [--stage inspect|startup|payment] ABSOLUTE_CONFIG_JSON ABSOLUTE_NEW_REPORT_JSON\nRead-only mainnet GETs and local report only; never generates keys or broadcasts."
    );
    return;
  }
  let stage = "inspect";
  if (args[0] === "--stage") {
    stage = args[1];
    args = args.slice(2);
  }
  assert.equal(
    args.length,
    2,
    "Expected config and NEW report paths (see --help)"
  );
  assert.ok(
    args.every((p) => path.isAbsolute(p)),
    "Absolute paths required"
  );
  // Reserve new report before network access; never overwrite keys/config/evidence.
  const fd = fs.openSync(args[1], "wx", 0o600);
  try {
    const c = JSON.parse(fs.readFileSync(args[0], "utf8"));
    const paced = async (url, opts) => {
      await new Promise((r) => setTimeout(r, 1500));
      return fetch(url, opts);
    };
    const report = await preflight(c, { fetchImpl: paced, stage });
    fs.writeFileSync(fd, JSON.stringify(report, null, 2) + "\n");
    console.log(
      "READ_ONLY_PREFLIGHT_PASS; broadcasts disabled; inspect local report"
    );
  } catch (e) {
    fs.writeFileSync(
      fd,
      JSON.stringify({
        status: "FAIL_CLOSED",
        broadcastAuthorized: false,
        requests: e.publicRequests || [],
      }) + "\n"
    );
    // Do not print malformed secret/config values through assertion messages.
    throw Error(
      "Preflight failed closed; check custody, public config, exact funding shape and indexer consistency. No broadcast attempted."
    );
  } finally {
    fs.closeSync(fd);
  }
}
module.exports = { fundingRows, configuration, getOnly, preflight, main };
if (require.main === module)
  main().catch((e) => {
    console.error(e.message);
    process.exitCode = 1;
  });
