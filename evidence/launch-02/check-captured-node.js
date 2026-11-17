'use strict'
// Cross-check historical RPC capture; DOES NOT contact or start a node.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict')
const root=path.resolve(__dirname,'../..'),base=path.join(root,'.audit-sources/bundle')
const M=require(path.join(base,'vault/src/four-ordinal-sponsored'))
const dir=path.join(base,'evidence/four-ordinal-sponsored/regtest-run-1')
const rows=fs.readFileSync(path.join(dir,'rpc.jsonl'),'utf8').trim().split('\n').map(JSON.parse)
const parents=new Map();for(const r of rows)if(r.method==='getrawtransaction'&&!r.response.error){const v=r.response.result,t=new M.bsv.Transaction(typeof v==='string'?v:v.hex);parents.set(t.id,t)}
let accepted=0,rejected=0,fees=0,probes=0
for(let pos=0;pos<rows.length;pos++){
 const r=rows[pos];if(r.method!=='sendrawtransaction')continue
 const raw=r.params[0],tx=new M.bsv.Transaction(raw),valid=!r.response.error
 assert.equal(M.verify(tx,[...parents.values()]).success,valid)
 if(valid){
  assert.equal(r.response.result,tx.id);accepted++
  fees+=tx.inputs.reduce((sum,i)=>sum+parents.get(i.prevTxId.toString('hex')).outputs[i.outputIndex].satoshis,0)-tx.outputs.reduce((sum,o)=>sum+o.satoshis,0)
  const detail=rows.slice(pos+1).find(r=>r.method==='getrawtransaction'&&r.params[0]===tx.id&&r.response.result?.confirmations>0)?.response.result
  assert.ok(detail);assert.equal(detail.hex,raw)
  const block=rows.slice(pos+1).find(r=>r.method==='getblock'&&r.params[0]===detail.blockhash)?.response.result
  assert.ok(block.tx.includes(tx.id))
 }else{
  rejected++;assert.equal(r.response.error.code,-26);assert.match(r.response.error.message,/mandatory-script/)
  for(const input of tx.inputs){
   const matches=r=>r.method==='gettxout'&&r.params[0]===input.prevTxId.toString('hex')&&r.params[1]===input.outputIndex
   const before=rows.slice(0,pos).filter(matches).at(-1),after=rows.slice(pos+1).find(matches)
   assert.ok(before?.response.result&&after?.response.result)
   const out=parents.get(input.prevTxId.toString('hex')).outputs[input.outputIndex]
   for(const p of [before,after]){assert.equal(Math.round(p.response.result.value*1e8),out.satoshis);assert.equal(p.response.result.scriptPubKey.hex,out.script.toHex());probes++}
  }
 }
}
const tx=new M.bsv.Transaction(fs.readFileSync(path.join(dir,'withdraw.hex'),'utf8').trim())
for(let i=0;i<5;i++){
 const u=rows.filter(r=>r.method==='gettxout'&&r.params[0]===tx.id&&r.params[1]===i).at(-1).response.result
 assert.equal(Math.round(u.value*1e8),1);assert.equal(u.scriptPubKey.hex,tx.outputs[i].script.toHex());assert.ok(u.confirmations>=1)
}
assert.equal(accepted,16);assert.equal(rejected,20);assert.equal(fees,8500)
assert.ok(rows.some(r=>r.method==='verifychain'&&r.response.result===true))
console.log(JSON.stringify({historicalCaptureCrossCheck:'PASS',accepted,rejected,fees,unspentBeforeAfterProbeChecks:probes,finalPrincipalOutputs:5,liveNodeStarted:false},null,2))
