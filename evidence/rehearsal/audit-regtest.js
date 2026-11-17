"use strict";
// Offline raw-byte/RPC cross-check; no regeneration, keys or chain connections.
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const M=require('../../vault/src/ordinal-pair');
const dir=path.resolve(process.argv[2]||'evidence/rehearsal/regtest');
const json=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const rows=fs.readFileSync(path.join(dir,'rpc.jsonl'),'utf8').trim().split(/\r?\n/).map(JSON.parse);
const transactions=new Map();
for(const r of rows){
 const v=r.response?.result;
 if(r.method==='getrawtransaction'&&v){const t=new M.bsv.Transaction(typeof v==='string'?v:v.hex);transactions.set(t.id,t);}
 if(r.method==='sendrawtransaction'){const t=new M.bsv.Transaction(r.params[0]);transactions.set(t.id,t);}
}
const load=n=>new M.bsv.Transaction(fs.readFileSync(path.join(dir,n+'.hex'),'utf8').trim());
const stages=['deposit','seal','transfer','buyer-open','buyer-withdraw'];
const f={foreign:load('inscription'),box:load('empty-box')};
const parents=Array.from({length:6},(_,i)=>load('prep-'+(i+2)));
const chain=stages.map(load);let fees=0;
for(let i=0;i<chain.length;i++){
 const t=chain[i], prev=t.inputs.map(x=>{const p=transactions.get(x.prevTxId.toString('hex'));assert.ok(p);return p});
 assert.equal(M.verify(t,prev).success,true);
 assert.equal(M.verifyHistory(f,chain.slice(0,i+1),parents).valid,true);
 const fee=t.inputs.reduce((n,x,j)=>n+prev[j].outputs[x.outputIndex].satoshis,0)-t.outputs.reduce((n,x)=>n+x.satoshis,0);assert.equal(fee,500);fees+=fee;
 assert.ok(rows.some(r=>r.method==='sendrawtransaction'&&r.params[0]===t.uncheckedSerialize()&&r.response?.result===t.id));
 const details=rows.filter(r=>r.method==='getrawtransaction'&&r.params[0]===t.id&&r.response?.result?.confirmations>0);
 assert.ok(details.length);
 for(const d of details){assert.equal(d.response.result.hex,t.uncheckedSerialize());assert.ok(rows.some(r=>r.method==='getblock'&&r.params[0]===d.response.result.blockhash&&r.response?.result?.tx.includes(t.id)));}
}
let prepFees=0;for(const t of parents){const prev=t.inputs.map(x=>transactions.get(x.prevTxId.toString('hex')));assert.equal(M.verify(t,prev).success,true);prepFees+=t.inputs.reduce((n,x,i)=>n+prev[i].outputs[x.outputIndex].satoshis,0)-t.outputs.reduce((n,x)=>n+x.satoshis,0);}
const attack=load('old-owner-open'),index=rows.findIndex(r=>r.method==='sendrawtransaction'&&r.params[0]===attack.uncheckedSerialize());assert.ok(index>0);
const error=rows[index].response.error;assert.equal(error.code,-26);assert.match(error.message,/mandatory-script-verify-flag-failed/);
assert.equal(M.verify(attack,attack.inputs.map(x=>transactions.get(x.prevTxId.toString('hex')))).success,false);
for(const input of attack.inputs.slice(0,2)){
 const match=r=>r.method==='gettxout'&&r.params[0]===input.prevTxId.toString('hex')&&r.params[1]===input.outputIndex;
 assert.ok(rows.slice(0,index).filter(match).at(-1).response.result);
 assert.ok(rows.slice(index+1).find(match).response.result);
}
const last=chain.at(-1);const final=[];
for(let i=0;i<2;i++){const u=rows.filter(r=>r.method==='gettxout'&&r.params[0]===last.id&&r.params[1]===i).at(-1).response.result;assert.equal(u.value,1e-8);assert.equal(u.scriptPubKey.hex,last.outputs[i].script.toHex());final.push({outpoint:last.id+':'+i,satoshis:1,script:u.scriptPubKey.hex});}
assert.equal(json('shutdown.json').exitCode,0);
assert.ok(rows.some(r=>r.method==='verifychain'&&r.response?.result===true));
assert.ok(rows.some(r=>r.method==='getconnectioncount'&&r.response?.result===0));
for(const r of rows.filter(r=>r.method==='getblockchaininfo'&&r.response?.result))assert.equal(r.response.result.chain,'regtest');
console.log(JSON.stringify({status:'PASS',lifecycleTransactions:chain.length,sponsorPreparations:parents.length,custodyFeeSats:fees,sponsorPreparationFeeSats:prepFees,oldOwnerRejection:error,finalUTXOs:final,origin:f.foreign.id+'_0',scope:'Fresh node captures replayed offline; historical final unspent snapshot, not current public chain state.'},null,2));
