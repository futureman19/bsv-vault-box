'use strict'
// LOCAL REGTEST ONLY. Run under Linux/WSL; never points at an existing RPC.
const fs=require('node:fs'), path=require('node:path'), os=require('node:os')
const {spawn,execFileSync}=require('node:child_process')
const crypto=require('node:crypto'), assert=require('node:assert/strict')
const M=require('../src/ordinal-pair'), {S,bsv,C,pay,output,outpoint,transition}=M
const binary=process.argv[2], base=process.argv[3], evidence=process.argv[4]
if(!binary || !base || !evidence) throw Error('Usage: node fullnode-regtest.js ABS_BITCOIND ABS_SCRATCH_BASE ABS_EVIDENCE_DIR')
for(const p of [binary,base,evidence]) assert.ok(path.isAbsolute(p),'absolute paths required')
assert.equal(process.platform,'linux','run in Linux/WSL')
assert.ok(!fs.existsSync(evidence),'refuse to overwrite prior evidence')
const data=fs.mkdtempSync(path.join(base,'boxsv-regtest-')); fs.mkdirSync(evidence,{recursive:true})
const log=(name,value)=>fs.writeFileSync(path.join(evidence,name),typeof value==='string'?value:JSON.stringify(value,null,2)+'\n')
const config=`regtest=1\nserver=1\nlisten=0\nconnect=0\ndnsseed=0\ndns=0\ndiscover=0\nupnp=0\ndisablewallet=1\ntxindex=1\nassumevalid=0\ngenesisactivationheight=1\nchronicleactivationheight=2\nrpcbind=127.0.0.1\nrpcallowip=127.0.0.1\nrpcport=19483\nexcessiveblocksize=100000000\nblockmaxsize=10000000\nmaxstackmemoryusageconsensus=100000000\ncoinsdbcache=32\ndbcache=16\nminminingtxfee=0.00000001\nacceptnonstdtxn=0\nacceptnonstdoutputs=1\n`;
fs.writeFileSync(path.join(data,'bitcoin.conf'),config); log('bitcoin.conf',config)
const sha=x=>crypto.createHash('sha256').update(x).digest('hex')
log('provenance.json',{binary,sha256:sha(fs.readFileSync(binary)),version:execFileSync(binary,['-version'],{encoding:'utf8'}),platform:os.platform(),release:os.release(),data,baseCommit:execFileSync('git',['rev-parse','HEAD'],{cwd:path.join(__dirname,'../..'),encoding:'utf8'}).trim(),artifactSha256:sha(JSON.stringify(require('../artifacts/ordinalPair.json'))),builderSha256:sha(fs.readFileSync(path.join(__dirname,'../src/ordinal-pair.js')))})
const stdout=fs.openSync(path.join(evidence,'node-stdout.log'),'w');const child=spawn(binary,[`-datadir=${data}`,`-conf=${data}/bitcoin.conf`],{stdio:['ignore',stdout,stdout]})
const journal=path.join(evidence,'rpc.jsonl');fs.writeFileSync(journal,'')
let id=0
async function rpc(method,params=[],allowError=false){
 const cookie=fs.readFileSync(path.join(data,'regtest/.cookie'),'utf8').trim()
 const response=await fetch('http://127.0.0.1:19483',{method:'POST',headers:{Authorization:'Basic '+Buffer.from(cookie).toString('base64'),'content-type':'application/json'},body:JSON.stringify({jsonrpc:'1.0',id:++id,method,params}),signal:AbortSignal.timeout(30000)})
 const body=await response.json();fs.appendFileSync(journal,JSON.stringify({method,params,response:body})+'\n')
 if(body.error&&!allowError)throw Error(method+': '+JSON.stringify(body.error));return allowError?body:body.result
}
const delay=ms=>new Promise(r=>setTimeout(r,ms)); const txs=[];const outcomes=[]
function saveTx(name,tx){log(name+'.hex',tx.uncheckedSerialize()+'\n');txs.push({name,txid:tx.id,bytes:tx.toBuffer().length})}
async function mine(){return rpc('generatetoaddress',[1,address])}
let address
async function admit(name,tx){saveTx(name,tx);assert.equal(await rpc('sendrawtransaction',[tx.uncheckedSerialize()]),tx.id);assert.ok((await rpc('getrawmempool')).includes(tx.id));let detail
 for(let n=0;n<5;n++){await delay(150);await mine();detail=await rpc('getrawtransaction',[tx.id,true]);if(detail.confirmations>0)break}
 assert.ok(detail.confirmations>0);const block=await rpc('getblock',[detail.blockhash]);assert.ok(block.tx.includes(tx.id));assert.equal(detail.hex,tx.uncheckedSerialize());outcomes.push({name,txid:tx.id,mempool:true,block:detail.blockhash,confirmations:detail.confirmations});return tx}
function spend(parent,index,outs,key){const tx=new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:parent.id,outputIndex:index,script:'',output:parent.outputs[index]}));outs.forEach(o=>tx.addOutput(o));const sig=S.signTx(tx,key,parent.outputs[index].script,parent.outputs[index].satoshis,0);tx.inputs[0].setScript(bsv.Script.fromASM(sig+' '+key.publicKey));return tx}
async function reject(name,tx,source){saveTx(name,tx);for(let i=0;i<2;i++)assert.ok(await rpc('gettxout',[source.id,i]));const response=await rpc('sendrawtransaction',[tx.uncheckedSerialize()],true);assert.ok(response.error,'attack admitted');assert.match(response.error.message,/script|mandatory|opcode|verify/i);assert.ok(!(await rpc('getrawmempool')).includes(tx.id));for(let i=0;i<2;i++)assert.ok(await rpc('gettxout',[source.id,i]));outcomes.push({name,txid:tx.id,rejection:response.error})}
async function main(){
 for(let n=0;n<100;n++){if(child.exitCode!==null)throw Error('node exited '+child.exitCode);if(fs.existsSync(path.join(data,'regtest/.cookie'))){try{await rpc('getblockchaininfo');break}catch{}}await delay(200)}
 assert.equal((await rpc('getblockchaininfo')).chain,'regtest');assert.equal(await rpc('getconnectioncount'),0);log('network.json',await rpc('getnetworkinfo'))
 const f=M.fixture(); address=f.alice.toAddress().toString();const bob=f.bob.publicKey.toString()
 const blocks=await rpc('generatetoaddress',[110,address]);const first=await rpc('getblock',[blocks[0]]);const coinbase=new bsv.Transaction(await rpc('getrawtransaction',[first.tx[0]]))
 // Split a genuinely matured coinbase into funding roots; no assumed UTXOs.
 const root=spend(coinbase,0,Array.from({length:12},()=>output(pay(f.alice.publicKey.toString()),1000000)).concat([output(pay(f.alice.publicKey.toString()),coinbase.outputs[0].satoshis-12000000-1000)]),f.alice)
 await admit('funding-root',root)
 const inscription=f.foreign.outputs[0].script
 f.foreign=await admit('existing-inscription',spend(root,0,[output(inscription),output(pay(f.alice.publicKey.toString()),999499)],f.alice))
 const c=new C(outpoint(f.foreign,0),0n,f.alice.publicKey.toString());c.phase=0n;c.owner=f.alice.publicKey.toString()
 f.box=await admit('empty-box',spend(root,1,[output(c.lockingScript),output(pay(f.alice.publicKey.toString()),999499)],f.alice));f.origin=f.foreign.id+'_0'
 let rootIndex=2;const fundingParents=[],chain=[]
 async function build(source,action,signer){const funding=await admit('sponsor-prep-'+rootIndex,spend(root,rootIndex++,[output(pay(bob),999500)],f.alice));fundingParents.push(funding);return transition(f,source,action,signer,bob,null,undefined,{sponsor:f.bob,funding:999500,fee:500,fundingTx:funding}).tx}
 let source=await admit('deposit',await build(null,0,f.alice));chain.push(source)
 source=await admit('seal',await build(source,1,f.alice));chain.push(source)
 await reject('attack-sealed-withdraw',await build(source,4,f.alice),source)
 source=await admit('transfer',await build(source,2,f.alice));chain.push(source)
 await reject('attack-old-owner-open',await build(source,3,f.alice),source)
 source=await admit('open',await build(source,3,f.bob));chain.push(source)
 await reject('attack-old-owner-withdraw',await build(source,4,f.alice),source)
 source=await admit('withdraw',await build(source,4,f.bob));chain.push(source)
 const final=[];for(let i=0;i<2;i++){const utxo=await rpc('gettxout',[source.id,i]);assert.equal(utxo.value,0.00000001);assert.equal(utxo.scriptPubKey.hex,pay(bob).toHex());final.push(utxo)}
 assert.equal(await rpc('gettxout',[f.foreign.id,0]),null)
 for(let i=0;i<chain.length;i++){const t=chain[i];assert.equal(t.inputs[0].prevTxId.toString('hex'),i?chain[i-1].id:f.foreign.id);assert.equal(t.inputs[0].outputIndex,0);assert.equal(t.outputs[0].satoshis,1);assert.equal(t.outputs[1].satoshis,1);assert.equal(t.outputs[2].satoshis,999000)}
 assert.equal(M.verifyHistory(f,chain,fundingParents).valid,true)
 assert.equal(await rpc('verifychain',[4,0]),true);assert.equal(await rpc('getconnectioncount'),0)
 log('result.json',{status:'PASS',origin:f.origin,tip:source.id+':0',outcomes,transactions:txs,finalUTXOs:final,chain:await rpc('getblockchaininfo'),boundary:'Independent BSV node mempool and mined acceptance; attacks rejected by mempool script validation, not submitted in candidate blocks. Identity positional ancestry checked by harness, not an indexer.'})
}
main().catch(e=>{log('failure.json',{error:e.stack,outcomes,transactions:txs});console.error(e);process.exitCode=1}).finally(async()=>{try{await rpc('stop')}catch{};await Promise.race([new Promise(r=>child.once('exit',r)),delay(10000)]);if(child.exitCode===null)child.kill('SIGTERM');const p=path.join(data,'regtest/bitcoind.log');if(fs.existsSync(p))fs.copyFileSync(p,path.join(evidence,'bitcoind.log'));console.log(JSON.stringify({evidence,data,exitCode:process.exitCode||0}))})
