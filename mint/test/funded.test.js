"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const Canary = require("../canary");
test("funded authorization is a deliberate gate, not a policy boolean", async () => {
  assert.throws(
    () =>
      Canary.broadcast(
        Canary.policy({ chain: "mainnet", canary: true, ownerAuthorized: true })
      ),
    /broadcasts disabled/
  );
  assert.equal(typeof Canary.authorizeRunner, "function");
  await assert.rejects(
    Canary.authorizeRunner({ chain: "mainnet", ownerAuthorized: false }),
    /Owner authorization/
  );
  await assert.rejects(
    Canary.authorizeRunner({ chain: "mainnet", ownerAuthorized: true }),
    /interactive/
  );
});
