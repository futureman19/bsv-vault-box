'use strict';
// Read-only export replay. External policy re-derived from documented PUBLIC fixture,
// never trusted from the evidence document. No wallet provider or network is invoked.
const C=require('./common'),E=require('./engine'),I=require('./integrated-wallet');
async function main(){
 const file=process.argv[2];C.assert.ok(file,'Usage: node launch/continuous/paid-replay.js evidence.json');
 const s=JSON.parse(C.fs.readFileSync(file)),wallet=await I.fixtureWallet();
 C.assert.deepEqual(s.policy,wallet.policy);C.assert.deepEqual(s.candidate,C.candidate());
 const binding={designId:s.candidate.item.slug,designIdentity:s.candidate.item.id,manifestSha256:s.candidate.manifestSha256,buyerPubkey:wallet.policy.buyer,metadataSha256:s.candidate.metadataSha256,origin:C.tx(s.inventory.foreign).id+'_0'};C.assert.deepEqual(s.binding,binding);
 C.assert.ok(C.M.verify(C.tx(s.inventory.foreign),[C.tx(s.inventory.originRoot)]).success);C.assert.ok(C.M.verify(C.tx(s.inventory.box),[C.tx(s.inventory.boxRoot)]).success);
 const state={...s,history:[]};
 for(const h of s.history){C.assert.deepEqual(h.request,E.requestFor(state,h.request.key,h.action));E.verifyResponse(state,h.request,h.response);state.history.push(h);}
 C.assert.ok(Object.values(E.provenance(state)).every(Boolean));C.assert.equal(state.history.length,5);
 C.assert.deepEqual(s.delivery.binding,binding);C.assert.equal(s.delivery.reservation.buyerPubkey,binding.buyerPubkey);C.assert.equal(s.delivery.reservation.inventoryId,C.tx(s.history[1].response.raw).id);C.assert.deepEqual(s.delivery.prepared,s.history[2].response);
 C.assert.equal(s.walletNetwork,'testnet');C.assert.equal(s.executionRealm,'offline-fixture');C.assert.equal(s.realSendingEnabled,false);
 console.log(JSON.stringify({file,stage:s.stage,binding,transitions:s.history.map(h=>({action:h.action,txid:C.tx(h.response.raw).id,serializedVM:true})),provenance:E.provenance(state),walletNetwork:s.walletNetwork,executionRealm:s.executionRealm,chainInclusion:false,launchReady:false},null,2));
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});
