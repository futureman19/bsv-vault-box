'use strict';
const {path,fs,assert,ACTIONS}=require('./common');
async function main(){
 const [command,directory,port='8791']=process.argv.slice(2);assert.ok(['demo','run','replay'].includes(command)&&directory,'Usage: node launch/continuous/paid-cli.js demo|run|replay DIRECTORY [PORT]');
 const dir=path.resolve(directory);
 if(command==='demo'){const server=await require('./server').start({dir,port:Number(port),paid:true});console.log('OFFLINE BRC-100 FIXTURE '+server.url);for(const sig of ['SIGINT','SIGTERM'])process.once(sig,async()=>{await server.close();process.exit(0);});return;}
 if(command==='run')assert.ok(!fs.existsSync(dir),'fresh destination required');else assert.ok(fs.existsSync(path.join(dir,'journal.sqlite')),'existing journal required');
 const e=await require('./paid').createPaid(dir);
 try{if(command==='run'){await e.reserve('paid-reserve-cli');for(const a of ['Pack','Seal'])await e.advance('paid-'+a+'-cli',a);await e.pay();for(const a of ['Open','Withdraw'])await e.advance('paid-'+a+'-cli',a);}
 const s=e.inspect();assert.equal(s.stage,'WITHDRAWN');assert.ok(Object.values(s.provenance).every(Boolean));
 if(command==='run')fs.writeFileSync(path.join(dir,'evidence.json'),JSON.stringify(s,null,2)+'\n',{flag:'wx'});
 console.log(JSON.stringify({stage:s.stage,binding:s.binding,policy:s.policy,deliveryStatus:s.delivery.status,receipt:s.delivery.receipt,provenance:s.provenance,transitions:s.history.map(h=>({action:h.action,txid:h.receipt.txid})),authorizations:s.authorizations.length,realSendingEnabled:false,chainInclusion:false,launchReady:false},null,2));
 }finally{e.close();}
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});
