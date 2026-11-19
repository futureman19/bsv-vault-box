'use strict';
// No keys, discovery, funds, createAction/signAction, HTTP or broadcast in this module.
const crypto=require('crypto');
const bsv=require('../../vault/node_modules/@scrypt-inc/bsv');
const HASH=/^[0-9a-f]{64}$/, PUB=/^(02|03)[0-9a-f]{64}$/;
function check(ok,code){if(!ok)throw Error(code);}
function object(x,keys,code='REQUEST_SHAPE') {
 check(x && Object.getPrototypeOf(x)===Object.prototype,code);
 check(Object.keys(x).sort().join(',')===keys.slice().sort().join(','),code);
}
// Reject getters, exotic objects, cyclic/deep/oversized inputs BEFORE serialization.
function snapshot(value) {
 let nodes=0;
 function visit(v,depth=0){
  check(++nodes<=10000 && depth<=12,'REQUEST_SIZE');
  if(v===null || typeof v==='boolean')return v;
  if(typeof v==='string'){check(v.length<=1000000,'REQUEST_SIZE');return v;}
  if(typeof v==='number'){check(Number.isSafeInteger(v),'REQUEST_NUMBER');return v;}
  check(v && typeof v==='object' && (Array.isArray(v)||Object.getPrototypeOf(v)===Object.prototype),'REQUEST_SHAPE');
  if(Array.isArray(v))check(v.length<=10000&&Object.keys(v).length===v.length&&Object.keys(v).every((k,i)=>String(i)===k),'REQUEST_ARRAY');
  const out=Array.isArray(v)?[]:{};
  for(const k of Object.keys(v)){check(!['__proto__','constructor','prototype'].includes(k),'REQUEST_SHAPE');const d=Object.getOwnPropertyDescriptor(v,k);check(d && 'value' in d,'REQUEST_ACCESSOR');out[k]=visit(d.value,depth+1);}
  return out;
 }
 const result=visit(value);check(JSON.stringify(result).length<=1000000,'REQUEST_SIZE');return result;
}
function canonical(x){if(Array.isArray(x))return '['+x.map(canonical).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';return JSON.stringify(x);}
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const requestHash=r=>sha(canonical(snapshot(r)));
function keyArgs(network){return {protocolID:[1,'boxsv custody'],keyID:network+':owner:v1',counterparty:'self'};}
function pub(key){check(typeof key==='string'&&PUB.test(key),'PUBLIC_KEY');check(bsv.PublicKey.fromString(key).toString()===key,'PUBLIC_KEY');}
function hex(s){check(typeof s==='string'&&s.length>0&&s.length<=800000&&s.length%2===0&&/^[0-9a-f]+$/.test(s),'TX_HEX');return s;}
function parse(s){const t=new bsv.Transaction(hex(s));check(t.uncheckedSerialize()===s,'TX_CANONICAL');return t;}
function validate(r,p,now) {
 object(r,['version','id','expiresAt','network','identityKey','signingKey','action','binding',...(r.action==='Reserve'?[]:['transaction','intent'])]);
 check(r.version===1 && typeof r.id==='string' && /^[a-zA-Z0-9_-]{8,128}$/.test(r.id),'REQUEST_ID');
 check(Number.isSafeInteger(r.expiresAt)&&r.expiresAt>now&&r.expiresAt<=now+300000,'EXPIRED');
 check(r.network===p.network,'NETWORK');check(r.identityKey===p.identityKey,'IDENTITY');check(r.signingKey===p.signingKey,'SIGNING_KEY');
 check(['Reserve','Pack','Seal','Transfer','Open','Withdraw'].includes(r.action),'ACTION');
 object(r.binding,['manifestSha256','designId','metadataSha256','origin','buyerPubkey']);
 check(HASH.test(r.binding.manifestSha256)&&HASH.test(r.binding.metadataSha256)&&/^[a-z0-9-]{1,80}$/.test(r.binding.designId)&&/^[0-9a-f]{64}_[0-9]{1,10}$/.test(r.binding.origin),'BINDING');pub(r.binding.buyerPubkey);
 if(['Reserve','Open','Withdraw'].includes(r.action))check(r.binding.buyerPubkey===p.signingKey,'BUYER');
 if(r.action==='Reserve')return null;
 object(r.transaction,['raw','parents','inputIndex']);object(r.intent,['outputs','maxFee']);
 const t=parse(r.transaction.raw),n=r.transaction.inputIndex;
 check(t.inputs.length>0&&t.inputs.length<=32&&Number.isInteger(n)&&n>=0&&n<t.inputs.length,'INPUT');
 check(t.inputs[n].script.toHex()==='','TARGET_ALREADY_SIGNED');
 check(Array.isArray(r.transaction.parents)&&r.transaction.parents.length===t.inputs.length,'PARENT');
 let total=0;const parents=r.transaction.parents.map(parse),seen=new Set();
 t.inputs.forEach((input,i)=>{const parent=parents[i],id=input.prevTxId.toString('hex'),out=parent.outputs[input.outputIndex],op=id+':'+input.outputIndex;
  check(parent.id===id&&out&&!seen.has(op),'PARENT');seen.add(op);check(Number.isSafeInteger(out.satoshis)&&out.satoshis>=0,'PARENT_VALUE');total+=out.satoshis;check(Number.isSafeInteger(total),'PARENT_VALUE');input.output=out;
 });
 check(Array.isArray(r.intent.outputs)&&r.intent.outputs.length===t.outputs.length&&t.outputs.length>0&&t.outputs.length<=32,'OUTPUT');
 let spent=0;t.outputs.forEach((out,i)=>{const want=r.intent.outputs[i];object(want,['script','satoshis']);check(out.script.toHex()===want.script&&out.satoshis===want.satoshis&&Number.isSafeInteger(out.satoshis)&&out.satoshis>=0,'OUTPUT');spent+=out.satoshis;});
 check(Number.isSafeInteger(spent)&&Number.isSafeInteger(r.intent.maxFee)&&r.intent.maxFee>=0&&total>=spent&&total-spent<=r.intent.maxFee,'FEE');
 const out=t.inputs[n].output;
 // Legacy bsv returns the digest reversed; BRC-100 expects big-endian hash bytes.
 const digest=Buffer.from(bsv.Transaction.sighash.sighash(t,0x41,n,out.script,new bsv.crypto.BN(out.satoshis))).reverse();
 return {t,parents,digest};
}
function verifyDER(signature,digest,key) {
 try{check(typeof signature==='string'&&/^[0-9a-f]{16,144}$/.test(signature)&&signature.length%2===0,'SIGNATURE');const s=bsv.crypto.Signature.fromDER(Buffer.from(signature,'hex'));check(s.toDER().toString('hex')===signature&&s.hasLowS()&&bsv.crypto.ECDSA.verify(digest,s,bsv.PublicKey.fromString(key)),'SIGNATURE');}catch{throw Error('SIGNATURE');}
}
function envelope(r,transactionSignature){return {version:1,kind:'VERIFIED_SIGNATURES_NOT_SENT',requestHash:requestHash(r),network:r.network,identityKey:r.identityKey,signingKey:r.signingKey,transactionSignature};}
function verifyResponse(request,response,policy,{now=Date.now()}={}) {
 const r=snapshot(request),s=snapshot(response);const prepared=validate(r,policy,now);
 object(s,['version','kind','requestHash','network','identityKey','signingKey','transactionSignature','signature'],'RESPONSE_SHAPE');
 check(s.requestHash===requestHash(r),'REQUEST_HASH');const expected=envelope(r,s.transactionSignature);
 for(const k of Object.keys(expected))check(s[k]===expected[k],'RESPONSE_BINDING');
 if(prepared){check(typeof s.transactionSignature==='string'&&s.transactionSignature.endsWith('41'),'SIGHASH');verifyDER(s.transactionSignature.slice(0,-2),prepared.digest,policy.signingKey);}else check(s.transactionSignature===null,'RESPONSE_SHAPE');
 verifyDER(s.signature,Buffer.from(sha(canonical(expected)),'hex'),policy.signingKey);return true;
}
class WalletTransport {
 #provider;#policy;#used=new Set();#busy=false;#closed=false;#cancel=null;
 constructor(provider,{network,identityKey,signingKey,allowSigning=false,timeoutMs=60000}={}) {
  check(['testnet','mainnet'].includes(network),'NETWORK');pub(identityKey);pub(signingKey);
  check(Number.isSafeInteger(timeoutMs)&&timeoutMs>0&&timeoutMs<=120000,'TIMEOUT_CONFIG');
  this.#provider=provider;this.#policy=Object.freeze({network,identityKey,signingKey,allowSigning:allowSigning===true,timeoutMs});
 }
 disconnect(){this.#closed=true;this.#cancel?.('DISCONNECTED');}
 send(){throw Error('SEND_DISABLED');}
 async request(request,{expectedRequestHash,signal}={}) {
  check(!this.#closed,'DISCONNECTED');check(this.#policy.allowSigning,'SIGNING_DISABLED');check(!this.#busy,'BUSY');check(!signal?.aborted,'CANCELLED');
  const r=snapshot(request),hash=requestHash(r);check(typeof expectedRequestHash==='string'&&HASH.test(expectedRequestHash)&&expectedRequestHash===hash,'REQUEST_HASH');
  const prepared=validate(r,this.#policy,Date.now());check(!this.#used.has(r.id),'REPLAY');this.#used.add(r.id);this.#busy=true;
  let timer,dead=false,rejectCancel;const cancelled=new Promise((_,reject)=>{rejectCancel=reject;});
  const cancel=code=>{dead=true;rejectCancel(Error(code));};this.#cancel=cancel;
  const onAbort=()=>cancel('CANCELLED');signal?.addEventListener('abort',onAbort,{once:true});
  timer=setTimeout(()=>cancel('TIMEOUT'),Math.min(this.#policy.timeoutMs,r.expiresAt-Date.now()));
  const alive=()=>{check(!dead&&!this.#closed,'STALE');check(Date.now()<r.expiresAt,'EXPIRED');};
  const call=async(method,args,fields)=>{
   alive();check(typeof this.#provider?.[method]==='function','UNAVAILABLE_'+method);
   let result;try{result=await this.#provider[method](snapshot(args));}catch{throw Error('PROVIDER_ERROR');}
   alive();const clean=snapshot(result);check(clean&&!clean.error,'PROVIDER_ERROR');object(clean,fields,'RESPONSE_SHAPE');return clean;
  };
  const bound=async()=>{
   check((await call('isAuthenticated',{},['authenticated'])).authenticated===true,'AUTH');
   check((await call('getNetwork',{},['network'])).network===r.network,'NETWORK');
   check((await call('getPublicKey',{identityKey:true},['publicKey'])).publicKey===r.identityKey,'IDENTITY');
   check((await call('getPublicKey',{...keyArgs(r.network),forSelf:true},['publicKey'])).publicKey===r.signingKey,'SIGNING_KEY');
  };
  const sign=async(args,digest)=>{const result=await call('createSignature',{...keyArgs(r.network),...args},['signature']);check(Array.isArray(result.signature)&&result.signature.length>=8&&result.signature.length<=72&&result.signature.every(n=>Number.isInteger(n)&&n>=0&&n<=255),'SIGNATURE');const der=Buffer.from(result.signature).toString('hex');verifyDER(der,digest,r.signingKey);return der;};
  const work=async()=>{
   check((await call('waitForAuthentication',{},['authenticated'])).authenticated===true,'AUTH');await bound();
   let transactionSignature=null;
   if(prepared){transactionSignature=(await sign({hashToDirectlySign:Array.from(prepared.digest)},prepared.digest))+'41';await bound();}
   const e=envelope(r,transactionSignature),data=Buffer.from(canonical(e));
   const signature=await sign({data:Array.from(data)},Buffer.from(sha(data),'hex'));await bound();alive();
   const response={...e,signature};verifyResponse(r,response,this.#policy);return Object.freeze(response);
  };
  try{return await Promise.race([work(),cancelled]);}
  finally{dead=true;clearTimeout(timer);signal?.removeEventListener('abort',onAbort);this.#cancel=null;this.#busy=false;}
 }
}
module.exports={WalletTransport,requestHash,verifyResponse,keyArgs};
