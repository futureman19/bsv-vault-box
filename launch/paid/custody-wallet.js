'use strict';
// LOCAL ONLY. Caller supplies trusted state, binding, fixed funding and sponsor.
const {M,NETWORK,ACTIONS,assert,sha,canonical,raw,tx}=require('../continuous/common');
const {requestFor,verifyResponse,verifyFunding}=require('../continuous/engine');
const add=(t,p,i)=>t.addInput(new M.bsv.Transaction.Input({prevTxId:p.id,outputIndex:i,script:'',output:p.outputs[i]}));
function prevouts(t){return t.inputs.map(i=>{const n=Buffer.alloc(4);n.writeUInt32LE(i.outputIndex);return Buffer.from(i.prevTxId).reverse().toString('hex')+n.toString('hex');}).join('');}
class CustodyWallet {
 constructor({transport,session,binding,getState,sponsor,getFunding,sellerWallet}){
  assert.equal(typeof transport?.signHash,'function');assert.equal(typeof getState,'function');assert.equal(typeof getFunding,'function');assert.ok(sponsor?.publicKey);
  assert.equal(session?.network,getState().policy.network==='mainnet'?'main':'test','session network mismatch');assert.equal(session.publicKey,binding.buyerPubkey,'session buyer mismatch');
  Object.assign(this,{transport,getState,sponsor,getFunding,sellerWallet,busy:false});this.session=structuredClone(session);this.binding=structuredClone(binding);
 }
 async sign(hash){
  assert.deepEqual(this.transport.session,this.session,'wallet session changed');
  const hex=await this.transport.signHash(hash);
  assert.deepEqual(this.transport.session,this.session,'wallet session changed');
  assert.match(hex,/^[0-9a-f]{16,144}$/,'invalid DER signature');
  const sig=M.bsv.crypto.Signature.fromDER(Buffer.from(hex,'hex'));
  assert.equal(sig.toDER().toString('hex'),hex,'noncanonical DER signature');
  assert.ok(sig.hasLowS()&&M.bsv.crypto.ECDSA.verify(Buffer.from(hash,'hex'),sig,M.bsv.PublicKey.fromString(this.session.publicKey)),'invalid buyer signature');
  return hex;
 }
 async build(r,s){
  const source=tx(r.source),c=M.C.fromHex(source.outputs[0].script.toHex());
  assert.equal(c.owner,this.session.publicKey,'source owner mismatch');assert.equal(c.phase,r.action==='Open'?2n:3n,'source phase mismatch');
  for(const o of source.outputs.slice(0,2)){assert.equal(o.satoshis,1);assert.equal(o.script.toHex(),source.outputs[0].script.toHex());}
  const supplied=await this.getFunding(structuredClone(r));
  const {funding,root}=verifyFunding(s,r,supplied),pub=this.sponsor.publicKey.toString();
  assert.equal(pub,s.policy.sponsor,'sponsor mismatch');
  if(!s.policy.fundingByAction)assert.equal(funding.nLockTime,source.nLockTime+1);
  const t=new M.bsv.Transaction();add(t,source,0);add(t,source,1);add(t,funding,0);
  const script=r.action==='Withdraw'?M.pay(c.owner):c.getNewStateScript({phase:3n,owner:c.owner});
  t.addOutput(M.output(script)).addOutput(M.output(script)).addOutput(M.output(M.pay(pub),99500));t.nLockTime=funding.nLockTime;
  // Stabilize all sequences before any signature.
  for(let attempts=0;;attempts++){
   assert.ok(attempts<=10000,'preimage grinding exhausted');const before=t.inputs.map(i=>i.sequenceNumber).join(',');
   for(let i=0;i<2;i++)M.S.getLowSPreimage(t,source.outputs[i].script,1,i);
   if(before===t.inputs.map(i=>i.sequenceNumber).join(','))break;
  }
  const bytes=funding.toBuffer(),prefix=bytes.subarray(0,47+bytes[41]).toString('hex'),locktime=bytes.subarray(-4).toString('hex');
  for(let i=0;i<2;i++){
   const o=source.outputs[i],pre=M.S.getLowSPreimage(t,o.script,1,i);
   // bsv sighash is reversed relative to SDK direct-hash (big endian).
   const hash=Buffer.from(M.bsv.Transaction.sighash.sighash(t,0x41,i,o.script,new M.bsv.crypto.BN(1))).reverse().toString('hex');
   const sig=(await this.sign(hash))+'41',sponsorSig=M.S.signTx(t,this.sponsor,o.script,1,i);
   t.inputs[i].setScript(M.C.fromHex(o.script.toHex()).move(sig,BigInt(r.actionIndex),this.session.publicKey,sha(Buffer.from(r.source,'hex')),pub,sponsorSig,prefix,locktime,100000n,99500n,pre,prevouts(t)).toScript());
  }
  t.inputs[2].setScript(M.bsv.Script.fromASM(M.S.signTx(t,this.sponsor,funding.outputs[0].script,100000,2)+' '+pub));
  assert.ok(M.verify(t,[source,funding]).success,'buyer transaction VM verification failed');
  return {raw:raw(t),funding:raw(funding),fundingRoot:raw(root)};
 }
 async request(request){
  assert.ok(!this.busy,'custody wallet busy');this.busy=true;
  try{
   const r=structuredClone(request),s=structuredClone(this.getState());
   assert.deepEqual(s.binding,this.binding,'trusted binding changed');assert.deepEqual(r.binding,this.binding,'request binding mismatch');assert.equal(s.policy.buyer,this.session.publicKey,'policy buyer mismatch');assert.equal(r.network,s.policy.network||NETWORK,'wrong request network');assert.equal(this.session.network,r.network==='mainnet'?'main':'test','session network mismatch');assert.match(r.key,/^[a-zA-Z0-9-]{1,80}$/);
   assert.ok(['Reserve',...ACTIONS].includes(r.action),'unsupported action');assert.deepEqual(r,requestFor(s,r.key,r.action),'request differs from trusted state');
   assert.equal(s.stage,({Reserve:'AVAILABLE',Pack:'RESERVED',Seal:'PACKED',Transfer:'SEALED',Open:'TRANSFERRED',Withdraw:'OPENED'})[r.action],'unexpected stage');
   assert.equal(s.holds.length,0,'reconciliation hold');assert.equal(s.pending,null,'pending request');assert.equal(r.action,s.stage==='AVAILABLE'?'Reserve':ACTIONS[s.history.length],'unexpected action');assert.deepEqual(this.transport.session,this.session,'wallet session changed');
   if(!['Reserve','Open','Withdraw'].includes(r.action)){
    assert.ok(this.sellerWallet,'explicit local seller adapter required');const response=await this.sellerWallet.request(r);assert.deepEqual(this.transport.session,this.session,'wallet session changed');assert.equal(canonical(this.getState()),canonical(s),'trusted state changed during signing');verifyResponse(s,r,response);return response;
   }
   const payload=r.action==='Reserve'?{}:await this.build(r,s);
   const response={network:s.policy.network||NETWORK,requestHash:sha(canonical(r)),signer:this.session.publicKey,...payload};
   const signature=await this.sign(sha(canonical(response)));
   assert.equal(canonical(this.getState()),canonical(s),'trusted state changed during signing');
   const result={...response,signature};verifyResponse(s,r,result);return result;
  }finally{this.busy=false;}
 }
}
module.exports={CustodyWallet};
