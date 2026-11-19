'use strict';
const test=require('node:test'), assert=require('node:assert/strict');
const fs=require('node:fs'), path=require('node:path');
const C=require('../../launch/continuous/common');
const F=require('../../launch/continuous/fixture-wallet');
const {requestFor}=require('../../launch/continuous/engine');
const api=()=>fs.existsSync(path.join(__dirname,'../delivery.js'))?require('../delivery'):{};
const root=path.join(__dirname,'.delivery-runs');fs.mkdirSync(root,{recursive:true});
const config={mode:'offline-rehearsal',network:C.NETWORK,issuerPubkey:F.policy.seller,paymentDepth:2,deliveryDepth:2,termsRef:'TEST-ONLY-NOT-APPROVED'};
const {fixture}=require('./delivery-fixture');
async function setup(t,options={}) {
  assert.equal(typeof api().Delivery,'function','durable reservation delivery missing');
  const file=path.join(fs.mkdtempSync(path.join(root,'case-')),'delivery.sqlite');
  const f=await fixture(options.slug,options.id);
  const wallet=new F.FixtureWallet(),transport=new F.FixtureTransport(options.ambiguous?'ambiguous':'ok');
  let p={satoshis:100,confirmations:2,refs:['a'.repeat(64)+':0']};
  const payment={read:async()=>structuredClone(p)};
  const opts={config,wallet,transport,payment,now:()=>100,hooks:options.hooks};
  let d=new (api().Delivery)(file,opts);t.after(()=>{if(d&&!d.closed)d.close();});
  d.enroll(f.reservation,f.state,f.funding);
  return {file,f,wallet,transport,opts,get d(){return d;},setPayment(x){p=x;},reopen(){d.close();d=new (api().Delivery)(file,opts);return d;}};
}
test('selected Japan reservation reaches signed custody with durable replay and exact buyer',async t=>{
  const x=await setup(t);let r=await x.d.tick('order-1');
  assert.equal(r.status,'LOCAL_ACCEPTED');assert.equal(r.binding.designId,'japan');
  assert.equal(r.binding.origin,x.f.state.binding.origin);assert.equal(x.transport.sent.length,1);
  assert.equal(C.M.C.fromHex(C.tx(r.prepared.raw).outputs[0].script.toHex()).owner,r.binding.buyerPubkey);
  x.reopen();await x.d.tick('order-1');assert.equal(x.transport.sent.length,1);assert.equal(x.wallet.calls,1);
  assert.deepEqual(x.d.inspect('order-1').binding,r.binding);
});
test('no execution with missing terms or default disabled mode',async t=>{
  const x=await setup(t);x.d.close();
  const d=new (api().Delivery)(x.file,{...x.opts,config:{...config,mode:'disabled'}});
  try {await assert.rejects(d.tick('order-1'),/configuration|disabled|policy/);} finally {d.close();}
  assert.equal(x.wallet.calls,0);assert.equal(x.transport.sent.length,0);
});
test('partial and insufficient depth cannot sign; replay observations do not duplicate receipts',async t=>{
  const x=await setup(t);x.setPayment({satoshis:50,confirmations:2,refs:['a'.repeat(64)+':0']});
  await x.d.tick('order-1');x.setPayment({satoshis:100,confirmations:1,refs:['a'.repeat(64)+':0']});
  await x.d.tick('order-1');assert.equal(x.wallet.calls,0);
  x.setPayment({satoshis:100,confirmations:2,refs:['a'.repeat(64)+':0']});await x.d.tick('order-1');
  const before=x.d.inspect('order-1');await x.d.tick('order-1');
  assert.deepEqual(x.d.inspect('order-1'),before);assert.equal(x.transport.sent.length,1);
});
test('immutable reservation buyer, design, origin and address bindings reject conflict',async t=>{
  const x=await setup(t);x.d.enroll(x.f.reservation,x.f.state,x.f.funding);
  for(const patch of [{buyerPubkey:F.policy.seller},{payAddress:'changed'},{inventoryId:'changed'},{priceSats:101}])
    assert.throws(()=>x.d.enroll({...x.f.reservation,...patch},x.f.state,x.f.funding));
  const other=await fixture('morocco');assert.throws(()=>x.d.enroll(other.reservation,other.state,other.funding));
  assert.equal(x.d.inspect('order-1').binding.designId,'japan');
});
test('ambiguous transport holds after restart without signing or replacement funding',async t=>{
  const x=await setup(t,{ambiguous:true});await x.d.tick('order-1');
  const before=x.d.inspect('order-1');assert.ok(before.holds.includes('AMBIGUOUS_SEND'));
  x.reopen();await x.d.tick('order-1');assert.equal(x.wallet.calls,1);assert.equal(x.transport.sent.length,1);
  assert.equal(x.d.inspect('order-1').prepared.raw,before.prepared.raw);
});
test('payment is revalidated after signing; loss prevents any send and survives restart',async t=>{
  const x=await setup(t);const request=x.wallet.request.bind(x.wallet);
  x.wallet.request=async r=>{const v=await request(r);x.setPayment({satoshis:0,confirmations:0,refs:[]});return v;};
  await x.d.tick('order-1');assert.equal(x.transport.sent.length,0);
  assert.ok(x.reopen().inspect('order-1').holds.includes('PAYMENT_FINALITY_LOST'));
});
test('terminal payment loss retains custody history and late excess is held',async t=>{
  const x=await setup(t);await x.d.tick('order-1');
  x.setPayment({satoshis:0,confirmations:0,refs:[]});await x.d.tick('order-1');
  assert.equal(x.d.inspect('order-1').status,'LOCAL_ACCEPTED');
  x.setPayment({satoshis:101,confirmations:3,refs:['a'.repeat(64)+':0','b'.repeat(64)+':1']});await x.d.tick('order-1');
  const r=x.reopen().inspect('order-1');assert.ok(r.holds.includes('EXCESS_PAYMENT'));assert.ok(r.holds.includes('PAYMENT_FINALITY_LOST'));assert.equal(x.transport.sent.length,1);
});
test('external issuer trust is required again on restart',async t=>{
  const x=await setup(t);x.d.close();
  assert.throws(()=>new (api().Delivery)(x.file,{...x.opts,config:{...config,issuerPubkey:F.policy.buyer}}),/policy|issuer/);
});
test('read-only recovery retains exact bytes without database writes',async t=>{
  const x=await setup(t);await x.d.tick('order-1');x.d.close();const before=fs.readFileSync(x.file);
  const r=api().inspectFile(x.file,'order-1',config);assert.equal(r.status,'LOCAL_ACCEPTED');
  assert.deepEqual(fs.readFileSync(x.file),before);
  const d=new (api().Delivery)(x.file,{config,readOnly:true});try{await assert.rejects(d.tick('order-1'),/read-only/);}finally{d.close();}
});
test('confirmed exact bytes can reconcile ambiguity but never clear hold; later loss retains ownership',async t=>{
  const x=await setup(t,{ambiguous:true});await x.d.tick('order-1');const r=x.d.inspect('order-1');
  const txid=C.tx(r.prepared.raw).id,hash='c'.repeat(64);
  const e={kind:'OFFLINE_INCLUSION_FIXTURE',raw:r.prepared.raw,txid,confirmations:2,block:{hash,height:10,confirmations:2,tx:[txid]},tip:{blocks:11,chain:C.NETWORK},detail:{blockhash:hash,blockheight:10,confirmations:2}};
  await x.d.reconcile('order-1',{transactionEvidence:async()=>e});
  let v=x.reopen().inspect('order-1');assert.equal(v.status,'REHEARSED_CONFIRMED');assert.ok(v.holds.includes('AMBIGUOUS_SEND'));
  await x.d.reconcile('order-1',{transactionEvidence:async()=>({...e,raw:'00'})});
  v=x.d.inspect('order-1');assert.equal(v.status,'REHEARSED_CONFIRMED');assert.ok(v.holds.includes('DELIVERY_FINALITY_UNAVAILABLE_OR_LOST'));assert.equal(x.transport.sent.length,1);
});
test('receipt uniqueness spans reservations, processes and restarts',async t=>{
  const x=await setup(t);await x.d.tick('order-1');const second=await fixture('morocco','order-2');
  second.reservation.payAddress=C.M.bsv.PublicKey.fromString(F.policy.seller).toAddress(C.M.bsv.Networks.testnet).toString();
  x.reopen().enroll(second.reservation,second.state,second.funding);
  await x.d.tick('order-2');assert.ok(x.d.inspect('order-2').holds.includes('RECEIPT_CONFLICT'));assert.equal(x.transport.sent.length,1);
});
test('prepared-only restart reuses signed bytes; attempted restart quarantines',async t=>{
  for(const hook of ['afterPrepared','afterAttempt']) {
    const x=await setup(t,{hooks:{[hook]:()=>{throw Error('crash boundary');}}});
    await assert.rejects(x.d.tick('order-1'),/crash boundary/);const raw=x.d.inspect('order-1').prepared.raw;
    delete x.opts.hooks[hook];x.reopen();await x.d.tick('order-1');
    assert.equal(x.wallet.calls,1);assert.equal(x.d.inspect('order-1').prepared.raw,raw);
    assert.equal(x.transport.sent.length,hook==='afterPrepared'?1:0);
    if(hook==='afterAttempt')assert.ok(x.d.inspect('order-1').holds.includes('INTERRUPTED_SEND'));
  }
});
test('expiry and excess never sign, refund or release allocation',async t=>{
  const x=await setup(t);x.opts.now=()=>20000;x.reopen();await x.d.tick('order-1');assert.ok(x.d.inspect('order-1').holds.includes('EXPIRED_RESERVATION'));
  const y=await setup(t);y.setPayment({satoshis:101,confirmations:2,refs:['a'.repeat(64)+':0']});await y.d.tick('order-1');assert.ok(y.d.inspect('order-1').holds.includes('EXCESS_PAYMENT'));assert.equal(y.wallet.calls,0);
});
test('two SQLite connections cannot obtain two signing attempts',async t=>{
  const x=await setup(t);let entered,release;const ready=new Promise(r=>entered=r),gate=new Promise(r=>release=r);
  const request=x.wallet.request.bind(x.wallet);x.wallet.request=async r=>{entered();await gate;return request(r);};
  const other=new (api().Delivery)(x.file,x.opts);
  try {const first=x.d.tick('order-1');await ready;await other.tick('order-1');release();await assert.rejects(first,/concurrent/);assert.equal(x.wallet.calls,1);assert.equal(x.transport.sent.length,0);assert.ok(other.inspect('order-1').holds.includes('INTERRUPTED_PREPARATION'));}
  finally {release();other.close();}
});
test('modified detached metadata and wrong signed transaction are rejected',async t=>{
  const x=await setup(t);const changed=structuredClone(x.f.state);changed.inventory.metadata+=' ';
  assert.throws(()=>x.d.enroll(x.f.reservation,changed,x.f.funding));
  x.wallet.mode='malicious';await assert.rejects(x.d.tick('order-1'),/signed response/);assert.equal(x.transport.sent.length,0);assert.ok(x.reopen().inspect('order-1').holds.includes('PREPARATION_FAILED'));
});
test('existing SaleStore reservation and PaymentWatcher callback drive this same coordinator',async t=>{
  const x=await setup(t);const {SaleStore}=require('../sale'),{PaymentWatcher}=require('../watcher'),Canary=require('../canary');
  const hd=C.M.bsv.HDPrivateKey.fromSeed(Buffer.alloc(32,7),C.M.bsv.Networks.testnet);
  const store=new SaleStore({file:path.join(path.dirname(x.file),'sales.jsonl'),xpub:hd.hdPublicKey.toString(),chain:'regtest'});
  try {
    const f=await fixture('morocco','box-1');
    const listed=store.list({priceSats:100,inventoryId:f.reservation.inventoryId});
    const reservation=store.reserve(listed.id,F.policy.buyer,10000);
    x.d.enroll(reservation,f.state,f.funding);
    const p={satoshis:100,confirmations:2,refs:['b'.repeat(64)+':0']};
    const payment={policy:Canary.policy({chain:'regtest'}),read:async()=>p};
    x.opts.payment=payment;x.reopen();
    const watcher=new PaymentWatcher({chain:'regtest',transport:payment,depth:2});watcher.watch(reservation);
    await watcher.poll(e=>x.d.onPayment(e));await watcher.poll(e=>x.d.onPayment(e));
    assert.equal(x.d.inspect('box-1').status,'LOCAL_ACCEPTED');assert.equal(x.transport.sent.length,1);
    assert.equal(store.get('box-1').state,'LISTED','offline evidence must not promote legacy sale ownership');
  } finally {store.close();}
});
test('actual process exits after durable claim, prepare and attempt recover conservatively',async t=>{
  const {spawnSync}=require('node:child_process');
  for(const hook of ['afterClaim','afterPrepared','afterAttempt']) {
    const x=await setup(t);x.d.close();
    const script=`const {Delivery}=require('./mint/delivery');const F=require('./launch/continuous/fixture-wallet');const d=new Delivery(process.argv[1],{config:JSON.parse(process.argv[3]),wallet:new F.FixtureWallet(),transport:new F.FixtureTransport(),now:()=>100,payment:{read:async()=>({satoshis:100,confirmations:2,refs:['a'.repeat(64)+':0']})},hooks:{[process.argv[2]]:()=>process.exit(75)}});d.tick('order-1').catch(e=>{console.error(e);process.exit(1)});`;
    const child=spawnSync(process.execPath,['-e',script,x.file,hook,JSON.stringify(config)],{cwd:C.ROOT,encoding:'utf8',timeout:30000});
    assert.equal(child.status,75,child.stderr);x.reopen();await x.d.tick('order-1');
    assert.equal(x.wallet.calls,0);assert.equal(x.transport.sent.length,hook==='afterPrepared'?1:0);
    if(hook!=='afterPrepared')assert.ok(x.d.inspect('order-1').holds.includes(hook==='afterClaim'?'INTERRUPTED_PREPARATION':'INTERRUPTED_SEND'));
  }
});
test('configuration without explicit terms fails closed before database creation',()=>{
  assert.throws(()=>new (api().Delivery)(path.join(root,'never.sqlite'),{config:{...config,termsRef:''}}),/terms/);
});
test('upstream custody holds cannot be discarded at enrollment',async t=>{
  const x=await setup(t);
  assert.throws(()=>x.d.enroll(x.f.reservation,{...x.f.state,holds:['FINALITY_LOST']},x.f.funding),/custody.*held/);
  assert.throws(()=>x.d.enroll(x.f.reservation,{...x.f.state,pending:{attempted:true}},x.f.funding),/custody.*pending/);
});
test('receipt-registry tampering is detected before recovery or another send',async t=>{
  const x=await setup(t);await x.d.tick('order-1');x.d.close();
  const {DatabaseSync}=require('node:sqlite');const db=new DatabaseSync(x.file);db.exec('DELETE FROM receipts');db.close();
  assert.throws(()=>api().inspectFile(x.file,'order-1',config),/receipt registry/);
});
module.exports={fixture,config};
