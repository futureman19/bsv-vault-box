"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict"),
  http = require("node:http"),
  fs = require("node:fs"),
  os = require("node:os"),
  path = require("node:path");
const { createRpc } = require("../node-rpc");
test("RPC rejects remote URLs and nonabsolute cookie paths", () => {
  for (const url of [
    "http://example.com:1234",
    "http://127.0.0.1.example.com",
    "https://127.0.0.1",
    "http://user:pass@127.0.0.1",
    "http://127.0.0.1/path",
  ])
    assert.throws(() => createRpc({ url, cookiePath: path.resolve("cookie") }));
  assert.throws(() =>
    createRpc({ url: "http://127.0.0.1:1234", cookiePath: "relative" })
  );
});
test("RPC uses cookie auth, captures only RPC data, propagates error and timeout", async (t) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "mint-rpc-"));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const cookiePath = path.join(dir, "cookie"),
    journalPath = path.join(dir, "rpc.jsonl");
  fs.writeFileSync(cookiePath, "__cookie__:fixture-not-secret");
  let auth;
  const server = http.createServer(async (req, res) => {
    auth = req.headers.authorization;
    let text = "";
    for await (const c of req) text += c;
    const q = JSON.parse(text);
    if (q.method === "hang") return;
    res.end(
      JSON.stringify({
        id: q.id,
        result: q.method === "ok" ? 42 : null,
        error: q.method === "bad" ? { code: -1, message: "rejected" } : null,
      })
    );
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  t.after(() => {
    server.closeAllConnections();
    server.close();
  });
  const rpc = createRpc({
    url: "http://127.0.0.1:" + server.address().port,
    cookiePath,
    journalPath,
    timeoutMs: 100,
  });
  assert.equal(await rpc("ok"), 42);
  assert.equal(
    auth,
    "Basic " + Buffer.from("__cookie__:fixture-not-secret").toString("base64")
  );
  await assert.rejects(rpc("bad"), /RPC bad failed/);
  await assert.rejects(rpc("hang"));
  const journal = fs.readFileSync(journalPath, "utf8");
  assert.ok(!journal.includes("fixture-not-secret"));
  assert.ok(!journal.includes(auth));
  assert.equal(journal.trim().split("\n").length, 2);
});
