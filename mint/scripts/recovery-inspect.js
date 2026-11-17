"use strict";
// Explicit local paths only. This command never opens a journal for writing,
// creates/removes locks, loads keys, calls RPC or authorizes resumption.
const fs = require("node:fs"),
  path = require("node:path");
const { classify } = require("../recovery");
function read(file) {
  if (!path.isAbsolute(file)) throw Error("Absolute evidence paths required");
  const stat = fs.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.size > 25000000)
    throw Error("Regular evidence file under 25 MB required");
  return fs.readFileSync(file, "utf8");
}
try {
  const args = process.argv.slice(2);
  if (args.length !== 6)
    throw Error(
      "Usage: node mint/scripts/recovery-inspect.js ABS_SALES_JSONL ABS_POOL_JSONL ABS_OBSERVATIONS_JSON SALE_ID SPONSOR_PUBLIC_KEY DEPTH"
    );
  const [sales, pool, observations, id, sponsorPubkey, depth] = args;
  const result = classify({
    id,
    sponsorPubkey,
    depth: Number(depth),
    saleText: read(sales),
    poolText: read(pool),
    observations: JSON.parse(read(observations)),
  });
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  process.exitCode = result.classification === "INCONSISTENT" ? 2 : 0;
} catch {
  process.stderr.write(
    "Read-only inspection failed: supply six explicit arguments and readable bounded local evidence files; no state changed.\n"
  );
  process.exitCode = 2;
}
