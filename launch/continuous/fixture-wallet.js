'use strict';
// PUBLIC deterministic scalars 1/2/3 only. NEVER FUND. No wallet discovery/network.
// This adapter boundary is NOT a real extension implementation.
const {M,NETWORK,sha,canonical,raw,tx,assert}=require('./common');
const key=n=>new M.bsv.PrivateKey(new M.bsv.crypto.BN(n),M.bsv.Networks.testnet);
const seller=key(1), buyer=key(2), sponsor=key(3);
const policy=Object.freeze({seller:seller.publicKey.toString(),buyer:buyer.publicKey.toString(),sponsor:sponsor.publicKey.toString(),network:NETWORK});
const sign=(text,k)=>M.bsv.crypto.ECDSA.sign(Buffer.from(sha(text),'hex'),k).toDER().toString('hex');
function root(tag,pub,value) {
  return new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:sha('continuous public synthetic root:'+tag),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty())})).addOutput(M.output(M.pay(pub),value));
}
function spend(parent,script,k) {
  const t=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:parent.id,outputIndex:0,script:'',output:parent.outputs[0]})).addOutput(M.output(script));
  t.inputs[0].setScript(M.bsv.Script.fromASM(M.S.signTx(t,k,parent.outputs[0].script,parent.outputs[0].satoshis,0)+' '+k.publicKey));
  assert.ok(M.verify(t,[parent]).success);
  return t;
}
function issue(c) {
  const inscription=M.bsv.Script.fromHex(M.pay(policy.seller).toHex()+'0063036f7264510a746578742f706c61696e0040'+Buffer.from(c.metadataSha256).toString('hex')+'68');
  const originRoot=root(c.metadataSha256+':origin',policy.seller,501);
  const foreign=spend(originRoot,inscription,seller);
  const contract=new M.C(M.outpoint(foreign,0),0n,policy.seller);
  contract.phase=0n;contract.owner=policy.seller;
  const boxRoot=root(c.metadataSha256+':box',policy.seller,501);
  const box=spend(boxRoot,contract.lockingScript,seller);
  const statement=JSON.stringify({protocol:'BOXSV-LAUNCH-CERT-1',collectionId:'boxes-from-impossible-places',designId:c.item.slug,collectibleOrigin:foreign.id+'_0',metadataSha256:c.metadataSha256});
  return {foreign:raw(foreign),box:raw(box),originRoot:raw(originRoot),boxRoot:raw(boxRoot),metadata:c.metadata,envelope:{statement,issuer:policy.seller,signature:sign(statement,seller)}};
}
class FixtureWallet {
  constructor(mode='ok'){this.mode=mode;this.calls=0;}
  async request(request) {
    this.calls++;
    if(this.mode==='reject') throw Error('Fixture wallet rejected request');
    if(this.mode==='disconnect') throw Error('Fixture wallet disconnected');
    assert.equal(request.network,NETWORK,'wallet wrong network');
    assert.equal(request.binding.buyerPubkey,policy.buyer,'wallet wrong buyer');
    let signer=request.action==='Reserve'||request.action==='Open'||request.action==='Withdraw'?buyer:seller;
    let payload={};
    if(request.action!=='Reserve') {
      const f={foreign:tx(request.inventory.foreign),box:tx(request.inventory.box)};
      const r=M.transition(f,request.source?tx(request.source):null,request.actionIndex,signer,policy.buyer,null,undefined,{sponsor});
      assert.ok(r.result.success,JSON.stringify(r.result));
      payload={raw:raw(r.tx),funding:raw(r.funding),fundingRoot:raw(r.fundingRoot)};
    }
    const response={network:NETWORK,requestHash:sha(canonical(request)),signer:signer.publicKey.toString(),...payload};
    if(this.mode==='wrong-network') response.network='mainnet';
    if(this.mode==='wrong-buyer') { signer=seller;response.signer=policy.seller; }
    const envelope={...response,signature:sign(canonical(response),signer)};
    if(this.mode==='malicious') envelope.signature='00';
    return envelope;
  }
}
class FixtureTransport {
  constructor(mode='ok'){this.mode=mode;this.sent=[];}
  async send(hex) {
    this.sent.push(hex);
    if(this.mode==='ambiguous') throw Error('Ambiguous fixture send');
    return {network:NETWORK,kind:'LOCAL_VM_ACCEPTED_NOT_CHAIN_INCLUSION',txid:tx(hex).id,rawSha256:sha(Buffer.from(hex,'hex'))};
  }
}
module.exports={policy,issue,FixtureWallet,FixtureTransport};
