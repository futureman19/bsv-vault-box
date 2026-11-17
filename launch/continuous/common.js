'use strict';
const fs=require('node:fs'), path=require('node:path'), crypto=require('node:crypto');
const assert=require('node:assert/strict');
const M=require('../../vault/src/ordinal-pair');
const ROOT=path.resolve(__dirname,'../..');
const MANIFEST_SHA='307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb';
const NETWORK='offline-fixture';
const ACTIONS=['Pack','Seal','Transfer','Open','Withdraw'];
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function canonical(x) {
  if(Array.isArray(x)) return '['+x.map(canonical).join(',')+']';
  if(x && typeof x==='object') return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';
  return JSON.stringify(x);
}
function candidate() {
  const bytes=fs.readFileSync(path.join(ROOT,'launch/collection/upstream/candidate-manifest.json'));
  assert.equal(sha(bytes),MANIFEST_SHA,'candidate manifest hash mismatch');
  const items=JSON.parse(bytes).items;
  assert.equal(items.length,201); assert.equal(new Set(items.map(x=>x.id)).size,201);
  const item=items.find(x=>x.slug==='iceland');
  const model=item.files.find(x=>x.role==='model'), art=item.files.find(x=>x.role==='promotional-illustration');
  const metadata=JSON.stringify({protocol:'BOXSV-LAUNCH-METADATA-1',collectionId:'boxes-from-impossible-places',designId:item.slug,modelSha256:model.sha256,artSha256:art.sha256});
  return {item,model,art,metadata,metadataSha256:sha(metadata),manifestSha256:MANIFEST_SHA};
}
function verifySignature(message,signature,pub) {
  try {
    assert.match(signature,/^[0-9a-f]{16,144}$/);
    const sig=M.bsv.crypto.Signature.fromDER(Buffer.from(signature,'hex'));
    return sig.toDER().toString('hex')===signature && sig.hasLowS() && M.bsv.crypto.ECDSA.verify(Buffer.from(sha(message),'hex'),sig,M.bsv.PublicKey.fromString(pub));
  } catch {return false;}
}
const raw=tx=>tx.uncheckedSerialize();
const tx=hex=>new M.bsv.Transaction(hex);
module.exports={fs,path,assert,M,ROOT,NETWORK,ACTIONS,sha,canonical,candidate,verifySignature,raw,tx};
