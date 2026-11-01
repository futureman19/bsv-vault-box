'use strict'
// Isolated local BSV regtest only. No default datadir, wallet or public RPC.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),net=require('node:net')
const {spawn,execFileSync}=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict')
const M=require('../src/four-ordinal-sponsored'),{S,bsv,C,pay,output,outpoint,transition}=M
const binary=process.argv[2],base=process.argv[3],evidence=process.argv[4]
assert.equal(process.platform,'linux');for(const p of [binary,base,evidence])assert.ok(p&&path.isAbsolute(p))
assert.ok(!fs.existsSync(evidence),'fresh evidence required');fs.mkdirSync(base,{recursive:true});fs.mkdirSync(evidence,{recursive:true})
const data=fs.mkdtempSync(path.join(base,'box4-regtest-'));fs.chmodSync(data,0o700)
const log=(n,v)=>fs.writeFileSync(path.join(evidence,n),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n')
const sha=x=>crypto.createHash('sha256').update(x).digest('hex')
let port,child,exited
const journal=path.join(evidence,'rpc.jsonl');fs.writeFileSync(journal,'')
let id=0
async function rpc(method,params=[],allowError=false){
 const cookie=fs.readFileSync(path.join(data,'regtest/.cookie'),'utf8').trim()
 const response=await fetch(`http://127.0.0.1:${port}`,{method:'POST',headers:{Authorization:'Basic '+Buffer.from(cookie).toString('base64'),'content-type':'application/json'},body:JSON.stringify({jsonrpc:'1.0',id:++id,method,params}),signal:AbortSignal.timeout(30000)})
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
async function reject(name,tx,parents){
 saveTx(name,tx)
 // All actual inputs, not merely the covenant, must be live before submission.
 const live=async()=>{for(const input of tx.inputs)assert.ok(await rpc('gettxout',[input.prevTxId.toString('hex'),input.outputIndex]),'attack input must remain unspent')}
 await live()
 const response=await rpc('sendrawtransaction',[tx.uncheckedSerialize()],true)
 assert.ok(response.error,'attack admitted');assert.equal(response.error.code,-26)
 assert.match(response.error.message,/mandatory-script-verify-flag-failed/)
 assert.doesNotMatch(response.error.message,/missing|spent|conflict/)
 assert.ok(!(await rpc('getrawmempool')).includes(tx.id));await live()
 outcomes.push({name,txid:tx.id,rejection:response.error,allInputsLiveBeforeAndAfter:true})
}
function witness(tx,source,field,value,index=0){
 const args=C.abiCoder.parseCallData(tx.inputs[index].script.toHex()).args,a=args.find(a=>a.name===field)
 a.value=typeof value==='function'?value(a.value):value
 tx.inputs[index].setScript(C.fromHex(source.outputs[index].script.toHex()).move(...args.map(a=>a.value)).toScript());return tx
}
async function main(){
 port=await new Promise((resolve,reject)=>{const s=net.createServer();s.once('error',reject);s.listen(0,'127.0.0.1',()=>{const p=s.address().port;s.close(()=>resolve(p))})})
 const config='regtest=1\nserver=1\nlisten=0\nconnect=0\ndnsseed=0\ndns=0\ndiscover=0\nupnp=0\ndisablewallet=1\ntxindex=1\nassumevalid=0\ngenesisactivationheight=1\nchronicleactivationheight=2\nrpcbind=127.0.0.1\nrpcallowip=127.0.0.1\nrpcport='+port+'\nexcessiveblocksize=100000000\nblockmaxsize=10000000\nmaxstackmemoryusageconsensus=100000000\ncoinsdbcache=32\ndbcache=16\nminminingtxfee=0.00000001\nacceptnonstdtxn=0\nacceptnonstdoutputs=1\n'
 // These are fresh, generated configuration bytes, never a pre-existing config.
 const actualConfig=config
 fs.writeFileSync(path.join(data,'bitcoin.conf'),actualConfig);log('bitcoin.conf',actualConfig)
 const args=[`-datadir=${data}`,`-conf=${data}/bitcoin.conf`,'-regtest','-disablewallet','-listen=0','-connect=0','-dnsseed=0','-dns=0','-discover=0','-upnp=0','-rpcbind=127.0.0.1','-rpcallowip=127.0.0.1',`-rpcport=${port}`]
 log('process-before.txt',execFileSync('ps',['-eo','pid,args'],{encoding:'utf8'}))
 const stdout=fs.openSync(path.join(evidence,'node-stdout.log'),'wx')
 child=spawn(binary,args,{stdio:['ignore',stdout,stdout]});fs.closeSync(stdout)
 exited=new Promise(resolve=>child.once('exit',resolve))
 log('provenance.json',{binary,binarySha256:sha(fs.readFileSync(binary)),args,data,port,ownedPid:child.pid,platform:os.platform(),release:os.release(),artifactSha256:sha(fs.readFileSync(path.join(__dirname,'../artifacts/fourOrdinalSponsored.json'))),builderSha256:sha(fs.readFileSync(path.join(__dirname,'../src/four-ordinal-sponsored.js')))})
 let ready=false
 for(let n=0;n<100;n++){if(child.exitCode!==null)throw Error('node exited '+child.exitCode);try{if((await rpc('getblockchaininfo')).chain==='regtest'){ready=true;break}}catch{}await delay(200)}
 assert.ok(ready,'startup deadline');assert.equal(await rpc('getconnectioncount'),0)
 log('network.json',await rpc('getnetworkinfo'));log('process-running.txt',execFileSync('ps',['-eo','pid,args'],{encoding:'utf8'}))
 const f=M.fixture(),alice=f.alice.publicKey.toString(),bob=f.bob.publicKey.toString();address=f.alice.toAddress().toString()
 const blocks=await rpc('generatetoaddress',[110,address]),first=await rpc('getblock',[blocks[0]])
 const coinbase=new bsv.Transaction(await rpc('getrawtransaction',[first.tx[0]]))
 const root=await admit('funding-root',spend(coinbase,0,Array.from({length:10},()=>output(pay(alice),1000000)).concat([output(pay(alice),coinbase.outputs[0].satoshis-10000000-1000)]),f.alice))
 for(const i of [0,2,3])f.assets[i]=await admit('original-'+i,spend(root,i,[output(f.assets[i].outputs[0].script),output(pay(alice),999499)],f.alice))
 // Certificate signs real original outpoints, before its own mint; no txid cycle.
 const statement=JSON.stringify({protocol:'BOX4-CERT-1',collectible:f.assets[0].id+'_0',objects:[f.assets[2].id+'_0',f.assets[3].id+'_0']})
 const issuer=M.key(3);f.certificate={statement,issuer:issuer.publicKey.toString(),signature:bsv.crypto.ECDSA.sign(Buffer.from(sha(statement),'hex'),issuer).toDER().toString('hex')}
 const payload=Buffer.from(sha(JSON.stringify(f.certificate))).toString('hex')
 const inscription=bsv.Script.fromHex(pay(alice).toHex()+'0063036f7264510a746578742f706c61696e0040'+payload+'68')
 f.assets[1]=await admit('original-1-certificate',spend(root,1,[output(inscription),output(pay(alice),999499)],f.alice))
 const c=new C(M.origins(f.assets),0n,alice);c.phase=0n;c.owner=alice
 f.box=await admit('initial-control',spend(root,4,[output(c.lockingScript),output(pay(alice),999499)],f.alice))
 const roles=['collectible-box','certificate','object-one','object-two']
 f.manifest=JSON.stringify({protocol:'BOX4-MANIFEST-1',items:f.assets.map((t,i)=>({role:roles[i],origin:t.id+'_0'}))})
 assert.equal(f.certificate.issuer,M.TRUSTED_POLICY.issuer)
 assert.ok(bsv.crypto.ECDSA.verify(Buffer.from(sha(statement),'hex'),bsv.crypto.Signature.fromDER(Buffer.from(f.certificate.signature,'hex')),issuer.publicKey))
 log('identity.json',{trustedPolicy:M.TRUSTED_POLICY,certificate:f.certificate,manifest:f.manifest,origins:f.assets.map(t=>t.id+'_0'),control:f.box.id+'_0'})
 const chain=[],fees=[],preps=[];let source
 for(const action of [0,1,2,3,4]){
  const funding=await admit('sponsor-prep-'+action,spend(root,5+action,[output(pay(bob),999500)],f.alice));preps.push(funding)
  const opts={sponsor:f.bob,funding:999500,fee:500,fundingTx:funding}
  const build=(signer,mutate,overrides={})=>transition(f,source,action,signer,bob,mutate,{...opts,...overrides}).tx
  const signer=action<3?f.alice:f.bob
  if(action===2){
   const attacks=[
    ['missing-sponsor-auth',()=>witness(build(signer),source,'sponsorSig','')],
    ['wrong-sponsor-auth',()=>{const t=build(signer);return witness(t,source,'sponsorSig',S.signTx(t,f.alice,source.outputs[0].script,1,0))}],
    ['malformed-parent-input-count',()=>witness(build(signer),source,'fundingPrefix',v=>v.slice(0,8)+'02'+v.slice(10))],
    ['malformed-parent-output-count',()=>witness(build(signer),source,'fundingPrefix',v=>v.slice(0,-2)+'02')],
    ['malformed-parent-length',()=>witness(build(signer),source,'fundingPrefix',v=>v.slice(0,82)+'fd'+v.slice(84))],
    ['reordered-input',()=>build(signer,t=>{[t.inputs[0],t.inputs[5]]=[t.inputs[5],t.inputs[0]]})],
    ['zero-fee-witness',()=>witness(build(signer),source,'change',999500n)],
    ['negative-fee-witness',()=>witness(build(signer),source,'change',999501n)],
    ['excess-fee',()=>build(signer,null,{fee:10001})],
    ['change-diversion',()=>build(signer,t=>{t.outputs[5]=output(pay(alice),999000)})],
    ['extra-output',()=>build(signer,t=>t.addOutput(output(pay(bob))))],
    ...Array.from({length:5},(_,i)=>['principal-diversion-'+i,()=>build(signer,t=>{t.outputs[i]=output(pay(bob))})]),
    ['missing-p2pkh-auth',()=>{const t=build(signer);t.inputs[5].setScript(bsv.Script.empty());return t}],
    ['sealed-withdrawal',()=>transition(f,source,4,signer,bob,null,opts).tx]
   ]
   for(const [name,make] of attacks)await reject('attack-'+name,make(),[source,funding])
  }
  if(action===3||action===4)await reject(action===3?'attack-old-owner-open':'attack-old-owner-withdraw',build(f.alice),[source,funding])
  const t=build(signer);assert.equal(M.verify(t,action===0?[...f.assets,f.box,funding]:[source,funding]).success,true)
  for(let i=0;i<5;i++){
   assert.equal(t.inputs[i].prevTxId.toString('hex'),action===0?(i<4?f.assets[i].id:f.box.id):source.id)
   assert.equal(t.inputs[i].outputIndex,action===0?0:i);assert.equal(t.outputs[i].satoshis,1)
  }
  assert.equal(t.inputs[5].prevTxId.toString('hex'),funding.id);assert.equal(t.outputs[5].satoshis,999000);assert.equal(t.outputs[5].script.toHex(),pay(bob).toHex())
  const name=['pack','seal','transfer','open','withdraw'][action]
  source=await admit(name,t);chain.push(t);fees.push({name,funding:999500,change:999000,fee:500,principalInput:5,principalOutput:5})
 }
 const final=[]
 for(let i=0;i<5;i++){
  const origin=i<4?f.assets[i]:f.box;assert.equal(await rpc('gettxout',[origin.id,0]),null)
  const utxo=await rpc('gettxout',[source.id,i]);assert.equal(utxo.value,0.00000001);assert.equal(utxo.scriptPubKey.hex,pay(bob).toHex())
  final.push({role:i<4?roles[i]:'control',origin:origin.id+':0',final:source.id+':'+i,utxo})
 }
 assert.equal(await rpc('verifychain',[4,0]),true);assert.equal(await rpc('getconnectioncount'),0)
 log('result.json',{status:'PASS',outcomes,transactions:txs,fees,feeTotals:{custody:fees.reduce((n,f)=>n+f.fee,0),sponsorPreparation:preps.length*500,fundingSplit:1000,originalsAndControl:2500},finalUTXOs:final,chain:await rpc('getblockchaininfo'),boundary:'Local regtest; mandatory script rejection at mempool admission, not invalid-block testing. Ordinal identity is positional ancestry, not indexer recognition. Certificate provenance is client-only with explicit fixture issuer. Zero/negative-fee witnesses isolated from ledger overspend; actual negative-fee output tested separately in VM.'})
}
main().catch(e=>{log('failure.json',{error:e.stack,outcomes,transactions:txs});console.error(e);process.exitCode=1}).finally(async()=>{
 if(child){
  if(child.exitCode===null){try{await rpc('stop')}catch{}await Promise.race([exited,delay(10000)])}
  if(child.exitCode===null){child.kill('SIGTERM');await Promise.race([exited,delay(5000)])}
  if(child.exitCode===null){child.kill('SIGKILL');await Promise.race([exited,delay(3000)])}
  const absent=!fs.existsSync('/proc/'+child.pid)
  log('shutdown.json',{ownedPid:child.pid,exitCode:child.exitCode,signal:child.signalCode,ownedProcessAbsent:absent})
  if(!absent)process.exitCode=1
 }
 const p=path.join(data,'regtest/bitcoind.log');if(fs.existsSync(p))fs.copyFileSync(p,path.join(evidence,'bitcoind.log'))
 log('process-after.txt',execFileSync('ps',['-eo','pid,args'],{encoding:'utf8'}))
 console.log(JSON.stringify({evidence,data,exitCode:process.exitCode||0}))
})
