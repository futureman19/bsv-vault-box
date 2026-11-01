'use strict'
// Offline only. No RPC client, keys, network, node startup, or production-site writes.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto')
const M=require('../../vault/src/four-ordinal-sponsored'),{bsv,C}=M
const stages=['pack','seal','transfer','open','withdraw']
const originals=['original-0','original-1-certificate','original-2','original-3','initial-control']
const roles=['collectible-box','certificate','object-one','object-two','control']
const labels=['Collectible Box','Certificate','Object one','Object two','Control']
// Public identity labels, not signing material. Trust policy is external to evidence.
const ALICE='0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798'
const BOB='02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5'
const ISSUER='02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9'
const sha=x=>crypto.createHash('sha256').update(x).digest('hex')
function safe(x){if(typeof x==='string')assert.ok(!/[<>\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(x),'unsafe string');else if(x&&typeof x==='object')for(const [k,v] of Object.entries(x)){safe(k);safe(v)}}
function inspect(dir){
 const files={},manifest=[]
 function read(name){const bytes=fs.readFileSync(path.join(dir,name));manifest.push({name,sha256:sha(bytes),bytes:bytes.length});files[name]=bytes.toString('utf8');return files[name]}
 function json(name){const v=JSON.parse(read(name));safe(v);return v}
 const identity=json('identity.json'),summary=json('result.json')
 const rpcText=fs.readFileSync(path.join(dir,'rpc.jsonl'),'utf8')
 const rows=rpcText.trim().split('\n').map(JSON.parse)
 const methods=new Set(['getrawtransaction','sendrawtransaction','getrawmempool','getblock','gettxout','getblockchaininfo','verifychain'])
 const selected=rows.filter(r=>methods.has(r.method));safe(selected)
 // Exact line bytes retained, not a reserialized imitation of the journal.
 files['rpc-subset.jsonl']=rpcText.split('\n').filter(l=>l.trim()&&methods.has(JSON.parse(l).method)).join('\n')+'\n'
 manifest.push({name:'rpc-subset.jsonl',sha256:sha(files['rpc-subset.jsonl']),bytes:Buffer.byteLength(files['rpc-subset.jsonl']),source:'rpc.jsonl',sourceSha256:sha(rpcText),selection:[...methods]})
 const query=(method)=>rows.filter(r=>r.method===method&&!r.response.error)
 const chain=query('getblockchaininfo').at(-1).response.result
 assert.equal(chain.chain,'regtest','chain');assert.deepEqual(summary.chain,chain,'chain summary')
 assert.ok(query('verifychain').some(r=>JSON.stringify(r.params)==='[4,0]'&&r.response.result===true),'recorded verifychain')
 const parents=query('getrawtransaction').map(r=>{const v=r.response.result,t=new bsv.Transaction(typeof v==='string'?v:v.hex);assert.equal(t.id,r.params[0],'RPC txid');if(typeof v==='object'){assert.equal(t.id,v.txid,'RPC decoded txid');v.vout.forEach((o,i)=>{assert.equal(Math.round(o.value*1e8),t.outputs[i].satoshis,'RPC value');assert.equal(o.scriptPubKey.hex,t.outputs[i].script.toHex(),'RPC script')})}return t})
 const names=fs.readdirSync(dir).filter(n=>n.endsWith('.hex')).sort()
 const txs=new Map(),byName={},sends=rows.filter(r=>r.method==='sendrawtransaction')
 assert.equal(names.length,sends.length,'RPC transaction count: missing or extra evidence');assert.equal(summary.outcomes.length,sends.length,'summary outcome count')
 for(const file of names){assert.match(file,/^[a-z0-9-]+\.hex$/,'unsafe filename');const raw=read(file).trim();assert.match(raw,/^(?:[a-f0-9]{2})+$/,'transaction hex');const t=new bsv.Transaction(raw);assert.ok(!txs.has(t.id),'duplicate transaction');txs.set(t.id,t);byName[file.slice(0,-4)]=t;assert.equal(sends.filter(r=>r.params[0]===raw).length,1,'RPC transaction bytes missing')}
 for(const name of [...originals,...stages])assert.ok(byName[name],'missing '+name)
 const blocks=query('getblock').map(r=>{assert.equal(r.params[0],r.response.result.hash,'block hash');return r.response.result})
 const records=[]
 for(const [name,t] of Object.entries(byName)){
  const idx=rows.findIndex(r=>r.method==='sendrawtransaction'&&r.params[0]===t.uncheckedSerialize()),r=rows[idx]
  assert.ok(r,'RPC transaction missing');const accepted=!r.response.error
  const o=summary.outcomes.find(o=>o.name===name);assert.ok(o,'summary outcome missing');assert.equal(o.txid,t.id,'summary txid');assert.equal(!!o.mempool,accepted,'summary acceptance')
  let fee=0,block=null
  if(accepted){
   assert.equal(r.response.result,t.id,'accepted txid');assert.ok(parents.some(p=>p.id===t.id),'RPC confirmed raw missing')
   block=blocks.find(b=>b.tx.includes(t.id));assert.ok(block&&block.confirmations>=1,'block membership missing');assert.equal(o.block,block.hash,'summary block');assert.equal(o.confirmations,block.confirmations,'summary confirmations')
   fee=t.inputs.reduce((n,i)=>{const p=parents.find(p=>p.id===i.prevTxId.toString('hex'));assert.ok(p&&p.outputs[i.outputIndex],'missing parent');return n+p.outputs[i.outputIndex].satoshis},0)-t.outputs.reduce((n,o)=>n+o.satoshis,0);assert.ok(fee>0,'fee')
  }else{
   assert.equal(r.response.error.code,-26,'RPC rejection');assert.match(r.response.error.message,/mandatory-script-verify-flag-failed/,'Script rejection');assert.deepEqual(o.rejection,r.response.error,'summary rejection')
   // Contiguous pre/post attack UTXO probes prove the claim in the captured journal.
   const before=rows.slice(idx-t.inputs.length,idx),after=rows.slice(idx+2,idx+2+t.inputs.length)
   for(const group of [before,after])t.inputs.forEach((input,i)=>{const q=group[i];assert.ok(q&&q.method==='gettxout'&&q.params[0]===input.prevTxId.toString('hex')&&q.params[1]===input.outputIndex&&q.response.result&&!q.response.error,'attack UTXO probe missing');const p=parents.find(p=>p.id===input.prevTxId.toString('hex')).outputs[input.outputIndex];assert.equal(Math.round(q.response.result.value*1e8),p.satoshis,'UTXO value');assert.equal(q.response.result.scriptPubKey.hex,p.script.toHex(),'UTXO script')})
  }
  records.push({name,txid:t.id,accepted,fee,block:block&&block.hash,rejection:r.response.error||null,bytes:t.toBuffer().length})
 }
 const assets=originals.map(n=>byName[n]),origins=assets.map(t=>t.id+'_0')
 assert.deepEqual(identity.origins,origins.slice(0,4),'identity origins');assert.equal(identity.control,origins[4],'control origin')
 const payloads=assets.slice(0,4).map(t=>{const m=/^76a914([a-f0-9]{40})88ac0063036f7264510a746578742f706c61696e00([a-f0-9]{2})([a-f0-9]*)68$/.exec(t.outputs[0].script.toHex());assert.ok(m,'tiny text inscription');assert.equal(parseInt(m[2],16)*2,m[3].length,'payload length');assert.equal(t.outputs[0].satoshis,1,'origin sat');assert.equal(m[1],bsv.crypto.Hash.sha256ripemd160(Buffer.from(ALICE,'hex')).toString('hex'),'original owner');const text=Buffer.from(m[3],'hex').toString('utf8');safe(text);return text})
 const cert=identity.certificate,statement=JSON.stringify({protocol:'BOX4-CERT-1',collectible:origins[0],objects:[origins[2],origins[3]]})
 assert.equal(cert.statement,statement,'certificate statement');assert.equal(cert.issuer,ISSUER,'external fixture issuer policy')
 assert.ok(bsv.crypto.ECDSA.verify(Buffer.from(sha(statement),'hex'),bsv.crypto.Signature.fromDER(Buffer.from(cert.signature,'hex')),bsv.PublicKey.fromString(ISSUER)),'certificate signature')
 assert.equal(payloads[1],sha(JSON.stringify({statement:cert.statement,issuer:cert.issuer,signature:cert.signature})),'certificate commitment')
 assert.equal(identity.manifest,JSON.stringify({protocol:'BOX4-MANIFEST-1',items:origins.slice(0,4).map((origin,i)=>({role:roles[i],origin}))}),'manifest origins')
 const initial=C.fromHex(assets[4].outputs[0].script.toHex());assert.equal(initial.phase,0n);assert.equal(initial.owner,ALICE);assert.equal(initial.ctorArgs().find(a=>a.name==='origins').value,M.origins(assets.slice(0,4)),'anchored origins')
 const history=stages.map((name,s)=>{
  const t=byName[name],owner=s<2?ALICE:BOB;assert.equal(t.inputs.length,6);assert.equal(t.outputs.length,6)
  for(let i=0;i<5;i++){assert.equal(t.inputs[i].prevTxId.toString('hex'),s?byName[stages[s-1]].id:assets[i].id,'ordered ancestry');assert.equal(t.inputs[i].outputIndex,s?i:0,'ordered output');assert.equal(t.outputs[i].satoshis,1,'protected sat');if(s<4){const c=C.fromHex(t.outputs[i].script.toHex());assert.equal(c.owner,owner,'state owner');assert.equal(Number(c.phase),[1,2,2,3][s],'state phase');assert.equal(c.ctorArgs().find(a=>a.name==='origins').value,M.origins(assets.slice(0,4)),'state origins')}else assert.equal(t.outputs[i].script.toHex(),M.pay(BOB).toHex(),'final Bob output')}
  assert.equal(t.inputs[5].prevTxId.toString('hex'),byName['sponsor-prep-'+s].id,'sponsor parent');assert.equal(t.inputs[5].outputIndex,0)
  const funding=byName['sponsor-prep-'+s].outputs[0].satoshis,change=t.outputs[5].satoshis
  assert.equal(t.outputs[5].script.toHex(),M.pay(BOB).toHex(),'sponsor change')
  return {...records.find(r=>r.name===name),owner:s<2?'Alice':'Bob',funding,change,phase:s===4?'Withdrawn':['Packed','Sealed','Sealed','Opened'][s]}
 })
 const final=byName.withdraw
 const items=assets.map((t,i)=>{
  const probes=query('gettxout').filter(r=>r.params[0]===final.id&&r.params[1]===i),u=probes.at(-1)?.response.result
  assert.ok(u&&u.confirmations>=1,'final UTXO missing');assert.equal(Math.round(u.value*1e8),final.outputs[i].satoshis,'final UTXO value');assert.equal(u.scriptPubKey.hex,final.outputs[i].script.toHex(),'final UTXO script');assert.equal(u.bestblock,chain.bestblockhash,'final UTXO tip')
  const item={role:roles[i],label:labels[i],origin:t.id+':0',final:final.id+':'+i,sats:final.outputs[i].satoshis,payload:payloads[i]||'Separate custody control sat',script:final.outputs[i].script.toHex(),confirmations:u.confirmations}
  const reported=summary.finalUTXOs[i];assert.equal(reported.origin,item.origin,'summary origin');assert.equal(reported.final,item.final,'summary final');assert.deepEqual(reported.utxo,u,'summary UTXO');return item
 })
 const accepted=records.filter(r=>r.accepted).length,rejected=records.length-accepted,totalFees=records.reduce((n,r)=>n+r.fee,0),lifecycleFees=history.reduce((n,r)=>n+r.fee,0)
 assert.equal(totalFees,Object.values(summary.feeTotals).reduce((a,b)=>a+b,0),'summary fees')
 // Re-execute each stored serialized transaction in the local Script VM, not in the browser.
 for(const r of records)assert.equal(M.verify(byName[r.name],parents).success,r.accepted,'offline replay '+r.name)
 return {accepted,rejected,totalFees,lifecycleFees,principal:items.reduce((n,i)=>n+i.sats,0),stages:history,items,records,certificate:cert,policy:{issuer:ISSUER,source:'Exporter external public-fixture policy; never adopted from bundle'},chain:{name:chain.chain,height:chain.blocks,tip:chain.bestblockhash},replay:'PASS',manifest,files}
}
function generate(dir,destination){
 const snapshot=inspect(dir),template=fs.readFileSync(path.join(__dirname,'template.html'),'utf8')
 const embedded=JSON.stringify(snapshot).replace(/</g,'\\u003c').replace(/>/g,'\\u003e').replace(/&/g,'\\u0026')
 fs.mkdirSync(path.dirname(destination),{recursive:true});fs.writeFileSync(destination,template.replace('/*EVIDENCE*/',()=>embedded))
 return {accepted:snapshot.accepted,rejected:snapshot.rejected,totalFees:snapshot.totalFees,replay:snapshot.replay,htmlSha256:sha(fs.readFileSync(destination))}
}
module.exports={inspect,generate}
if(require.main===module){const dir=process.argv[2]||path.resolve(__dirname,'../../evidence/four-ordinal-sponsored/regtest-run-1');const dest=process.argv[3]||path.join(__dirname,'boxsv-evidence.html');console.log(JSON.stringify(generate(dir,dest),null,2))}
