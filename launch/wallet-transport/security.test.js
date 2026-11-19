'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {fixture,bsv}=require('./fixture');
const {WalletTransport,requestHash,verifyResponse}=require('./adapter');
async function setup(options={}) {const f=await fixture();f.adapter=new WalletTransport(f.provider,{...f.policy,...options});return f;}
const sign=f=>f.adapter.request(f.request,{expectedRequestHash:requestHash(f.request)});
test('SDK-derived signature spends exact fixture transaction; envelope verifies',async()=>{
 const f=await setup(),r=await sign(f);assert.equal(verifyResponse(f.request,r,f.policy),true);
 const sig=bsv.crypto.Signature.fromTxFormat(Buffer.from(r.transactionSignature,'hex'));
 assert.equal(bsv.Transaction.sighash.verify(f.transaction,sig,bsv.PublicKey.fromString(f.policy.signingKey),0,f.parent.outputs[0].script,new bsv.crypto.BN(1000)),true);
 assert.equal(r.kind,'VERIFIED_SIGNATURES_NOT_SENT');assert.equal(f.calls.filter(x=>x[0]==='createSignature').length,2);
});
test('disabled signing makes no calls',async()=>{const f=await setup({allowSigning:false});await assert.rejects(sign(f),/SIGNING_DISABLED/);assert.equal(f.calls.length,0);});
test('send always disabled',async()=>{const f=await setup();assert.throws(()=>f.adapter.send('00'),/SEND_DISABLED/);});
test('trusted request hash required',async()=>{const f=await setup();await assert.rejects(f.adapter.request(f.request,{}),/REQUEST_HASH/);assert.equal(f.calls.length,0);});
test('Reserve signs binding only',async()=>{const f=await setup();f.request.action='Reserve';delete f.request.transaction;delete f.request.intent;const r=await sign(f);assert.equal(verifyResponse(f.request,r,f.policy),true);assert.equal(f.calls.filter(x=>x[0]==='createSignature').length,1);});
for(const [name,mutate,pattern] of [
 ['network',f=>{f.provider.getNetwork=async()=>({network:'mainnet'});},/NETWORK/],
 ['identity',f=>{f.provider.getPublicKey=async()=>({publicKey:f.policy.signingKey});},/IDENTITY/],
 ['signing key',f=>{const original=f.provider.getPublicKey;f.provider.getPublicKey=async a=>a.identityKey?original(a):({publicKey:f.policy.identityKey});},/SIGNING_KEY/],
 ['authentication',f=>{f.provider.waitForAuthentication=async()=>({authenticated:false});},/AUTH/],
 ['provider rejection',f=>{f.provider.createSignature=async()=>{throw Error('user-rejected');};},/PROVIDER_ERROR/],
 ['malformed signature',f=>{f.provider.createSignature=async()=>({signature:[1,2,3]});},/SIGNATURE/],
 ['action error',f=>{f.provider.createSignature=async()=>({error:'user-rejected',signature:[1]});},/PROVIDER_ERROR/],
 ['wrong key',f=>{const {ProtoWallet,PrivateKey}=require('@bsv/sdk');f.provider.createSignature=a=>new ProtoWallet(new PrivateKey(3)).createSignature(a);},/SIGNATURE/],
 ['extra response fields',f=>{const original=f.provider.createSignature;f.provider.createSignature=async a=>({...await original(a),txid:'ab'});},/RESPONSE_SHAPE/],
 ['wrong parent',f=>{f.request.transaction.parents[0]=f.request.transaction.raw;},/PARENT/],
 ['output diversion',f=>{f.request.intent.outputs[0].satoshis=899;},/OUTPUT/],
 ['excess fee',f=>{f.request.intent.maxFee=99;},/FEE/],
 ['expired',f=>{f.request.expiresAt=Date.now()-1;},/EXPIRED/],
 ['unknown action',f=>{f.request.action='Reseal';},/ACTION/],
 ['extra fields',f=>{f.request.send=true;},/REQUEST_SHAPE/]
]) test('rejects '+name,async()=>{const f=await setup();mutate(f);await assert.rejects(sign(f),pattern);});
test('request IDs cannot replay',async()=>{const f=await setup();await sign(f);const n=f.calls.length;await assert.rejects(sign(f),/REPLAY/);assert.equal(f.calls.length,n);});
test('disconnect discards late signature',async()=>{const f=await setup();const original=f.provider.createSignature;let release,started;const gate=new Promise(r=>release=r),ready=new Promise(r=>started=r);f.provider.createSignature=async a=>{started();await gate;return original(a);};const p=sign(f);await ready;f.adapter.disconnect();await assert.rejects(p,/DISCONNECTED/);release();await assert.rejects(sign(f),/DISCONNECTED/);});
test('abort cancels a hung request locally',async()=>{const f=await setup();f.provider.waitForAuthentication=()=>new Promise(()=>{});const c=new AbortController(),p=f.adapter.request(f.request,{expectedRequestHash:requestHash(f.request),signal:c.signal});c.abort();await assert.rejects(p,/CANCELLED/);});
test('timeout and single flight',async()=>{const f=await setup({timeoutMs:30});f.provider.waitForAuthentication=()=>new Promise(()=>{});const p=sign(f);await assert.rejects(sign(f),/BUSY/);await assert.rejects(p,/TIMEOUT/);});
test('network switch after signing rejects',async()=>{const f=await setup();const original=f.provider.createSignature;f.provider.createSignature=async a=>{const r=await original(a);f.provider.getNetwork=async()=>({network:'mainnet'});return r;};await assert.rejects(sign(f),/NETWORK/);});
test('response tamper and cross-request substitution',async()=>{const f=await setup(),r=await sign(f);for(const field of ['requestHash','signature','transactionSignature'])assert.throws(()=>verifyResponse(f.request,{...r,[field]:'00'},f.policy));const changed=structuredClone(f.request);changed.binding.designId='japan';assert.throws(()=>verifyResponse(changed,r,f.policy),/REQUEST_HASH/);});
test('sparse arrays are rejected before serialization',()=>{assert.throws(()=>requestHash({a:new Array(2)}),/REQUEST_ARRAY/);});
test('buyer actions reject a different bound owner before any provider call',async()=>{const f=await setup();f.request.binding.buyerPubkey=f.policy.identityKey;await assert.rejects(sign(f),/BUYER/);assert.equal(f.calls.length,0);});
test('response accessors are rejected without invoking them',async()=>{const f=await setup();let touched=false;f.provider.createSignature=async()=>Object.defineProperty({},'error',{enumerable:true,get(){touched=true;return 'evil';}});await assert.rejects(sign(f));assert.equal(touched,false);});
test('default policy disables signing',async()=>{const f=await fixture();delete f.policy.allowSigning;f.adapter=new WalletTransport(f.provider,f.policy);await assert.rejects(sign(f),/SIGNING_DISABLED/);assert.equal(f.calls.length,0);});
test('caller mutation cannot alter signed snapshot',async()=>{const f=await setup(),hash=requestHash(f.request),originalRequest=structuredClone(f.request);const original=f.provider.waitForAuthentication;f.provider.waitForAuthentication=async a=>{f.request.transaction.raw='00';return original(a);};const r=await f.adapter.request(f.request,{expectedRequestHash:hash});assert.equal(verifyResponse(originalRequest,r,f.policy),true);});
