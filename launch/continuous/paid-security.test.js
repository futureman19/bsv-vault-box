'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const C=require('./common'),I=require('./integrated-wallet'),E=require('./engine'),A=require('../wallet-transport/adapter');
const {createPaid}=require('./paid');
async function setup(t,options={}){const dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));let e=await createPaid(dir,options);t.after(()=>{e.close();fs.rmSync(dir,{recursive:true,force:true});});return {dir,get e(){return e;},async reopen(){e.close();e=await createPaid(dir);return e;},async seal(){await e.reserve('reserve-security-1');await e.advance('pack-security-1','Pack');await e.advance('seal-security-1','Seal');}};}
test('malicious responses, rejection, disconnect and cancellation cannot reserve; rejected IDs stay consumed after restart',async t=>{
 const x=await setup(t);for(const mode of ['malicious','reject','disconnect','wrong-buyer','wrong-network']){x.e.wallet.mode=mode;await assert.rejects(x.e.reserve('reject-'+mode+'-001'));assert.equal(x.e.inspect().stage,'AVAILABLE');}
 await x.reopen();await assert.rejects(x.e.reserve('reject-malicious-001'),/UNIQUE/);assert.equal(x.e.inspect().stage,'AVAILABLE');
 const f=await require('../wallet-transport/fixture').fixture(),adapter=new A.WalletTransport(f.provider,f.policy),controller=new AbortController();controller.abort();await assert.rejects(adapter.request(f.request,{expectedRequestHash:A.requestHash(f.request),signal:controller.signal}),/CANCELLED/);assert.equal(f.calls.length,0);
});
test('binding, identity and signed custody byte substitutions fail independent receiving boundary',async t=>{
 const wallet=await I.fixtureWallet(),dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));const e=E.createDemo(path.join(dir,'journal.sqlite'),{wallet,policy:wallet.policy});t.after(()=>{e.close();fs.rmSync(dir,{recursive:true,force:true});});
 await e.reserve('reserve-security-1');for(const a of ['Pack','Seal','Transfer'])await e.advance('signed-'+a+'-001',a);
 const s=e.inspect(),request=E.requestFor(s,'signed-Open-001','Open'),response=await wallet.request(request);E.verifyResponse(s,request,response);
 for(const change of [r=>r.authorizations[0].request.binding.origin='ab'.repeat(32)+'_0',r=>r.authorizations[0].request.identityKey=s.policy.seller,r=>r.authorizations[0].response.signature='00',r=>{const v=C.tx(r.raw);v.outputs[0].satoshis=2;r.raw=C.raw(v);},r=>r.authorizations[0].request.network='mainnet']){const r=structuredClone(response);change(r);assert.throws(()=>E.verifyResponse(s,request,r));}
 assert.equal(e.inspect().stage,'TRANSFERRED');
});
test('ambiguous paid send survives restart and reconciliation without replacement or ownership projection',async t=>{
 const x=await setup(t);await x.seal();x.e.transport.mode='ambiguous';await assert.rejects(x.e.pay(),/hold/);const before=x.e.inspect();assert.equal(before.stage,'SEALED');assert.ok(before.holds.includes('AMBIGUOUS_SEND'));assert.equal(x.e.transport.sent.length,3,'Pack, Seal and one attempted Transfer');
 await x.reopen();await assert.rejects(x.e.pay(),/hold/);assert.equal(x.e.transport.sent.length,0);const r=x.e.inspect().delivery;assert.equal(r.prepared.raw,before.delivery.prepared.raw);
 const txid=C.tx(r.prepared.raw).id,hash='c'.repeat(64),e={kind:'OFFLINE_INCLUSION_FIXTURE',raw:r.prepared.raw,txid,confirmations:2,block:{hash,height:10,confirmations:2,tx:[txid]},tip:{blocks:11,chain:C.NETWORK},detail:{blockhash:hash,blockheight:10,confirmations:2}};
 await x.e.delivery.reconcile('box-1',{transactionEvidence:async()=>e});assert.equal(x.e.inspect().delivery.status,'REHEARSED_CONFIRMED');assert.ok(x.e.inspect().holds.includes('AMBIGUOUS_SEND'));assert.equal(x.e.inspect().stage,'SEALED');
 await x.e.delivery.reconcile('box-1',{transactionEvidence:async()=>({...e,raw:'00'})});assert.ok(x.e.inspect().holds.includes('DELIVERY_FINALITY_UNAVAILABLE_OR_LOST'));
});
test('terminal payment loss blocks buyer signing and preserves transfer history across restart',async t=>{
 const x=await setup(t);await x.seal();await x.e.pay();const before=x.e.inspect();x.e.setPayment({satoshis:0,confirmations:0,refs:[]});await assert.rejects(x.e.advance('after-loss-open','Open'),/reconciliation hold/);
 await x.reopen();const after=x.e.inspect();assert.equal(after.stage,'TRANSFERRED');assert.equal(after.delivery.prepared.raw,before.delivery.prepared.raw);assert.ok(after.holds.includes('PAYMENT_FINALITY_LOST'));assert.equal(after.authorizations.length,before.authorizations.length);
});
test('prepared buyer transaction survives restart without a second wallet request',async t=>{
 const hooks={afterPrepared:()=>{if(hooks.enabled)throw Error('prepared crash');}},x=await setup(t,{hooks});await x.seal();await x.e.pay();hooks.enabled=true;
 await assert.rejects(x.e.advance('prepared-open-001','Open'),/prepared crash/);const before=x.e.inspect();assert.ok(before.pending&&!before.pending.attempted);
 await x.reopen();await x.e.advance('prepared-open-001','Open');const after=x.e.inspect();assert.equal(after.stage,'OPENED');assert.equal(after.authorizations.length,before.authorizations.length);assert.equal(after.history.at(-1).response.raw,before.pending.response.raw);
});
test('integrated ambiguous transport mode also holds the existing Pack action',async t=>{
 const x=await setup(t);await x.e.reserve('ambiguous-pack-reserve');x.e.transport.mode='ambiguous';await assert.rejects(x.e.advance('ambiguous-pack-001','Pack'),/Ambiguous/);assert.ok(x.e.inspect().holds.includes('AMBIGUOUS_SEND'));
});
test('pending authorization persisted before callback; abrupt process exit blocks restart without signing',async t=>{
 const dir=fs.mkdtempSync(path.join(__dirname,'.integration-test-'));const {spawnSync}=require('node:child_process');
 const script=`require('./launch/continuous/paid').createPaid(process.argv[1],{authorize:async()=>process.exit(75)}).then(e=>e.reserve('interrupted-reserve-001')).catch(e=>{console.error(e);process.exit(1)});`;
 const child=spawnSync(process.execPath,['-e',script,dir],{cwd:C.ROOT,encoding:'utf8',timeout:30000});assert.equal(child.status,75,child.stderr);
 // A crashed SaleStore lock is deliberately NOT automatically reclaimed. Documented operator step,
 // after confirming this owned child has exited; no ledger or allocation reset.
 assert.ok(fs.existsSync(path.join(dir,'sales.jsonl.lock')));fs.unlinkSync(path.join(dir,'sales.jsonl.lock'));
 const e=await createPaid(dir);try{assert.ok(e.inspect().holds.includes('INTERRUPTED_WALLET_HANDOFF'));assert.equal(e.inspect().authorizations[0].status,'PENDING');await assert.rejects(e.reserve('new-reserve-001'),/interrupted/);assert.equal(e.inspect().stage,'AVAILABLE');}finally{e.close();fs.rmSync(dir,{recursive:true,force:true});}
});
