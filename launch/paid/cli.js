'use strict';
const {fs,path,assert,sha}=require('../continuous/common');
const {DatabaseSync}=require('node:sqlite');
const {createDemo,Journal,Engine}=require('../continuous/engine');
const {walletFor,receiptFeed,address}=require('./fixtures');
const Payment=require('./payment');
async function main(){
 const [command,...args]=process.argv.slice(2);const opts={};for(let n=0;n<args.length;n+=2){assert.ok(['--dir','--port'].includes(args[n]),'unsupported option');opts[args[n]]=args[n+1];}
 assert.ok(opts['--dir'],'--dir required');const dir=path.resolve(opts['--dir']),file=path.join(dir,'journal.sqlite');
 if(command==='inspect'||command==='replay'){
  assert.ok(fs.existsSync(file),'existing journal required');const before=sha(fs.readFileSync(file));
  const journal=Object.create(Journal.prototype);journal.db=new DatabaseSync(file,{readOnly:true});
  const e=new Engine(journal,{});try{const s=e.inspect();if(command==='replay'){assert.equal(s.stage,'WITHDRAWN');assert.equal(s.history.length,5);assert.ok(Object.values(s.provenance).every(Boolean));}console.log(JSON.stringify(s,null,2));}finally{e.close();}
  assert.equal(sha(fs.readFileSync(file)),before,'inspection changed journal');return;
 }
 if(command==='demo'){
  const app=await require('./server').start({dir,port:Number(opts['--port']||8790),broadcastEnabled:false,browserWallet:true});console.log(app.url);
  for(const signal of ['SIGINT','SIGTERM'])process.once(signal,async()=>{await app.close();process.exit(0);});return;
 }
 assert.equal(command,'run','use demo, run, inspect or replay');assert.ok(!fs.existsSync(dir),'fresh output directory required');fs.mkdirSync(dir,{recursive:true});
 const e=createDemo(file);try{
  const w=await walletFor(e);e.wallet=w.adapter;e.paymentObserver=receiptFeed('none').observer;
  Payment.configure(e,{id:'fixture-paid-iceland',binding:e.inspect().binding,address,amount:1000,expiresAt:Date.now()+3600000,network:'offline-fixture',minimumDepth:2});
  await e.reserve('reserve');await e.advance('pack','Pack');await e.advance('seal','Seal');
  await assert.rejects(e.advance('unpaid-transfer','Transfer'),/payment/);
  const feed=receiptFeed('paid');await Payment.poll(e,feed.observer);
  for(const a of ['Transfer','Open','Withdraw'])await e.advance(a.toLowerCase(),a);
  const s=e.inspect();assert.equal(s.stage,'WITHDRAWN');assert.ok(Object.values(s.provenance).every(Boolean));
  fs.writeFileSync(path.join(dir,'evidence.json'),JSON.stringify(s,null,2));fs.writeFileSync(path.join(dir,'provider-calls.json'),JSON.stringify(w.calls,null,2));fs.writeFileSync(path.join(dir,'indexer-routes.json'),JSON.stringify(feed.calls,null,2));
  console.log(JSON.stringify({stage:s.stage,events:s.events,transitions:s.history.length,signatures:w.calls.length,binding:s.binding,chainInclusion:false,broadcastEnabled:false},null,2));
 }finally{e.close();}
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
