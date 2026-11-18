'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {M,candidate,tx,raw,sha,canonical,ACTIONS}=require('../continuous/common');
const {ConfirmedReceiptObserver}=require('./payment');
const {HttpTransport}=require('../../mint/watcher');
const F=require('../continuous/fixture-wallet');
const {SigningBridge}=require('./signing-bridge');
const {ReceiptRegistry}=require('./receipt-registry');
const {createConfigured}=require('./configured');
const key=n=>new M.bsv.PrivateKey(new M.bsv.crypto.BN(n));
function setup(network='testnet'){
 const dir=fs.mkdtempSync(path.join(process.env.TMPDIR||os.tmpdir(),'configured-'));
 const registry=new ReceiptRegistry(path.join(dir,'registry.sqlite'));
 const c=candidate(),genesis=F.issue(c),buyer=key(4),policy={...F.policy,buyer:buyer.publicKey.toString(),network};
 const binding={designId:c.item.slug,designIdentity:c.item.id,manifestSha256:c.manifestSha256,buyerPubkey:policy.buyer,metadataSha256:c.metadataSha256,origin:tx(genesis.foreign).id+'_0'};
 const bridge=new SigningBridge({network:network==='mainnet'?'main':'test'});
 const {session}=bridge.connect({network:bridge.network,identityKey:policy.buyer,publicKey:policy.buyer});
 const invoice={id:'configured',network,address:key(8).publicKey.toAddress(network==='mainnet'?M.bsv.Networks.livenet:M.bsv.Networks.testnet).toString(),amount:1000,expiresAt:10000,minimumDepth:2,binding};
 const calls=[],fundingByAction={};
 // Public test roots deliberately do NOT use the legacy synthetic-root identity.
 // Their bytes are pinned by the caller, never selected from wallet responses.
 for(const [index,action] of ACTIONS.entries()){
  const script=M.pay(policy.sponsor),root=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:sha('external public test root:'+action),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty())})).addOutput(M.output(script,100500));
  const funding=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:root.id,outputIndex:0,script:'',output:root.outputs[0]})).addOutput(M.output(script,100000));funding.nLockTime=index+1;
  funding.inputs[0].setScript(M.bsv.Script.fromASM(M.S.signTx(funding,key(3),script,100500,0)+' '+policy.sponsor));
  fundingByAction[action]={funding:raw(funding),fundingRoot:raw(root)};
 }
 policy.fundingByAction=fundingByAction;
 const options={dryRun:true,policy,genesis,binding,session,bridge,invoice,paymentRegistry:registry,paymentObserver:{read:async i=>{calls.push('observe');return {invoiceId:i.id,binding:i.binding,address:i.address,network:i.network,observedAt:1,available:true,historyTxids:[],receipts:[]};}},sponsor:key(3),getFunding:async r=>structuredClone(fundingByAction[r.action]),sellerWallet:{request:async r=>{
  calls.push(r.action);const f=fundingByAction[r.action];
  const built=M.transition({foreign:tx(genesis.foreign),box:tx(genesis.box)},r.source?tx(r.source):null,r.actionIndex,key(1),policy.buyer,null,undefined,{sponsor:key(3),fundingTx:tx(f.funding)});
  assert.ok(built.result.success);const response={network,requestHash:sha(canonical(r)),signer:policy.seller,raw:raw(built.tx),...f};
  return {...response,signature:M.bsv.crypto.ECDSA.sign(Buffer.from(sha(canonical(response)),'hex'),key(1)).toDER().toString('hex')};
 }}};
 return {options,buyer,calls,file:path.join(dir,'invoice.sqlite'),cleanup(){bridge.invalidate();registry.close();fs.rmSync(dir,{recursive:true,force:true});}};
}
async function approveAll(x,fn){
 let done=false;const pending=fn();pending.then(()=>done=true,()=>done=true);
 while(!done){const envelope=x.options.bridge.peek();if(envelope){x.options.bridge.approve(envelope);x.options.bridge.respond({envelope,signature:M.bsv.crypto.ECDSA.sign(Buffer.from(envelope.hash,'hex'),x.buyer).toDER().toString('hex')});}await new Promise(r=>setImmediate(r));}
 return pending;
}
function paidObserver(x){
 const {invoice:i}=x.options,script=M.bsv.Script.buildPublicKeyHashOut(i.address);
 const t=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:'a'.repeat(64),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty(),2000)})).addOutput(M.output(script,1000));
 const hash='b'.repeat(64),tip={chain:i.network==='mainnet'?'main':'test',blocks:10,bestblockhash:'c'.repeat(64)};
 const data={'chain/info':tip,['address/'+i.address+'/history']:[{tx_hash:t.id,height:9}],['tx/'+t.id]:{txid:t.id,blockhash:hash,blockheight:9,confirmations:2,vout:[{n:0,value:0.00001,scriptPubKey:{hex:script.toHex()}}]},['tx/'+t.id+'/hex']:raw(t),['block/hash/'+hash]:{hash,height:9,confirmations:2,tx:[t.id]}};
 const transport=new HttpTransport({baseUrl:'http://fixture.invalid',chain:i.network,canary:i.network==='mainnet',fetchImpl:async url=>{const route=url.split(i.network==='mainnet'?'/main/':'/test/')[1];assert.ok(Object.hasOwn(data,route));return {ok:true,json:async()=>structuredClone(data[route]),text:async()=>data[route]};}});
 return new ConfirmedReceiptObserver({transport,network:i.network,clock:()=>2});
}
for(const network of ['testnet','mainnet'])test('configured factory binds non-fixture buyer and '+network,async()=>{
 const x=setup(network);let e;
 try{
  e=createConfigured(x.file,x.options);assert.equal(e.inspect().binding.buyerPubkey,x.options.policy.buyer);
  e.transport={send:async()=>assert.fail('dry run must never invoke send')};
  const result=e.reserve('reserve');
  for(let i=0;i<50&&!x.options.bridge.peek();i++)await new Promise(r=>setImmediate(r));
  const envelope=x.options.bridge.peek();assert.ok(envelope);assert.equal(envelope.request.network,network);assert.deepEqual(x.calls,['observe']);
  x.options.bridge.approve(envelope);
  x.options.bridge.respond({envelope,signature:M.bsv.crypto.ECDSA.sign(Buffer.from(envelope.hash,'hex'),x.buyer).toDER().toString('hex')});
  assert.equal((await result).stage,'RESERVED');
  await e.advance('pack','Pack');await e.advance('seal','Seal');
  await assert.rejects(e.advance('unpaid','Transfer'),/payment/);
  e.paymentObserver=paidObserver(x);
  await e.advance('transfer','Transfer');
  // The adapter closes over this supplied callback; swapping a response cannot
  // select a new trust anchor, even if that funding has valid signatures.
  const originalOpen=x.options.policy.fundingByAction.Open;
  x.options.policy.fundingByAction.Open=x.options.policy.fundingByAction.Withdraw;
  await assert.rejects(e.advance('bad-open','Open'),/caller-pinned funding/);
  assert.equal(x.options.bridge.peek(),null);assert.equal(e.inspect().pending,null);
  x.options.policy.fundingByAction.Open=originalOpen;
  for(const action of ['Open','Withdraw'])await approveAll(x,()=>e.advance(action.toLowerCase(),action));
  assert.equal(e.inspect().stage,'WITHDRAWN');assert.equal(e.inspect().withdrawnOwner,x.options.policy.buyer);
  assert.ok(Object.values(e.inspect().provenance).every(Boolean));
  assert.equal(e.inspect().history.length,5);
  for(const h of e.inspect().history){assert.equal(h.response.network,network);assert.equal(h.receipt.network,network);assert.equal(h.receipt.dryRun,true);assert.equal(h.receipt.chainInclusion,false);assert.deepEqual({funding:h.response.funding,fundingRoot:h.response.fundingRoot},x.options.policy.fundingByAction[h.action]);}
  assert.equal(e.inspect().chainInclusion,false);assert.equal(e.inspect().launchReady,false);
  assert.deepEqual(e.inspect().payment.observations.slice(-2).map(o=>o.receipts.length),[1,1]);
  e.close();e=null;e=createConfigured(x.file,x.options);assert.equal(e.inspect().stage,'WITHDRAWN');
 }finally{e?.close();x.cleanup();}
});
test('configuration rejects mismatched trust/session and send opt-in',()=>{
 const x=setup();try{
  assert.throws(()=>createConfigured(x.file,{...x.options,sendEnabled:true}),/disabled/);
  for(const dryRun of [undefined,false])assert.throws(()=>createConfigured(x.file,{...x.options,dryRun}),/dryRun/);
  assert.throws(()=>createConfigured(x.file,{...x.options,policy:{...x.options.policy,fundingByAction:undefined}}),/fundingByAction/);
  const pins=x.options.policy.fundingByAction;
  assert.throws(()=>createConfigured(x.file,{...x.options,policy:{...x.options.policy,fundingByAction:{...pins,Open:pins.Withdraw}}}),/reused funding/);
  assert.throws(()=>createConfigured(x.file,{...x.options,session:{...x.options.session,network:'main'}}),/network/);
  assert.throws(()=>createConfigured(x.file,{...x.options,binding:{...x.options.binding,buyerPubkey:F.policy.buyer}}),/buyer/);
  assert.throws(()=>createConfigured(x.file,{...x.options,paymentRegistry:undefined}),/registry/);
 }finally{x.cleanup();}
});
test('bridge disconnection during reservation cannot persist consent',async()=>{
 const x=setup();let e;try{
  e=createConfigured(x.file,x.options);
  const pending=e.reserve('disconnect');
  const rejected=assert.rejects(pending,/disconnected/i);
  for(let i=0;i<50&&!x.options.bridge.peek();i++)await new Promise(r=>setImmediate(r));
  assert.ok(x.options.bridge.peek());x.options.bridge.invalidate();await rejected;
  assert.equal(e.inspect().stage,'AVAILABLE');assert.equal(e.inspect().pending,null);
 }finally{e?.close();x.cleanup();}
});
test('configured Transfer rechecks payment after seller signs and retains bytes without acceptance',async()=>{
 const x=setup();let e;try{
  const seller=x.options.sellerWallet;
  x.options.sellerWallet={request:async r=>{const response=await seller.request(r);if(r.action==='Transfer')e.paymentObserver={clock:()=>3,read:async()=>{throw Error('offline after signing');}};return response;}};
  e=createConfigured(x.file,x.options);await approveAll(x,()=>e.reserve('reserve'));
  for(const a of ['Pack','Seal'])await e.advance(a,a);
  e.paymentObserver=paidObserver(x);await assert.rejects(e.advance('transfer','Transfer'),/payment/);
  const s=e.inspect();assert.equal(s.stage,'SEALED');assert.equal(s.pending.attempted,false);assert.ok(s.pending.response.raw);assert.ok(s.holds.includes('PAYMENT_UNAVAILABLE'));
 }finally{e?.close();x.cleanup();}
});
test('caller pins do not bypass amount, script or funding signature checks',()=>{
 const x=setup();try{
  for(const mutate of [t=>t.outputs[0].satoshis--,t=>t.outputs[0].setScript(M.pay(key(9).publicKey.toString())),t=>t.inputs[0].setScript(M.bsv.Script.empty())]){
   const policy=structuredClone(x.options.policy),t=tx(policy.fundingByAction.Open.funding);mutate(t);policy.fundingByAction.Open.funding=raw(t);
   assert.throws(()=>createConfigured(x.file,{...x.options,policy}));assert.equal(fs.existsSync(x.file),false);
  }
 }finally{x.cleanup();}
});
test('restart pins externally trusted policy',()=>{
 const x=setup();let e;try{
  e=createConfigured(x.file,x.options);e.close();e=null;
  const wrongSponsor={...x.options,policy:{...x.options.policy,sponsor:key(9).publicKey.toString()},sponsor:{publicKey:key(9).publicKey}};
  assert.throws(()=>createConfigured(x.file,wrongSponsor));
  const pins=x.options.policy.fundingByAction;
  const changed={...x.options,policy:{...x.options.policy,fundingByAction:{...pins,Pack:pins.Seal,Seal:pins.Pack}}};
  assert.throws(()=>createConfigured(x.file,changed),/trusted initialization/);
  e=createConfigured(x.file,x.options);assert.equal(e.inspect().stage,'AVAILABLE');
 }finally{e?.close();x.cleanup();}
});
