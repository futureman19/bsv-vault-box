'use strict';
const {YoursTransport}=require('./wallet');
const {canonical,digest,verify}=require('./browser-wallet-crypto');
class BrowserWallet {
 constructor({getWallet,network='test',base='/api/wallet',fetch:fetcher=(...args)=>globalThis.fetch(...args),onChange=()=>{}}={}){
  if(typeof getWallet!=='function')throw Error('Explicit WalletInterface provider required');
  Object.assign(this,{getWallet,network,base,fetcher,onChange});this.epoch=0;this.transport=null;this.connection=null;this.pending=null;this.busy=false;
 }
 async post(route,data={},connection=this.connection){
  const r=await this.fetcher(this.base+route,{method:'POST',headers:{'Content-Type':'application/json','X-BoxSV-Demo':'1',...(connection?{'X-BoxSV-Wallet-Session':connection.token}:{})},body:JSON.stringify(data)});
  const p=await r.json();if(!r.ok)throw Error(p.error||'Wallet bridge rejected request');return p;
 }
 // Only call from an explicit Connect click; construction never touches provider.
 async connect(){
  if(this.busy||this.connection)throw Error('Disconnect before connecting again');this.busy=true;const epoch=++this.epoch;
  try{
   const wallet=await this.getWallet();if(epoch!==this.epoch)throw Error('Connect cancelled');
   this.transport=new YoursTransport({wallet,network:this.network,verify});
   const session=await this.transport.connect();if(epoch!==this.epoch)throw Error('Connect cancelled');
   const c=await this.post('/connect',{session},null);
   if(epoch!==this.epoch){await this.post('/disconnect',{},c);throw Error('Connect cancelled');}
   if(canonical(c.session)!==canonical(session))throw Error('Bridge session mismatch');
   this.connection=c;this.onChange({session,pending:null});return session;
  }finally{this.busy=false;}
 }
 async disconnect(){
  ++this.epoch;this.transport?.disconnect();const c=this.connection;this.connection=null;this.pending=null;this.onChange({session:null,pending:null});
  if(c)await this.post('/disconnect',{},c);
 }
 cancel(){return this.disconnect();}
 accountChanged(){return this.disconnect();}
 validate(p){
  const c=this.connection;
  if(!c||p.generation!==c.generation||canonical(p.session)!==canonical(c.session)||p.requestDigest!==digest(p.request)||p.action!==p.request.action||p.key!==p.request.key||p.request.binding?.buyerPubkey!==c.session.publicKey||!/^[a-f0-9]{64}$/.test(p.hash))throw Error('Bridge request binding mismatch');
 }
 // Polling fetches intent only. It NEVER authenticates or signs.
 async poll(){
  if(!this.connection)return null;const epoch=this.epoch;
  const {pending}=await this.post('/pending');if(epoch!==this.epoch)return null;
  if(pending)this.validate(pending);this.pending=pending;this.onChange({session:this.connection.session,pending});return pending;
 }
 // Separate explicit Approve click for EACH digest (custody actions may use several).
 async approve(){
  if(this.busy||!this.pending)throw Error('No pending consent or wallet busy');
  this.busy=true;const epoch=this.epoch,p=JSON.parse(JSON.stringify(this.pending));
  try{
   this.validate(p);const current=await this.post('/pending');
   if(epoch!==this.epoch||canonical(current.pending)!==canonical(p))throw Error('Pending request changed');
   await this.post('/approve',{envelope:p});if(epoch!==this.epoch)throw Error('Approval cancelled');
   const signature=await this.transport.signHash(p.hash); // actual wallet.js, bundled SDK verification
   if(epoch!==this.epoch)throw Error('Signature cancelled');
   const result=await this.post('/signature',{envelope:p,signature});
   this.pending=null;this.onChange({session:this.connection?.session,pending:null});return result;
  }catch(e){await this.disconnect().catch(()=>{});throw e;}finally{this.busy=false;}
 }
}
function mount({root,getWallet,network='test',base='/api/wallet',label='WalletInterface'}={}){
 if(!root)throw Error('Root element required');
 root.replaceChildren();
 const status=document.createElement('pre');status.textContent='Disconnected — '+label;
 const connect=document.createElement('button');connect.textContent='Connect '+label;
 const approve=document.createElement('button');approve.textContent='Approve pending signature';approve.disabled=true;
 const cancel=document.createElement('button');cancel.textContent='Cancel / disconnect';
 root.append(connect,approve,cancel,status);
 const client=new BrowserWallet({getWallet,network,base,onChange:({session,pending})=>{
  connect.disabled=!!session;approve.disabled=!pending;
  status.textContent=JSON.stringify({session,pending},null,2); // show exact request, digest and buyer, not only hash
 }});
 const run=fn=>async()=>{try{await fn();}catch(e){status.textContent=e.message;}};
 connect.addEventListener('click',run(()=>client.connect()));approve.addEventListener('click',run(()=>client.approve()));cancel.addEventListener('click',run(()=>client.disconnect()));
 let polling=false;const timer=setInterval(async()=>{if(polling||client.busy)return;polling=true;try{await client.poll();}catch(e){status.textContent=e.message;}finally{polling=false;}},500);
 return {client,dispose:async()=>{clearInterval(timer);await client.disconnect();root.replaceChildren();}};
}
module.exports={BrowserWallet,mount,verify,createProvider:require('./provider').createProvider};
if(typeof window!=='undefined')window.BoxSVBrowserWallet=module.exports;
