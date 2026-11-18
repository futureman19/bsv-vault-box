'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),http=require('node:http'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const {SigningBridge}=require('./signing-bridge');
async function setup(t){
 const bridge=new SigningBridge({timeoutMs:2000});let origin;
 const server=http.createServer(async(req,res)=>{if(!await bridge.handle(req,res,{origin})){res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));origin='http://127.0.0.1:'+server.address().port;t.after(()=>new Promise(r=>server.close(r)));
 const requests=[];
 const fetcher=(url,opts)=>{requests.push(url);return fetch(origin+url,{...opts,headers:{...opts.headers,Origin:origin}});};
 const context=vm.createContext({window:{},URL,TextEncoder,setTimeout,clearTimeout,setInterval,clearInterval,console});
 for(const name of ['browser-wallet','browser-wallet-fixture'])vm.runInContext(fs.readFileSync(path.join(__dirname,name+'.bundle.js'),'utf8'),context);
 const f=context.window.BoxSVBrowserWalletFixture.createFixtureProvider();let discovered=0;
 const client=new context.window.BoxSVBrowserWallet.BrowserWallet({getWallet:()=>{discovered++;return f.wallet;},fetch:fetcher});
 assert.equal(discovered,0);assert.equal(f.calls.length,0);assert.equal(await client.poll(),null);assert.equal(f.calls.length,0);
 const session=await client.connect();const request={action:'Reserve',key:'browser-request',binding:{buyerPubkey:session.publicKey},arbitraryFullField:{x:[1,2]}};
 t.after(()=>bridge.invalidate());return {client,bridge,f,request,origin,requests};
}
test('self-contained browser bundles -> real YoursTransport -> HTTP bridge -> local DER verification',async t=>{
 const {client,bridge,f,request}=await setup(t);
 await bridge.withRequest(request,async()=>{
  const promise=bridge.signHash('11'.repeat(32));await client.poll();assert.equal(f.calls.filter(c=>c.method==='createSignature').length,0);
  assert.equal((await client.approve()).accepted,true);assert.match(await promise,/^30/);
 });
 assert.equal(f.calls.filter(c=>c.method==='createSignature').length,1);assert.ok(f.calls.every(c=>!['createAction','signAction'].includes(c.method)));await client.disconnect();assert.equal(bridge.session,null);
});
for(const mode of ['malicious','account-switch','reject'])test('browser fails closed: '+mode,async t=>{
 const {client,bridge,f,request,requests}=await setup(t);
 await bridge.withRequest(request,async()=>{
  const promise=bridge.signHash('11'.repeat(32)),failure=assert.rejects(promise,/disconnected/);await client.poll();f.control.mode=mode;
  await assert.rejects(client.approve());await failure;
 });assert.equal(bridge.session,null);assert.equal(requests.includes('/api/wallet/signature'),false,'Rejected locally before posting DER to server');
});
test('browser cancellation drops delayed signature and server rejects replay',async t=>{
 const {client,bridge,f,request}=await setup(t);f.control.delayMs=100;
 await bridge.withRequest(request,async()=>{
  const promise=bridge.signHash('11'.repeat(32)),failure=assert.rejects(promise,/disconnected/);await client.poll();const envelope=bridge.peek();
  const approving=assert.rejects(client.approve(),/cancelled|disconnected/);
  while(!f.calls.some(c=>c.method==='createSignature'))await new Promise(r=>setTimeout(r,5));
  await client.cancel();await approving;await failure;assert.throws(()=>bridge.approve(envelope),/pending/);
 });
});
test('HTTP origin and bearer sessions enforced',async t=>{
 const {origin,client}=await setup(t);
 const post=headers=>fetch(origin+'/api/wallet/pending',{method:'POST',headers:{'Content-Type':'application/json','X-BoxSV-Demo':'1',...headers},body:'{}'});
 assert.equal((await post({Origin:'https://evil.example'})).status,409);
 assert.equal((await post({Origin:origin,'X-BoxSV-Wallet-Session':'incorrect'})).status,409);await client.disconnect();
});
