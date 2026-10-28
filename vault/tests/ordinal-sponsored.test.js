'use strict'
const assert = require('node:assert/strict')
const M = require('../src/ordinal-pair')
const { fixture, transition, bsv, output, pay, verifyHistory } = M
const f = fixture(), bob = f.bob.publicKey.toString()
const options = { sponsor: f.bob, funding: 100000, fee: 500 }
function step(source, action, signer, mutate, overrides = {}) {
 return transition(f, source, action, signer, bob, mutate, undefined, { ...options, ...overrides })
}
const packed = step(null,0,f.alice).tx
const sealed = step(packed,1,f.alice).tx
const transferred = step(sealed,2,f.alice).tx
const opened = step(transferred,3,f.bob).tx
function vm(tx, source, index=0) {
 const machine = new bsv.Script.Interpreter()
 const o = source.outputs[index]
 return machine.verify(tx.inputs[index].script,o.script,tx,index,M.S.DEFAULT_FLAGS,new bsv.crypto.BN(o.satoshis))
}
function reject(mutate, overrides={}) {
 const r=step(sealed,2,f.alice,mutate,overrides)
 assert.equal(r.result.success,false)
 assert.equal(vm(r.tx,sealed),false,'must fail covenant VM, not merely UTXO admission')
}
function witnessReject(update) {
 const r=step(sealed,2,f.alice)
 const args=M.C.abiCoder.parseCallData(r.tx.inputs[0].script.toHex()).args
 update(args,r)
 r.tx.inputs[0].setScript(M.C.fromHex(sealed.outputs[0].script.toHex()).move(...args.map(a=>a.value)).toScript())
 assert.equal(vm(r.tx,sealed),false)
}
describe('bounded sponsored external custody (serialized Script VM)', function () {
 this.timeout(120000)
 it('funds the full lifecycle without spending either principal sat', () => {
  const chain = [], fundingParents = []; let source
  for (const action of [0,1,2,3,4]) {
   const r = step(source, action, action < 3 ? f.alice : f.bob)
   assert.equal(r.result.success, true, JSON.stringify(r.result))
   assert.equal(r.tx.inputs.length, 3, 'missing fee sponsor input')
   assert.equal(r.tx.outputs.length, 3)
   assert.equal(r.tx.outputs[0].satoshis, 1)
   assert.equal(r.tx.outputs[1].satoshis, 1)
   assert.equal(r.tx.outputs[2].satoshis, 99500)
   assert.equal(r.tx.outputs[2].script.toHex(), pay(bob).toHex())
   chain.push(r.tx); fundingParents.push(r.funding); source = r.tx
  }
  assert.equal(verifyHistory(f, chain, fundingParents).valid, true)
 })
 it('keeps repeated transfer serialized witnesses bounded', () => {
  let r = step(null,0,f.alice); assert.equal(r.result.success,true)
  r = step(r.tx,1,f.alice); assert.equal(r.result.success,true)
  const sizes=[];let owner=f.alice
  for(let i=0;i<12;i++) {
   const buyer=owner===f.alice?f.bob:f.alice
   r=transition(f,r.tx,2,owner,buyer.publicKey.toString(),null,undefined,options)
   assert.equal(r.result.success,true,JSON.stringify(r.result))
   assert.equal(transition(f,r.tx,3,owner,buyer.publicKey.toString(),null,undefined,options).result.success,false)
   owner=buyer
   sizes.push(r.tx.toBuffer().length)
   assert.ok(sizes[i]<30000, `recursive transaction: ${sizes[i]}`)
  }
  assert.ok(Math.max(...sizes)-Math.min(...sizes)<64)
 })
 it('uses a genuinely signed bounded P2PKH funding parent',()=>{
  const r=step(sealed,2,f.alice)
  assert.ok(r.funding.inputs[0].script.toBuffer().length>0)
  assert.equal(M.verify(r.funding,[r.fundingRoot]).success,true)
 })
 it('accepts exact positive fee boundaries and no-change funding',()=>{
  for(const fee of [1,10000]) assert.equal(step(sealed,2,f.alice,null,{fee}).result.success,true)
  const r=step(sealed,2,f.alice,null,{funding:500,fee:500})
  assert.equal(r.result.success,true);assert.equal(r.tx.outputs.length,2)
 })
 it('rejects zero fee even with both signatures',()=>reject(null,{fee:0}))
 it('rejects fee above the 10000-sat cap even with both signatures',()=>reject(null,{fee:10001}))
 it('rejects negative fee',()=>reject(null,{fee:-1}))
 it('rejects change destination diversion with fresh owner and sponsor signatures',()=>reject(t=>{t.outputs[2]=output(pay(f.alice.publicKey.toString()),99500)}))
 it('rejects excess change with fresh signatures',()=>reject(t=>{t.outputs[2].satoshis++}))
 it('rejects missing change with fresh signatures',()=>reject(t=>{t.outputs.pop()}))
 it('rejects extra change outputs with fresh signatures',()=>reject(t=>{t.addOutput(output(pay(bob),1))}))
 it('rejects ordinal principal diversion',()=>reject(t=>{t.outputs[0].satoshis=0}))
 it('rejects control principal diversion',()=>reject(t=>{t.outputs[1].satoshis=0}))
 it('rejects fourth input',()=>reject(t=>{t.addInput(new bsv.Transaction.Input({prevTxId:f.foreign.id,outputIndex:0,script:'',output:f.foreign.outputs[0]}))}))
 it('rejects sponsor input relocation ahead of the ordinal',()=>reject(t=>{[t.inputs[0],t.inputs[2]]=[t.inputs[2],t.inputs[0]]}))
 it('rejects wrong actual sponsor outpoint in covenant VM',()=>reject(t=>{t.inputs[2].prevTxId=Buffer.from('77'.repeat(32),'hex')}))
 it('rejects wrong sponsor output index in covenant VM',()=>reject(t=>{t.inputs[2].outputIndex=1}))
 for(const [name,value] of [['fundingValue',100001n],['change',99499n],['fundingLocktime','00000000'],['parent','00'.repeat(32)],['sponsor',f.alice.publicKey.toString()],['sponsorSig','']]) {
  it(`rejects tampered ${name} witness in covenant VM`,()=>witnessReject(args=>{args.find(a=>a.name===name).value=value}))
 }
 it('rejects oversized parent digest',()=>witnessReject(args=>{args.find(a=>a.name==='parent').value+='00'}))
 it('rejects prefix input-count ambiguity',()=>witnessReject(args=>{const a=args.find(a=>a.name==='fundingPrefix');a.value=a.value.slice(0,8)+'02'+a.value.slice(10)}))
 it('rejects prefix output-count ambiguity',()=>witnessReject(args=>{const a=args.find(a=>a.name==='fundingPrefix');a.value=a.value.slice(0,-2)+'02'}))
 it('rejects noncanonical/long scriptSig boundary',()=>witnessReject(args=>{const a=args.find(a=>a.name==='fundingPrefix');a.value=a.value.slice(0,82)+'fd'+a.value.slice(84)}))
 for(const field of ['sig','sponsorSig']) for(const type of [0x42,0xc1]) {
  it(`rejects ${field} sighash ${type.toString(16)} even if cryptographically signed`,()=>witnessReject((args,r)=>{
   args.find(a=>a.name===field).value=M.S.signTx(r.tx,field==='sig'?f.alice:f.bob,sealed.outputs[0].script,1,0,type)
  }))
 }
 it('requires the actual funding P2PKH authorization too',()=>{
  const r=step(sealed,2,f.alice);r.tx.inputs[2].setScript(bsv.Script.empty())
  assert.equal(vm(r.tx,sealed),true)
  const result=M.verify(r.tx,[sealed,r.funding]);assert.equal(result.success,false);assert.equal(result.input,2)
 })
 it('rejects substituted sponsor locking script despite an asserted key',()=>{
  const funding=new bsv.Transaction(step(sealed,2,f.alice).funding.uncheckedSerialize())
  funding.outputs[0]=output(bsv.Script.fromASM('OP_TRUE'),100000)
  reject(null,{fundingTx:funding})
 })
 it('rejects an actual two-output funding parent',()=>{
  const funding=new bsv.Transaction(step(sealed,2,f.alice).funding.uncheckedSerialize())
  funding.addOutput(output(pay(bob),1));reject(null,{fundingTx:funding})
 })
 it('accepts canonical maximum 108-byte funding scriptSig and rejects 109',()=>{
  for(const size of [108,109]) {
   const funding=new bsv.Transaction(step(sealed,2,f.alice).funding.uncheckedSerialize())
   funding.inputs[0].setScript(bsv.Script.fromHex('61'.repeat(size)))
   const r=step(sealed,2,f.alice,null,{fundingTx:funding})
   assert.equal(r.result.success,size===108)
   assert.equal(vm(r.tx,sealed),size===108)
  }
 })
 it('sponsorship does not let the former owner open or withdraw',()=>{
  for(const [source,action] of [[transferred,3],[opened,4]]) {
   const r=step(source,action,f.alice);assert.equal(r.result.success,false);assert.equal(vm(r.tx,source),false)
  }
 })
 it('sponsorship cannot bypass sealed withdrawal or counterfeit companion code',()=>{
  assert.equal(step(sealed,4,f.alice).result.success,false)
  reject(t=>{t.outputs[1]=output(bsv.Script.fromASM('OP_TRUE'))})
 })
 it('counterfeit copied-label spend is locally valid but not anchored NFT history',()=>{
  const fake=new bsv.Transaction(sealed.uncheckedSerialize());fake.nLockTime++
  const r=step(fake,2,f.alice);assert.equal(r.result.success,true)
  assert.equal(verifyHistory(f,[fake,r.tx],[r.funding]).valid,false)
 })
})
