"use strict";
// Only GETs, fixed public proofs. No keys, signing, RPC or broadcast imports.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const { createHash } = require("node:crypto");
const { HttpTransport } = require("../watcher");
const { findVaultOutputs } = require("../../docs/vaultcheck");
const proofs = [
  [
    "A",
    "f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39",
    0,
    "fe2c763f0a4fa1c01ef2af8f4c0628d89d6e1389d995b0a5e202e06baafae95d",
  ],
  [
    "B",
    "2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f",
    1,
    null,
  ],
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function main() {
  const destination = path.resolve(
    process.argv[2] ||
      path.join(__dirname, "../../evidence/mainnet-indexer-readonly")
  );
  fs.mkdirSync(destination, { recursive: true });
  const file = path.join(
    destination,
    "run-" + new Date().toISOString().replace(/[:.]/g, "-") + ".json"
  );
  const report = {
    status: "RUNNING",
    startedAt: new Date().toISOString(),
    boundary:
      "Mainnet public GETs only; legacy VAULT-0001 proofs, not ordinal-pair miner acceptance or SPV.",
    requests: [],
    proofs: [],
  };
  const transport = new HttpTransport({
    baseUrl: "https://api.whatsonchain.com",
    apiPrefix: "/v1/bsv",
    chain: "mainnet",
    canary: true,
    timeoutMs: 15000,
    fetchImpl: async (url, options) => {
      assert.equal(options.method, "GET");
      assert.equal(new URL(url).origin, "https://api.whatsonchain.com");
      assert.match(new URL(url).pathname, /^\/v1\/bsv\/main\//);
      for (let attempt = 1; attempt <= 3; attempt++) {
        await sleep(600);
        const started = Date.now(),
          r = await fetch(url, options);
        report.requests.push({
          method: "GET",
          url,
          status: r.status,
          attempt,
          elapsedMs: Date.now() - started,
          retryAfter: r.headers.get("retry-after"),
        });
        if (r.status !== 429 || attempt === 3) return r;
        await r.arrayBuffer();
        await sleep(attempt * 3000);
      }
    },
  });
  try {
    for (const [box, txid, state, parent] of proofs) {
      const e = await transport.transactionEvidence(txid);
      const outputs = findVaultOutputs(e.detail);
      assert.equal(outputs.length, 1);
      assert.equal(outputs[0].vout, 0);
      assert.equal(outputs[0].satoshis, 1);
      assert.equal(outputs[0].state.boxState, state);
      if (parent) assert.equal(e.detail.vin[0].txid, parent);
      else assert.match(e.detail.vin[0].txid, /^9a3007e5[0-9a-f]+0303$/);
      // Published deployment source fixes these commitment hashes independently of responses.
      const hash256 = (s) =>
        createHash("sha256")
          .update(createHash("sha256").update(s).digest())
          .digest("hex");
      for (const field of ["id", "content"])
        assert.ok(
          outputs[0].scriptHex.includes(
            hash256("VAULT-0001 live box " + box + " " + field)
          )
        );
      const address = e.detail.vout.find(
        (o) => o.scriptPubKey.addresses?.length === 1
      )?.scriptPubKey.addresses[0];
      assert.ok(address);
      // Exercise the actual balance/unspent/details payment path as well, with no injected evidence.
      const payment = await transport.read(address, 1);
      report.proofs.push({
        box,
        expectedState: state === 0 ? "SEALED" : "OPENED",
        scriptSha256: createHash("sha256")
          .update(Buffer.from(outputs[0].scriptHex, "hex"))
          .digest("hex"),
        paymentAddress: address,
        payment,
        ...e,
      });
    }
    report.status = "PASS";
    report.observations = {
      rateLimitedResponses: report.requests.filter((r) => r.status === 429)
        .length,
      requestSpacingMs: 600,
      consistency:
        "Raw txid and every output script/value matched; block membership and tip-height+1 depth matched; stable tip required.",
      canary:
        "Poll serially at >=15s intervals; back off on 429/5xx; fail closed on inconsistency. HTTP read counts only unspent receipts; do not sweep pending payments.",
      coverage:
        "WoC /v1/bsv surface exercised; /api/v1/bsv compatibility supported but bananablocks not separately tested.",
    };
  } catch (e) {
    report.status = "FAIL";
    report.error = e.stack;
    throw e;
  } finally {
    report.finishedAt = new Date().toISOString();
    fs.writeFileSync(file, JSON.stringify(report, null, 2) + "\n", {
      flag: "wx",
    });
    console.log(
      JSON.stringify({
        status: report.status,
        proofs: report.proofs.map((p) => ({
          box: p.box,
          state: p.expectedState,
          confirmations: p.confirmations,
        })),
        requests: report.requests.length,
        evidence: file,
      })
    );
  }
}
main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
