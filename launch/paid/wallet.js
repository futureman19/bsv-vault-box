'use strict';
// BRC-100 WalletInterface. Never createAction/signAction/send.
const DERIVATION=Object.freeze({protocolID:Object.freeze([1,'boxsv covenant']),keyID:'paid-delivery-v1',counterparty:'self'});
class YoursTransport {
 constructor({wallet,network,verify,timeoutMs=60000}){
  if(!['main','test'].includes(network)||typeof verify!=='function')throw Error('Explicit network and signature verifier required');
  this.wallet=wallet;this.network=network;this.verify=verify;this.timeoutMs=timeoutMs;this.epoch=0;this.session=null;this.busy=false;
 }
 disconnect(){this.epoch++;this.session=null;}
 cancel(){this.disconnect();} // Cannot dismiss wallet prompt; discard late results.
 async bounded(fn,epoch){
  let timer;
  try{const result=await Promise.race([Promise.resolve().then(fn),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Wallet request timed out')),this.timeoutMs);})]);
   if(epoch!==this.epoch)throw Error('Wallet request cancelled/disconnected');
   if(result?.error)throw Error('Wallet rejected: '+String(result.error));return result;
  }finally{clearTimeout(timer);}
 }
 async exclusive(fn){if(this.busy)throw Error('Wallet busy');this.busy=true;try{return await fn(this.epoch);}catch(e){this.disconnect();throw e;}finally{this.busy=false;}}
 async keys(epoch){
  const network=await this.bounded(()=>this.wallet.getNetwork({}),epoch);
  if(network?.network!==this.network)throw Error('Wallet network changed');
  const identity=await this.bounded(()=>this.wallet.getPublicKey({identityKey:true}),epoch);
  const derived=await this.bounded(()=>this.wallet.getPublicKey({...DERIVATION,protocolID:[...DERIVATION.protocolID],forSelf:true}),epoch);
  for(const pub of [identity?.publicKey,derived?.publicKey])if(typeof pub!=='string'||!/^0[23][0-9a-f]{64}$/.test(pub))throw Error('Invalid wallet public key');
  return {network:this.network,identityKey:identity.publicKey,publicKey:derived.publicKey};
 }
 async connect(){return this.exclusive(async epoch=>{
  if(!this.wallet)throw Error('Yours BRC100 transport unavailable');
  const auth=await this.bounded(()=>this.wallet.waitForAuthentication({}),epoch);
  if(auth?.authenticated!==true)throw Error('Wallet authentication rejected');
  this.session=Object.freeze(await this.keys(epoch));return this.session;
 });}
 async signHash(hash){return this.exclusive(async epoch=>{
  if(!this.session)throw Error('Wallet disconnected');
  if(typeof hash!=='string'||!/^[0-9a-f]{64}$/.test(hash))throw Error('Exact digest required');
  const expected=this.session;
  const same=s=>JSON.stringify(s)===JSON.stringify(expected);
  if(!same(await this.keys(epoch)))throw Error('Wallet identity changed');
  const result=await this.bounded(()=>this.wallet.createSignature({...DERIVATION,protocolID:[...DERIVATION.protocolID],hashToDirectlySign:hash.match(/../g).map(x=>parseInt(x,16))}),epoch);
  const sig=result?.signature;
  if(!Array.isArray(sig)||sig.length<8||sig.length>72||sig.some(n=>!Number.isInteger(n)||n<0||n>255)||!this.verify(hash,sig,expected.publicKey))throw Error('Malicious wallet signature');
  if(!same(await this.keys(epoch)))throw Error('Wallet identity changed');
  return sig.map(n=>n.toString(16).padStart(2,'0')).join('');
 });}
}
if(typeof module!=='undefined')module.exports={YoursTransport,DERIVATION};
else globalThis.BoxSVWallet={YoursTransport,DERIVATION};
