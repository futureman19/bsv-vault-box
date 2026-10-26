'use strict';
const fs=require('node:fs');
const {RegtestRPC}=require('./rpc.cjs');
const {Watcher,local}=require('./watcher.cjs');
async function main(){
 const args=process.argv.slice(2),i=args.indexOf('--config');if(i<0||!args[i+1])throw Error('Usage: operator.cjs --config <repo-local.json> [--once]');
 const c=JSON.parse(fs.readFileSync(local(args[i+1]),'utf8'));
 const rpc=new RegtestRPC(JSON.parse(fs.readFileSync(local(c.rpcFile),'utf8')));
 const watcher=new Watcher(c,rpc);let stop=false;
 process.on('SIGINT',()=>{stop=true;});process.on('SIGTERM',()=>{stop=true;});
 try{do{const r=await watcher.poll();console.log(JSON.stringify(r));if(args.includes('--once'))break;await new Promise(resolve=>setTimeout(resolve,c.pollMs??1000));}while(!stop);}finally{watcher.close();}
}
main().catch(e=>{console.error(JSON.stringify({status:'HALTED',error:e.message}));process.exitCode=1;});
