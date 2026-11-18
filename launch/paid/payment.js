'use strict';
// Bounded, read-only payment evidence; explicit transport and shared live registry.
// No network default, wallet, allocation, broadcast or sale-price selection.
// PaymentWatcher is deliberately NOT used: it skips zero/low-depth observations
// and deduplicates amount/refs without block identity, hiding finality loss.
const {assert,M,NETWORK,canonical,sha,tx}=require('../continuous/common');
const {HttpTransport}=require('../../mint/watcher');
const {ReceiptRegistry,journalOwner}=require('./receipt-registry');
const CHAINS=Object.freeze({'offline-fixture':'regtest',testnet:'test',mainnet:'main'});
const MAX_RECEIPTS=1000;
const hash=x=>typeof x==='string'&&/^[0-9a-f]{64}$/.test(x);
function validateInvoice(s,i){
 assert.ok(i&&typeof i==='object','invoice required');
 assert.deepEqual(Object.keys(i).sort(),['address','amount','binding','expiresAt','id','minimumDepth','network']);
 assert.match(i.id,/^[a-zA-Z0-9-]{1,80}$/);
 assert.deepEqual(i.binding,s.binding,'invoice binding mismatch');
 assert.ok(Object.hasOwn(CHAINS,i.network),'invoice network mismatch');
 assert.equal(i.network,s.policy.network||NETWORK,'invoice network mismatch');
 assert.equal(M.bsv.Address.fromString(i.address).network.name,i.network==='mainnet'?'livenet':'testnet','invoice address network');
 assert.equal(M.bsv.Address.fromString(i.address).type,'pubkeyhash','invoice address must be P2PKH');
 for(const k of ['amount','expiresAt','minimumDepth'])assert.ok(Number.isSafeInteger(i[k])&&i[k]>0,'invalid invoice '+k);
 assert.ok(i.minimumDepth<=10000,'depth bound');
}
function gate(s,action){if(!s.payment)return;if(action==='Reserve')assert.ok(s.payment.addressFresh&&s.holds.length===0,'fresh zero-history payment address required');if(action==='Transfer')assert.ok(s.payment.qualified&&s.holds.length===0,'confirmed exact payment required');}
function verifyEvidence(e,network){
 assert.ok(e&&hash(e.txid)&&hash(e.tip?.bestblockhash),'invalid transaction evidence');
 assert.ok(Object.hasOwn(CHAINS,network),'payment network');
 assert.equal(e.tip.chain,CHAINS[network],'payment evidence chain mismatch');
 assert.match(e.raw,/^(?:[0-9a-f]{2})+$/);const t=tx(e.raw);
 assert.equal(t.id,e.txid,'payment transaction identity');assert.equal(t.toBuffer().toString('hex'),e.raw,'payment raw bytes');
 const {detail:d,block:b,tip}=e;
 assert.equal(d.txid,e.txid);assert.ok(Array.isArray(d.vout)&&d.vout.length===t.outputs.length,'payment outputs');
 t.outputs.forEach((o,n)=>{assert.equal(d.vout[n].n,n);assert.equal(d.vout[n].scriptPubKey?.hex,o.script.toHex());assert.ok(Number.isSafeInteger(o.satoshis)&&o.satoshis>=0);assert.equal(d.vout[n].value,o.satoshis/1e8,'exact payment sats');});
 assert.ok(hash(b.hash)&&hash(d.blockhash),'payment block hash');assert.equal(b.hash,d.blockhash);
 assert.ok(Number.isSafeInteger(tip.blocks)&&Number.isSafeInteger(b.height)&&b.height>=0&&b.height<=tip.blocks,'payment block height');
 const depth=tip.blocks-b.height+1;
 assert.equal(d.blockheight,b.height);assert.equal(d.confirmations,depth);assert.equal(b.confirmations,depth);assert.equal(e.confirmations,depth);
 assert.ok(Array.isArray(b.tx)&&b.tx.includes(t.id),'payment block membership');
 return t;
}
function validateObservation(i,o){
 assert.equal(o.invoiceId,i.id,'observation invoice mismatch');assert.deepEqual(o.binding,i.binding,'observation binding mismatch');assert.equal(o.address,i.address,'observation address mismatch');assert.equal(o.network,i.network,'observation network mismatch');
 assert.ok(Number.isSafeInteger(o.observedAt)&&o.observedAt>=0,'observation time');assert.equal(typeof o.available,'boolean');assert.ok(Array.isArray(o.receipts)&&o.receipts.length<=MAX_RECEIPTS,'receipt bound');
 if(!o.available){assert.equal(o.receipts.length,0);assert.equal(typeof o.error,'string');return;}
 assert.ok(Array.isArray(o.historyTxids)&&o.historyTxids.length<=MAX_RECEIPTS&&o.historyTxids.every(hash),'complete payment history required');
 assert.equal(new Set(o.historyTxids).size,o.historyTxids.length,'duplicate history IDs');
 const seen=new Set();let total=0,tip=null;
 for(const r of o.receipts){
  const t=verifyEvidence(r.evidence,i.network);assert.ok(o.historyTxids.includes(t.id),'receipt missing from history');assert.equal(r.txid,t.id);assert.ok(Number.isSafeInteger(r.index)&&r.index>=0&&r.index<t.outputs.length,'receipt index');
  assert.equal(r.outpoint,t.id+':'+r.index,'receipt outpoint');assert.ok(!seen.has(r.outpoint),'duplicate receipt');seen.add(r.outpoint);
  const out=t.outputs[r.index];assert.equal(r.satoshis,out.satoshis);assert.equal(r.script,out.script.toHex());assert.equal(r.script,M.bsv.Script.buildPublicKeyHashOut(i.address).toHex(),'receipt address');
  assert.ok(r.satoshis>0,'zero receipt');total+=r.satoshis;assert.ok(Number.isSafeInteger(total),'receipt total overflow');
  const stamp=canonical(r.evidence.tip);if(tip!==null)assert.equal(stamp,tip,'inconsistent payment tip');tip=stamp;
 }
}
function paymentEvent(s,e){
 if(e.type==='PAYMENT_CONFIG'){
  validateInvoice(s,e.invoice);assert.equal(s.stage,'AVAILABLE','configure before Reserve');assert.equal(s.pending,null);assert.ok(!s.payment,'immutable payment configuration');
  assert.equal(typeof e.registryId,'string');assert.equal(typeof e.registryOwner,'string');
  s.payment={invoice:e.invoice,registryId:e.registryId,registryOwner:e.registryOwner,addressFresh:false,observations:[],fingerprints:[],qualified:false,acceptedReceipts:[]};return s;
 }
 assert.ok(s.payment,'missing payment configuration');const p=s.payment,o=e.observation;validateObservation(p.invoice,o);
 const fingerprint=sha(canonical(o));
 if(p.observations.length)assert.ok(o.observedAt>=p.observations.at(-1).observedAt,'payment clock moved backwards');
 p.observations.push(o);p.fingerprints.push(fingerprint);
 const hold=reason=>{if(!s.holds.includes(reason))s.holds.push(reason);};
 if(!o.available){hold('PAYMENT_UNAVAILABLE');if(p.acceptedReceipts.length)hold('FINALITY_LOST');p.qualified=false;return s;}
 if(e.purpose==='reserve'){assert.equal(s.stage,'AVAILABLE');if(o.historyTxids.length||o.receipts.length)hold('PAYMENT_ADDRESS_USED');else p.addressFresh=true;}
 const eligible=o.receipts.filter(r=>r.evidence.confirmations>=p.invoice.minimumDepth);
 const previous=p.acceptedReceipts;
 if(previous.some(old=>!eligible.some(r=>r.outpoint===old.outpoint&&r.evidence.block.hash===old.blockHash)))hold('FINALITY_LOST');
 const total=o.receipts.reduce((n,r)=>n+r.satoshis,0);
 if(total>p.invoice.amount)hold('EXCESS_PAYMENT');
 // Once paid on time, subsequent reads after expiry do not revoke that receipt.
 if(o.observedAt>=p.invoice.expiresAt&&!previous.length)hold('PAYMENT_EXPIRED');
 p.qualified=total===p.invoice.amount&&eligible.length===o.receipts.length&&s.holds.length===0;
 if(p.qualified&&!previous.length)p.acceptedReceipts=eligible.map(r=>({outpoint:r.outpoint,blockHash:r.evidence.block.hash}));
 return s;
}
function registryFor(engine,invoice){
 if(!engine.paymentRegistry&&invoice.network===NETWORK)engine.paymentRegistry=new ReceiptRegistry(engine.journal.db,{fixtureOnly:true});
 const registry=engine.paymentRegistry;assert.ok(registry instanceof ReceiptRegistry,'explicit shared durable payment registry required');
 if(invoice.network!==NETWORK)assert.ok(!registry.fixtureOnly,'live invoice requires shared durable registry');
 return registry;
}
function configure(engine,invoice,{registry}={}){
 assert.ok(!engine.busy,'operation busy');const {state:s,head}=engine.journal.read();validateInvoice(s,invoice);
 if(registry)engine.paymentRegistry=registry;
 if(s.payment)assert.deepEqual(invoice,s.payment.invoice,'immutable payment configuration');
 else {assert.equal(s.stage,'AVAILABLE','configure before Reserve');assert.equal(s.pending,null);}
 const r=registryFor(engine,invoice),owner=journalOwner(engine.journal);
 if(s.payment){assert.equal(r.id,s.payment.registryId,'payment registry identity mismatch');assert.equal(owner,s.payment.registryOwner,'payment registry owner mismatch');}
 // Commit allocation before journal configuration. A crash burns, never frees, it.
 r.allocate(invoice,owner);
 if(s.payment)return engine.inspect();
 engine.journal.append({type:'PAYMENT_CONFIG',binding:s.binding,invoice:structuredClone(invoice),registryId:r.id,registryOwner:owner},head);return engine.inspect();
}
// Must run under Engine.exclusive: avoids nested locks and persists every read.
async function observeFresh(engine,purpose='poll'){
 assert.ok(engine.busy,'fresh payment observation requires exclusive operation');
 const {state:s,head}=engine.journal.read();assert.ok(s.payment,'missing payment configuration');const i=s.payment.invoice,observer=engine.paymentObserver;
 let observation;
 try{
  const registry=registryFor(engine,i);assert.equal(registry.id,s.payment.registryId,'payment registry identity mismatch');assert.equal(journalOwner(engine.journal),s.payment.registryOwner,'payment registry owner mismatch');
  assert.ok(observer&&typeof observer.read==='function','runtime payment observer required');
  observation=await observer.read(structuredClone(i));validateObservation(i,observation);assert.ok(observation.observedAt>=(s.payment.observations.at(-1)?.observedAt||0),'payment clock moved backwards');
  if(observation.available)registry.claim(i,s.payment.registryOwner,observation.receipts);
 }catch(error){
  let now=Date.now();try{if(typeof observer?.clock==='function')now=observer.clock();}catch{}if(!Number.isSafeInteger(now)||now<0)now=Date.now();
  observation={invoiceId:i.id,binding:i.binding,address:i.address,network:i.network,observedAt:Math.max(now,s.payment.observations.at(-1)?.observedAt||0),available:false,receipts:[],error:String(error.message||error).slice(0,500)};
 }
 engine.journal.append({type:'PAYMENT_OBSERVATION',binding:s.binding,observation,purpose},head);
 return engine.journal.read();
}
async function poll(engine,observer){return engine.exclusive(async()=>{engine.paymentObserver=observer;await observeFresh(engine);return engine.inspect();});}
class ConfirmedReceiptObserver {
 constructor({transport,network,clock=Date.now,maxTransactions=100}={}){
  assert.ok(transport instanceof HttpTransport,'explicit HttpTransport required');assert.ok(Object.hasOwn(CHAINS,network),'explicit payment network required');assert.equal(transport.policy.rpcChain,CHAINS[network],'transport chain mismatch');
  assert.ok(Number.isSafeInteger(maxTransactions)&&maxTransactions>0&&maxTransactions<=1000,'history bound');
  this.transport=transport;this.network=network;this.clock=clock;this.maxTransactions=maxTransactions;
 }
 async read(invoice){
  assert.equal(invoice.network,this.network,'observer network mismatch');const h=this.transport;
  const tip=await h.json('chain/info');assert.equal(tip.chain,CHAINS[invoice.network],'payment evidence chain mismatch');assert.ok(hash(tip.bestblockhash)&&Number.isSafeInteger(tip.blocks),'invalid chain tip');
  const rows=await h.json('address/'+encodeURIComponent(invoice.address)+'/history');assert.ok(Array.isArray(rows)&&rows.length<=this.maxTransactions,'bounded complete address history required');
  const ids=new Map();for(const row of rows){assert.ok(hash(row.tx_hash)&&Number.isSafeInteger(row.height)&&row.height>=0,'invalid history row');if(ids.has(row.tx_hash))assert.equal(ids.get(row.tx_hash),row.height,'conflicting duplicate history');ids.set(row.tx_hash,row.height);}
  const receipts=[],script=M.bsv.Script.buildPublicKeyHashOut(invoice.address).toHex();
  for(const [id,height] of [...ids].sort(([a],[b])=>a.localeCompare(b))){
   // Genuinely unconfirmed rows wait; an accepted receipt disappearing still holds.
   if(height===0)continue;
   const evidence=await h.transactionEvidence(id),t=verifyEvidence(evidence,invoice.network);
   assert.equal(evidence.block.height,height,'history block height mismatch');assert.deepEqual(evidence.tip,tip,'chain changed during payment scan');
   t.outputs.forEach((o,index)=>{if(o.script.toHex()===script&&o.satoshis>0)receipts.push({outpoint:id+':'+index,txid:id,index,satoshis:o.satoshis,script,evidence});});
   assert.ok(receipts.length<=MAX_RECEIPTS,'receipt bound');
  }
  assert.deepEqual(await h.json('chain/info'),tip,'chain changed during payment scan');
  const observation={invoiceId:invoice.id,binding:invoice.binding,address:invoice.address,network:invoice.network,observedAt:this.clock(),available:true,historyTxids:[...ids.keys()].sort(),receipts};validateObservation(invoice,observation);return observation;
 }
}
module.exports={configure,poll,observeFresh,ConfirmedReceiptObserver,validateInvoice,validateObservation,paymentEvent,gate};
