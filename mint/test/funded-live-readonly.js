"use strict";
// Public-fixture GET-only shape probe; no keys, gate, signing or submissions.
const fs = require("node:fs"),
  path = require("node:path"),
  assert = require("node:assert/strict");
const { bsv } = require("../../vault/src/ordinal-pair");
const { createMainnetAdapter } = require("../broadcast");
const { fundingRows } = require("../scripts/canary-preflight");
async function main(file) {
  assert.ok(path.isAbsolute(file));
  const fd = fs.openSync(file, "wx", 0o600),
    requests = [];
  try {
    const adapter = createMainnetAdapter({
      requests,
      fetchImpl: async (url, opts) => {
        assert.equal(opts.method, "GET");
        assert.equal(opts.redirect, "error");
        assert.ok(!opts.body);
        await new Promise((r) => setTimeout(r, 1500));
        return fetch(url, opts);
      },
    });
    const address = "1NDTiygBwjhUwsK9n9qJqrKitDURg4csxP"; // public scalar 101; NEVER fund
    const rows = await fundingRows(adapter.transport, address, true);
    assert.deepEqual(rows, []);
    const hash = bsv.crypto.Hash.sha256(
      bsv.Script.buildPublicKeyHashOut(address).toBuffer()
    )
      .reverse()
      .toString("hex");
    const script = await adapter.transport.json(
      "script/" + hash + "/unspent/all"
    );
    assert.equal(script.script, hash);
    assert.equal(script.error, "");
    assert.deepEqual(script.result, []);
    fs.writeFileSync(
      fd,
      JSON.stringify(
        {
          status: "GET_ONLY_COMPLETE_UTXO_PASS",
          createdAt: Date.now(),
          address,
          scriptHash: hash,
          script,
          requests,
        },
        null,
        2
      ) + "\n"
    );
    console.log("GET_ONLY_COMPLETE_UTXO_PASS");
  } catch (e) {
    fs.writeFileSync(
      fd,
      JSON.stringify({ status: "FAIL_CLOSED", requests }) + "\n"
    );
    throw e;
  } finally {
    fs.closeSync(fd);
  }
}
if (require.main === module)
  main(process.argv[2]).catch(() => {
    console.error("Read-only UTXO probe failed");
    process.exitCode = 1;
  });
