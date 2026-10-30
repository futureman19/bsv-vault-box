"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const Canary = require("../canary");
const { createMainnetAdapter } = require("../broadcast");
const { bsv, fixture } = require("../../vault/src/ordinal-pair");
async function authorized(t) {
  const rl = require("node:readline/promises");
  // Unit-only terminal simulation. Every HTTP call is a stub, never live.
  for (const stream of [process.stdin, process.stdout]) {
    const before = Object.getOwnPropertyDescriptor(stream, "isTTY");
    Object.defineProperty(stream, "isTTY", { value: true, configurable: true });
    t.after(() => {
      if (before) Object.defineProperty(stream, "isTTY", before);
      else delete stream.isTTY;
    });
  }
  t.mock.method(rl, "createInterface", () => ({
    question: async (q) => q.split("Type exactly: ")[1].split("\n")[0],
    close() {},
  }));
  return Canary.authorizeRunner({
    chain: "mainnet",
    ownerAuthorized: true,
    binding: "UNIT TEST ONLY",
  });
}
test("incorrect interactive challenge refuses and closes the gate", async (t) => {
  for (const stream of [process.stdin, process.stdout]) {
    const before = Object.getOwnPropertyDescriptor(stream, "isTTY");
    Object.defineProperty(stream, "isTTY", { value: true, configurable: true });
    t.after(() => {
      if (before) Object.defineProperty(stream, "isTTY", before);
      else delete stream.isTTY;
    });
  }
  let closed = false;
  t.mock.method(require("node:readline/promises"), "createInterface", () => ({
    question: async () => "AUTHORIZE mainnet replayed-or-wrong-challenge",
    close() {
      closed = true;
    },
  }));
  await assert.rejects(
    Canary.authorizeRunner({
      chain: "mainnet",
      ownerAuthorized: true,
      rehearsal: true,
    }),
    /Owner authorization refused/
  );
  assert.equal(closed, true);
  assert.throws(
    () =>
      Canary.broadcast(
        Canary.policy({
          chain: "mainnet",
          canary: true,
          ownerAuthorized: true,
        })
      ),
    /broadcasts disabled/
  );
});
test("forged and wrong-chain grants cannot reach fetch", async () => {
  let calls = 0;
  const local = await Canary.authorizeRunner({
    chain: "regtest",
    ownerAuthorized: true,
    rehearsal: true,
  });
  for (const authorization of [undefined, true, {}, local]) {
    const a = createMainnetAdapter({
      authorization,
      fetchImpl: async () => {
        calls++;
      },
    });
    await assert.rejects(
      a.rpc("sendrawtransaction", ["not even parsed"]),
      /broadcasts disabled/
    );
  }
  assert.equal(calls, 0);
});
test("owner gate arms only branded policies; adapter pins WoC POST and verifies txid", async (t) => {
  const authorization = await authorized(t),
    raw = fixture().foreign.uncheckedSerialize(),
    id = new bsv.Transaction(raw).id;
  const calls = [];
  const a = createMainnetAdapter({
    authorization,
    fetchImpl: async (url, opts) => {
      calls.push({ url, opts });
      return { ok: true, status: 200, text: async () => JSON.stringify(id) };
    },
  });
  assert.equal(await a.rpc("sendrawtransaction", [raw]), id);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, "https://api.whatsonchain.com/v1/bsv/main/tx/raw");
  assert.equal(calls[0].opts.redirect, "error");
  assert.deepEqual(JSON.parse(calls[0].opts.body), { txhex: raw });
  assert.throws(() => Canary.broadcast({ ...a.policy }), /broadcasts disabled/);
  assert.throws(
    () => Canary.broadcast(Canary.policy(JSON.parse(JSON.stringify(a.policy)))),
    /broadcasts disabled/
  );
});
for (const fault of ["http", "id", "timeout"])
  test("ambiguous submission has no fallback or retry: " + fault, async (t) => {
    const authorization = await authorized(t);
    let calls = 0;
    const a = createMainnetAdapter({
      authorization,
      fetchImpl: async () => {
        calls++;
        if (fault === "timeout") throw Error("timeout");
        return {
          ok: fault !== "http",
          status: 500,
          text: async () => "ab".repeat(32),
        };
      },
    });
    await assert.rejects(
      a.rpc("sendrawtransaction", [fixture().foreign.uncheckedSerialize()])
    );
    assert.equal(calls, 1);
  });
