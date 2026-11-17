"use strict";
// Pure local checks. No keys, networking or chain queries.
const M = require("./ordinal-pair"),
  crypto = require("node:crypto");
const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
const identifier = /^[a-z0-9][a-z0-9-]{0,127}$/;
const digest = /^[0-9a-f]{64}$/;
function exact(value, fields) {
  if (
    !value ||
    Array.isArray(value) ||
    typeof value !== "object" ||
    Object.keys(value).length !== fields.length ||
    fields.some(
      (k) =>
        !Object.prototype.hasOwnProperty.call(value, k) ||
        typeof value[k] !== "string"
    )
  )
    throw Error("Invalid fields");
  return Object.fromEntries(fields.map((k) => [k, value[k]]));
}
function canonical(raw, fields, protocol) {
  if (typeof raw !== "string" || raw.length > 4096)
    throw Error("Invalid canonical record");
  const o = exact(JSON.parse(raw), fields);
  if (
    JSON.stringify(o) !== raw ||
    o.protocol !== protocol ||
    !identifier.test(o.collectionId) ||
    !identifier.test(o.designId)
  )
    throw Error("Noncanonical record");
  return o;
}
function admission(f) {
  const hex = f.foreign.outputs[0].script.toHex();
  const match =
    /^76a914[0-9a-f]{40}88ac0063036f7264510a746578742f706c61696e0040([0-9a-f]{128})68$/.exec(
      hex
    );
  if (
    !match ||
    f.foreign.outputs[0].satoshis !== 1 ||
    !M.verifyHistory(f, []).valid
  )
    throw Error("Unsupported launch admission");
  const hash = Buffer.from(match[1], "hex").toString("ascii");
  if (!digest.test(hash) || Buffer.from(hash).toString("hex") !== match[1])
    throw Error("Invalid commitment");
  return hash;
}
function verifyLaunch({
  f,
  entries,
  fundingParents,
  envelope,
  metadata,
  mediaHashes,
  policy,
}) {
  const result = {
    originalIssuanceProvenance: false,
    originalManifestComplete: false,
    currentCustodyIntegrity: false,
  };
  try {
    result.currentCustodyIntegrity = M.verifyHistory(
      f,
      entries,
      fundingParents
    ).valid;
  } catch {}
  let commitment;
  try {
    commitment = admission(f);
  } catch {
    return result;
  }
  try {
    const e = exact(envelope, ["statement", "issuer", "signature"]);
    const p = exact(policy, ["issuer", "collectionId", "designId"]);
    const s = canonical(
      e.statement,
      [
        "protocol",
        "collectionId",
        "designId",
        "collectibleOrigin",
        "metadataSha256",
      ],
      "BOXSV-LAUNCH-CERT-1"
    );
    if (
      !/^0[23][0-9a-f]{64}$/.test(e.issuer) ||
      e.issuer !== p.issuer ||
      !M.bsv.PublicKey.isValid(e.issuer) ||
      s.collectionId !== p.collectionId ||
      s.designId !== p.designId ||
      !/^[0-9a-f]{64}_0$/.test(s.collectibleOrigin) ||
      s.collectibleOrigin !== f.foreign.id + "_0" ||
      !digest.test(s.metadataSha256) ||
      s.metadataSha256 !== commitment ||
      !/^[0-9a-f]{16,144}$/.test(e.signature) ||
      e.signature.length % 2
    )
      throw Error("Provenance mismatch");
    const sig = M.bsv.crypto.Signature.fromDER(Buffer.from(e.signature, "hex"));
    if (
      sig.toDER().toString("hex") !== e.signature ||
      !sig.hasLowS() ||
      !M.bsv.crypto.ECDSA.verify(
        Buffer.from(sha(e.statement), "hex"),
        sig,
        M.bsv.PublicKey.fromString(p.issuer)
      )
    )
      throw Error("Invalid signature");
    result.originalIssuanceProvenance = true;
  } catch {}
  try {
    const m = canonical(
      metadata,
      ["protocol", "collectionId", "designId", "modelSha256", "artSha256"],
      "BOXSV-LAUNCH-METADATA-1"
    );
    const h = exact(mediaHashes, ["modelSha256", "artSha256"]);
    if (
      !digest.test(m.modelSha256) ||
      !digest.test(m.artSha256) ||
      sha(metadata) !== commitment ||
      m.modelSha256 !== h.modelSha256 ||
      m.artSha256 !== h.artSha256 ||
      !policy ||
      m.collectionId !== policy.collectionId ||
      m.designId !== policy.designId
    )
      throw Error("Manifest mismatch");
    result.originalManifestComplete = true;
  } catch {}
  return result;
}
module.exports = { verifyLaunch };
