"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict"),
  fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const M = require("../../vault/src/ordinal-pair"),
  { buildBuyer } = require("../scripts/canary-buyer");
function fixture() {
  const f = M.fixture(),
    sponsor = new M.bsv.PrivateKey(
      new M.bsv.crypto.BN(3),
      M.bsv.Networks.testnet
    ),
    history = [],
    parents = [];
  let source = null;
  for (const action of [0, 1, 2]) {
    const r = M.transition(
      f,
      source,
      action,
      f.alice,
      f.bob.publicKey.toString(),
      null,
      undefined,
      { sponsor }
    );
    assert.ok(r.result.success);
    history.push(r.tx);
    parents.push(r.funding);
    source = r.tx;
  }
  const feeRoot = new M.bsv.Transaction()
    .addInput(
      new M.bsv.Transaction.Input({
        prevTxId: "aa".repeat(32),
        outputIndex: 0,
        script: "",
        output: M.output(M.bsv.Script.empty(), 3500),
      })
    )
    .addOutput(M.output(M.pay(f.bob.publicKey.toString()), 1500))
    .addOutput(M.output(M.pay(f.bob.publicKey.toString()), 1500));
  const bundle = {
    chain: "regtest",
    foreign: f.foreign.uncheckedSerialize(),
    box: f.box.uncheckedSerialize(),
    history: history.map((t) => t.uncheckedSerialize()),
    fundingParents: parents.map((t) => t.uncheckedSerialize()),
    transfer: source.uncheckedSerialize(),
    buyerPubkey: f.bob.publicKey.toString(),
  };
  return {
    bundle,
    key: f.bob,
    wrong: f.alice,
    sources: [0, 1].map((index) => ({
      raw: feeRoot.uncheckedSerialize(),
      index,
    })),
    parents: [feeRoot, source],
  };
}
test("offline buyer proves history, exact two fee sources, buyer ownership and both actions", () => {
  const f = fixture(),
    signed = buildBuyer(f.bundle, f.key, f.sources);
  assert.deepEqual(
    signed.map((r) => r.fee),
    [500, 1000, 500, 1000]
  );
  assert.equal(new M.bsv.Transaction(signed[3].raw).outputs.length, 2);
  assert.throws(() => buildBuyer(f.bundle, f.wrong, f.sources), /Wrong buyer/);
  assert.throws(() =>
    buildBuyer({ ...f.bundle, history: [] }, f.key, f.sources)
  );
  assert.throws(
    () => buildBuyer(f.bundle, f.key, [f.sources[0], f.sources[0]]),
    /distinct/
  );
});
test("separate signed-only publisher exercises adapter serially with MOCK HTTP, never real mainnet", async (t) => {
  const f = fixture(),
    signed = buildBuyer(f.bundle, f.key, f.sources),
    db = new Map(f.parents.map((tx) => [tx.id, tx]));
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "buyer-publish-"));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const file = path.join(dir, "signed.json");
  fs.writeFileSync(file, JSON.stringify(signed));
  for (const stream of [process.stdin, process.stdout]) {
    const before = Object.getOwnPropertyDescriptor(stream, "isTTY");
    Object.defineProperty(stream, "isTTY", { value: true, configurable: true });
    t.after(() => {
      if (before) Object.defineProperty(stream, "isTTY", before);
      else delete stream.isTTY;
    });
  }
  t.mock.method(require("node:readline/promises"), "createInterface", () => ({
    question: async (q) => q.split("Type exactly: ")[1].split("\n")[0],
    close() {},
  }));
  t.mock.method(global, "setTimeout", (fn) => {
    fn();
    return 0;
  });
  const hash = "bb".repeat(32),
    posts = [];
  t.mock.method(global, "fetch", async (url, opts) => {
    assert.equal(opts.redirect, "error");
    const route = new URL(url).pathname.replace("/v1/bsv/main/", "");
    let data;
    if (opts.method === "POST") {
      assert.equal(route, "tx/raw");
      const tx = new M.bsv.Transaction(JSON.parse(opts.body).txhex);
      assert.equal(tx.id, signed[posts.length].txid);
      posts.push(tx.id);
      db.set(tx.id, tx);
      return { ok: true, status: 200, text: async () => JSON.stringify(tx.id) };
    }
    assert.equal(opts.method, "GET");
    if (route === "chain/info")
      data = { chain: "main", blocks: 10, bestblockhash: hash };
    else if (route.startsWith("tx/")) {
      const tx = db.get(route.split("/")[1]);
      assert.ok(tx);
      if (route.endsWith("/hex"))
        return {
          ok: true,
          status: 200,
          text: async () => tx.uncheckedSerialize(),
        };
      data = {
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
    } else if (route.startsWith("block/"))
      data = { hash, height: 10, confirmations: 1, tx: [...db.keys()] };
    else if (route.startsWith("script/")) {
      const script = route.split("/")[1],
        result = [];
      for (const tx of db.values())
        for (const [tx_pos, o] of tx.outputs.entries())
          if (
            M.bsv.crypto.Hash.sha256(o.script.toBuffer())
              .reverse()
              .toString("hex") === script
          )
            result.push({
              tx_hash: tx.id,
              tx_pos,
              height: 10,
              value: o.satoshis,
              status: "confirmed",
              isSpentInMempoolTx: false,
            });
      data = { script, error: "", result };
    } else throw Error("Unexpected mock route " + route);
    return { ok: true, status: 200, json: async () => data };
  });
  const { main } = require("../scripts/canary-publish");
  await assert.rejects(
    main([file, path.join(dir, "refuse")]),
    /Owner authorization/
  );
  assert.equal(posts.length, 0);
  await main(["--owner-authorized", file, path.join(dir, "evidence")]);
  assert.equal(posts.length, 4);
  assert.equal(
    JSON.parse(fs.readFileSync(path.join(dir, "evidence/result.json"))).status,
    "BUYER_WITHDRAW_CONFIRMED"
  );
});
