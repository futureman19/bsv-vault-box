'use strict'
const assert = require('node:assert/strict')
const M = require('../src/four-ordinal')
describe('four independent ordinals (serialized compiled Script VM)', function () {
 this.timeout(180000)
 let f, chain
 before(function () { f=M.fixture() })
 it('admits four independently existing one-sat inscriptions plus separate control', function () {
  assert.equal(f.assets.length,4,'fixed bundle must contain four independent assets')
  assert.equal(new Set(f.assets.map(t=>t.id)).size,4)
  for(const t of f.assets) assert.equal(t.outputs[0].satoshis,1)
  assert.ok(!f.assets.some(t=>t.id===f.box.id))
 })
 it('executes pack/seal/transfer/open/withdraw and anchored replay with trusted issuer', function () {
  chain=[]; let p
  for(const action of [0,1,2,3,4]) {
   const r=M.transition(f,p,action,action<3?f.alice:f.bob,f.bob.publicKey.toString())
   assert.equal(r.result.success,true,JSON.stringify(r.result));chain.push(r.tx);p=r.tx
  }
  assert.equal(M.verifyHistory(f,chain,M.TRUSTED_POLICY).valid,true)
  for(const tx of chain) {
   assert.equal(tx.inputs.length,5);assert.equal(tx.outputs.length,5)
   assert.equal(tx.outputs.reduce((s,o)=>s+o.satoshis,0),5)
   for(let i=0;i<5;i++) assert.equal(tx.outputs[i].satoshis,1)
  }
  for(const o of chain[4].outputs) assert.equal(o.script.toHex(),M.pay(f.bob.publicKey.toString()).toHex())
 })
 const attack=(name,index,action,who,mutate)=>it(name,function(){
  const r=M.transition(f,chain[index],action,f[who],f.bob.publicKey.toString(),mutate)
  assert.equal(r.result.success,false,JSON.stringify(r.result))
 })
 attack('sealed withdrawal rejected',1,4,'alice')
 attack('former owner open rejected',2,3,'alice')
 attack('former owner withdrawal rejected',3,4,'alice')
 attack('missing input rejected',1,2,'alice',t=>t.inputs.splice(0,1))
 attack('duplicate input rejected',1,2,'alice',t=>{t.inputs[1].outputIndex=0})
 attack('reordered assets rejected',1,2,'alice',t=>{[t.inputs[0],t.inputs[2]]=[t.inputs[2],t.inputs[0]]})
 attack('substituted asset rejected',1,2,'alice',t=>{t.inputs[2].prevTxId=Buffer.from('88'.repeat(32),'hex')})
 attack('extra input rejected',1,2,'alice',t=>t.inputs.push(t.inputs[0]))
 attack('missing output rejected',1,2,'alice',t=>t.outputs.splice(1,1))
 attack('extra output rejected',1,2,'alice',t=>t.addOutput(M.output(M.pay(f.bob.publicKey.toString()))))
 attack('changed output owner rejected with fresh signatures',1,2,'alice',t=>{const c=M.C.fromHex(t.outputs[2].script.toHex());t.outputs[2]=M.output(c.getNewStateScript({phase:2n,owner:f.alice.publicKey.toString()}))})
 attack('changed output code rejected',1,2,'alice',t=>{t.outputs[3]=M.output(M.bsv.Script.fromASM('OP_TRUE'))})
 attack('principal cannot become a fee',1,2,'alice',t=>{t.outputs[0].satoshis=0})
 attack('principal cannot be enlarged',1,2,'alice',t=>{t.outputs[0].satoshis=2})
 attack('withdrawal redirected to old owner rejected',3,4,'bob',t=>{t.outputs[1]=M.output(M.pay(f.alice.publicKey.toString()))})
 it('all five real covenant inputs independently reject ordered-prevout mutation',function(){
  const r=M.transition(f,chain[1],2,f.alice,f.bob.publicKey.toString(),t=>{[t.inputs[0],t.inputs[1]]=[t.inputs[1],t.inputs[0]]})
  for(let i=0;i<5;i++) assert.equal(M.vmInput(r.tx,chain[1].outputs[0],i).success,false,'input '+i)
 })
 it('admission control rejects swapped independent origins in VM',function(){
  const r=M.transition(f,null,0,f.alice,null,t=>{[t.inputs[0],t.inputs[2]]=[t.inputs[2],t.inputs[0]]})
  assert.equal(M.vmInput(r.tx,f.box.outputs[0],4).success,false)
 })
 it('same-label counterfeit can pass standalone VM but fails anchored replay',function(){
  const fake=new M.bsv.Transaction(chain[0].uncheckedSerialize());fake.nLockTime++
  const r=M.transition(f,fake,1,f.alice)
  assert.equal(r.result.success,true)
  assert.equal(M.verifyHistory(f,[fake,r.tx],M.TRUSTED_POLICY).valid,false)
 })
 it('forged certificate rejected at client policy boundary',function(){
  const fake={...f,certificate:{...f.certificate,signature:'00'}}
  assert.equal(M.verifyHistory(fake,chain,M.TRUSTED_POLICY).valid,false)
 })
 it('certificate with changed origin rejected',function(){
  const fake={...f,certificate:{...f.certificate,statement:f.certificate.statement+' '}}
  assert.equal(M.verifyHistory(fake,chain,M.TRUSTED_POLICY).valid,false)
 })
 it('unknown issuer cannot self-declare trust inside bundle',function(){
  const fake=M.fixture({issuer:M.key(9)})
  fake.trustedIssuer=fake.certificate.issuer
  const packed=M.transition(fake,null,0,fake.alice)
  assert.equal(packed.result.success,true,'Script custody does not authenticate the issuer')
  const r=M.verifyHistory(fake,[packed.tx],M.TRUSTED_POLICY)
  assert.equal(r.valid,false);assert.match(r.error,/issuer/)
 })
 it('explicit external policy is mandatory',function(){
  assert.equal(M.verifyHistory(f,chain).valid,false)
 })
 it('changed initial ordered origin anchor rejected',function(){
  const fake={...f,assets:[...f.assets]};[fake.assets[0],fake.assets[2]]=[fake.assets[2],fake.assets[0]]
  assert.equal(M.verifyHistory(fake,chain,M.TRUSTED_POLICY).valid,false)
 })
 it('immutable ordered commitment cannot change in continuation outputs',function(){
  const r=M.transition(f,chain[1],2,f.alice,f.bob.publicKey.toString(),t=>{
   const c=new M.C('77'.repeat(144),2n,f.bob.publicKey.toString());c.phase=2n;c.owner=f.bob.publicKey.toString()
   for(let i=0;i<5;i++) t.outputs[i]=M.output(c.lockingScript)
  })
  for(let i=0;i<5;i++) assert.equal(M.vmInput(r.tx,chain[1].outputs[i],i).success,false)
 })
 it('a well-formed wrong-key issuer signature is rejected',function(){
  const hash=M.bsv.crypto.Hash.sha256(Buffer.from(f.certificate.statement))
  const signature=M.bsv.crypto.ECDSA.sign(hash,M.key(9)).toDER().toString('hex')
  const r=M.verifyHistory({...f,certificate:{...f.certificate,signature}},chain,M.TRUSTED_POLICY)
  assert.equal(r.valid,false);assert.match(r.error,/forged certificate/)
 })
 it('covenant outside allowed parent output range rejects independently',function(){
  const fake=new M.bsv.Transaction(chain[1].uncheckedSerialize());fake.addOutput(M.output(fake.outputs[0].script))
  const r=M.transition(f,fake,2,f.alice,f.bob.publicKey.toString(),t=>{t.inputs[4].outputIndex=5})
  assert.equal(M.vmInput(r.tx,fake.outputs[5],4).success,false)
 })
 it('every ordinal slot stays one-sat in ordered ancestry',function(){
  for(let step=0;step<chain.length;step++) for(let i=0;i<4;i++) {
   const parent=step===0?f.assets[i]:chain[step-1]
   assert.equal(chain[step].inputs[i].prevTxId.toString('hex'),parent.id)
   assert.equal(chain[step].inputs[i].outputIndex,step===0?0:i)
   assert.equal(parent.outputs[step===0?0:i].satoshis,1)
   assert.equal(chain[step].outputs[i].satoshis,1)
  }
 })
 it('exported origin metadata must equal the actual transaction origin',function(){
  const v=M.vectors();v.assets[0].origin='00'.repeat(32)+'_0'
  const r=M.replayVectors(v,M.TRUSTED_POLICY)
  assert.equal(r.valid,false);assert.match(r.error,/origin metadata/)
 })
 it('unsupported evidence format fails closed',function(){
  const v=M.vectors();v.format='UNTRUSTED-OTHER-PROTOCOL'
  assert.equal(M.replayVectors(v,M.TRUSTED_POLICY).valid,false)
 })
 it('raw fixture export reproduces all transactions deterministically',function(){
  const a=M.vectors(),b=M.vectors();assert.deepEqual(a,b)
  assert.equal(a.lifecycle.length,5);assert.equal(a.assets.length,4)
  assert.equal(M.replayVectors(a,M.TRUSTED_POLICY).valid,true)
 })
})
