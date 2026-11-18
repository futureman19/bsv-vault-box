'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const api=fs.existsSync(path.join(__dirname,'server.js'))?require('./server'):{};
test('local paid browser server exists and refuses real send configuration',async()=>{
 assert.equal(typeof api.start,'function');await assert.rejects(api.start({dir:'unused',broadcastEnabled:true}),/disabled/);
});
test('HTTP lifecycle gates payment, uses BRC100 signatures and persists terminal excess',async t=>{
 if(!api.start)return assert.fail('server missing');
 const dir=fs.mkdtempSync(path.join(process.env.TMPDIR||os.tmpdir(),'paid-server-'));
 const app=await api.start({dir,port:0});t.after(async()=>{await app.close();fs.rmSync(dir,{recursive:true,force:true});});
 const post=async data=>{const r=await fetch(app.url+'/api/action',{method:'POST',headers:{Origin:app.url,'Content-Type':'application/json','X-BoxSV-Demo':'1'},body:JSON.stringify(data)});return {status:r.status,body:await r.json()};};
 assert.equal((await fetch(app.url)).status,200);
 for(const action of ['Reserve','Pack','Seal'])assert.equal((await post({action,key:action,mode:'ok'})).status,200);
 assert.equal((await post({action:'Transfer',key:'Transfer',mode:'ok'})).status,409);
 const payment=await post({action:'Observe',scenario:'paid'});assert.equal(payment.status,200);assert.equal(payment.body.payment.qualified,true);
 for(const action of ['Transfer','Open','Withdraw'])assert.equal((await post({action,key:action,mode:'ok'})).status,200);
 const excess=await post({action:'Observe',scenario:'excess'});assert.equal(excess.body.stage,'WITHDRAWN');assert.ok(excess.body.holds.includes('EXCESS_PAYMENT'));
 assert.equal(app.signatureCalls.length,7);assert.ok(app.signatureCalls.every(x=>x.counterparty==='self'&&x.hashToDirectlySign.length===32));
 const before=app.engine.inspect().events;assert.equal((await fetch(app.url+'/api/evidence')).status,200);assert.equal(app.engine.inspect().events,before);
 assert.equal((await fetch(app.url+'/api/action',{method:'POST',body:'{}'})).status,403);
});
