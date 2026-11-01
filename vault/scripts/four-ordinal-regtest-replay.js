'use strict'
// Offline cross-check of the actual saved node run; never starts a node.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict')
const M=require('../src/four-ordinal-sponsored')
const dir=process.argv[2];assert.ok(dir,'evidence directory required')
const read=name=>fs.readFileSync(path.join(dir,name),'utf8')
const rows=read('rpc.jsonl').trim().split('\n').map(JSON.parse),parents=[]
for(const r of rows){
 if(r.method==='getrawtransaction'&&!r.response.error){
  const v=r.response.result,t=new M.bsv.Transaction(typeof v==='string'?v:v.hex)
  if(!parents.some(p=>p.id===t.id))parents.push(t)
 }
}
const result=JSON.parse(read('result.json'));assert.equal(result.status,'PASS')
let accepted=0,rejected=0,totalFees=0
for(const o of result.outcomes){
 const t=new M.bsv.Transaction(read(o.name+'.hex').trim()),v=M.verify(t,parents)
 assert.equal(t.id,o.txid)
 assert.equal(v.success,!!o.mempool,o.name+JSON.stringify(v))
 if(o.mempool){
  accepted++
  const incoming=t.inputs.reduce((n,i)=>n+parents.find(p=>p.id===i.prevTxId.toString('hex')).outputs[i.outputIndex].satoshis,0)
  totalFees+=incoming-t.outputs.reduce((n,o)=>n+o.satoshis,0)
 }else{rejected++;assert.equal(o.allInputsLiveBeforeAndAfter,true)}
}
assert.equal(accepted,16);assert.equal(rejected,20)
assert.equal(totalFees,Object.values(result.feeTotals).reduce((a,b)=>a+b,0))
assert.equal(JSON.parse(read('shutdown.json')).ownedProcessAbsent,true)
console.log(JSON.stringify({accepted,rejected,totalFees,storedSerializedReplay:'PASS'}))
