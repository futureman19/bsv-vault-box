"use strict";
// Read-only verifier for the committed rehearsal pack. Never contacts a chain.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const root = path.resolve(process.argv[2]);
const read = (p) => JSON.parse(fs.readFileSync(path.join(root, p), "utf8"));
let gets = 0,
  localBroadcasts = 0;
for (const file of ["live-preflight.json", "live-complete-utxo.json"]) {
  const data = read(file);
  assert.match(data.status, /PASS$/);
  for (const request of data.requests) {
    assert.equal(request.method, "GET");
    assert.equal(new URL(request.url).origin, "https://api.whatsonchain.com");
    assert.equal(request.status, 200);
    gets++;
  }
}
assert.deepEqual(read("rehearsal/runner/http-requests.json"), []);
for (const dir of ["official-sale", "rehearsal/node"]) {
  const config = fs.readFileSync(path.join(root, dir, "bitcoin.conf"), "utf8");
  for (const line of [
    "regtest=1",
    "disablewallet=1",
    "listen=0",
    "connect=0",
    "dnsseed=0",
    "discover=0",
    "rpcbind=127.0.0.1",
  ])
    assert.ok(config.split(/\r?\n/).includes(line));
  assert.equal(read(dir + "/shutdown.json").exitCode, 0);
  const rows = fs
    .readFileSync(path.join(root, dir, "rpc.jsonl"), "utf8")
    .trim()
    .split(/\r?\n/)
    .map(JSON.parse);
  const info = rows.filter(
    (r) => r.method === "getblockchaininfo" && r.response?.result
  );
  assert.ok(info.length);
  for (const r of info) assert.equal(r.response.result.chain, "regtest");
  for (const r of rows)
    if (r.method === "sendrawtransaction") localBroadcasts++;
}
assert.equal(read("rehearsal/result.json").status, "PASS");
assert.equal(read("rehearsal/runner/result.json").status, "TRANSFER_CONFIRMED");
assert.equal(
  read("rehearsal/owner-gate-refusal.json").networkCallsBeforeRefusal,
  0
);
assert.equal(read("rehearsal/funding-gate-refusal.json").status, "PASS");
assert.equal(
  read("rehearsal/onchain-funding-refusal.json").runnerBroadcasts,
  0
);
assert.deepEqual(read("rehearsal/runner/runner-shutdown.json"), {
  serviceClosed: true,
  storeClosed: true,
  poolClosed: true,
});
const suspects = [];
function scan(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scan(file);
      continue;
    }
    assert.ok(
      !/\.(wif|key)$|^\.cookie$|^wallet\.dat$/i.test(entry.name),
      "Secret filename"
    );
    const text = fs.readFileSync(file, "utf8");
    if (
      /(?:^|[^A-Za-z0-9])(?:[KLc][1-9A-HJ-NP-Za-km-z]{51}|5[1-9A-HJ-NP-Za-km-z]{50}|[xt]prv[1-9A-HJ-NP-Za-km-z]{100,})(?![A-Za-z0-9])|-----BEGIN .*PRIVATE KEY-----|rpcpassword\s*=/m.test(
        text
      )
    )
      suspects.push(path.relative(root, file));
  }
}
scan(root);
assert.deepEqual(
  suspects,
  [],
  "Potential key material; inspect before publication"
);
console.log(
  JSON.stringify(
    {
      status: "PASS",
      liveMainnetGETs: gets,
      mainnetWrites: 0,
      guardedLocalBroadcastAttempts: localBroadcasts,
      secretScan: "no serialized keys or credentials found",
      shutdown: "both nodes and runner closed",
    },
    null,
    2
  )
);
