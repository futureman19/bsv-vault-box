'use strict'
// LOCAL ONLY: synthetic fixture; no network, credentials or broadcast.
const S = require('scryptlib')
const { bsv } = S
// Match scryptlib's post-Genesis local interpreter limits.
bsv.Script.Interpreter.MAX_SCRIPT_ELEMENT_SIZE = Number.MAX_SAFE_INTEGER
bsv.Script.Interpreter.MAXIMUM_ELEMENT_SIZE = Number.MAX_SAFE_INTEGER
const C = S.buildContractClass(require('../artifacts/ordinalPair.json'))
const key = n => new bsv.PrivateKey(new bsv.crypto.BN(n), bsv.Networks.testnet)
const output = (script, satoshis = 1) => new bsv.Transaction.Output({ script, satoshis })
const pay = pub => bsv.Script.buildPublicKeyHashOut(bsv.PublicKey.fromString(pub).toAddress())
const outpoint = (tx, i) => Buffer.from(tx.id, 'hex').reverse().toString('hex') + Buffer.from([i,0,0,0]).toString('hex')
const prevouts = tx => tx.inputs.map(i => Buffer.from(i.prevTxId).reverse().toString('hex') + (() => { const n = Buffer.alloc(4); n.writeUInt32LE(i.outputIndex); return n.toString('hex') })()).join('')
function add(tx, parent, index) { tx.addInput(new bsv.Transaction.Input({prevTxId:parent.id, outputIndex:index, script:'', output:parent.outputs[index]})); return tx }
function seed(script, tag) { return new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:tag.repeat(32), outputIndex:0, script:'', output:output(bsv.Script.empty())})).addOutput(output(script)) }
function fixture() {
 const alice = key(1), bob = key(2)
 const inscription = pay(alice.publicKey.toString()).toHex() + '0063036f7264510a746578742f706c61696e000b426f7853562d746573746168'
 const foreign = seed(bsv.Script.fromHex(inscription), '11')
 const c = new C(outpoint(foreign,0), 0n, alice.publicKey.toString())
 c.phase = 0n; c.owner = alice.publicKey.toString()
 const box = seed(c.lockingScript, '22')
 return {alice,bob,foreign,box,origin:foreign.id+'_0'}
}
function verify(tx, parents) {
 // Roundtrip serialization before VM. Parent map supplies actual spent outputs,
 // never an attacker-selected locking script. This is the local UTXO boundary.
 tx = new bsv.Transaction(tx.uncheckedSerialize())
 const seen = new Set(); let incoming = 0
 for (let i=0;i<tx.inputs.length;i++) {
  const input=tx.inputs[i], id=input.prevTxId.toString('hex'), ref=id+':'+input.outputIndex
  if(seen.has(ref)) return {success:false,error:'duplicate input'}
  seen.add(ref)
  const p=parents.find(p=>p.id===id), o=p && p.outputs[input.outputIndex]
  if(!o) return {success:false,error:'unknown outpoint'}
  incoming += o.satoshis
  const vm = new bsv.Script.Interpreter()
  if(!vm.verify(input.script,o.script,tx,i,S.DEFAULT_FLAGS,new bsv.crypto.BN(o.satoshis))) return {success:false,error:vm.errstr,input:i}
 }
 if(tx.outputs.reduce((n,o)=>n+o.satoshis,0)>incoming) return {success:false,error:'overspend'}
 return {success:true}
}
function transition(f, source, action, signer, recipient, mutate, proof) {
 const deposit = action === 0
 const c = C.fromHex((deposit ? f.box.outputs[0] : source.outputs[0]).script.toHex())
 const parents = deposit ? [f.foreign,f.box] : [source]
 const tx = new bsv.Transaction()
 if(deposit) {add(tx,f.foreign,0);add(tx,f.box,0)} else {add(tx,source,0);add(tx,source,1)}
 const nextPhase = ({0:1,1:2,3:3})[action] ?? Number(c.phase)
 recipient = recipient || c.owner
 const newOwner = action===2 ? recipient : c.owner
 const script = action===4 ? pay(newOwner) : c.getNewStateScript({phase:BigInt(nextPhase),owner:newOwner})
 tx.addOutput(output(script)).addOutput(output(script))
 if(mutate) mutate(tx)
 // Low-S grinding changes hashSequence: stabilize ALL inputs before signing ANY.
 for(let attempts=0;;attempts++) {
  if(attempts>10000) throw Error('preimage grinding exhausted')
  const before=tx.inputs.map(i=>i.sequenceNumber).join(',')
  for(let i=deposit?1:0;i<Math.min(2,tx.inputs.length);i++) S.getLowSPreimage(tx,deposit?f.box.outputs[0].script:source.outputs[i].script,1,i)
  if(before===tx.inputs.map(i=>i.sequenceNumber).join(',')) break
 }
 for(let i=0;i<Math.min(2,tx.inputs.length);i++) {
  const o = deposit ? parents[i].outputs[0] : source.outputs[i]
  if(deposit && i===0) {
   const sig=S.signTx(tx,signer,o.script,1,i)
   tx.inputs[i].setScript(bsv.Script.fromASM(sig+' '+signer.publicKey.toString()))
  } else {
   const instance=C.fromHex(o.script.toHex())
   const pre=S.getLowSPreimage(tx,o.script,1,i)
   const sig=S.signTx(tx,signer,o.script,1,i)
   const call=instance.move(sig,BigInt(action),recipient,proof ?? (deposit ? f.box : source).uncheckedSerialize(),pre,prevouts(tx))
   tx.inputs[i].setScript(call.toScript())
  }
 }
 return {tx,result:verify(tx,parents)}
}
class Ledger {
 constructor(parents) {this.parents=[...parents];this.spent=new Set()}
 accept(tx) {
  const refs=tx.inputs.map(i=>i.prevTxId.toString('hex')+':'+i.outputIndex)
  if(refs.some(r=>this.spent.has(r))) throw Error('conflicting ledger spend')
  const r=verify(tx,this.parents);if(!r.success) throw Error(JSON.stringify(r))
  refs.forEach(r=>this.spent.add(r));this.parents.push(tx)
 }
}
function verifyHistory(f, entries) {
 try {
  const hex=f.foreign.outputs[0].script.toHex()
  const match=/^76a914([0-9a-f]{40})88ac0063036f7264510a746578742f706c61696e00([0-9a-f]{2})([0-9a-f]*)68$/.exec(hex)
  if(!match || parseInt(match[2],16)>75 || parseInt(match[2],16)<1 || match[3].length!==parseInt(match[2],16)*2 || f.foreign.outputs[0].satoshis!==1) throw Error('unsupported inscription grammar')
  const initial=C.fromHex(f.box.outputs[0].script.toHex())
  if(initial.lockingScript.toHex()!==f.box.outputs[0].script.toHex() || f.box.outputs[0].satoshis!==1) throw Error('noncanonical initial box')
  if(initial.phase!==0n || initial.ctorArgs().find(a=>a.name==='origin').value!==outpoint(f.foreign,0)) throw Error('unanchored box')
  if(bsv.crypto.Hash.sha256ripemd160(Buffer.from(initial.owner,'hex')).toString('hex')!==match[1]) throw Error('foreign owner mismatch')
  const ledger=new Ledger([f.foreign,f.box]); let previous=null
  for(const tx of entries) {
   const expected=previous?outpoint(previous,0)+outpoint(previous,1):outpoint(f.foreign,0)+outpoint(f.box,0)
   if(prevouts(tx)!==expected) throw Error('origin continuity failure')
   ledger.accept(tx);previous=tx
  }
  return {valid:true,origin:f.foreign.id+'_0',tip:previous?previous.id+':0':f.foreign.id+':0',ordinalInput:0,ordinalOutput:0}
 } catch(e) {return {valid:false,error:e.message}}
}
module.exports={S,bsv,C,fixture,transition,verify,verifyHistory,Ledger,pay,output,outpoint}
