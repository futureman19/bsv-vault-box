'use strict'
// Deterministic, entirely offline fixtures. Public test keys 1/2: NEVER FUND.
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict')
const M=require('../src/ordinal-pair')
const f=M.fixture(),entries=[],fundingParents=[]
let source,owner=f.alice
const actions=[0,1,...Array(12).fill(2),3,4]
for(const [index,action] of actions.entries()) {
 const buyer=action===2?(owner===f.alice?f.bob:f.alice):owner
 const r=M.transition(f,source,action,owner,buyer.publicKey.toString(),null,undefined,{sponsor:f.bob,funding:100000,fee:500})
 owner=buyer
 assert.equal(r.result.success,true,JSON.stringify(r.result))
 assert.equal(M.verify(r.funding,[r.fundingRoot]).success,true)
 const calls=r.tx.inputs.slice(action===0?1:0,2).map(input=>M.C.abiCoder.parseCallData(input.script.toHex()).args)
 const parentCommitmentBytes=calls.map(args=>args.find(a=>a.name==='parent').value.length/2)
 assert.ok(parentCommitmentBytes.every(n=>n===32))
 const fundingPrefixBytes=calls.map(args=>args.find(a=>a.name==='fundingPrefix').value.length/2)
 assert.ok(fundingPrefixBytes.every(n=>n<=155))
 entries.push({index,action,txid:r.tx.id,bytes:r.tx.toBuffer().length,inputScriptBytes:r.tx.inputs.map(i=>i.script.toBuffer().length),parentCommitmentBytes,fundingPrefixBytes,fee:500,fundingBytes:r.funding.toBuffer().length,raw:r.tx.uncheckedSerialize(),fundingRaw:r.funding.uncheckedSerialize(),fundingRootRaw:r.fundingRoot.uncheckedSerialize()})
 fundingParents.push(r.funding);source=r.tx
}
const history=M.verifyHistory(f,entries.map(e=>new M.bsv.Transaction(e.raw)),fundingParents)
assert.equal(history.valid,true)
const transferSizes=entries.filter(e=>e.action===2).map(e=>e.bytes)
assert.ok(Math.max(...transferSizes)-Math.min(...transferSizes)<64)
assert.ok(Math.max(...transferSizes)<30000)
const summary={history,transitions:entries.length,transferSizes,transferMinimum:Math.min(...transferSizes),transferMaximum:Math.max(...transferSizes),custodyHistoryBytes:entries.reduce((n,e)=>n+e.bytes,0),fundingParentHistoryBytes:entries.reduce((n,e)=>n+e.fundingBytes,0),measurements:entries.map(({index,action,bytes,inputScriptBytes,parentCommitmentBytes,fundingPrefixBytes,fundingBytes,fee})=>({index,action,bytes,inputScriptBytes,parentCommitmentBytes,fundingPrefixBytes,fundingBytes,fee}))}
const result={schema:'BOX-ORDINAL-PAIR-1-DRAFT-SPONSORED-BOUNDED',synthetic:true,broadcast:false,testScalars:[1,2],feeCap:10000,foreignRaw:f.foreign.uncheckedSerialize(),emptyBoxRaw:f.box.uncheckedSerialize(),contractArtifactSha256:crypto.createHash('sha256').update(JSON.stringify(JSON.parse(fs.readFileSync('artifacts/ordinalPair.json','utf8')))).digest('hex'),summary,entries}
const path='fixtures/ordinal-sponsored-vectors.json',serialized=JSON.stringify(result,null,2)+'\n'
if(process.argv.includes('--write')) fs.writeFileSync(path,serialized)
else assert.equal(fs.readFileSync(path,'utf8').replace(/\r\n/g,'\n'),serialized,'deterministic sponsored vectors drifted')
console.log(JSON.stringify(summary,null,2))
