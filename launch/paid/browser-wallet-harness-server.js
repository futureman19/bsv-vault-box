'use strict';
// Isolated local PUBLIC-fixture QA server. Not the paid-app server.
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const {SigningBridge}=require('./signing-bridge');
async function start(port=0){
 const bridge=new SigningBridge();let origin,result=null;
 const server=http.createServer(async(req,res)=>{
  if(await bridge.handle(req,res,{origin}))return;
  const send=(type,data)=>{res.writeHead(200,{'Content-Type':type,'Content-Security-Policy':"default-src 'self'; script-src 'self'; connect-src 'self'",'Cache-Control':'no-store'});res.end(data);};
  if(req.url==='/')return send('text/html','<!doctype html><meta charset="utf-8"><title>PUBLIC fixture WalletInterface harness</title><h1>Public fixture only</h1><div data-boxsv-fixture-harness></div><script src="/browser-wallet.bundle.js"></script><script src="/browser-wallet-fixture.bundle.js"></script><script src="/browser-wallet-harness.js"></script>');
  if(['/browser-wallet.bundle.js','/browser-wallet-fixture.bundle.js','/browser-wallet-harness.js'].includes(req.url))return send('text/javascript',fs.readFileSync(path.join(__dirname,req.url.slice(1))));
  if(req.url==='/fixture/state')return send('application/json',JSON.stringify({result,pending:bridge.peek(),session:bridge.session}));
  if(req.url==='/fixture/request'&&req.method==='POST'&&req.headers.origin===origin&&bridge.session){
   const request={key:'public-fixture-request',action:'Reserve',binding:{buyerPubkey:bridge.session.publicKey},details:{purpose:'Public scalar-2 test only'}};
   result=null;bridge.withRequest(request,()=>bridge.signHash('11'.repeat(32))).then(signature=>{result={signature};},error=>{result={error:error.message};});
   return send('application/json','{"queued":true}');
  }
  res.writeHead(404);res.end();
 });
 await new Promise(r=>server.listen(port,'127.0.0.1',r));origin='http://127.0.0.1:'+server.address().port;
 return {origin,server,bridge};
}
if(require.main===module)start(Number(process.argv[2]||0)).then(({origin})=>console.log(origin));
module.exports={start};
