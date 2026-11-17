"use strict";
// Deliberately RED security acceptance tests against the reviewed parent.
// No network, key files, node process, or broadcast. Public deterministic fixture.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {TransferWorker} = require('../../mint/transfer');
const {classify} = require('../../mint/recovery');
const {fixture} = require('../../vault/tests/launch-fixture');
const {verifyLaunch} = require('../../vault/src/launch-record');
const base = path.join(__dirname, '../contracts');
const seed = {
 id:'box-1', saleText:fs.readFileSync(path.join(base,'fixture-sales.jsonl'),'utf8'),
 poolText:fs.readFileSync(path.join(base,'fixture-pool.jsonl'),'utf8'),
 sponsorPubkey:'02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5',
 observations:[], depth:2
};
const initial = () => JSON.parse(seed.saleText);
const lines = rows => rows.map(JSON.stringify).join('\n')+'\n';
test('CONTROL: authentic saved transfer is classified and always quarantined',()=>{
 const r=classify(seed); assert.equal(r.classification,'UNCERTAIN_SEND');
 assert.equal(r.quarantined,true); assert.equal(r.mayResume,false);
});
test('S-01: reject erased historical inclusion instead of reporting BUILT',()=>{
 const prior=initial(); prior.box.state='TRANSFERRED'; prior.box.transfer.stage='INCLUDED';
 const later=structuredClone(prior); later.box.transfer.stage='BUILT'; later.box.state='PAID_PENDING';
 const r=classify({...seed,saleText:lines([prior,later]), observations:[{txid:prior.box.transfer.txid,raw:prior.box.transfer.raw,confirmations:0}]});
 assert.equal(r.mayResume,false); assert.equal(r.quarantined,true);
 assert.ok(['INCONSISTENT','FINALITY_LOST'].includes(r.classification),JSON.stringify(r));
});
test('S-01: reject erased monotonic reconciliation hold',()=>{
 const prior=initial(); prior.box.reconciliationRequired=true; prior.box.reconciliationReasons=['PAYMENT_FINALITY_LOST'];
 const later=structuredClone(prior); later.box.reconciliationRequired=false; later.box.reconciliationReasons=[];
 const r=classify({...seed,saleText:lines([prior,later])});
 assert.ok(r.classification==='INCONSISTENT'||r.reconciliationRequired===true,JSON.stringify(r));
});
const tx=initial().box.transfer;
const blockhash='ab'.repeat(32);
function worker(block){
 const w=Object.create(TransferWorker.prototype); w.depth=2;
 w.rpc=async method=>{
  if(method==='getrawtransaction')return {hex:tx.raw,confirmations:3,blockhash};
  if(method==='getblock')return block;
  throw Error('Unexpected RPC '+method);
 };
 return w;
}
test('CONTROL: consistent deep block membership accepted',async()=>{
 assert.equal(await worker({hash:blockhash,confirmations:3,tx:[tx.txid]}).included(tx.txid,tx.raw),true);
});
for(const [name,block] of [
 ['block below required depth',{hash:blockhash,confirmations:1,tx:[tx.txid]}],
 ['mismatched block identity',{hash:'cd'.repeat(32),confirmations:3,tx:[tx.txid]}],
 ['noninteger block confirmation',{hash:blockhash,confirmations:0.5,tx:[tx.txid]}]
])test('S-02: reject '+name,async()=>{
 let accepted=false;
 try{accepted=await worker(block).included(tx.txid,tx.raw);}catch{}
 assert.equal(accepted,false);
});
test('CONTROL: absent block membership rejected',async()=>{
 assert.equal(await worker({hash:blockhash,confirmations:3,tx:[]}).included(tx.txid,tx.raw),false);
});
const p=fixture();
test('CONTROL: valid external-policy launch record accepted',()=>{
 assert.equal(verifyLaunch(p).originalIssuanceProvenance,true);
});
test('S-03: exact envelope schema rejects inherited signature and unexpected own field',()=>{
 const envelope=Object.assign(Object.create({signature:p.envelope.signature}),{statement:p.envelope.statement,issuer:p.envelope.issuer,extra:'unexpected'});
 assert.equal(verifyLaunch({...p,envelope}).originalIssuanceProvenance,false);
});
