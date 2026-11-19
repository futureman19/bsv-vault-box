'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {DatabaseSync}=require('node:sqlite');
const {createPaid}=require('./paid');
const cases={
 loss:{payment:{satoshis:0,confirmations:0,refs:[]},hold:'PAYMENT_FINALITY_LOST'},
 depth:{payment:{satoshis:100,confirmations:1},hold:'PAYMENT_FINALITY_LOST'},
 receipts:{payment:{satoshis:100,confirmations:2,refs:['ab'.repeat(32)+':0']},hold:'PAYMENT_RECEIPTS_CHANGED'},
 excess:{payment:{satoshis:101,confirmations:2},hold:'EXCESS_PAYMENT'},
 unavailable:{payment:null,hold:'PAYMENT_OBSERVATION_UNAVAILABLE'}
};
for(const action of ['Open','Withdraw'])for(const recovery of [false,true])for(const [name,c] of Object.entries(cases))test(`${action} ${recovery?'prepared recovery':'signing race'} ${name}: durable hold, zero sends, exact prepared bytes`,async()=>{
 const dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));let e;const hooks={};
 try{
  e=await createPaid(dir,{hooks});await e.reserve('reserve-finality');await e.advance('pack-finality','Pack');await e.advance('seal-finality','Seal');await e.pay();
  if(action==='Withdraw')await e.advance('open-finality','Open');
  const prior=e.inspect(),key='guard-'+action;
  const mutate=()=>{const db=new DatabaseSync(path.join(dir,'authorizations.sqlite'));try{db.prepare('UPDATE fixture_payment SET payload=? WHERE id=1').run(JSON.stringify(c.payment===null?null:{...prior.delivery.payment,...c.payment}));}finally{db.close();}};
  let prepared;
  if(recovery){
   hooks.afterPrepared=()=>{throw Error('prepared crash');};await assert.rejects(e.advance(key,action),/prepared crash/);prepared=e.inspect().pending.response.raw;
   e.close();e=await createPaid(dir);
   // Lose finality after the initial pre-action observation, before resumed ATTEMPT.
   const read=e.payment.read;let reads=0;e.payment.read=async(...args)=>{const p=await read(...args);if(++reads===1)mutate();return p;};
  }else{
   const authorize=e.wallet.authorize;e.wallet.authorize=async(...args)=>{const response=await authorize(...args);if(args[0].action===action)mutate();return response;};
  }
  const sent=e.transport.sent.length;
  await assert.rejects(e.advance(key,action),/reconciliation hold/);
  const after=e.inspect();assert.equal(after.stage,prior.stage);assert.deepEqual(after.history,prior.history);assert.ok(after.holds.includes(c.hold));assert.equal(e.transport.sent.length,sent);assert.equal(after.pending.attempted,false);
  if(prepared)assert.equal(after.pending.response.raw,prepared);prepared=after.pending.response.raw;
  const authCount=after.authorizations.length;e.close();e=await createPaid(dir);
  await assert.rejects(e.advance(key,action),/reconciliation hold/);assert.equal(e.transport.sent.length,0);assert.equal(e.inspect().pending.response.raw,prepared);assert.equal(e.inspect().authorizations.length,authCount);assert.equal(e.inspect().stage,prior.stage);
 }finally{if(e)e.close();fs.rmSync(dir,{recursive:true,force:true});}
});
