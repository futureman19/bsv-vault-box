'use strict'
// Public disposable fixtures only. Mandatory sponsor; separate from saved offline proof.
const F=require('./four-ordinal')
const {S,bsv,pay,output,outpoint,verify,vmInput}=F
const C=S.buildContractClass(require('../artifacts/fourOrdinalSponsored.json'))
const origins=assets=>assets.map(t=>outpoint(t,0)).join('')
const prevouts=t=>t.inputs.map(i=>{const n=Buffer.alloc(4);n.writeUInt32LE(i.outputIndex);return Buffer.from(i.prevTxId).reverse().toString('hex')+n.toString('hex')}).join('')
function fixture(){const f=F.fixture();const c=new C(origins(f.assets),0n,f.alice.publicKey.toString());c.phase=0n;c.owner=f.alice.publicKey.toString();f.box.outputs[0]=output(c.lockingScript);return f}
function transition(f,source,action,signer,recipient,mutate,options={}){
 const sponsor=options.sponsor||f.bob,fundingValue=options.funding??100000,change=fundingValue-(options.fee??500)
 // Synthetic, distinct signed one-input/one-output preparation for VM tests only.
 // Node runner ALWAYS supplies a genuine confirmed fundingTx instead.
 let funding=options.fundingTx
 if(!funding){
  const script=pay(sponsor.publicKey.toString())
  const root=new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:bsv.crypto.Hash.sha256(Buffer.from('BOX4 sponsor:'+(source?source.id:f.box.id))).toString('hex'),outputIndex:0,script:'',output:output(script,fundingValue+1000)})).addOutput(output(script,fundingValue+500))
  funding=new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:root.id,outputIndex:0,script:'',output:root.outputs[0]})).addOutput(output(script,fundingValue))
  funding.inputs[0].setScript(bsv.Script.fromASM(S.signTx(funding,sponsor,script,fundingValue+500,0)+' '+sponsor.publicKey.toString()))
 }
 const raw=funding.toBuffer(),prefix=raw.subarray(0,47+raw[41]).toString('hex'),locktime=raw.subarray(-4).toString('hex')
 const pack=action===0,current=pack?f.box:source,parents=pack?[...f.assets,f.box,funding]:[source,funding]
 const c=C.fromHex(current.outputs[0].script.toHex()),tx=new bsv.Transaction()
 for(let i=0;i<5;i++){const p=pack?parents[i]:source,index=pack?0:i;tx.addInput(new bsv.Transaction.Input({prevTxId:p.id,outputIndex:index,script:'',output:p.outputs[index]}))}
 tx.addInput(new bsv.Transaction.Input({prevTxId:funding.id,outputIndex:0,script:'',output:funding.outputs[0]}))
 recipient=recipient||c.owner
 const phase=({0:1,1:2,3:3})[action]??Number(c.phase),owner=action===2?recipient:c.owner
 const script=action===4?pay(owner):c.getNewStateScript({phase:BigInt(phase),owner})
 for(let i=0;i<5;i++)tx.addOutput(output(script))
 if(change>0)tx.addOutput(output(pay(sponsor.publicKey.toString()),change))
 if(mutate)mutate(tx)
 const spent=tx.inputs.map(input=>{const p=parents.find(p=>p.id===input.prevTxId.toString('hex'));if(!p||!p.outputs[input.outputIndex])throw Error('builder requires known actual parents');return p.outputs[input.outputIndex]})
 const isContract=i=>spent[i].script.toHex()===current.outputs[0].script.toHex()
 for(let attempts=0;;attempts++){
  if(attempts>10000)throw Error('preimage stabilization exhausted')
  const before=tx.inputs.map(i=>i.sequenceNumber).join(',')
  for(let i=0;i<tx.inputs.length;i++)if(isContract(i))S.getLowSPreimage(tx,spent[i].script,spent[i].satoshis,i)
  if(before===tx.inputs.map(i=>i.sequenceNumber).join(','))break
 }
 const stable=tx.inputs.map(i=>i.sequenceNumber).join(',')
 for(let i=0;i<tx.inputs.length;i++){
  const o=spent[i]
  if(!isContract(i)){
   const k=tx.inputs[i].prevTxId.toString('hex')===funding.id?sponsor:signer
   tx.inputs[i].setScript(bsv.Script.fromASM(S.signTx(tx,k,o.script,o.satoshis,i)+' '+k.publicKey.toString()))
  }else{
   const pre=S.getLowSPreimage(tx,o.script,o.satoshis,i)
   if(stable!==tx.inputs.map(i=>i.sequenceNumber).join(','))throw Error('sequence changed after stabilization')
   const instance=C.fromHex(o.script.toHex()),parent=bsv.crypto.Hash.sha256(current.toBuffer()).toString('hex')
   tx.inputs[i].setScript(instance.move(S.signTx(tx,signer,o.script,o.satoshis,i),BigInt(action),recipient,parent,sponsor.publicKey.toString(),S.signTx(tx,sponsor,o.script,o.satoshis,i),prefix,locktime,BigInt(fundingValue),BigInt(change),pre,prevouts(tx)).toScript())
  }
 }
 return {tx:new bsv.Transaction(tx.uncheckedSerialize()),result:verify(tx,parents),funding}
}
module.exports={S,bsv,C,key:F.key,TRUSTED_POLICY:F.TRUSTED_POLICY,fixture,transition,origins,pay,output,outpoint,verify,vmInput}
