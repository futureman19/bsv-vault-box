'use strict';
const http=require('node:http'),{execFileSync}=require('node:child_process');
const {fs,path,assert,ROOT,candidate,sha,ACTIONS}=require('./common');
const {createDemo}=require('./engine');
const {FixtureWallet,FixtureTransport}=require('./fixture-wallet');
function artBytes(){const a=candidate().art;const bytes=execFileSync('git',['show',a.source.commit+':'+a.source.path],{cwd:ROOT,maxBuffer:5000000});assert.equal(sha(bytes),a.sha256,'candidate art mismatch');return bytes;}
async function start({dir,port=8789,paid=false}) {
 fs.mkdirSync(dir,{recursive:true});
 const art=artBytes();let pending=null;
 const authorize=(request,hash,mode)=>new Promise((resolve,reject)=>{
  assert.equal(pending,null,'wallet busy');
  const timer=setTimeout(()=>{pending=null;reject(Error('wallet handoff timeout'));},90000);
  pending={request,hash,mode,resolve:r=>{clearTimeout(timer);pending=null;resolve(r);},reject:e=>{clearTimeout(timer);pending=null;reject(e);}};
 });
 const engine=paid?await require('./paid').createPaid(dir,{authorize}):createDemo(path.join(dir,'journal.sqlite'),{wallet:new FixtureWallet(),transport:new FixtureTransport()});
 const {wallet,transport}=engine;
 let url;
 const server=http.createServer(async(req,res)=>{
  const reply=(status,data,type='application/json')=>{res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'"});res.end(type==='application/json'?JSON.stringify(data):data);};
  if(req.headers.host!==new URL(url).host)return reply(403,{error:'loopback host required'});
  try {
   if(req.method==='GET') {
    const files={'/':['index.html','text/html; charset=utf-8'],'/app.js':['app.js','text/javascript'],'/style.css':['style.css','text/css']};
    if(files[req.url]){const [file,type]=files[req.url];let bytes=fs.readFileSync(path.join(__dirname,file));if(paid&&file==='index.html')bytes=bytes.toString().replace('</head>','<script defer src="/wallet.js"></script></head>').replace('FIXTURE WALLET · NO EXTENSION CONNECTION','BRC-100 BROWSER FIXTURE · NO EXTENSION CONNECTION').replace('No random draw, payment or sale.','No real payment or sale.');return reply(200,bytes,type);}
    if(paid&&req.url==='/wallet.js')return reply(200,fs.readFileSync(path.join(__dirname,'browser/wallet.js')),'text/javascript');
    if(paid&&req.url==='/api/wallet/request')return reply(200,pending?{request:pending.request,hash:pending.hash,mode:pending.mode}:null);
    if(req.url==='/candidate.webp')return reply(200,art,'image/webp');
    if(req.url==='/api/state')return reply(200,engine.inspect());
    if(req.url==='/api/evidence')return reply(200,engine.inspect());
    if(req.url==='/favicon.ico'){res.writeHead(204);return res.end();}
    return reply(404,{error:'not found'});
   }
   if(req.method!=='POST'||!['/api/action',...(paid?['/api/wallet/response']:[])].includes(req.url))return reply(405,{error:'method forbidden'});
   if(req.headers.origin!==url||req.headers['x-boxsv-demo']!=='1'||req.headers['content-type']!=='application/json')return reply(403,{error:'same-origin fixture request required'});
   let body='';for await(const chunk of req){body+=chunk;assert.ok(body.length<=(req.url==='/api/wallet/response'?1000000:2048),'request too large');}
   const p=JSON.parse(body);
   if(req.url==='/api/wallet/response'){assert.ok(pending&&pending.request.id===p.id,'stale wallet response');assert.deepEqual(Object.keys(p).sort(),(p.error?['error','id']:['id','response']));if(p.error)pending.reject(Error(String(p.error)));else pending.resolve(p.response);return reply(200,{accepted:true});}
   assert.deepEqual(Object.keys(p).sort(),['action','key','mode']);
   assert.ok(['Reserve',...ACTIONS,...(paid?['Pay']:[])].includes(p.action),'unsupported action');
   assert.ok(['ok','reject','disconnect','wrong-buyer','wrong-network','malicious','ambiguous',...(paid?['cancel']:[])].includes(p.mode),'unsupported fixture mode');
   assert.ok(!engine.busy,'operation busy');
   wallet.mode=p.mode==='ambiguous'?'ok':p.mode;transport.mode=p.mode==='ambiguous'?'ambiguous':'ok';
   const result=p.action==='Pay'?await engine.pay():p.action==='Reserve'?await engine.reserve(p.key):await engine.advance(p.key,p.action);
   return reply(200,result);
  }catch(error){return reply(409,{error:error.message});}
 });
 try{await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(port,'127.0.0.1',resolve);});}
 catch(e){engine.close();throw e;}
 url='http://127.0.0.1:'+server.address().port;
 return {url,engine,close:async()=>{if(pending)pending.reject(Error('server shutdown'));await new Promise(r=>server.close(r));engine.close();}};
}
module.exports={start,artBytes};
