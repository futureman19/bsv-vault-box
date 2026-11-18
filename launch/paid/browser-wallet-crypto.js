'use strict';
const {BigNumber, Signature, PublicKey, ECDSA, Hash}=require('@bsv/sdk/primitives');
const hex=a=>Array.from(a,n=>n.toString(16).padStart(2,'0')).join('');
function canonical(x){if(Array.isArray(x))return '['+x.map(canonical).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';return JSON.stringify(x);}
const digest=x=>hex(Hash.sha256(Array.from(new TextEncoder().encode(canonical(x)))));
function verify(hash,bytes,pub){try{
 if(!/^[a-f0-9]{64}$/.test(hash)||!Array.isArray(bytes)||bytes.some(n=>!Number.isInteger(n)||n<0||n>255))return false;
 const s=Signature.fromDER(bytes);
 return hex(s.toDER())===hex(bytes)&&s.s.cmp(new BigNumber('7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a0',16))<=0&&ECDSA.verify(new BigNumber(hash,16),s,PublicKey.fromString(pub));
}catch{return false;}}
module.exports={canonical,digest,verify,hex};
