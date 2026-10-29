"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const { createService } = require("../service");
test("loopback binding enforced", () => {
  assert.throws(() => createService({ host: "0.0.0.0" }), /Loopback/);
});
test("API keeps skeleton envelopes; rejects invalid methods and client state", async (t) => {
  const boxes = [];
  const store = {
    all: () => boxes,
    get: (id) => boxes.find((b) => b.id === id),
    list: () => {
      const b = {
        id: "box-1",
        state: "LISTED",
        payAddress: "fixture",
        buyerPubkey: null,
      };
      boxes.push(b);
      return b;
    },
    reserve: () => {
      throw Error("bad buyer");
    },
  };
  const app = createService({
    store,
    inventory: [{ inventoryId: "sealed", priceSats: 1000 }],
  });
  await app.listen(0);
  t.after(() => app.close());
  const url = `http://127.0.0.1:${app.address().port}`;
  assert.equal(
    (await (await fetch(url + "/health")).json()).service,
    "boxsv-mint"
  );
  assert.deepEqual(await (await fetch(url + "/v1/boxes")).json(), {
    boxes: [],
  });
  let r = await fetch(url + "/v1/boxes", { method: "POST" });
  assert.equal(r.status, 201);
  assert.equal((await r.json()).state, "LISTED");
  assert.equal((await fetch(url + "/v1/boxes/box-1")).status, 200);
  assert.equal(
    (await fetch(url + "/v1/boxes/box-1", { method: "DELETE" })).status,
    405
  );
  assert.equal(
    (
      await fetch(url + "/v1/boxes", {
        method: "POST",
        body: JSON.stringify({ state: "TRANSFERRED" }),
      })
    ).status,
    400
  );
});
