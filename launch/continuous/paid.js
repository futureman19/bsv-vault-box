'use strict';
// Bounded offline composition; no RPC/HTTP/production transport. Never fund fixtures.
const C=require('./common'),F=require('./fixture-wallet'),E=require('./engine'),I=require('./integrated-wallet');
const {Delivery}=require('../../mint/delivery'),{SaleStore}=require('../../mint/sale'),{PaymentWatcher}=require('../../mint/watcher');
const Canary=require('../../mint/canary'),A=require('../wallet-transport/adapter');
const {DatabaseSync}=require('node:sqlite');
const {assert,fs,path,canonical,sha,tx,M}=C;
async function createPaid(directory,{authorize,hooks={}}={}) {
 const dir=path.resolve(directory);fs.mkdirSync(dir,{recursive:true});
 const wallet=await I.fixtureWallet(authorize),nativeAuthorize=wallet.authorize;
 const auth=new DatabaseSync(path.join(dir,'authorizations.sqlite'));
 auth.exec('PRAGMA synchronous=FULL; CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,payload TEXT NOT NULL,hash TEXT NOT NULL,status TEXT NOT NULL,response TEXT); CREATE TABLE IF NOT EXISTS fixture_payment(id INTEGER PRIMARY KEY,payload TEXT NOT NULL);');
 let interrupted=auth.prepare("SELECT id FROM requests WHERE status='PENDING'").all().length>0;
 wallet.authorize=async(request,hash,mode)=>{
  assert.ok(!interrupted,'interrupted wallet handoff: operator reconciliation required');
  assert.equal(hash,A.requestHash(request));
  auth.prepare('INSERT INTO requests VALUES(?,?,?,?,NULL)').run(request.id,canonical(request),hash,'PENDING');
  try{const response=await nativeAuthorize(request,hash,mode);A.verifyResponse(request,response,wallet.policy.wallet);auth.prepare("UPDATE requests SET status='VERIFIED',response=? WHERE id=?").run(canonical(response),request.id);return response;}
  catch(e){auth.prepare("UPDATE requests SET status='REJECTED' WHERE id=?").run(request.id);throw e;}
 };
 const transport=new F.FixtureTransport();
 const engine=E.createDemo(path.join(dir,'journal.sqlite'),{wallet,policy:wallet.policy,transport,hooks});
 const hd=M.bsv.HDPrivateKey.fromSeed(Buffer.alloc(32,7),M.bsv.Networks.testnet);
 const store=new SaleStore({file:path.join(dir,'sales.jsonl'),xpub:hd.hdPublicKey.toString(),chain:'testnet'});
 const payment={policy:Canary.policy({chain:'testnet'}),read:async()=>JSON.parse(auth.prepare('SELECT payload FROM fixture_payment WHERE id=1').get()?.payload||'{"satoshis":0,"confirmations":0,"refs":[]}')};
 const config={mode:'offline-rehearsal',network:C.NETWORK,issuerPubkey:F.policy.seller,paymentDepth:2,deliveryDepth:2,termsRef:'FIXTURE-ONLY-NOT-APPROVED'};
 const delivery=new Delivery(path.join(dir,'delivery.sqlite'),{config,wallet,transport,payment,now:()=>100,hooks:hooks.delivery});
 const watcher=new PaymentWatcher({chain:'testnet',transport:payment,depth:2});
 let working=false;
 // Deterministic preview construction fixes the allocated sealed inventory ID before reservation.
 const original=engine.inspect(),sealed={...original,history:[]};
 for(const action of ['Pack','Seal']) {const request=E.requestFor(sealed,'inventory-'+action,action),response=await wallet.request(request);sealed.history.push({action,request,response});}
 const preview=I.build(E.requestFor(sealed,'delivery-box-1','Transfer'));
 const funding={raw:C.raw(preview.funding),root:C.raw(preview.fundingRoot),amount:100000,change:99500};
 const inventoryId=tx(sealed.history[1].response.raw).id;
 if(store.all().length===0)store.list({priceSats:100,inventoryId});
 assert.equal(store.all().length,1);assert.equal(store.get('box-1').inventoryId,inventoryId);
 function syncReservation(){
  const s=engine.inspect();if(s.stage==='AVAILABLE')return;
  let r=store.get('box-1');if(!r.buyerPubkey)r=store.reserve(r.id,s.policy.buyer,10000);
  assert.equal(r.buyerPubkey,s.binding.buyerPubkey);assert.equal(r.inventoryId,inventoryId);
  if(s.history.length>=2){const custody={...s,history:s.history.slice(0,2),pending:null};delivery.enroll(r,custody,funding);watcher.watch(r);}
 }
 // No automatic sign, send, receipt or payment on restart.
 syncReservation();
 const inspect=()=>{
  const s=engine.inspect(),r=store.get('box-1');
  const d=s.history.length>=2?delivery.inspect(r.id):null;
  const holds=[...s.holds,...(d?.holds||[]),...(interrupted?['INTERRUPTED_WALLET_HANDOFF']:[])];
  return {...s,holds,paidIntegration:true,reservation:r,delivery:d,walletNetwork:wallet.policy.wallet.network,executionRealm:C.NETWORK,realSendingEnabled:false,authorizations:auth.prepare('SELECT * FROM requests ORDER BY rowid').all()};
 };
 async function exclusive(fn){assert.ok(!working,'operation busy');assert.ok(!interrupted,'interrupted wallet handoff: operator reconciliation required');working=true;try{return await fn();}finally{working=false;}}
 async function advance(key,action){
  syncReservation();
  if(action==='Transfer'){
   assert.equal(key,'delivery-box-1','delivery action key');
   const d=await delivery.tick('box-1');assert.ok(!d.holds.length,'delivery hold: '+d.holds.join(','));assert.equal(d.status,'LOCAL_ACCEPTED','confirmed fixture payment required');
   // Project exactly the already persisted local acceptance, never another send.
   const priorWallet=engine.wallet,priorTransport=engine.transport;
   engine.wallet={request:async request=>{assert.equal(d.prepared.requestHash,sha(canonical(request)));return d.prepared;}};
   engine.transport={send:async hex=>{assert.equal(hex,d.prepared.raw);return d.receipt;}};
   try{await engine.advance(key,action);}finally{engine.wallet=priorWallet;engine.transport=priorTransport;}
  }else{
   if(['Open','Withdraw'].includes(action)){const d=await delivery.observe('box-1');assert.equal(d.holds.length,0,'delivery reconciliation hold');}
   await engine.advance(key,action);
  }
  syncReservation();return inspect();
 }
 return {wallet,transport,delivery,store,payment,config,get busy(){return working||engine.busy;},inspect,
  reserve:key=>exclusive(async()=>{await engine.reserve(key);syncReservation();return inspect();}),
  advance:(key,action)=>exclusive(()=>advance(key,action)),
  pay:()=>exclusive(async()=>{
   assert.ok(engine.inspect().history.length>=2,'seal before payment');
   auth.prepare('INSERT OR REPLACE INTO fixture_payment VALUES(1,?)').run(canonical({satoshis:100,confirmations:2,refs:[sha('public simulated payment:'+inventoryId)+':0']}));
   syncReservation();await watcher.poll(event=>delivery.onPayment(event));
   if(engine.inspect().stage==='SEALED')return advance('delivery-box-1','Transfer');
   await delivery.tick('box-1');return inspect();
  }),
  setPayment:p=>{assert.ok(!working);auth.prepare('INSERT OR REPLACE INTO fixture_payment VALUES(1,?)').run(canonical(p));},
  close:()=>{assert.ok(!working);engine.close();delivery.close();store.close();auth.close();}
 };
}
module.exports={createPaid};
