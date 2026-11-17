"use strict";
const M = require("../src/ordinal-pair"),
  crypto = require("node:crypto");
const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
const media = require("../../evidence/contracts/media.json");
function fixture() {
  const f = M.fixture();
  const metadata = JSON.stringify({
    protocol: "BOXSV-LAUNCH-METADATA-1",
    collectionId: "boxes-from-impossible-places",
    designId: "iceland",
    modelSha256: media.model.sha256,
    artSha256: media.art.sha256,
  });
  const hash = sha(metadata);
  f.foreign.outputs[0].setScript(
    M.bsv.Script.fromHex(
      M.pay(f.alice.publicKey.toString()).toHex() +
        "0063036f7264510a746578742f706c61696e0040" +
        Buffer.from(hash).toString("hex") +
        "68"
    )
  );
  const c = new M.C(M.outpoint(f.foreign, 0), 0n, f.alice.publicKey.toString());
  c.phase = 0n;
  c.owner = f.alice.publicKey.toString();
  f.box.outputs[0].setScript(c.lockingScript);
  f.origin = f.foreign.id + "_0";
  const statement = JSON.stringify({
    protocol: "BOXSV-LAUNCH-CERT-1",
    collectionId: "boxes-from-impossible-places",
    designId: "iceland",
    collectibleOrigin: f.origin,
    metadataSha256: hash,
  });
  const envelope = {
    statement,
    issuer: f.alice.publicKey.toString(),
    signature: M.bsv.crypto.ECDSA.sign(
      Buffer.from(sha(statement), "hex"),
      f.alice
    )
      .toDER()
      .toString("hex"),
  };
  const policy = {
    issuer: envelope.issuer,
    collectionId: "boxes-from-impossible-places",
    designId: "iceland",
  };
  const entries = [],
    fundingParents = [],
    fundingRoots = [];
  let source = null;
  for (const action of [0, 1, 2, 3, 4]) {
    const r = M.transition(
      f,
      source,
      action,
      action < 3 ? f.alice : f.bob,
      f.bob.publicKey.toString(),
      null,
      undefined,
      { sponsor: f.bob }
    );
    if (!r.result.success) throw Error(JSON.stringify(r.result));
    entries.push(new M.bsv.Transaction(r.tx.uncheckedSerialize()));
    fundingParents.push(r.funding);
    fundingRoots.push(r.fundingRoot);
    source = r.tx;
  }
  return {
    f,
    metadata,
    envelope,
    policy,
    entries,
    fundingParents,
    fundingRoots,
    mediaHashes: {
      modelSha256: media.model.sha256,
      artSha256: media.art.sha256,
    },
  };
}
module.exports = { fixture, sha };
