'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
test('local server serves manifest-pinned art and real state; blocks foreign origins and stale actions',async()=>{
 const api=fs.existsSync(path.join(__dirname,'server.js'))?require('./server'):{};
 assert.equal(typeof api.start,'function','connected local server missing');
 const dir=fs.mkdtempSync(path.join(__dirname,'.test-runs/server-'));
 const server=await api.start({dir,port:0});
 try{
  const url=server.url;
  assert.equal((await fetch(url)).status,200);
  const initial=await(await fetch(url+'/api/state')).json();assert.equal(initial.stage,'AVAILABLE');
  const image=await fetch(url+'/candidate.webp');assert.equal(image.headers.get('content-type'),'image/webp');
  const {sha}=require('./common');assert.equal(sha(Buffer.from(await image.arrayBuffer())),initial.candidate.art.sha256);
  const payload=JSON.stringify({action:'Reserve',key:'reserve',mode:'ok'});
  assert.equal((await fetch(url+'/api/action',{method:'POST',headers:{'Content-Type':'application/json','Origin':'https://evil.invalid','X-BoxSV-Demo':'1'},body:payload})).status,403);
  const headers={'Content-Type':'application/json','Origin':url,'X-BoxSV-Demo':'1'};
  const r=await fetch(url+'/api/action',{method:'POST',headers,body:payload});assert.equal(r.status,200);assert.equal((await r.json()).stage,'RESERVED');
  const bad=await fetch(url+'/api/action',{method:'POST',headers,body:JSON.stringify({action:'Withdraw',key:'bad',mode:'ok'})});assert.equal(bad.status,409);
 }finally{await server.close();}
});
