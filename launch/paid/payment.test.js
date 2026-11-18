'use strict';
// Synthetic 1000 sats / depth 2 are TEST VALUES, not launch sale terms.
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {createDemo,Engine,Journal,requestFor,reduce}=require('../continuous/engine');
const {M,NETWORK,raw,tx}=require('../continuous/common');
const F=require('../continuous/fixture-wallet');
const {HttpTransport}=require('../../mint/watcher');
const api=fs.existsSync(path.join(__dirname,'payment.js'))?require('./payment'):{};
const root=path.join(process.env.TMPDIR||__dirname,'paid-payment-tests');fs.mkdirSync(root,{recursive:true});
const address=M.bsv.PublicKey.fromString(F.policy.seller).toAddress(M.bsv.Networks.testnet).toString();
function setup(t){const file=path.join(fs.mkdtempSync(path.join(root,'run-')),'journal.sqlite');let e=createDemo(file,{paymentObserver:http({history:false}).observer()});t.after(()=>{e.close();fs.rmSync(path.dirname(file),{recursive:true,force:true});});return {get e(){return e;},file,restart(){e.close();e=new Engine(new Journal(file),{});return e;}};}
function invoice(e,extra={}){return {id:'fixture-invoice-1',binding:e.inspect().binding,address,amount:1000,expiresAt:2000,network:NETWORK,minimumDepth:2,...extra};}
function http({amount=1000,height=9,tipHeight=10,history=true,mutate=()=>{},clock=()=>1000,network=NETWORK,payAddress=address}={}){
 const address=payAddress,chain={testnet:'testnet',mainnet:'mainnet',[NETWORK]:'regtest'}[network];
 const script=M.bsv.Script.buildPublicKeyHashOut(address),transaction=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:'a'.repeat(64),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty(),2000)})).addOutput(M.output(script,amount));
 const id=transaction.id,hash='b'.repeat(64),tip={chain:{regtest:'regtest',testnet:'test',mainnet:'main'}[chain],blocks:tipHeight,bestblockhash:'c'.repeat(64)};
 const detail={txid:id,blockhash:hash,blockheight:height,confirmations:tipHeight-height+1,vout:[{n:0,value:amount/1e8,scriptPubKey:{hex:script.toHex()}}]};
 const block={hash,height,confirmations:tipHeight-height+1,tx:[id]};
 const data={'chain/info':tip,['tx/'+id]:detail,['tx/'+id+'/hex']:raw(transaction),['block/hash/'+hash]:block,['address/'+address+'/history']:history?[{tx_hash:id,height}]:[]};mutate(data,{id,hash,transaction});
 const calls=[];const transport=new HttpTransport({baseUrl:'http://fixture.invalid',chain,canary:network==='mainnet',fetchImpl:async url=>{const route=url.split(network==='testnet'?'/test/':'/main/')[1];calls.push(route);if(!(route in data))throw Error('unexpected HTTP route '+route);return {ok:true,json:async()=>structuredClone(data[route]),text:async()=>data[route]};}});
 return {observer:()=>new api.ConfirmedReceiptObserver({transport,network,clock}),data,calls,id};
}
async function sealed(e){await e.reserve('reserve');await e.advance('pack');await e.advance('seal');}
test('previously seen empty snapshot after payment still detects finality loss',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await api.poll(e,http({history:false}).observer());await api.poll(e,http().observer());assert.equal(e.inspect().payment.qualified,true);await api.poll(e,http({history:false}).observer());assert.ok(e.inspect().holds.includes('FINALITY_LOST'));assert.equal(e.inspect().payment.observations.length,3);
});
test('backwards observer clock becomes durable unavailable hold',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await api.poll(e,http({clock:()=>1100}).observer());await api.poll(e,http({clock:()=>1000}).observer());assert.ok(e.inspect().holds.includes('PAYMENT_UNAVAILABLE'));assert.equal(e.inspect().payment.qualified,false);
});
for(const field of ['binding','address','invoiceId','outpoint','satoshis'])test('reducer rejects forged receipt '+field,async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));const s=e.inspect(),o=await http().observer().read(s.payment.invoice);
 if(field==='binding')o.binding={...o.binding,origin:'wrong'};else if(field==='address')o.address='wrong';else if(field==='invoiceId')o.invoiceId='wrong';else if(field==='outpoint')o.receipts[0].outpoint='d'.repeat(64)+':0';else o.receipts[0].satoshis=1001;
 assert.throws(()=>reduce(s,{type:'PAYMENT_OBSERVATION',binding:s.binding,observation:o}));
});
test('partial can complete; depth loss and later restoration remain held',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await api.poll(e,http({amount:500}).observer());assert.equal(e.inspect().payment.qualified,false);await api.poll(e,http().observer());assert.equal(e.inspect().payment.qualified,true);await api.poll(e,http({tipHeight:9}).observer());assert.ok(e.inspect().holds.includes('FINALITY_LOST'));await api.poll(e,http().observer());assert.equal(e.inspect().payment.qualified,false);
});
test('settled receipt survives expiry and duplicate history rows without double counting',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));const feed=http({mutate:d=>d['address/'+address+'/history'].push({...d['address/'+address+'/history'][0]})});await api.poll(e,feed.observer());assert.equal(e.inspect().payment.qualified,true);await api.poll(e,http({clock:()=>3000}).observer());assert.equal(e.inspect().payment.qualified,true);assert.equal(e.inspect().payment.acceptedReceipts.length,1);
});
test('actual unconfirmed transaction waits without manufacturing block evidence',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));const feed=http({height:0,mutate:(d,{id})=>{delete d['tx/'+id].blockhash;d['tx/'+id].confirmations=0;}});await api.poll(e,feed.observer());assert.deepEqual(e.inspect().holds,[]);assert.equal(e.inspect().payment.qualified,false);assert.ok(!feed.calls.some(x=>x.startsWith('tx/')));
});
test('Transfer freshly detects a vanished cached payment before signing',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await sealed(e);const feed=http();await api.poll(e,feed.observer());feed.data['address/'+address+'/history']=[];
 let signed=0;const wallet=e.wallet;e.wallet={request:async r=>{signed++;return wallet.request(r);}};
 await assert.rejects(e.advance('transfer'),/payment/i);assert.equal(signed,0);assert.ok(e.inspect().holds.includes('FINALITY_LOST'));assert.equal(e.transport.sent.length,2);
});
test('payment loss during async signing retains PREPARED bytes without ATTEMPT',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await sealed(e);const feed=http();await api.poll(e,feed.observer());const wallet=e.wallet;
 e.wallet={request:async r=>{const response=await wallet.request(r);feed.data['address/'+address+'/history']=[];return response;}};
 await assert.rejects(e.advance('transfer'),/payment/i);assert.ok(e.inspect().pending.response.raw);assert.equal(e.inspect().pending.attempted,false);assert.equal(e.transport.sent.length,2);
});
test('resumed PREPARED requires runtime observer and retains exact bytes',async t=>{
 const h=setup(t);api.configure(h.e,invoice(h.e));await sealed(h.e);await api.poll(h.e,http().observer());h.e.hooks.afterPrepared=()=>{throw Error('crash');};await assert.rejects(h.e.advance('transfer'),/crash/);const bytes=h.e.inspect().pending.response.raw;
 h.restart();h.e.transport=new F.FixtureTransport();await assert.rejects(h.e.advance('transfer'),/payment/i);assert.equal(h.e.inspect().pending.response.raw,bytes);assert.equal(h.e.inspect().pending.attempted,false);assert.equal(h.e.transport.sent.length,0);assert.ok(h.e.inspect().holds.includes('PAYMENT_UNAVAILABLE'));
});
test('Reserve requires fresh complete zero-history including unconfirmed rows',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));e.paymentObserver=http({height:0}).observer();await assert.rejects(e.reserve('reserve'),/fresh|history|payment/i);assert.equal(e.inspect().stage,'AVAILABLE');
});
test('configuration after unpaid Reserve is forbidden',async t=>{const {e}=setup(t);await e.reserve('reserve');assert.throws(()=>api.configure(e,invoice(e)),/before Reserve/);});
test('observer has no public network default',()=>{assert.throws(()=>new api.ConfirmedReceiptObserver(),/explicit/);});
test('missing shared registry rejects live configuration even with matching policy',t=>{
 const {e}=setup(t),state=e.inspect();state.policy={...state.policy,network:'testnet'};const engine={journal:{read:()=>({state,head:'unused'})},busy:false};
 assert.throws(()=>api.configure(engine,invoice(e,{network:'testnet'})),/shared durable payment registry/);
});
test('shared registry prevents address and same-invoice reuse across real journals',t=>{
 const {ReceiptRegistry}=require('./receipt-registry'),a=setup(t),b=setup(t),dir=fs.mkdtempSync(path.join(root,'registry-')),r=new ReceiptRegistry(path.join(dir,'shared.sqlite'));t.after(()=>{r.close();fs.rmSync(dir,{recursive:true,force:true});});
 api.configure(a.e,invoice(a.e),{registry:r});assert.throws(()=>api.configure(b.e,invoice(b.e,{id:'other'}),{registry:r}),/UNIQUE/);assert.throws(()=>api.configure(b.e,invoice(b.e),{registry:r}),/owner/);assert.equal(b.e.inspect().payment,undefined);
});
test('unavailable post-sign read preserves exact bytes and no send',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await sealed(e);const observer=http().observer();await api.poll(e,observer);const wallet=e.wallet;let signed;
 e.wallet={request:async r=>{signed=await wallet.request(r);observer.read=async()=>{throw Error('unavailable after sign');};return signed;}};
 await assert.rejects(e.advance('transfer'),/payment/i);assert.equal(e.inspect().pending.response.raw,signed.raw);assert.equal(e.inspect().pending.attempted,false);assert.ok(e.inspect().holds.includes('PAYMENT_UNAVAILABLE'));assert.equal(e.transport.sent.length,2);
});
test('resumed PREPARED with attached observer observes twice and sends identical bytes once',async t=>{
 const h=setup(t);api.configure(h.e,invoice(h.e));await sealed(h.e);const observer=http().observer();await api.poll(h.e,observer);h.e.hooks.afterPrepared=()=>{throw Error('crash');};await assert.rejects(h.e.advance('transfer'),/crash/);const bytes=h.e.inspect().pending.response.raw;
 h.restart();h.e.transport=new F.FixtureTransport();let reads=0;h.e.paymentObserver={clock:observer.clock,read:async i=>{reads++;return observer.read(i);}};
 await h.e.advance('transfer');assert.equal(reads,2);assert.equal(h.e.inspect().history.at(-1).response.raw,bytes);assert.equal(h.e.transport.sent.length,1);
});
test('after ATTEMPT restart never observes or sends again',async t=>{
 const h=setup(t);api.configure(h.e,invoice(h.e));await sealed(h.e);await api.poll(h.e,http().observer());h.e.hooks.afterAttempt=()=>{throw Error('crash');};await assert.rejects(h.e.advance('transfer'),/crash/);const bytes=h.e.inspect().pending.response.raw;
 h.restart();let reads=0;h.e.paymentObserver={read:async()=>{reads++;throw Error('must not read');}};h.e.transport=new F.FixtureTransport();await assert.rejects(h.e.advance('transfer'),/Interrupted send/);assert.equal(reads,0);assert.equal(h.e.transport.sent.length,0);assert.equal(h.e.inspect().pending.response.raw,bytes);assert.ok(h.e.inspect().holds.includes('INTERRUPTED_SEND'));
});
for(const network of ['testnet','mainnet'])test('explicit '+network+' observer verifies matching read-only chain',async t=>{
 const {e}=setup(t),payAddress=M.bsv.PublicKey.fromString(F.policy.seller).toAddress(network==='mainnet'?M.bsv.Networks.livenet:M.bsv.Networks.testnet).toString();const i=invoice(e,{network,address:payAddress});const s=e.inspect();s.policy={...s.policy,network};api.validateInvoice(s,i);
 const feed=http({network,payAddress});const observation=await feed.observer().read(i);api.validateObservation(i,observation);assert.equal(observation.receipts.length,1);
 feed.data['chain/info'].chain='regtest';await assert.rejects(feed.observer().read(i),/chain/);
});
test('payment API is available',()=>{assert.equal(typeof api.configure,'function');assert.equal(typeof api.poll,'function');assert.equal(typeof api.ConfirmedReceiptObserver,'function');});
test('same journal signs invoice, blocks direct delivery, restarts read-only, completes once',async t=>{
 const h=setup(t),i=invoice(h.e);api.configure(h.e,i);assert.deepEqual(requestFor(h.e.inspect(),'reserve','Reserve').invoice,i);
 const count=h.e.inspect().events;api.configure(h.e,i);assert.equal(h.e.inspect().events,count);
 await sealed(h.e);await assert.rejects(h.e.advance('transfer'),/payment/i);
 const feed=http();await api.poll(h.e,feed.observer());const paid=h.e.inspect();assert.equal(paid.payment.qualified,true);assert.equal(paid.payment.observations.length,3);
 await api.poll(h.e,feed.observer());assert.equal(h.e.inspect().events,paid.events+1);
 h.restart();assert.equal(h.e.inspect().payment.qualified,true);h.e.wallet=new F.FixtureWallet();h.e.transport=new F.FixtureTransport();h.e.paymentObserver=feed.observer();
 for(const action of ['Transfer','Open','Withdraw'])await h.e.advance(action.toLowerCase());
 await api.poll(h.e,feed.observer());await h.e.advance('transfer','Transfer');
 assert.equal(h.e.inspect().history.length,5);assert.equal(h.e.transport.sent.length,3);assert.equal(h.e.inspect().stage,'WITHDRAWN');assert.ok(h.e.inspect().provenance.currentCustodyIntegrity);
 assert.ok(feed.calls.every(x=>!x.includes('unspent')&&!x.includes('balance')));
});
test('configuration rejects changed binding, invalid address/network and changes after reservation',async t=>{
 const {e}=setup(t);assert.throws(()=>api.configure(e,invoice(e,{binding:{...e.inspect().binding,origin:'bad'}})),/binding/);
 assert.throws(()=>api.configure(e,invoice(e,{address:'wrong'})));assert.throws(()=>api.configure(e,invoice(e,{network:'mainnet'})),/network/);
 api.configure(e,invoice(e));assert.throws(()=>api.configure(e,invoice(e,{amount:999})),/immutable/);await e.reserve('reserve');assert.throws(()=>api.configure(e,invoice(e,{id:'other'})));
});
for(const [name,opts,hold] of [['zero',{history:false},null],['partial',{amount:999},null],['unconfirmed depth',{tipHeight:9},null],['excess',{amount:1001},'EXCESS_PAYMENT'],['expired',{clock:()=>2000},'PAYMENT_EXPIRED']])test(name+' cannot unlock Transfer',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await sealed(e);await api.poll(e,http(opts).observer());assert.equal(e.inspect().payment.qualified,false);await assert.rejects(e.advance('transfer'));if(hold)assert.ok(e.inspect().holds.includes(hold));assert.equal(e.inspect().payment.observations.length,3);
});
test('reducer PREPARED and ATTEMPT cannot bypass payment gate',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await sealed(e);const s=e.inspect(),request=requestFor(s,'transfer','Transfer'),response=await e.wallet.request(request);
 assert.throws(()=>reduce(structuredClone(s),{type:'PREPARED',binding:s.binding,request,response}),/payment/);
 s.pending={request,response,attempted:false};assert.throws(()=>reduce(s,{type:'ATTEMPT',binding:s.binding,txid:tx(response.raw).id}),/payment/);
});
for(const stage of ['TRANSFERRED','OPENED','WITHDRAWN'])test('finality loss is monotonic without erasing '+stage,async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await sealed(e);await api.poll(e,http().observer());await e.advance('transfer');if(stage!=='TRANSFERRED')await e.advance('open');if(stage==='WITHDRAWN')await e.advance('withdraw');
 await api.poll(e,http({history:false}).observer());assert.equal(e.inspect().stage,stage);assert.ok(e.inspect().holds.includes('FINALITY_LOST'));await api.poll(e,http().observer());assert.ok(e.inspect().holds.includes('FINALITY_LOST'));assert.equal(e.inspect().payment.qualified,false);
});
test('unavailable observation is durable and blocks subsequent happy observation',async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));await api.poll(e,{clock:()=>1000,read:async()=>{throw Error('offline');}});assert.ok(e.inspect().holds.includes('PAYMENT_UNAVAILABLE'));assert.equal(e.inspect().payment.observations[0].available,false);await api.poll(e,http().observer());assert.equal(e.inspect().payment.qualified,false);
});
for(const mutation of ['txid','raw','script','amount','block','height','membership','history','network'])test('HTTP observer rejects inconsistent '+mutation,async t=>{
 const {e}=setup(t);api.configure(e,invoice(e));const feed=http({mutate:(d,{id,hash})=>{if(mutation==='txid')d['tx/'+id].txid='d'.repeat(64);if(mutation==='raw')d['tx/'+id+'/hex']='00';if(mutation==='script')d['tx/'+id].vout[0].scriptPubKey.hex='51';if(mutation==='amount')d['tx/'+id].vout[0].value=0.1;if(mutation==='block')d['block/hash/'+hash].hash='d'.repeat(64);if(mutation==='height')d['tx/'+id].blockheight=8;if(mutation==='membership')d['block/hash/'+hash].tx=[];if(mutation==='history')d['address/'+address+'/history'][0].height=8;if(mutation==='network')d['chain/info'].chain='main';}});
 await api.poll(e,feed.observer());assert.ok(e.inspect().holds.includes('PAYMENT_UNAVAILABLE'));assert.equal(e.inspect().payment.qualified,false);
});
