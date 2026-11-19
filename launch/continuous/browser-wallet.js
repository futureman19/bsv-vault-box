'use strict';
// Explicit synthetic provider only. Does not inspect any injected wallet object.
const {ProtoWallet,PrivateKey}=require('../wallet-transport/node_modules/@bsv/sdk');
const {WalletTransport}=require('../wallet-transport/adapter');
async function sign(request,hash,mode){
 const proto=new ProtoWallet(new PrivateKey(2));
 const provider={waitForAuthentication:async()=>({authenticated:true}),isAuthenticated:async()=>({authenticated:true}),getNetwork:async()=>({network:mode==='wrong-network'?'mainnet':'testnet'}),getPublicKey:args=>mode==='wrong-buyer'?proto.getPublicKey({identityKey:true}):proto.getPublicKey(args),createSignature:args=>{if(mode==='reject')throw Error('fixture reject');if(mode==='malicious')return {signature:[0]};return proto.createSignature(args);}};
 const adapter=new WalletTransport(provider,{network:'testnet',identityKey:request.identityKey,signingKey:request.signingKey,allowSigning:true});
 if(mode==='disconnect')adapter.disconnect();
 const cancel=new AbortController();if(mode==='cancel')cancel.abort();
 return adapter.request(request,{expectedRequestHash:hash,signal:cancel.signal});
}
let last=null;
async function poll(){
 try{const r=await fetch('/api/wallet/request');if(!r.ok)return;const p=await r.json();
 if(p&&p.request.id!==last){last=p.request.id;let result;
 try{result={id:last,response:await sign(p.request,p.hash,p.mode)};}catch(e){result={id:last,error:e.message};}
 await fetch('/api/wallet/response',{method:'POST',headers:{'Content-Type':'application/json','X-BoxSV-Demo':'1'},body:JSON.stringify(result)});
 }}catch(e){console.error('Fixture wallet bridge',e.message);}finally{setTimeout(poll,250);}
}
poll();
