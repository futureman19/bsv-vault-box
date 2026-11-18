'use strict';
// PUBLIC TEST SCALAR 2. Explicit fixture import only; never reads window.CWI.
const {PrivateKey,BigNumber,ECDSA}=require('@bsv/sdk/primitives');
const {DERIVATION}=require('./wallet');
const {canonical}=require('./browser-wallet-crypto');
function createFixtureProvider(){
 const key=new PrivateKey(2),publicKey=key.toPublicKey().toString();
 const calls=[],control={mode:'ok',delayMs:0};
 const exact=(a,b)=>{if(canonical(a)!==canonical(b))throw Error('Fixture: wrong WalletInterface arguments');};
 const record=(method,args)=>calls.push({method,args:JSON.parse(JSON.stringify(args))});
 const wallet={
  async waitForAuthentication(args){record('waitForAuthentication',args);exact(args,{});return {authenticated:control.mode!=='reject'};},
  async getNetwork(args){record('getNetwork',args);exact(args,{});return {network:control.mode==='wrong-network'?'main':'test'};},
  async getPublicKey(args){record('getPublicKey',args);if(!args.identityKey)exact(args,{...DERIVATION,forSelf:true});else exact(args,{identityKey:true});return {publicKey:control.mode==='account-switch'?new PrivateKey(3).toPublicKey().toString():publicKey};},
  async createSignature(args){
   record('createSignature',args);const hash=args.hashToDirectlySign;
   exact(Object.keys(args).sort(),['protocolID','keyID','counterparty','hashToDirectlySign'].sort());exact({...args,hashToDirectlySign:undefined},{...DERIVATION,hashToDirectlySign:undefined});
   if(!Array.isArray(hash)||hash.length!==32||hash.some(n=>!Number.isInteger(n)||n<0||n>255))throw Error('Exact 32-byte direct hash required');
   if(control.delayMs)await new Promise(r=>setTimeout(r,control.delayMs));
   if(control.mode==='reject')throw Error('Fixture approval rejected');
   return {signature:control.mode==='malicious'?[48,6,2,1,1,2,1,1]:ECDSA.sign(new BigNumber(hash),key,true).toDER()};
  }
 };
 return {wallet,calls,control,publicKey,identityKey:publicKey,mode:'PUBLIC-SCALAR-2-FIXTURE'};
}
module.exports={createFixtureProvider};
if(typeof window!=='undefined')window.BoxSVBrowserWalletFixture=module.exports;
