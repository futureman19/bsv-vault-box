'use strict';
// Explicit PUBLIC fixture only. No fetch, RPC, production key loader or broadcasts.
const {M,NETWORK,sha,raw,tx}=require('../continuous/common');
const F=require('../continuous/fixture-wallet');
const {YoursTransport}=require('./wallet');
const {CustodyWallet}=require('./custody-wallet');
const {HttpTransport}=require('../../mint/watcher');
const {ConfirmedReceiptObserver}=require('./payment');
const key=n=>new M.bsv.PrivateKey(new M.bsv.crypto.BN(n),M.bsv.Networks.testnet);
const sponsor=key(3),buyer=key(2);
const address=key(1).publicKey.toAddress(M.bsv.Networks.testnet).toString();
function funding(r){
 const source=tx(r.source),script=M.pay(sponsor.publicKey.toString());
 const root=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:sha('BoxSV sponsor root:'+source.id),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty())})).addOutput(M.output(script,100500));
 const t=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:root.id,outputIndex:0,script:'',output:root.outputs[0]})).addOutput(M.output(script,100000));t.nLockTime=source.nLockTime+1;
 t.inputs[0].setScript(M.bsv.Script.fromASM(M.S.signTx(t,sponsor,script,100500,0)+' '+sponsor.publicKey));return {funding:raw(t),fundingRoot:raw(root)};
}
async function walletFor(engine){
 const calls=[],control={mode:'ok'};
 const wallet={waitForAuthentication:async()=>({authenticated:true}),getNetwork:async()=>({network:control.mode==='wrong-network'?'main':'test'}),getPublicKey:async()=>({publicKey:control.mode==='wrong-buyer'?key(4).publicKey.toString():F.policy.buyer}),createSignature:async a=>{
  calls.push(structuredClone(a));if(control.mode==='reject')throw Error('Public fixture user-rejected');if(control.mode==='disconnect')throw Error('Public fixture disconnected');
  return {signature:control.mode==='malicious'?[0]:[...M.bsv.crypto.ECDSA.sign(Buffer.from(a.hashToDirectlySign),buyer).toDER()]};
 }};
 const transport=new YoursTransport({wallet,network:'test',verify:(h,s,p)=>{try{const sig=M.bsv.crypto.Signature.fromDER(Buffer.from(s));return sig.hasLowS()&&sig.toDER().equals(Buffer.from(s))&&M.bsv.crypto.ECDSA.verify(Buffer.from(h,'hex'),sig,M.bsv.PublicKey.fromString(p));}catch{return false;}}});
 const session=await transport.connect();
 const adapter=new CustodyWallet({transport,session,binding:engine.inspect().binding,getState:()=>engine.journal.read().state,sponsor,getFunding:funding,sellerWallet:new F.FixtureWallet()});
 return {adapter,transport,calls,control};
}
function receiptFeed(scenario,clock=Date.now){
 const amount=scenario==='partial'?500:scenario==='excess'?1001:1000,height=9,tipHeight=scenario==='shallow'?9:10;
 const script=M.bsv.Script.buildPublicKeyHashOut(address);
 const t=new M.bsv.Transaction().addInput(new M.bsv.Transaction.Input({prevTxId:'a'.repeat(64),outputIndex:0,script:'',output:M.output(M.bsv.Script.empty(),2000)})).addOutput(M.output(script,amount));
 const id=t.id,blockhash='b'.repeat(64),depth=tipHeight-height+1;
 const data={'chain/info':{chain:'regtest',blocks:tipHeight,bestblockhash:'c'.repeat(64)},['address/'+address+'/history']:['none','lost'].includes(scenario)?[]:[{tx_hash:id,height}],['tx/'+id]:{txid:id,blockhash,blockheight:height,confirmations:depth,vout:[{n:0,value:amount/1e8,scriptPubKey:{hex:script.toHex()}}]},['tx/'+id+'/hex']:raw(t),['block/hash/'+blockhash]:{hash:blockhash,height,confirmations:depth,tx:[id]}};
 const calls=[];
 const transport=new HttpTransport({baseUrl:'https://fixture.invalid',chain:'regtest',fetchImpl:async(url,options)=>{
  if(options.method!=='GET'||options.redirect!=='error')throw Error('Fixture GET only');
  const route=url.split('/main/')[1];calls.push(route);if(scenario==='unavailable')throw Error('Fixture indexer unavailable');if(!(route in data))throw Error('Unexpected fixture route');return {ok:true,json:async()=>structuredClone(data[route]),text:async()=>data[route]};
 }});
 return {observer:new ConfirmedReceiptObserver({transport,network:NETWORK,clock}),calls};
}
module.exports={walletFor,receiptFeed,address,funding};
