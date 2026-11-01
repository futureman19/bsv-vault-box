'use strict'
const assert=require('node:assert/strict'),fs=require('node:fs')
// Before extension exists, exercise the established baseline: behavioral RED,
// not a missing-module exception. Once present, only the new module is tested.
const M=require(fs.existsSync(require('node:path').join(__dirname,'../src/four-ordinal-sponsored.js'))?'../src/four-ordinal-sponsored':'../src/four-ordinal')
const {bsv,S,pay,output}=M
const f=M.fixture(),bob=f.bob.publicKey.toString()
function step(source,action,signer=f.alice,mutate,opts={}) {return M.transition(f,source,action,signer,bob,mutate,{sponsor:f.bob,...opts})}
function vm(r,source,index=0){return M.vmInput(r.tx,source.outputs[index],index).success}
function witness(r,source,field,value,index=0){const args=M.C.abiCoder.parseCallData(r.tx.inputs[index].script.toHex()).args;const a=args.find(a=>a.name===field);a.value=typeof value==='function'?value(a.value,r):value;r.tx.inputs[index].setScript(M.C.fromHex(source.outputs[index].script.toHex()).move(...args.map(a=>a.value)).toScript());return r}
describe('four original ordinals with bounded external sponsorship',function(){
 this.timeout(180000)
 let packed,sealed,transferred,opened
 it('adds sponsor input after all five principals and pays exact positive fee through a full lifecycle',()=>{
  let source;const chain=[]
  for(const action of [0,1,2,3,4]){
   const r=step(source,action,action<3?f.alice:f.bob)
   assert.equal(r.result.success,true,JSON.stringify(r.result))
   assert.equal(r.tx.inputs.length,6,'missing external fee sponsor after five principals')
   assert.equal(r.tx.outputs.length,6)
   for(let i=0;i<5;i++)assert.equal(r.tx.outputs[i].satoshis,1)
   assert.equal(r.tx.outputs[5].satoshis,99500)
   assert.equal(r.tx.outputs[5].script.toHex(),pay(bob).toHex())
   assert.equal(r.funding.outputs[0].satoshis-r.tx.outputs[5].satoshis,500)
   source=r.tx;chain.push(source)
  }
  ;[packed,sealed,transferred,opened]=chain
 })
 it('uses distinct sponsor parents across custody steps',()=>{
  const a=step(null,0),b=step(a.tx,1);assert.notEqual(a.funding.id,b.funding.id,'sponsor cannot be double spent across lifecycle')
 })
 it('accepts boundary fees and exact no-change sponsorship',()=>{
  for(const fee of [1,10000])assert.equal(step(sealed,2,f.alice,null,{fee}).result.success,true)
  const r=step(sealed,2,f.alice,null,{funding:500,fee:500});assert.equal(r.result.success,true);assert.equal(r.tx.outputs.length,5)
 })
 for(const fee of [0,-1,10001])it('compiled covenant rejects fee '+fee,()=>{const r=step(sealed,2,f.alice,null,{fee});assert.equal(vm(r,sealed),false)})
 for(const [name,mutate] of [
  ['change diversion',t=>{t.outputs[5]=output(pay(f.alice.publicKey.toString()),99500)}],
  ['extra output',t=>t.addOutput(output(pay(bob)))],
  ['missing change',t=>t.outputs.pop()],
  ...Array.from({length:5},(_,i)=>['principal diversion '+i,t=>{t.outputs[i]=output(pay(bob))}]),
  ['reordered sponsor',t=>{[t.inputs[0],t.inputs[5]]=[t.inputs[5],t.inputs[0]]}],
  ['missing sponsor',t=>t.inputs.pop()]
 ])it('compiled covenant rejects '+name,()=>{const r=step(sealed,2,f.alice,mutate);const index=name==='reordered sponsor'?1:0;assert.equal(vm(r,sealed,index),false)})
 for(const [name,value] of [
  ['sponsorSig',''],['sponsor',f.alice.publicKey.toString()],['fundingValue',100001n],['change',99501n],['fundingLocktime','00'],
  ['fundingPrefix',v=>v.slice(0,8)+'02'+v.slice(10)],
  ['fundingPrefix',v=>v.slice(0,-2)+'02'],
  ['fundingPrefix',v=>v.slice(0,82)+'fd'+v.slice(84)]
 ])it('compiled covenant rejects malformed/auth witness '+name,()=>{const r=witness(step(sealed,2),sealed,name,value);assert.equal(vm(r,sealed),false)})
 it('rejects genuinely signed wrong sponsor authorization',()=>{const r=step(sealed,2);witness(r,sealed,'sponsorSig',S.signTx(r.tx,f.alice,sealed.outputs[0].script,1,0));assert.equal(vm(r,sealed),false)})
 for(const field of ['sig','sponsorSig'])for(const type of [0x42,0xc1])it('rejects '+field+' sighash '+type,()=>{const r=step(sealed,2);witness(r,sealed,field,S.signTx(r.tx,field==='sig'?f.alice:f.bob,sealed.outputs[0].script,1,0,type));assert.equal(vm(r,sealed),false)})
 it('actual sponsor P2PKH independently requires authorization',()=>{const r=step(sealed,2);r.tx.inputs[5].setScript(bsv.Script.empty());assert.equal(vm(r,sealed),true);assert.equal(M.verify(r.tx,[sealed,r.funding]).success,false)})
 for(const [name,source,action,signer] of [['sealed withdrawal',()=>sealed,4,()=>f.alice],['old-owner open',()=>transferred,3,()=>f.alice],['old-owner withdraw',()=>opened,4,()=>f.alice]])it('rejects '+name,()=>{const r=step(source(),action,signer());assert.equal(vm(r,source()),false)})
 it('every covenant independently rejects changed principal output',()=>{const r=step(sealed,2,f.alice,t=>{t.outputs[3]=output(pay(bob))});for(let i=0;i<5;i++)assert.equal(vm(r,sealed,i),false)})
})
