'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {spawnSync}=require('node:child_process');
const {createDemo}=require('./engine');
const {FixtureWallet,FixtureTransport}=require('./fixture-wallet');
const dir=path.join(__dirname,'.test-runs');fs.mkdirSync(dir,{recursive:true});
for(const point of ['afterPrepared','afterAttempt'])test('actual child-process exit at '+point+' replays safely in fresh process connection',async()=>{
 const p=path.join(fs.mkdtempSync(path.join(dir,'process-')),'journal.sqlite');
 const script=`const {createDemo}=require('./launch/continuous/engine');(async()=>{const e=createDemo(process.argv[1],{hooks:{${point}(){process.exit(75)}}});await e.reserve('reserve');await e.advance('pack','Pack');})().catch(e=>{console.error(e);process.exit(1)});`;
 const result=spawnSync(process.execPath,['-e',script,p],{cwd:path.resolve(__dirname,'../..'),encoding:'utf8',timeout:30000});
 assert.equal(result.status,75,result.stderr);
 const wallet=new FixtureWallet('disconnect'),transport=new FixtureTransport(),e=createDemo(p,{wallet,transport});
 try{
  const before=e.inspect();assert.ok(before.pending.response.raw);
  if(point==='afterPrepared'){
   await e.advance('pack','Pack');assert.equal(e.inspect().stage,'PACKED');assert.equal(transport.sent[0],before.pending.response.raw);
  }else{
   await assert.rejects(e.advance('pack','Pack'),/Interrupted send quarantined/);
   assert.deepEqual(e.inspect().pending.response,before.pending.response);assert.equal(transport.sent.length,0);
  }
  assert.equal(wallet.calls,0);
 }finally{e.close();}
});
