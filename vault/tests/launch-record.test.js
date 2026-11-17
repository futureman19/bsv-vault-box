"use strict";
const assert = require("node:assert/strict"),
  M = require("../src/ordinal-pair");
const { verifyLaunch } = require("../src/launch-record"),
  { fixture, sha } = require("./launch-fixture");
const p = fixture();
describe("single collectible with detached signed launch record", function () {
  this.timeout(120000);
  it("accepts canonical detached record independently of serialized custody replay", () => {
    assert.deepEqual(verifyLaunch(p), {
      originalIssuanceProvenance: true,
      originalManifestComplete: true,
      currentCustodyIntegrity: true,
    });
  });
  it("retains immutable origin, one-sat principals and fresh valid sponsor preparations through withdrawal", () => {
    assert.equal(new Set(p.fundingParents.map((t) => t.id)).size, 5);
    p.entries.forEach((tx, i) => {
      assert.equal(tx.outputs[0].satoshis, 1);
      assert.equal(tx.outputs[1].satoshis, 1);
      assert.equal(
        tx.inputs[0].prevTxId.toString("hex"),
        i ? p.entries[i - 1].id : p.f.foreign.id
      );
      assert.equal(tx.inputs[0].outputIndex, 0);
      assert.equal(
        M.verify(p.fundingParents[i], [p.fundingRoots[i]]).success,
        true
      );
      assert.equal(
        M.verifyHistory(p.f, p.entries.slice(0, i + 1), p.fundingParents)
          .origin,
        p.f.origin
      );
    });
  });
  for (const [label, change] of [
    [
      "unknown issuer",
      (x) => {
        x.envelope.issuer = p.f.bob.publicKey.toString();
        x.envelope.signature = M.bsv.crypto.ECDSA.sign(
          Buffer.from(sha(x.envelope.statement), "hex"),
          p.f.bob
        )
          .toDER()
          .toString("hex");
      },
    ],
    ["forged signature", (x) => (x.envelope.signature = "00")],
    ["missing external policy", (x) => (x.policy = undefined)],
    ["wrong collection policy", (x) => (x.policy.collectionId = "another")],
    ["wrong design policy", (x) => (x.policy.designId = "japan")],
    ["extra envelope field", (x) => (x.envelope.extra = "x")],
    ["noncanonical statement", (x) => (x.envelope.statement += " ")],
    [
      "changed origin",
      (x) => {
        let s = JSON.parse(x.envelope.statement);
        s.collectibleOrigin = "11".repeat(32) + "_0";
        x.envelope.statement = JSON.stringify(s);
      },
    ],
    [
      "uppercase digest",
      (x) => {
        let s = JSON.parse(x.envelope.statement);
        s.metadataSha256 = s.metadataSha256.toUpperCase();
        x.envelope.statement = JSON.stringify(s);
      },
    ],
    [
      "extra statement field",
      (x) => {
        let s = JSON.parse(x.envelope.statement);
        s.extra = "x";
        x.envelope.statement = JSON.stringify(s);
      },
    ],
    [
      "missing statement field",
      (x) => {
        let s = JSON.parse(x.envelope.statement);
        delete s.designId;
        x.envelope.statement = JSON.stringify(s);
      },
    ],
  ])
    it("rejects provenance: " + label, () => {
      const x = { ...p, policy: { ...p.policy }, envelope: { ...p.envelope } };
      change(x);
      const r = verifyLaunch(x);
      assert.equal(r.originalIssuanceProvenance, false);
      assert.equal(r.currentCustodyIntegrity, true);
    });
  for (const [label, metadata, mediaHashes] of [
    [
      "tampered metadata",
      p.metadata.replace("iceland", "japan"),
      p.mediaHashes,
    ],
    ["noncanonical metadata", p.metadata + " ", p.mediaHashes],
    [
      "changed media bytes",
      p.metadata,
      { ...p.mediaHashes, modelSha256: "00".repeat(32) },
    ],
    ["missing art", p.metadata, { modelSha256: p.mediaHashes.modelSha256 }],
  ])
    it("rejects manifest: " + label, () =>
      assert.equal(
        verifyLaunch({ ...p, metadata, mediaHashes }).originalManifestComplete,
        false
      )
    );
  it("rejects copied current script presented as original independently of its label", () => {
    const f = {
      ...p.f,
      foreign: new M.bsv.Transaction(p.f.foreign.uncheckedSerialize()),
    };
    f.foreign.outputs[0].setScript(p.entries[1].outputs[0].script);
    const r = verifyLaunch({ ...p, f });
    assert.equal(r.originalIssuanceProvenance, false);
    assert.equal(r.currentCustodyIntegrity, false);
  });
  it("rejects unsupported full-art grammar", () => {
    const f = {
      ...p.f,
      foreign: new M.bsv.Transaction(p.f.foreign.uncheckedSerialize()),
    };
    f.foreign.outputs[0].setScript(
      M.bsv.Script.fromHex(
        f.foreign.outputs[0].script
          .toHex()
          .replace("746578742f706c61696e", "6d6f64656c2f676c7466")
      )
    );
    assert.equal(verifyLaunch({ ...p, f }).originalIssuanceProvenance, false);
  });
  it("rejects missing, duplicate and substituted principal serialized spends", () => {
    for (const mutation of [
      (t) => t.inputs.splice(1, 1),
      (t) => {
        t.inputs[1] = t.inputs[0];
      },
      (t) => {
        t.inputs[0].prevTxId = Buffer.alloc(32, 9);
      },
    ]) {
      const entries = p.entries.map(
        (t) => new M.bsv.Transaction(t.uncheckedSerialize())
      );
      mutation(entries[2]);
      assert.equal(
        verifyLaunch({ ...p, entries }).currentCustodyIntegrity,
        false
      );
    }
  });
  it("rejects sealed withdrawal, former owner open/withdraw and opened-to-seal reuse", () => {
    for (const [source, action, key] of [
      [p.entries[1], 4, p.f.alice],
      [p.entries[2], 3, p.f.alice],
      [p.entries[3], 4, p.f.alice],
      [p.entries[3], 1, p.f.bob],
    ])
      assert.equal(
        M.transition(p.f, source, action, key, null, null, undefined, {
          sponsor: p.f.bob,
        }).result.success,
        false
      );
  });
});
