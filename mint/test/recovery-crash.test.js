"use strict";
const { test } = require("node:test"),
  assert = require("node:assert/strict");
const fs = require("node:fs"),
  path = require("node:path"),
  os = require("node:os");
const { spawnSync } = require("node:child_process");
const { SaleStore } = require("../sale"),
  { SponsorPool } = require("../pool"),
  { TransferWorker } = require("../transfer"),
  { classify } = require("../recovery");
const { fixture } = require("../../vault/tests/launch-fixture"),
  M = require("../../vault/src/ordinal-pair");
const p = fixture(),
  xpub = M.bsv.HDPrivateKey.fromSeed(
    Buffer.alloc(32, 7),
    M.bsv.Networks.testnet
  ).hdPublicKey.toString();
for (const boundary of [
  "before reservation fsync",
  "after reservation fsync",
  "after dispense",
  "after send before stage",
  "short write",
])
  test(
    "POSIX injected crash boundary: " + boundary,
    { skip: process.platform === "win32" },
    async (t) => {
      const dir = fs.mkdtempSync(path.join(os.tmpdir(), "recovery-crash-")),
        saleFile = path.join(dir, "sales.jsonl"),
        poolFile = path.join(dir, "pool.jsonl");
      const keyPaths = ["owner", "sponsor"].map((n) => path.join(dir, n));
      for (const [i, key] of [p.f.alice, p.f.bob].entries())
        fs.writeFileSync(keyPaths[i], key.toWIF(), { mode: 0o600 });
      let store = new SaleStore({ file: saleFile, xpub }),
        pool,
        sends = 0,
        dispenses = 0;
      t.after(() => {
        store.close();
        pool?.close();
        fs.rmSync(dir, { recursive: true, force: true });
      });
      const root = p.fundingRoots[2],
        source = p.entries[1];
      let funding;
      const rpc = async (m, args) => {
        if (m === "getblockchaininfo") return { chain: "regtest" };
        if (m === "gettxout") {
          const tx = [root, source, funding].find((x) => x?.id === args[0]);
          const o = tx?.outputs[args[1]];
          return o
            ? {
                value: o.satoshis / 1e8,
                scriptPubKey: { hex: o.script.toHex() },
                confirmations: 6,
              }
            : null;
        }
        if (m === "getrawtransaction") {
          const e = Error("not captured");
          e.code = -5;
          throw e;
        }
        if (m === "sendrawtransaction") {
          sends++;
          return new M.bsv.Transaction(args[0]).id;
        }
        throw Error(m);
      };
      const poolOptions = { keyPath: keyPaths[1], ledgerPath: poolFile, rpc };
      pool = new SponsorPool(poolOptions);
      funding = await pool.prepare(root, 0);
      sends = 0;
      const b = store.list({ priceSats: 1000, inventoryId: "iceland" });
      store.reserve(b.id, p.f.bob.publicKey.toString(), Date.now() + 60000);
      store.payment(b.id, {
        satoshis: 1000,
        confirmations: 6,
        refs: ["fixture:0"],
      });
      const dispense = pool.dispense.bind(pool);
      pool.dispense = async () => {
        dispenses++;
        const out = await dispense();
        if (boundary === "after dispense")
          throw Error("injected after dispense");
        return out;
      };
      const makeWorker = () =>
        new TransferWorker({
          store,
          pool,
          rpc,
          inventory: () => ({ f: p.f, source }),
          inventoryKeyPath: keyPaths[0],
          sponsorKeyPath: keyPaths[1],
          paymentTransport: {
            read: async () => ({ satoshis: 1000, confirmations: 6 }),
          },
        });
      let w = makeWorker();
      const originalSync = fs.fsyncSync,
        originalWrite = fs.writeSync,
        update = store.update.bind(store);
      let armed = true;
      if (boundary.includes("reservation fsync"))
        fs.fsyncSync = function (fd) {
          if (fd === store.fd && armed) {
            armed = false;
            if (boundary.startsWith("after")) originalSync(fd);
            throw Error("injected fsync failure");
          }
          return originalSync(fd);
        };
      if (boundary === "short write")
        fs.writeSync = function (fd, buf, offset, len) {
          if (fd === store.fd) {
            if (armed) {
              armed = false;
              return originalWrite(fd, buf, offset, 10);
            }
            return 0;
          }
          return originalWrite(fd, buf, offset, len);
        };
      if (boundary === "after send before stage")
        store.update = (id, patch) => {
          if (patch.transfer?.stage === "SUBMITTED" && armed) {
            armed = false;
            throw Error("injected stage persistence");
          }
          return update(id, patch);
        };
      try {
        if (boundary === "after send before stage") await w.run(b.id);
        else await assert.rejects(w.run(b.id), /injected|short write/);
      } finally {
        fs.fsyncSync = originalSync;
        fs.writeSync = originalWrite;
      }
      const text = fs.readFileSync(saleFile, "utf8"),
        poolText = fs.readFileSync(poolFile, "utf8");
      const input = {
        id: b.id,
        saleText: text,
        poolText,
        sponsorPubkey: p.f.bob.publicKey.toString(),
        observations: [],
      };
      const result = classify(input);
      assert.equal(
        result.classification,
        boundary === "short write"
          ? "INCONSISTENT"
          : boundary === "after send before stage"
          ? "UNCERTAIN_SEND"
          : "RESERVING"
      );
      assert.equal(sends, boundary === "after send before stage" ? 1 : 0);
      assert.ok(dispenses <= 1);
      assert.equal(result.mayResume, false);
      store.close();
      pool.close();
      if (boundary === "short write")
        assert.throws(
          () => new SaleStore({ file: saleFile, xpub }),
          /Truncated/
        );
      else {
        store = new SaleStore({ file: saleFile, xpub });
        pool = new SponsorPool(poolOptions);
        pool.dispense = async () => {
          throw Error("replacement forbidden");
        };
        w = makeWorker();
        if (boundary === "after send before stage") {
          assert.equal(store.get(b.id).transfer.txid, result.txid);
          assert.equal(
            store.get(b.id).transfer.raw,
            JSON.parse(text.trim().split("\n").at(-1)).box.transfer.raw
          );
        } else await assert.rejects(w.run(b.id), /Ambiguous funding/);
      }
      assert.deepEqual(classify(input), result);
      // CLI must not acquire/remove locks or alter any evidence, even during inspection.
      const observationFile = path.join(dir, "observations.json");
      fs.writeFileSync(observationFile, "[]");
      const before = [saleFile, poolFile].map((f) => fs.readFileSync(f));
      const cli = spawnSync(
        process.execPath,
        [
          path.resolve(__dirname, "../scripts/recovery-inspect.js"),
          saleFile,
          poolFile,
          observationFile,
          b.id,
          p.f.bob.publicKey.toString(),
          "1",
        ],
        { encoding: "utf8" }
      );
      assert.equal(
        cli.status,
        result.classification === "INCONSISTENT" ? 2 : 0,
        cli.stderr
      );
      assert.deepEqual(JSON.parse(cli.stdout), result);
      [saleFile, poolFile].forEach((f, i) =>
        assert.deepEqual(fs.readFileSync(f), before[i])
      );
    }
  );
