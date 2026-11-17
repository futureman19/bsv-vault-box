'use strict'
// Offline audit repro. No node process, HTTP, key loading, or broadcast.
const path=require('node:path'),fs=require('node:fs'),assert=require('node:assert/strict')
const root=path.resolve(__dirname,'../..'),funded=path.join(root,'.audit-sources/funded'),bundle=path.join(root,'.audit-sources/bundle')
const M=require(path.join(bundle,'vault/src/ordinal-pair'))
const {TransferWorker}=require(path.join(funded,'mint/transfer'))
const Canary=require(path.join(funded,'mint/canary'))
async function main(){
 const f=M.fixture(),entries=[];let source
 for(const action of [0,1,2,3]){const r=M.transition(f,source,action,action<3?f.alice:f.bob,f.bob.publicKey.toString());assert.equal(r.result.success,true);source=r.tx;entries.push(source)}
 const reseal=M.transition(f,source,1,f.bob)
 assert.equal(reseal.result.success,false)
 console.log('GAP-REUSE: opened -> seal rejected:',JSON.stringify(reseal.result))
 const original=M.verifyHistory(f,entries);assert.equal(original.valid,true)
 const foreign=new M.bsv.Transaction(fs.readFileSync(path.join(bundle,'vault/fixtures/primary-1sat-example.hex'),'utf8').trim())
 const art=M.verifyHistory({...f,foreign},[]);assert.equal(art.valid,false)
 console.log('GAP-ART: saved real model/gltf-binary inscription admission:',JSON.stringify(art))
 const raw=fs.readFileSync(path.join(funded,'evidence/mint-canary-funded-rehearsal/rehearsal/runner/transfer.hex'),'utf8').trim(),txid=new M.bsv.Transaction(raw).id
 let row={id:'audit',state:'PAID_PENDING',priceSats:1000,transfer:{stage:'SUBMITTED',txid,raw,attempts:1}}, paymentReads=0,inclusionReads=0,included=true
 // White-box persisted-state test deliberately bypasses constructor/key loading.
 // Real run(), guard(), checkCaps(), included() methods are exercised.
 const w=Object.create(TransferWorker.prototype);Canary.bind(w,{chain:'regtest'})
 Object.assign(w,{fee:500,depth:1,maxAttempts:3,retryMs:0,pool:{},store:{get:()=>structuredClone(row),update:(_,p)=>(row={...row,...p})},paymentTransport:{read:async()=>{paymentReads++;return {satoshis:0,confirmations:0}}},rpc:async(method)=>{
 if(method==='getblockchaininfo')return {chain:'regtest'}
 if(method==='getrawtransaction'){inclusionReads++;if(!included){const e=Error('missing');e.code=-5;throw e}return {hex:raw,confirmations:1,blockhash:'audit-block'}}
 if(method==='getblock')return {confirmations:1,tx:[txid]}
 throw Error('Forbidden/unexpected RPC: '+method)
 }})
 await w.run('audit');assert.equal(row.state,'TRANSFERRED');assert.equal(paymentReads,0)
 included=false;await w.run('audit');assert.equal(row.state,'TRANSFERRED');assert.equal(inclusionReads,1)
 console.log('F-01: payment disappeared but completion='+row.state+', payment reads='+paymentReads+'; later inclusion loss ignored (total inclusion reads='+inclusionReads+')')
 console.log('PASS: reproduced two explicit construction gaps and finality observation defect; no live chain claims')
}
main().catch(e=>{console.error(e);process.exitCode=1})
