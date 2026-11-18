'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {SigningBridge}=require('./signing-bridge');
const {createFixtureProvider}=require('./browser-wallet-fixture');
const {YoursTransport}=require('./wallet');
const {verify}=require('./browser-wallet-crypto');
const hash='11'.repeat(32);
async function setup(){const f=createFixtureProvider(),t=new YoursTransport({wallet:f.wallet,network:'test',verify}),session=await t.connect(),b=new SigningBridge({timeoutMs:500});b.connect(session);return {f,t,b,r:{key:'request-1',action:'Reserve',binding:{buyerPubkey:session.publicKey},full:{nested:['retained',1]}}};}
test('no unsolicited or pre-consent signature; exact request and one-shot response',async()=>{
 const {t,b,r}=await setup();assert.throws(()=>b.signHash(hash),/active action/);assert.throws(()=>b.respond({}),/pending/);
 await b.withRequest(r,async()=>{const promise=b.signHash(hash),envelope=b.peek(),signature=await t.signHash(hash);
 assert.throws(()=>b.respond({envelope,signature}),/approval/);
 for(const wrong of [{...envelope,id:'other'},{...envelope,generation:0},{...envelope,action:'Withdraw'},{...envelope,key:'other'},{...envelope,hash:'22'.repeat(32)},{...envelope,request:{...r,full:{nested:['changed']}}},{...envelope,session:{...envelope.session,publicKey:'other'}}])assert.throws(()=>b.approve(wrong),/Wrong/);
 b.approve(envelope);assert.throws(()=>b.approve(envelope),/Already/);assert.throws(()=>b.respond({envelope,signature:'3006020101020101'}),/Invalid signature/);
 b.respond({envelope,signature});assert.equal(await promise,signature);assert.throws(()=>b.respond({envelope,signature}),/pending/);
 });
});
test('disconnect invalidates in-flight result and generation',async()=>{
 const {t,b,r}=await setup();await b.withRequest(r,async()=>{const promise=b.signHash(hash),envelope=b.peek(),signature=await t.signHash(hash);const rejection=assert.rejects(promise,/disconnected/);b.invalidate();await rejection;assert.throws(()=>b.respond({envelope,signature}),/pending/);});
});
test('consent timeout clears session; wrong buyer refused',async()=>{
 const {b,r}=await setup();assert.rejects(b.withRequest({...r,binding:{buyerPubkey:'other'}},async()=>{}),/Buyer/);
 await assert.rejects(b.withRequest(r,()=>b.signHash(hash)),/timed out/);assert.equal(b.session,null);
});
