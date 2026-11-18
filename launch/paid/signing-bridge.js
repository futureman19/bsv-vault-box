'use strict';
const {randomBytes,randomUUID}=require('node:crypto');
const {canonical,digest,verify}=require('./browser-wallet-crypto');
const clone=x=>JSON.parse(JSON.stringify(x));
function check(ok,message){if(!ok)throw Error(message);}
class SigningBridge {
 constructor({network='test',timeoutMs=60000}={}){check(['test','main'].includes(network),'network required');this.network=network;this.timeoutMs=timeoutMs;this.generation=0;this.session=null;this.context=null;this.pending=null;this.token=null;}
 invalidate(reason='Wallet disconnected'){
  this.generation++;this.session=null;this.token=null;this.context=null;
  if(this.pending){const p=this.pending;this.pending=null;clearTimeout(p.timer);p.reject(Error(reason));}
 }
 connect(session){
  check(session?.network===this.network,'network mismatch');
  for(const k of ['identityKey','publicKey'])check(/^0[23][a-f0-9]{64}$/.test(session[k]),'invalid public key');
  this.invalidate('Wallet session replaced');this.session=Object.freeze({network:session.network,identityKey:session.identityKey,publicKey:session.publicKey});this.token=randomBytes(32).toString('hex');
  return {session:this.session,generation:this.generation,token:this.token};
 }
 async withRequest(request,fn){
  check(this.session&&!this.context,'Disconnected or action busy');
  const r=clone(request);check(typeof r.key==='string'&&['Reserve','Pack','Seal','Transfer','Open','Withdraw'].includes(r.action),'Invalid action context');
  check(r.binding?.buyerPubkey===this.session.publicKey,'Buyer binding mismatch');
  const context={request:r,requestDigest:digest(r),generation:this.generation};this.context=context;
  try{return await fn();}finally{if(this.context===context){if(this.pending)this.invalidate('Action ended with pending signature');else this.context=null;}}
 }
 signHash(hash){
  check(this.context&&this.session&&!this.pending,'No active action or signature busy');check(/^[a-f0-9]{64}$/.test(hash),'Invalid digest');
  const c=this.context;
  const envelope={id:randomUUID(),generation:this.generation,action:c.request.action,key:c.request.key,requestDigest:c.requestDigest,request:clone(c.request),hash,session:clone(this.session)};
  return new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>this.invalidate('Signing consent timed out'),this.timeoutMs);
   this.pending={envelope,approved:false,resolve,reject,timer};
  });
 }
 peek(){return this.pending?clone(this.pending.envelope):null;}
 match(envelope){check(this.pending&&this.session&&this.context,'No pending signature');check(canonical(envelope)===canonical(this.pending.envelope),'Wrong signature request');check(envelope.generation===this.generation&&envelope.requestDigest===digest(this.context.request),'Stale request');return this.pending;}
 approve(envelope){const p=this.match(envelope);check(!p.approved,'Already approved');p.approved=true;return {approved:true};}
 respond({envelope,signature}){
  const p=this.match(envelope);check(p.approved,'Explicit approval required');check(typeof signature==='string'&&/^[a-f0-9]{16,144}$/.test(signature),'Invalid signature encoding');
  const bytes=signature.match(/../g).map(h=>parseInt(h,16));check(verify(envelope.hash,bytes,this.session.publicKey),'Invalid signature');
  this.pending=null;clearTimeout(p.timer);p.resolve(signature);return {accepted:true};
 }
 // Mount BEFORE application's GET/POST fallback. Never expose cross-origin.
 async handle(req,res,{origin,prefix='/api/wallet'}={}){
  if(!req.url?.startsWith(prefix+'/'))return false;
  const reply=(status,data)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));};
  try{
   check(origin&&req.headers.host===new URL(origin).host,'Invalid host');
   const route=req.url.slice(prefix.length);
   check(req.method==='POST','POST required');check(req.headers.origin===origin&&req.headers['content-type']==='application/json'&&req.headers['x-boxsv-demo']==='1','Same-origin JSON required');
   let body='';for await(const part of req){body+=part;check(body.length<=1024*1024,'Body too large');}const data=JSON.parse(body||'{}');
   if(route==='/connect'){reply(200,this.connect(data.session));return true;}
   check(this.token&&req.headers['x-boxsv-wallet-session']===this.token,'Invalid wallet session');
   let result;
   if(route==='/pending')result={pending:this.peek()};
   else if(route==='/approve')result=this.approve(data.envelope);
   else if(route==='/signature')result=this.respond(data);
   else if(route==='/disconnect'){this.invalidate();result={disconnected:true};}
   else throw Error('Unknown wallet route');
   reply(200,result);
  }catch(e){reply(409,{error:e.message});}return true;
 }
}
module.exports={SigningBridge};
