'use strict';
const test=require('node:test'), assert=require('node:assert/strict');
const {M,NETWORK,sha,canonical,candidate,raw,tx}=require('../continuous/common');
const F=require('../continuous/fixture-wallet');
const {requestFor,verifyResponse}=require('../continuous/engine');
const {CustodyWallet}=require('./custody-wallet');
const key=n=>new M.bsv.PrivateKey(new M.bsv.crypto.BN(n),M.bsv.Networks.testnet);
const buyer=key(2), sponsor=key(3);
function fundingFor(r){
 const source=tx(r.source), script=M.pay(sponsor.publicKey.toString());
 const root=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:sha('BoxSV sponsor root:'+source.id),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty())})).addOutput(M.output(script,100500));
 const funding=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:root.id,outputIndex:0,script:'',output:root.outputs[0]})).addOutput(M.output(script,100000));
 funding.nLockTime=source.nLockTime+1;
 funding.inputs[0].setScript(M.bsv.Script.fromASM(M.S.signTx(funding,sponsor,script,100500,0)+' '+sponsor.publicKey));
 return {funding:raw(funding),fundingRoot:raw(root)};
}
function harness(){
 const c=candidate(),inventory=F.issue(c);
 const binding={designId:c.item.slug,designIdentity:c.item.id,manifestSha256:c.manifestSha256,buyerPubkey:F.policy.buyer,metadataSha256:c.metadataSha256,origin:tx(inventory.foreign).id+'_0'};
 const state={candidate:c,inventory,binding,policy:F.policy,stage:'AVAILABLE',history:[],holds:[],pending:null};
 const hashes=[],session={network:'test',identityKey:F.policy.buyer,publicKey:F.policy.buyer};
 const transport={session,async signHash(h){hashes.push(h);return M.bsv.crypto.ECDSA.sign(Buffer.from(h,'hex'),buyer).toDER().toString('hex');},createAction(){throw Error('forbidden');},signAction(){throw Error('forbidden');},broadcast(){throw Error('forbidden');}};
 const adapter=new CustodyWallet({transport,session,binding,getState:()=>state,sponsor,getFunding:fundingFor,sellerWallet:new F.FixtureWallet()});
 return {state,adapter,transport,hashes};
}
async function step(h,action){
 const r=requestFor(h.state,'test-'+action,action),response=await h.adapter.request(r);
 verifyResponse(h.state,r,response);
 if(action!=='Reserve')h.state.history.push({action,request:r,response});
 h.state.stage={Reserve:'RESERVED',Pack:'PACKED',Seal:'SEALED',Transfer:'TRANSFERRED',Open:'OPENED',Withdraw:'WITHDRAWN'}[action];
 return {r,response};
}
test('Reserve signs exact canonical response digest; full fixed custody lifecycle VM replays',async()=>{
 const h=harness();const {response}=await step(h,'Reserve');
 const {signature,...signed}=response;assert.equal(h.hashes[0],sha(canonical(signed)));
 for(const a of ['Pack','Seal','Transfer'])await step(h,a);
 for(const a of ['Open','Withdraw']){
  const before=h.hashes.length;const {r,response}=await step(h,a);
  const t=tx(response.raw),source=tx(r.source);
  for(let i=0;i<2;i++){
   const digest=M.bsv.Transaction.sighash.sighash(t,0x41,i,source.outputs[i].script,new M.bsv.crypto.BN(1));
   assert.equal(h.hashes[before+i],Buffer.from(digest).reverse().toString('hex'),'direct SDK hash must be big endian');
  }
  const expected=M.transition({foreign:tx(r.inventory.foreign),box:tx(r.inventory.box)},source,r.actionIndex,buyer,F.policy.buyer,null,undefined,{sponsor});
  assert.equal(response.raw,raw(expected.tx),'byte-identical fixed transaction');
  assert.equal(h.hashes.length,before+3);
 }
 assert.equal(h.state.stage,'WITHDRAWN');
});
test('rejects inconsistent trusted stage before prompting',async()=>{
 const h=harness();h.state.stage='WITHDRAWN';
 await assert.rejects(h.adapter.request(requestFor(h.state,'bad-stage','Pack')),/stage/);
 assert.equal(h.hashes.length,0);
});
test('request mutations and disconnected session never prompt',async()=>{
 const h=harness();await step(h,'Reserve');for(const a of ['Pack','Seal','Transfer'])await step(h,a);
 const r=requestFor(h.state,'open','Open');
 for(const mutate of [r=>r.actionIndex=4,r=>r.source=r.inventory.box,r=>r.inventory.metadata='changed',r=>r.binding.origin='00_0',r=>r.network='mainnet',r=>r.extra=true]){
  const changed=structuredClone(r);mutate(changed);const before=h.hashes.length;
  await assert.rejects(h.adapter.request(changed));assert.equal(h.hashes.length,before);
 }
 h.transport.session=null;const before=h.hashes.length;
 await assert.rejects(h.adapter.request(r),/session/);assert.equal(h.hashes.length,before);
});
test('bad DER, wrong-key and reversed-digest signatures are rejected',async()=>{
 for(const sign of [()=> '00',h=>M.bsv.crypto.ECDSA.sign(Buffer.from(h,'hex'),key(1)).toDER().toString('hex'),h=>M.bsv.crypto.ECDSA.sign(Buffer.from(h,'hex').reverse(),buyer).toDER().toString('hex')]){
  const h=harness();h.transport.signHash=async hash=>sign(hash);
  await assert.rejects(step(h,'Reserve'),/signature/);
 }
});
test('invalid independently supplied funding is rejected before buyer signing',async()=>{
 const h=harness();await step(h,'Reserve');for(const a of ['Pack','Seal','Transfer'])await step(h,a);
 h.adapter.getFunding=r=>{const f=fundingFor(r),t=tx(f.funding);t.outputs[0].satoshis--;return {...f,funding:raw(t)};};
 const before=h.hashes.length;await assert.rejects(step(h,'Open'));assert.equal(h.hashes.length,before);
});
test('seller response network and session changes cannot be accepted',async()=>{
 for(const mode of ['network','disconnect']){
  const h=harness();await step(h,'Reserve');const seller=h.adapter.sellerWallet;
  h.adapter.sellerWallet={request:async r=>{const response=await seller.request(r);if(mode==='network')response.network='mainnet';else h.transport.session=null;return response;}};
  const before=h.hashes.length;await assert.rejects(step(h,'Pack'),mode==='network'?/network/:/session/);assert.equal(h.hashes.length,before);assert.equal(h.state.stage,'RESERVED');
 }
});
test('real YoursTransport BRC100 boundary and continuous Engine complete locally',async()=>{
 const {YoursTransport}=require('./wallet');const {createDemo}=require('../continuous/engine');
 const calls=[];
 const wallet={async waitForAuthentication(){return {authenticated:true};},async getNetwork(){return {network:'test'};},async getPublicKey(){return {publicKey:F.policy.buyer};},async createSignature(args){calls.push(args);return {signature:[...M.bsv.crypto.ECDSA.sign(Buffer.from(args.hashToDirectlySign),buyer).toDER()]};},createAction(){assert.fail('createAction');},signAction(){assert.fail('signAction');},broadcast(){assert.fail('broadcast');}};
 const transport=new YoursTransport({wallet,network:'test',verify:(h,s,p)=>M.bsv.crypto.ECDSA.verify(Buffer.from(h,'hex'),M.bsv.crypto.Signature.fromDER(Buffer.from(s)),M.bsv.PublicKey.fromString(p))});
 const session=await transport.connect(),engine=createDemo(':memory:');
 try{
  engine.wallet=new CustodyWallet({transport,session,binding:engine.inspect().binding,getState:()=>engine.journal.read().state,sponsor,getFunding:fundingFor,sellerWallet:new F.FixtureWallet()});
  await engine.reserve('reserve');for(const a of ['Pack','Seal','Transfer','Open','Withdraw'])await engine.advance('step-'+a,a);
  const s=engine.inspect();assert.equal(s.stage,'WITHDRAWN');assert.equal(s.withdrawnOwner,session.publicKey);assert.ok(Object.values(s.provenance).every(Boolean));assert.equal(s.chainInclusion,false);
  assert.equal(calls.length,7);for(const call of calls){assert.deepEqual(call.protocolID,[1,'boxsv covenant']);assert.equal(call.keyID,'paid-delivery-v1');assert.equal(call.counterparty,'self');}
 }finally{engine.close();}
});
