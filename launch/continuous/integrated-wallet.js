'use strict';
// Construction/assembly bridge. Buyer signing is exclusively WalletTransport;
// public scalar 1/3 service fixtures are not production issuer/sponsor custody.
const C=require('./common'),F=require('./fixture-wallet'),A=require('../wallet-transport/adapter');
const {M,assert,sha,canonical,raw,tx}=C;
const key=n=>new M.bsv.PrivateKey(new M.bsv.crypto.BN(n),M.bsv.Networks.testnet);
const seller=key(1),sponsor=key(3);
const sign=(text,k)=>M.bsv.crypto.ECDSA.sign(Buffer.from(sha(text),'hex'),k).toDER().toString('hex');
const binding=b=>({manifestSha256:b.manifestSha256,designId:b.designId,metadataSha256:b.metadataSha256,origin:b.origin,buyerPubkey:b.buyerPubkey});
function unsigned(hex){const t=tx(hex);for(let i=0;i<2;i++)t.inputs[i].setScript(M.bsv.Script.empty());return raw(t);}
function build(request,signatures) {
 const f={foreign:tx(request.inventory.foreign),box:tx(request.inventory.box)};
 const buyer=['Open','Withdraw'].includes(request.action);
 return M.transition(f,request.source?tx(request.source):null,request.actionIndex,buyer?{publicKey:M.bsv.PublicKey.fromString(request.binding.buyerPubkey)}:seller,request.binding.buyerPubkey,null,undefined,{sponsor,...(buyer?{ownerSignature:(_t,_o,i)=>signatures?.[i]||'00'}:{})});
}
function prepared(request,policy,index,construction) {
 const r={version:1,id:request.key+'-input-'+index,expiresAt:Date.now()+120000,network:policy.network,identityKey:policy.identityKey,signingKey:policy.signingKey,action:request.action,binding:binding(request.binding)};
 if(construction)Object.assign(r,{transaction:{raw:unsigned(raw(construction.tx)),parents:[request.source,request.source,raw(construction.funding)],inputIndex:index},intent:{outputs:construction.tx.outputs.map(o=>({script:o.script.toHex(),satoshis:o.satoshis})),maxFee:500}});
 return r;
}
function verifyAuthorizations(s,request,response) {
 assert.ok(s.policy.wallet,'independent enrollment required');
 const w=s.policy.wallet,items=response.authorizations;
 assert.equal(w.signingKey,s.policy.buyer);assert.equal(w.network,'testnet','offline demo wallet network');
 assert.ok(['Reserve','Open','Withdraw'].includes(request.action),'wallet role');
 assert.equal(response.signer,w.signingKey);assert.equal(response.requestHash,sha(canonical(request)));assert.equal(response.network,s.policy.network);
 assert.equal(items.length,request.action==='Reserve'?1:2);
 for(const [i,a] of items.entries()) {
  assert.deepEqual(a.request.binding,binding(s.binding));assert.equal(a.request.action,request.action);assert.equal(a.request.id,request.key+'-input-'+i);
  assert.equal(a.request.identityKey,w.identityKey);assert.equal(a.request.signingKey,w.signingKey);assert.equal(a.request.network,w.network);
  assert.ok(Number.isSafeInteger(a.acceptedAt));
  A.verifyResponse(a.request,a.response,w,{now:a.acceptedAt});
  if(request.action!=='Reserve') {
   assert.equal(a.request.transaction.raw,unsigned(response.raw),'wallet signed different transaction');
   assert.equal(a.request.transaction.inputIndex,i);
   assert.deepEqual(a.request.transaction.parents,[request.source,request.source,response.funding]);
   assert.equal(a.request.intent.maxFee,500);
  }
 }
 if(request.action!=='Reserve') {
  const assembled=build(request,items.map(a=>a.response.transactionSignature));
  assert.equal(raw(assembled.tx),response.raw,'covenant signature assembly mismatch');
  assert.equal(raw(assembled.funding),response.funding);assert.equal(raw(assembled.fundingRoot),response.fundingRoot);
  assert.ok(assembled.result.success,'assembled Script failed');
 }
}
class IntegratedWallet {
 constructor(policy,authorize){this.policy=policy;this.authorize=authorize;this.mode='ok';this.calls=0;}
 async request(request) {
  this.calls++;assert.equal(request.network,this.policy.network);assert.equal(request.binding.buyerPubkey,this.policy.buyer);
  let payload={};const buyer=['Reserve','Open','Withdraw'].includes(request.action);
  const construction=request.action==='Reserve'?null:build(request);
  if(construction)payload={raw:raw(construction.tx),funding:raw(construction.funding),fundingRoot:raw(construction.fundingRoot)};
  const response={network:this.policy.network,requestHash:sha(canonical(request)),signer:buyer?this.policy.buyer:this.policy.seller,...payload};
  if(!buyer){assert.ok(construction.result.success);return {...response,signature:sign(canonical(response),seller)};}
  const authorizations=[];
  for(let i=0;i<(construction?2:1);i++) {
   const r=prepared(request,this.policy.wallet,i,construction),hash=A.requestHash(r);
   const result=await this.authorize(r,hash,this.mode);
   const acceptedAt=Date.now();A.verifyResponse(r,result,this.policy.wallet,{now:acceptedAt});
   authorizations.push({request:r,response:result,acceptedAt});
  }
  if(construction){const assembled=build(request,authorizations.map(a=>a.response.transactionSignature));assert.ok(assembled.result.success);response.raw=raw(assembled.tx);}
  return {...response,authorizations};
 }
}
async function fixtureWallet(authorize) {
 const f=await require('../wallet-transport/fixture').fixture();
 const policy={...F.policy,buyer:f.policy.signingKey,wallet:{network:f.policy.network,identityKey:f.policy.identityKey,signingKey:f.policy.signingKey}};
 const wallet=new IntegratedWallet(policy,authorize|| (async(r,hash,mode)=>{
  const provider={...f.provider};
  if(mode==='reject')provider.createSignature=async()=>{throw Error('fixture rejection');};
  if(mode==='wrong-network')provider.getNetwork=async()=>({network:'mainnet'});
  if(mode==='wrong-buyer')provider.getPublicKey=async()=>({publicKey:F.policy.buyer});
  if(mode==='malicious')provider.createSignature=async()=>({signature:[0]});
  const adapter=new A.WalletTransport(provider,{...f.policy,allowSigning:true});
  if(mode==='disconnect')adapter.disconnect();
  return adapter.request(r,{expectedRequestHash:hash});
 }));
 wallet.fixture=f;return wallet;
}
module.exports={IntegratedWallet,fixtureWallet,verifyAuthorizations,build,unsigned};
