'use strict';
const http=require('node:http');
const {fs,path,assert,ACTIONS,NETWORK}=require('../continuous/common');
const {createDemo}=require('../continuous/engine');
const {artBytes}=require('../continuous/server');
const Payment=require('./payment'),Fixtures=require('./fixtures');
async function start({dir,port=8790,broadcastEnabled=false,browserWallet=false}={}){
 assert.equal(broadcastEnabled,false,'Real send disabled; no broadcast adapter exists');
 fs.mkdirSync(dir,{recursive:true});const engine=createDemo(path.join(dir,'journal.sqlite'));
 if(!engine.inspect().payment)Payment.configure(engine,{id:'fixture-paid-iceland',binding:engine.inspect().binding,address:Fixtures.address,amount:1000,expiresAt:Date.now()+3600000,network:NETWORK,minimumDepth:2});
 const w=await Fixtures.walletFor(engine);engine.wallet=w.adapter;const art=artBytes();let scenario='none',url;
 engine.paymentObserver=Fixtures.receiptFeed('none').observer;
 const {SigningBridge}=require('./signing-bridge');
 const bridge=new SigningBridge({network:'test'});
 if(browserWallet)engine.wallet={request:async r=>{
  assert.equal(bridge.session?.publicKey,engine.inspect().binding.buyerPubkey,'Connect the bound public fixture buyer first');
  const {CustodyWallet}=require('./custody-wallet');
  const F=require('../continuous/fixture-wallet'),{M}=require('../continuous/common');
  const custody=new CustodyWallet({transport:bridge,session:bridge.session,binding:engine.inspect().binding,getState:()=>engine.journal.read().state,sponsor:new M.bsv.PrivateKey(new M.bsv.crypto.BN(3)),getFunding:Fixtures.funding,sellerWallet:new F.FixtureWallet()});
  return bridge.withRequest(r,()=>custody.request(r));
 }};
 const server=http.createServer(async(req,res)=>{
  const reply=(status,data,type='application/json')=>{res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'"});res.end(type==='application/json'?JSON.stringify(data):data);};
  if(req.headers.host!==new URL(url).host)return reply(403,{error:'loopback Host required'});
  try{
   if(browserWallet&&await bridge.handle(req,res,{origin:url}))return;
   if(req.method==='GET'){
    const files={'/':['index.html','text/html; charset=utf-8'],'/app.js':['app.js','text/javascript'],'/style.css':['style.css','text/css'],'/wallet.js':['wallet.js','text/javascript']};
    if(browserWallet&&['/browser-wallet.bundle.js','/browser-wallet-fixture.bundle.js'].includes(req.url))return reply(200,fs.readFileSync(path.join(__dirname,req.url.slice(1))),'text/javascript');
    if(req.url==='/api/config')return reply(200,{browserWallet,providerMode:browserWallet?'browser-public-fixture':'server-public-fixture'});
    if(files[req.url]){const [f,t]=files[req.url];return reply(200,fs.readFileSync(path.join(__dirname,f)),t);}
    if(req.url==='/candidate.webp')return reply(200,art,'image/webp');
    if(['/api/state','/api/evidence'].includes(req.url))return reply(200,{...engine.inspect(),signatureCalls:w.calls.length,broadcastEnabled:false,providerMode:browserWallet?'browser-public-fixture':'server-public-fixture'});
    if(req.url==='/favicon.ico')return reply(204,'','text/plain');return reply(404,{error:'not found'});
   }
   if(req.method!=='POST'||req.url!=='/api/action')return reply(405,{error:'method forbidden'});
   if(req.headers.origin!==url||req.headers['x-boxsv-demo']!=='1'||req.headers['content-type']!=='application/json')return reply(403,{error:'same-origin local request required'});
   let body='';for await(const chunk of req){body+=chunk;assert.ok(body.length<=2048,'request too large');}const p=JSON.parse(body);
   assert.ok(!engine.busy,'operation busy');
   if(p.action==='Observe'){
    assert.deepEqual(Object.keys(p).sort(),['action','scenario']);assert.ok(['none','partial','shallow','paid','excess','lost','unavailable'].includes(p.scenario));
    scenario=p.scenario;return reply(200,await Payment.poll(engine,Fixtures.receiptFeed(scenario).observer));
   }
   assert.deepEqual(Object.keys(p).sort(),['action','key','mode']);assert.ok(['Reserve',...ACTIONS].includes(p.action));
   assert.ok(['ok','reject','disconnect','wrong-network','wrong-buyer','malicious','ambiguous'].includes(p.mode));
   // Re-observe immediately before delivery. Restart defaults to no observed payment,
   // so operators must explicitly restore the synthetic feed, never cached success.
   if(p.action==='Transfer'&&!Object.hasOwn(engine.inspect().requests,p.key))await Payment.poll(engine,Fixtures.receiptFeed(scenario).observer);
   assert.equal(engine.inspect().holds.length,0,'reconciliation hold');
   w.control.mode=p.mode==='ambiguous'?'ok':p.mode;engine.transport.mode=p.mode==='ambiguous'?'ambiguous':'ok';
   if(!w.transport.session){w.control.mode='ok';await w.transport.connect();w.control.mode=p.mode;}
   const result=p.action==='Reserve'?await engine.reserve(p.key):await engine.advance(p.key,p.action);return reply(200,result);
  }catch(e){return reply(409,{error:e.message});}
 });
 try{await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(port,'127.0.0.1',resolve);});}catch(e){engine.close();throw e;}
 url='http://127.0.0.1:'+server.address().port;
 return {url,engine,signatureCalls:w.calls,close:async()=>{bridge.invalidate('Server closed');await new Promise(r=>server.close(r));engine.close();}};
}
module.exports={start};
