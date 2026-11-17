"use strict";
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
async function main(args = process.argv.slice(2)) {
  if (args.length === 1 && args[0] === "--help") {
    console.log(
      "Mainnet (LATER owner execution only): node mint/scripts/canary-run.js --owner-authorized ABS_CONFIG ABS_STARTUP_REPORT ABS_NEW_EVIDENCE\nGuarded local rehearsal: node mint/scripts/canary-run.js --owner-authorized --regtest-rehearsal ABS_NEW_EVIDENCE"
    );
    return;
  }
  assert.equal(args[0], "--owner-authorized", "Owner authorization required");
  args = args.slice(1);
  if (args[0] === "--regtest-rehearsal") {
    assert.equal(args.length, 2);
    return require("./canary-rehearsal").main(args[1]);
  }
  assert.equal(
    args.length,
    3,
    "Expected config, fresh startup report and new evidence directory"
  );
  assert.ok(args.every((p) => path.isAbsolute(p)));
  const { runCanary } = require("../funded-runner");
  return runCanary({
    config: JSON.parse(fs.readFileSync(args[0], "utf8")),
    report: JSON.parse(fs.readFileSync(args[1], "utf8")),
    evidence: args[2],
    ownerAuthorized: true,
  });
}
module.exports = { main };
if (require.main === module)
  main().catch(() => {
    console.error(
      "Owner authorization required, or canary halted. Check gate, custody and staged preflight; reconcile preserved evidence before any further action."
    );
    process.exitCode = 1;
  });
