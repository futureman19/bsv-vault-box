'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const {YoursTransport}=require('./wallet');
const {M,sha}=require('../continuous/common');
const key=new M.bsv.PrivateKey(new M.bsv.crypto.BN(2),M.bsv.Networks.testnet),pub=key.publicKey.toString();
function provider(){return {waitForAuthentication:async()=>({authenticated:true}),getNetwork:async()=>({network:'test'}),getPublicKey:async()=>({publicKey:pub}),createSignature:async args=>({signature:[...M.bsv.crypto.ECDSA.sign(Buffer.from(args.hashToDirectlySign),key).toDER()]})};}
function verify(hash,sig,p){try{return M.bsv.crypto.ECDSA.verify(Buffer.from(hash,'hex'),M.bsv.crypto.Signature.fromDER(Buffer.from(sig)),M.bsv.PublicKey.fromString(p));}catch{return false;}}
const make=p=>new YoursTransport({wallet:p,network:'test',verify,timeoutMs:100});
test('real BRC100 wire shape signs exact digest with derived key, no action or broadcast',async()=>{
 const p=provider(),calls=[];const sign=p.createSignature;p.createSignature=async a=>{calls.push(a);return sign(a);};
 p.createAction=()=>assert.fail('must not construct/broadcast wallet actions');
 const w=make(p),session=await w.connect();assert.equal(session.publicKey,pub);assert.equal(session.identityKey,pub);
 const hash=sha('request');assert.ok(await w.signHash(hash));assert.equal(calls.length,1);assert.deepEqual(calls[0].hashToDirectlySign,[...Buffer.from(hash,'hex')]);assert.equal(calls[0].counterparty,'self');assert.equal(calls[0].data,undefined);
});
for(const mutation of ['reject','network','identity','malformed','wrong-signature'])test('rejects '+mutation+' without accepting a signature',async()=>{
 const p=provider(),w=make(p);await w.connect();
 if(mutation==='reject')p.createSignature=async()=>({error:'user-rejected'});
 if(mutation==='network')p.getNetwork=async()=>({network:'main'});
 if(mutation==='identity')p.getPublicKey=async()=>({publicKey:new M.bsv.PrivateKey(new M.bsv.crypto.BN(4)).publicKey.toString()});
 if(mutation==='malformed')p.createSignature=async()=>({signature:[NaN]});
 if(mutation==='wrong-signature')p.createSignature=async()=>({signature:[...M.bsv.crypto.ECDSA.sign(Buffer.from(sha('other'),'hex'),key).toDER()]});
 await assert.rejects(w.signHash(sha('request')));assert.equal(w.session,null);
});
test('disconnect fences late signing result and duplicates are busy-rejected',async()=>{
 const p=provider(),w=make(p);await w.connect();let release,started;
 const ready=new Promise(r=>started=r),original=p.createSignature;
 p.createSignature=async a=>{started();await new Promise(r=>release=r);return original(a);};
 const signing=w.signHash(sha('cancel'));await ready;await assert.rejects(w.signHash(sha('duplicate')),/busy/);w.cancel();release();await assert.rejects(signing,/cancelled/);assert.equal(w.session,null);
});
test('hung provider times out and needs explicit reconnection',async()=>{
 const p=provider(),w=make(p);await w.connect();p.createSignature=()=>new Promise(()=>{});await assert.rejects(w.signHash(sha('timeout')),/timed out/);assert.equal(w.session,null);assert.equal(w.busy,false);
});
test('identity switched during signature invalidates otherwise authentic DER',async()=>{
 const p=provider(),w=make(p);await w.connect();const original=p.createSignature;p.createSignature=async a=>{const result=await original(a);p.getPublicKey=async()=>({publicKey:new M.bsv.PrivateKey(new M.bsv.crypto.BN(4)).publicKey.toString()});return result;};
 await assert.rejects(w.signHash(sha('switch')),/identity/);
});
module.exports={provider,verify,pub};
