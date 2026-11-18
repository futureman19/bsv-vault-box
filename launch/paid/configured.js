'use strict';
// Configured integration, NOT chain delivery. Caller supplies trusted genesis and
// policy out-of-band on every restart, plus ONE shared durable receipt registry.
// No provider discovery, keys, funding creation, RPC defaults or broadcast here.
const {assert,M,candidate}=require('../continuous/common');
const {Engine,Journal,reduce}=require('../continuous/engine');
const {CustodyWallet}=require('./custody-wallet');
const Payment=require('./payment');
const {ReceiptRegistry}=require('./receipt-registry');
const DISABLED='Network sending disabled: configured custody supports explicit dryRun:true only';
class ConfiguredEngine extends Engine {
 inspect(){return {...super.inspect(),configured:true,dryRun:true,sendEnabled:false,deliveryAvailable:true,deliveryLimitation:DISABLED};}
}
/**
 * createConfigured(file, {policy, genesis, binding, bridge, session, invoice,
 *   paymentObserver, paymentRegistry, sponsor, getFunding, sellerWallet,
 *   dryRun:true, sendEnabled=false}) -> Engine
 * genesis is the inventory shape (foreign, box, originRoot, boxRoot, metadata,
 * envelope). Only the frozen launch candidate is supported. bridge is the
 * WalletInterface signing bridge (session, withRequest, signHash), already
 * connected by the caller. Factory never connects a wallet or starts HTTP.
 * policy.fundingByAction pins {funding,fundingRoot} raw hex for each of the five
 * custody actions before opening the journal. These are trust anchors, NOT
 * evidence of chain inclusion or unspentness. Amounts and scripts remain fixed.
 * Seller signs Pack/Seal/Transfer; the bridge signs Reserve/Open/Withdraw.
 * Only local VM receipts are recorded; no send transport is invoked.
 * close() closes only the journal; caller owns bridge and shared registry.
 */
function createConfigured(file,options={}){
 const {policy,genesis,binding,bridge,session,invoice,paymentObserver,paymentRegistry,sponsor,getFunding,sellerWallet,dryRun,sendEnabled=false}=options;
 assert.equal(sendEnabled,false,DISABLED);
 assert.equal(dryRun,true,'explicit dryRun:true required');
 assert.ok(['testnet','mainnet'].includes(policy?.network),'explicit policy network required');
 assert.ok(policy.fundingByAction,'caller-pinned fundingByAction required');
 if(policy.dryRun!==undefined)assert.equal(policy.dryRun,true,'policy dryRun mismatch');
 for(const role of ['buyer','seller','sponsor']){
  assert.match(policy[role],/^0[23][0-9a-f]{64}$/,'invalid policy '+role);
  assert.ok(M.bsv.PublicKey.isValid(policy[role]),'invalid policy '+role);
 }
 assert.equal(binding?.buyerPubkey,policy.buyer,'binding buyer mismatch');
 assert.equal(session?.network,policy.network==='mainnet'?'main':'test','session network mismatch');
 assert.equal(session.publicKey,policy.buyer,'session buyer mismatch');
 assert.ok(M.bsv.PublicKey.isValid(session.identityKey),'invalid session identity');
 assert.deepEqual(bridge?.session,session,'bridge session mismatch');
 assert.equal(typeof bridge?.withRequest,'function','explicit signing bridge required');
 assert.equal(typeof bridge?.signHash,'function','explicit signing bridge required');
 assert.equal(typeof paymentObserver?.read,'function','explicit payment observer required');
 assert.ok(paymentRegistry instanceof ReceiptRegistry&&!paymentRegistry.fixtureOnly,'shared durable registry required');
 assert.equal(sponsor?.publicKey?.toString(),policy.sponsor,'sponsor mismatch');
 assert.equal(typeof getFunding,'function','explicit funding adapter required');
 assert.equal(typeof sellerWallet?.request,'function','explicit seller adapter required');
 const initial=structuredClone({type:'INIT',candidate:candidate(),inventory:genesis,policy:{...policy,dryRun:true},binding});
 // Validate before opening a journal or allocating an address.
 const initialState=reduce(null,initial,initial);
 const fixedInvoice=structuredClone(invoice),fixedSession=structuredClone(session);
 Payment.validateInvoice(initialState,fixedInvoice);
 const journal=new Journal(file,()=>initial,{trustedInitial:initial});
 try{
  const custody=new CustodyWallet({transport:bridge,session:fixedSession,binding:initial.binding,getState:()=>journal.read().state,sponsor,getFunding,sellerWallet});
  const wallet={request:request=>bridge.withRequest(request,()=>custody.request(request))};
  const engine=new ConfiguredEngine(journal,{wallet,transport:{send:async()=>{throw Error(DISABLED);}},paymentObserver,paymentRegistry});
  Payment.configure(engine,fixedInvoice);
  return engine;
 }catch(error){journal.close();throw error;}
}
module.exports={createConfigured};
