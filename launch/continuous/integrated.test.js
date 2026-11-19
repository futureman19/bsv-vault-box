'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const C=require('./common');
const fs=require('node:fs'),path=require('node:path');
test('continuous demo pins enrolled derived buyer and verifies BRC reservation',async()=>{
 const I=require('./integrated-wallet');
 const wallet=await I.fixtureWallet();
 const dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));
 const engine=require('./engine').createDemo(path.join(dir,'journal.sqlite'),{wallet,policy:wallet.policy});
 try {const s=await engine.reserve('reserve-brc-001');assert.equal(s.policy.buyer,wallet.policy.wallet.signingKey);assert.notEqual(s.policy.buyer,s.policy.wallet.identityKey);assert.equal(s.stage,'RESERVED');for(const action of C.ACTIONS)await engine.advance('brc-'+action+'-001',action);assert.equal(engine.inspect().stage,'WITHDRAWN');assert.ok(Object.values(engine.inspect().provenance).every(Boolean));}
 finally{engine.close();fs.rmSync(dir,{recursive:true,force:true});}
});
test('paid composition refuses unpaid transfer and binds watcher delivery through restart',async()=>{
 const {createPaid}=require('./paid');const dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));let e=await createPaid(dir);
 try{await e.reserve('paid-reserve-001');await e.advance('paid-pack-001','Pack');await e.advance('paid-seal-001','Seal');
 await assert.rejects(e.advance('delivery-box-1','Transfer'),/payment/);
 const s=await e.pay();assert.equal(s.stage,'TRANSFERRED');assert.equal(s.delivery.status,'LOCAL_ACCEPTED');assert.equal(s.delivery.binding.buyerPubkey,s.policy.buyer);assert.equal(e.payment.policy.chain,'testnet');assert.equal(e.store.policy.chain,'testnet');
 const hex=s.delivery.prepared.raw;await e.pay();assert.equal(e.inspect().delivery.prepared.raw,hex);e.close();e=await createPaid(dir);
 await e.advance('paid-open-001','Open');await e.advance('paid-withdraw-001','Withdraw');assert.equal(e.inspect().stage,'WITHDRAWN');assert.equal(e.inspect().delivery.prepared.raw,hex);
 }finally{e.close();fs.rmSync(dir,{recursive:true,force:true});}
});
test('paid server serves the same journey with explicit browser fixture signing',async()=>{
 const dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));const s=await require('./server').start({dir,port:0,paid:true});
 try{const state=await (await fetch(s.url+'/api/state')).json();assert.equal(state.paidIntegration,true);const html=await(await fetch(s.url)).text();assert.ok(html.includes('/wallet.js'));assert.equal(await(await fetch(s.url+'/api/wallet/request')).text(),'null');}
 finally{await s.close();fs.rmSync(dir,{recursive:true,force:true});}
});
test('transaction construction accepts external owner signatures without owner private key',()=>{
 const f=C.M.fixture(),sponsor=new C.M.bsv.PrivateKey(new C.M.bsv.crypto.BN(3));let calls=0;
 const signer={publicKey:f.alice.publicKey};
 const r=C.M.transition(f,null,0,signer,f.bob.publicKey.toString(),null,undefined,{sponsor,ownerSignature:(t,o,i)=>{calls++;return C.M.S.signTx(t,f.alice,o.script,1,i);}});
 assert.equal(calls,2);assert.equal(r.result.success,true);
});
