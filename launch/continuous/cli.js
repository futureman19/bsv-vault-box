'use strict';
const {fs,path,assert,ROOT,sha,ACTIONS}=require('./common');
const {createDemo}=require('./engine');
async function main(args){
 const [command,...rest]=args;assert.ok(['run','demo','replay'].includes(command),'Usage: node launch/continuous/cli.js run|demo|replay --dir PATH [--port 8789]');
 const opts={};for(let i=0;i<rest.length;i+=2){assert.ok(['--dir','--port'].includes(rest[i])&&rest[i+1],'invalid arguments');assert.ok(!opts[rest[i]],'duplicate option');opts[rest[i]]=rest[i+1];}
 assert.ok(opts['--dir'],'--dir required');const dir=path.resolve(opts['--dir']);
 if(command==='demo'){
  const {start}=require('./server');const s=await start({dir,port:Number(opts['--port']||8789)});console.log('SIMULATION ONLY '+s.url+' | persisted journal: '+dir);
  for(const sig of ['SIGINT','SIGTERM'])process.once(sig,async()=>{await s.close();process.exit(0);});return;
 }
 if(command==='run')assert.ok(!fs.existsSync(dir),'fresh evidence directory required');
 if(command==='replay')assert.ok(fs.existsSync(path.join(dir,'journal.sqlite')),'existing journal required');
 const e=createDemo(path.join(dir,'journal.sqlite'));
 try{
  if(command==='run'){await e.reserve('reserve-fixture-1');for(const action of ACTIONS)await e.advance(action.toLowerCase()+'-fixture-1',action);}
  const result=e.inspect();assert.equal(result.stage,'WITHDRAWN','complete journey required');
  if(command==='run'){
   fs.writeFileSync(path.join(dir,'evidence.json'),JSON.stringify(result,null,2)+'\n',{flag:'wx'});
   const files=['common.js','fixture-wallet.js','engine.js','server.js','cli.js','index.html','style.css','app.js'];
   const sources=Object.fromEntries(files.map(f=>['launch/continuous/'+f,sha(fs.readFileSync(path.join(__dirname,f)))]));
   for(const f of ['vault/src/ordinal-pair.js','vault/src/launch-record.js','vault/artifacts/ordinalPair.json','launch/collection/upstream/candidate-manifest.json'])sources[f]=sha(fs.readFileSync(path.join(ROOT,f)));
   fs.writeFileSync(path.join(dir,'sources.json'),JSON.stringify(sources,null,2)+'\n',{flag:'wx'});
  }
  console.log(JSON.stringify({mode:'SIMULATION',stage:result.stage,binding:result.binding,transitions:result.history.map(h=>({action:h.action,txid:h.receipt.txid,vm:h.vm})),events:result.events,journalHead:result.head,provenance:result.provenance,chainInclusion:false,launchReady:false},null,2));
 }finally{e.close();}
}
if(require.main===module)main(process.argv.slice(2)).catch(e=>{console.error(e.message);process.exitCode=1;});
module.exports={main};
