'use strict'
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict')
const M=require('../src/ordinal-pair'),f=M.fixture(),entries=[]
let parent
for(const action of [0,1,2,3,4]) {
 const r=M.transition(f,parent,action,action<3?f.alice:f.bob,f.bob.publicKey.toString())
 assert.equal(r.result.success,true)
 entries.push({action,txid:r.tx.id,raw:r.tx.uncheckedSerialize(),bytes:r.tx.toBuffer().length});parent=r.tx
}
const result={schema:'BOX-ORDINAL-PAIR-1-DRAFT',synthetic:true,broadcast:false,fees:0,sourceSpecCommit:'4f6d8d78d90acd807843cd254a9068586c793c20',origin:f.origin,foreignRaw:f.foreign.uncheckedSerialize(),emptyBoxRaw:f.box.uncheckedSerialize(),contractArtifactSha256:crypto.createHash('sha256').update(JSON.stringify(JSON.parse(fs.readFileSync('artifacts/ordinalPair.json','utf8')))).digest('hex'),entries,history:M.verifyHistory(f,entries.map(e=>new M.bsv.Transaction(e.raw)))}
const serialized=JSON.stringify(result,null,2)+'\n',path='fixtures/ordinal-pair-vectors.json'
if(process.argv.includes('--write')) fs.writeFileSync(path,serialized)
else assert.equal(fs.readFileSync(path,'utf8').replace(/\r\n/g,'\n'),serialized,'deterministic vectors drifted')
console.log(JSON.stringify({verified:result.history,transactions:entries.map(e=>({action:e.action,txid:e.txid,bytes:e.bytes}))},null,2))
