'use strict'
// Offline only. Public disposable scalars; NEVER FUND. Existing helpers unchanged.
const {S,bsv,pay,output,outpoint,verify,Ledger}=require('./ordinal-pair')
const C=S.buildContractClass(require('../artifacts/fourOrdinal.json'))
const key=n=>new bsv.PrivateKey(new bsv.crypto.BN(n),bsv.Networks.testnet)
const TRUSTED_POLICY=Object.freeze({issuer:key(3).publicKey.toString()})
const digest=s=>bsv.crypto.Hash.sha256(Buffer.from(s)).toString('hex')
const roles=['collectible-box','certificate','object-one','object-two']
const id=t=>t.id+'_0'
const origins=assets=>assets.map(t=>outpoint(t,0)).join('')
const prevouts=t=>t.inputs.map(i=>{const n=Buffer.alloc(4);n.writeUInt32LE(i.outputIndex);return Buffer.from(i.prevTxId).reverse().toString('hex')+n.toString('hex')}).join('')
function seed(script,tag) {
 return new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:tag.repeat(32),outputIndex:0,script:'',output:output(bsv.Script.empty())})).addOutput(output(script))
}
function inscription(pub,text,tag) {
 const bytes=Buffer.from(text,'utf8')
 if(bytes.length<1||bytes.length>75) throw Error('text payload outside 1..75 bytes')
 return seed(bsv.Script.fromHex(pay(pub).toHex()+'0063036f7264510a746578742f706c61696e00'+Buffer.from([bytes.length]).toString('hex')+bytes.toString('hex')+'68'),tag)
}
function statementFor(assets) {return JSON.stringify({protocol:'BOX4-CERT-1',collectible:id(assets[0]),objects:[id(assets[2]),id(assets[3])]})}
function envelope(c) {return JSON.stringify({statement:c.statement,issuer:c.issuer,signature:c.signature})}
function manifestFor(assets) {return JSON.stringify({protocol:'BOX4-MANIFEST-1',items:assets.map((t,i)=>({role:roles[i],origin:id(t)}))})}
function fixture(options={}) {
 const alice=key(1),bob=key(2),issuer=options.issuer||key(3),pub=alice.publicKey.toString()
 const assets=[inscription(pub,'Box from an impossible place','51'),null,inscription(pub,'Object one: mountain','53'),inscription(pub,'Object two: river','54')]
 const statement=statementFor(assets)
 const signature=bsv.crypto.ECDSA.sign(Buffer.from(digest(statement),'hex'),issuer).toDER().toString('hex')
 const certificate={statement,issuer:issuer.publicKey.toString(),signature}
 // Exactly 64 ASCII hex bytes in certificate NFT; signed envelope is detached.
 assets[1]=inscription(pub,digest(envelope(certificate)),'52')
 const c=new C(origins(assets),0n,pub);c.phase=0n;c.owner=pub
 const box=seed(c.lockingScript,'55')
 return {alice,bob,assets,box,certificate,manifest:manifestFor(assets)}
}
function vmInput(tx,o,i) {
 tx=new bsv.Transaction(tx.uncheckedSerialize())
 const vm=new bsv.Script.Interpreter()
 const success=vm.verify(tx.inputs[i].script,o.script,tx,i,S.DEFAULT_FLAGS,new bsv.crypto.BN(o.satoshis))
 return {success,error:vm.errstr}
}
function transition(f,source,action,signer,recipient,mutate) {
 const pack=action===0,parents=pack?[...f.assets,f.box]:[source]
 const current=pack?f.box:source,c=C.fromHex(current.outputs[0].script.toHex()),tx=new bsv.Transaction()
 for(let i=0;i<5;i++) {
  const p=pack?parents[i]:source,index=pack?0:i
  tx.addInput(new bsv.Transaction.Input({prevTxId:p.id,outputIndex:index,script:'',output:p.outputs[index]}))
 }
 recipient=recipient||c.owner
 const phase=({0:1,1:2,3:3})[action]??Number(c.phase),owner=action===2?recipient:c.owner
 const script=action===4?pay(owner):c.getNewStateScript({phase:BigInt(phase),owner})
 for(let i=0;i<5;i++) tx.addOutput(output(script))
 if(mutate) mutate(tx)
 const spent=tx.inputs.map((input,i)=>{
  const p=parents.find(p=>p.id===input.prevTxId.toString('hex'))
  return (p&&p.outputs[input.outputIndex])||(pack?parents[Math.min(i,4)].outputs[0]:source.outputs[0])
 })
 const isContract=i=>!pack||spent[i].script.toHex()===f.box.outputs[0].script.toHex()
 // Stabilize ALL hashSequence-affecting grinding before signing ANY input.
 for(let attempts=0;;attempts++) {
  if(attempts>10000) throw Error('preimage stabilization exhausted')
  const before=tx.inputs.map(i=>i.sequenceNumber).join(',')
  for(let i=0;i<tx.inputs.length;i++) if(isContract(i)) S.getLowSPreimage(tx,spent[i].script,spent[i].satoshis,i)
  if(before===tx.inputs.map(i=>i.sequenceNumber).join(',')) break
 }
 const stable=tx.inputs.map(i=>i.sequenceNumber).join(',')
 for(let i=0;i<tx.inputs.length;i++) {
  const o=spent[i]
  if(!isContract(i)) {
   tx.inputs[i].setScript(bsv.Script.fromASM(S.signTx(tx,signer,o.script,o.satoshis,i)+' '+signer.publicKey.toString()))
  } else {
   const instance=C.fromHex(o.script.toHex()),pre=S.getLowSPreimage(tx,o.script,o.satoshis,i)
   if(stable!==tx.inputs.map(i=>i.sequenceNumber).join(',')) throw Error('sequence changed after stabilization')
   const sig=S.signTx(tx,signer,o.script,o.satoshis,i),parent=bsv.crypto.Hash.sha256(current.toBuffer()).toString('hex')
   tx.inputs[i].setScript(instance.move(sig,BigInt(action),recipient,parent,pre,prevouts(tx)).toScript())
  }
 }
 return {tx:new bsv.Transaction(tx.uncheckedSerialize()),result:verify(tx,parents)}
}
function parseInscription(tx) {
 const o=tx.outputs[0],match=o&&/^76a914([0-9a-f]{40})88ac0063036f7264510a746578742f706c61696e00([0-9a-f]{2})([0-9a-f]*)68$/.exec(o.script.toHex())
 if(!match||o.satoshis!==1||parseInt(match[2],16)<1||parseInt(match[2],16)>75||match[3].length!==parseInt(match[2],16)*2) throw Error('unsupported one-push text inscription')
 return {owner:match[1],payload:Buffer.from(match[3],'hex').toString('utf8')}
}
function verifyHistory(f,entries,policy) {
 try {
  if(!policy||typeof policy.issuer!=='string') throw Error('explicit trusted issuer policy required')
  if(!f.certificate||f.certificate.issuer!==policy.issuer) throw Error('unknown issuer')
  if(f.assets.length!==4||new Set(f.assets.map(id)).size!==4) throw Error('exact four independent origins required')
  const admitted=f.assets.map(parseInscription)
  if(f.certificate.statement!==statementFor(f.assets)) throw Error('certificate origins mismatch')
  const sig=bsv.crypto.Signature.fromDER(Buffer.from(f.certificate.signature,'hex'))
  if(!bsv.crypto.ECDSA.verify(Buffer.from(digest(f.certificate.statement),'hex'),sig,bsv.PublicKey.fromString(policy.issuer))) throw Error('forged certificate signature')
  if(admitted[1].payload!==digest(envelope(f.certificate))) throw Error('certificate inscription commitment mismatch')
  if(f.manifest!==manifestFor(f.assets)) throw Error('noncanonical manifest')
  const c=C.fromHex(f.box.outputs[0].script.toHex())
  if(f.box.outputs[0].satoshis!==1||c.phase!==0n||c.lockingScript.toHex()!==f.box.outputs[0].script.toHex()||c.ctorArgs().find(a=>a.name==='origins').value!==origins(f.assets)) throw Error('unanchored initial box')
  const owner=bsv.crypto.Hash.sha256ripemd160(Buffer.from(c.owner,'hex')).toString('hex')
  if(admitted.some(a=>a.owner!==owner)) throw Error('initial owner mismatch')
  const ledger=new Ledger([...f.assets,f.box]);let previous
  for(const tx of entries) {
   const expected=previous?[0,1,2,3,4].map(i=>outpoint(previous,i)).join(''):origins(f.assets)+outpoint(f.box,0)
   if(tx.inputs.length!==5||prevouts(tx)!==expected) throw Error('origin continuity failure')
   if(tx.outputs.length!==5||tx.outputs.some(o=>o.satoshis!==1)) throw Error('principal/order conservation failure')
   ledger.accept(tx);previous=tx
  }
  return {valid:true,origins:f.assets.map(id),tip:previous?previous.id:f.box.id}
 } catch(e) {return {valid:false,error:e.message}}
}
function vectors() {
 const f=fixture(),lifecycle=[];let p
 for(const action of [0,1,2,3,4]) {
  const r=transition(f,p,action,action<3?f.alice:f.bob,f.bob.publicKey.toString())
  if(!r.result.success) throw Error(JSON.stringify(r.result))
  p=r.tx;lifecycle.push({action,txid:p.id,bytes:p.toBuffer().length,raw:p.uncheckedSerialize()})
 }
 return {format:'BOX4-OFFLINE-1',assumptions:'Synthetic roots, public scalars 1/2/3; no chain existence, zero fees, text/plain only.',artifactSha256:digest(JSON.stringify(JSON.parse(require('node:fs').readFileSync(require.resolve('../artifacts/fourOrdinal.json'),'utf8')))),policy:TRUSTED_POLICY,assets:f.assets.map(t=>({origin:id(t),raw:t.uncheckedSerialize()})),box:f.box.uncheckedSerialize(),manifest:f.manifest,certificate:f.certificate,lifecycle}
}
function replayVectors(v,policy) {
 try {
  if(v.format!=='BOX4-OFFLINE-1') throw Error('unsupported evidence format')
  for(const asset of v.assets) if(asset.origin!==id(new bsv.Transaction(asset.raw))) throw Error('origin metadata mismatch')
  if(v.artifactSha256!==digest(JSON.stringify(JSON.parse(require('node:fs').readFileSync(require.resolve('../artifacts/fourOrdinal.json'),'utf8'))))) throw Error('artifact mismatch')
  const f={assets:v.assets.map(a=>new bsv.Transaction(a.raw)),box:new bsv.Transaction(v.box),manifest:v.manifest,certificate:v.certificate}
  const txs=v.lifecycle.map(t=>{const tx=new bsv.Transaction(t.raw);if(tx.id!==t.txid||tx.toBuffer().length!==t.bytes) throw Error('transaction metadata mismatch');return tx})
  return verifyHistory(f,txs,policy)
 }catch(e){return {valid:false,error:e.message}}
}
module.exports={S,bsv,C,key,TRUSTED_POLICY,fixture,transition,verifyHistory,vmInput,vectors,replayVectors,pay,output,outpoint,verify}
