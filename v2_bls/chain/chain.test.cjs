'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),http=require('node:http');
const {RegtestRPC}=require('./rpc.cjs');
const {decodeVault,traceOpening,releaseScript,bsv,Vault,local,Watcher,artifactFingerprint}=require('./watcher.cjs');
const box='11'.repeat(32),ref='22'.repeat(32),owner='02'+'33'.repeat(32),bob='03'+'44'.repeat(32);
function vault(state=0n,who=owner,content=ref){return new Vault(state,box,content,who).lockingScript;}
function tx(prev,script){return new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:prev??'00'.repeat(32),outputIndex:0,script:bsv.Script.empty(),output:new bsv.Transaction.Output({script:bsv.Script.empty(),satoshis:1})})).addOutput(new bsv.Transaction.Output({script,satoshis:1}));}
function fixture({depth=3,changed=false,badContent=false,reorg=false}={}){
 const genesis=tx(null,vault()),transfer=tx(genesis.id,vault(0n,bob)),open=tx(transfer.id,vault(1n,bob,badContent?'aa'.repeat(32):ref));
 const list=[genesis,transfer,open],blocks=['a','b','c',...Array.from({length:depth-1},(_,i)=>'d'+i)];
 const rpc={assertRegtest:async()=>({bestblockhash:blocks.at(-1),blocks:blocks.length-1}),call:async(m,p=[])=>{
 if(m==='getrawtransaction'){const t=list.find(t=>t.id===p[0]);if(!t)throw Error('missing');return p[1]?{hex:t.toString(),blockhash:'a',confirmations:blocks.length}:t.toString();}
 if(m==='getblockheader')return {height:0};
 if(m==='getblockhash')return reorg&&p[0]===0?'fork':blocks[p[0]];
 if(m==='getbestblockhash')return changed?'fork':blocks.at(-1);
 if(m==='getblock'){const i=blocks.indexOf(p[0]);return {tx:i<3?[list[i].id]:[]};}
 throw Error(m);
 }};return {rpc,genesis:{txid:genesis.id,vout:0}};
}
test('artifact decoder reconstructs exact canonical script, rejects appended data',()=>{assert.equal(decodeVault(vault().toHex()).state,0);assert.throws(()=>decodeVault(vault().toHex()+'61'));});
test('decoder preserves genesis defaults and original constructor owner across transfer/open',()=>{
 const g=new Vault(0n,box,ref,owner);g.markAsGenesis();
 assert.equal(decodeVault(g.lockingScript.toHex()).owner,owner);
 const t=g.next();t.owner=bob;
 assert.equal(decodeVault(t.lockingScript.toHex()).owner,bob);
 const o=t.next();o.boxState=1n;
 assert.equal(decodeVault(o.lockingScript.toHex()).state,1);
 assert.equal(decodeVault(o.lockingScript.toHex()).owner,bob);
});
test('invalid state rejected',()=>assert.throws(()=>decodeVault(vault(2n).toHex())));
test('actual serialized fixture lineage follows sealed transfer then opening',async()=>{const f=fixture();assert.equal((await traceOpening(f.rpc,f.genesis,box)).status,'READY');});
test('two confirmations insufficient',async()=>{const f=fixture({depth:2});assert.equal((await traceOpening(f.rpc,f.genesis,box)).status,'IMMATURE');});
test('content substitution rejected',async()=>{const f=fixture({badContent:true});await assert.rejects(traceOpening(f.rpc,f.genesis,box),/immutable/);});
test('reorg during scan rejected',async()=>{const f=fixture({changed:true});await assert.rejects(traceOpening(f.rpc,f.genesis,box),/changed/);});
test('orphan genesis rejected',async()=>{const f=fixture({reorg:true});await assert.rejects(traceOpening(f.rpc,f.genesis,box),/genesis/);});
test('threshold lower than three rejected',async()=>{const f=fixture();await assert.rejects(traceOpening(f.rpc,f.genesis,box,2),/depth/);});
test('strict release wire lengths and prefix',()=>{const r={box_id:box,operator_idx:0,ibe_key_share:'55'.repeat(48),operator_sig:'66'.repeat(64)};const s=releaseScript(r);assert.ok(s.startsWith('006a0a5641554c54322d52454c20'));assert.throws(()=>releaseScript({...r,ibe_key_share:'00'}));assert.throws(()=>releaseScript({...r,operator_idx:256}));});
test('paths cannot escape repository',()=>assert.throws(()=>local('../escape')));
test('durable prepared release retries exact bytes; restart never signs again; reorg halts',async()=>{
 const fs=require('node:fs');const dir=local('v2_bls/chain/.test-'+process.pid);fs.mkdirSync(dir,{recursive:true});
 const f=fixture(),view=await traceOpening(f.rpc,f.genesis,box);
 const release=tx(null,bsv.Script.fromHex(releaseScript({box_id:box,operator_idx:0,ibe_key_share:'55'.repeat(48),operator_sig:'66'.repeat(64)})));
 const stateFile=dir+'/state.json',c={stateFile,genesis:f.genesis,boxId:box,operatorIndex:0,operatorFile:dir+'/missing-share',executable:dir+'/missing-exe'};
 fs.writeFileSync(stateFile,JSON.stringify({boxId:box,operatorIndex:0,genesis:f.genesis,artifactFingerprint,opening:view.opening,raw:release.toString(),txid:release.id,status:'prepared'}));
 let known=false,sends=0;const original=f.rpc.call;
 f.rpc.call=async(m,p=[])=>{if(m==='getrawmempool')return known?[release.id]:[];if(m==='getrawtransaction'&&p[0]===release.id){if(!known){const e=Error('not found');e.code=-5;throw e;}return release.toString();}if(m==='sendrawtransaction'){assert.equal(p[0],release.toString());sends++;known=true;return release.id;}return original(m,p);};
 let w;
 try{w=new Watcher(c,f.rpc);assert.throws(()=>new Watcher(c,f.rpc),/locked/);assert.equal((await w.poll()).status,'RELEASED');w.close();w=new Watcher(c,f.rpc);assert.equal((await w.poll()).status,'RELEASED');assert.equal(sends,1);w.close();w=new Watcher(c,fixture({depth:2}).rpc);await assert.rejects(w.poll(),/DISCREPANCY/);assert.equal(sends,1);}finally{if(w&&w.lock)w.close();fs.rmSync(dir,{recursive:true,force:true});}
});
test('retrievable orphan release is rebroadcast using exactly the persisted bytes',async()=>{
 const fs=require('node:fs');const dir=local('.local/orphan-test-'+process.pid);fs.mkdirSync(dir,{recursive:true});
 const f=fixture(),view=await traceOpening(f.rpc,f.genesis,box);
 const release=tx(null,bsv.Script.fromHex(releaseScript({box_id:box,operator_idx:0,ibe_key_share:'55'.repeat(48),operator_sig:'66'.repeat(64)})));
 const stateFile=dir+'/state.json',c={stateFile,genesis:f.genesis,boxId:box,operatorIndex:0,operatorFile:dir+'/missing',executable:dir+'/missing'};
 fs.writeFileSync(stateFile,JSON.stringify({boxId:box,operatorIndex:0,genesis:f.genesis,artifactFingerprint,opening:view.opening,raw:release.toString(),txid:release.id,status:'published'}));
 let sends=0;const original=f.rpc.call;
 f.rpc.call=async(m,p=[])=>{
  if(m==='getrawmempool')return sends?[release.id]:[];
  if(m==='getrawtransaction'&&p[0]===release.id)return p[1]?{hex:release.toString(),blockhash:'orphan',confirmations:-1}:release.toString();
  if(m==='sendrawtransaction'){assert.equal(p[0],release.toString());sends++;return release.id;}
  return original(m,p);
 };
 let w;try{w=new Watcher(c,f.rpc);assert.equal((await w.poll()).status,'RELEASED');assert.equal(sends,1);assert.equal((await w.poll()).status,'RELEASED');assert.equal(sends,1);}finally{if(w)w.close();fs.rmSync(dir,{recursive:true,force:true});}
});
test('RPC rejects public addresses, hostnames and URL credentials',()=>{for(const url of ['http://example.com','http://localhost','http://192.168.1.1','https://127.0.0.1','http://u:p@127.0.0.1'])assert.throws(()=>new RegtestRPC({url}));});
test('RPC independently gates each mutation and rejects redirects',async()=>{
 let chain='main',active=false,redirect=false;const calls=[];
 const server=http.createServer((req,res)=>{let b='';req.on('data',x=>b+=x);req.on('end',()=>{const {method}=JSON.parse(b);calls.push(method);if(redirect){res.writeHead(302,{Location:'http://example.com'});return res.end('{}');}const result=method==='getblockchaininfo'?{chain}:method==='getnetworkinfo'?{networkactive:active,connections:0}:method==='getpeerinfo'?[]:'ok';res.end(JSON.stringify({result,error:null}));});});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 try{const rpc=new RegtestRPC({url:`http://127.0.0.1:${server.address().port}`});for(const method of ['fundrawtransaction','signrawtransaction','sendrawtransaction'])await assert.rejects(rpc.call(method),/Safety/);assert.ok(!calls.includes('sendrawtransaction'));chain='regtest';active=true;await assert.rejects(rpc.call('sendrawtransaction'),/Safety/);active=false;assert.equal(await rpc.call('sendrawtransaction'),'ok');chain='test';await assert.rejects(rpc.call('sendrawtransaction'),/Safety/);redirect=true;await assert.rejects(rpc.call('getblockcount'),/redirect/);}finally{await new Promise(r=>server.close(r));}
});
