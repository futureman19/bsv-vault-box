'use strict';
// Bounded real-regtest integration. Three independent watcher processes per
// round; each receives one DKG share file. No mocked RPC or covenant-valid flag.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const { spawn, spawnSync } = require('node:child_process');
const assert = require('node:assert/strict');
const { localRPC, prepare, createBox, transferBox, openBox, root } = require('./covenant.cjs');
const { bsv, releaseScript, artifactFingerprint } = require('../chain/watcher.cjs');
const exe = path.join(root, '.local/vault2.exe');
const runDir = fs.mkdtempSync(path.join(root, '.local/milestone1-'));
const setup = path.join(runDir, 'committee'), pub = path.join(setup, 'public.json');
const boxId = crypto.randomBytes(32).toString('hex');
const nft = Buffer.from('NFT-0001: pre-assigned before covenant creation');
function cli(args, input, expectedOK = true) {
 const r = spawnSync(exe, args, { input, encoding: 'utf8', timeout: 30000, windowsHide: true });
 if (expectedOK && r.status !== 0) throw Error(`vault2 ${args[0]} failed: ${r.stderr}`);
 if (!expectedOK) { assert.notEqual(r.status, 0, 'negative decryption/verification unexpectedly succeeded'); return; }
 return r.stdout;
}
function json(file, data) { fs.writeFileSync(file, JSON.stringify(data), { mode: 0o600 }); }
async function dataTx(rpc, tag, parts) {
 const script = new bsv.Script().add(bsv.Opcode.OP_FALSE).add(bsv.Opcode.OP_RETURN).add(Buffer.from(tag));
 for (const part of parts) script.add(part);
 const raw = new bsv.Transaction().addOutput(new bsv.Transaction.Output({script, satoshis:0})).uncheckedSerialize();
 const funded = await rpc.call('fundrawtransaction', [raw, {changePosition:1,lockUnspents:true}]);
 const signed = await rpc.call('signrawtransaction', [funded.hex]);
 assert.equal(signed.complete, true);
 const txid = await rpc.call('sendrawtransaction', [signed.hex]);
 assert.equal(await rpc.call('getrawtransaction', [txid]), signed.hex);
 return txid;
}
async function round(configs, expected) {
 const results = await Promise.all(configs.map(config => new Promise((resolve,reject) => {
  const child = spawn(process.execPath, [path.join(root,'v2_bls/chain/operator.cjs'),'--config',config,'--once'], {cwd:root,windowsHide:true,stdio:['ignore','pipe','pipe']});
  const pid=child.pid; let out='',err='';
  const timer=setTimeout(()=>{child.kill();reject(Error('operator exceeded 45-second bound'));},45000);
  child.stdout.on('data', b=>out+=b); child.stderr.on('data', b=>err+=b);
  child.on('error',e=>{clearTimeout(timer);reject(e);});
  child.on('close',code=>{clearTimeout(timer);if(code!==0)return reject(Error(`operator failed: ${err}`));try{const value=JSON.parse(out.trim());assert.equal(value.status,expected);resolve({pid,...value});}catch(e){reject(e);}});
 })));
 assert.equal(new Set(results.map(r=>r.pid)).size,3);
 console.log(JSON.stringify({phase:expected,operators:results.map(r=>r.pid)}));
 return results;
}
async function main() {
 const rpc=localRPC(); await rpc.assertRegtest();
 cli(['setup','--dir',setup]);
 const ct=cli(['encrypt','--public',pub,'--box',boxId],nft);
 const cipher=path.join(runDir,'cipher.json'); fs.writeFileSync(cipher,ct);
 const releases=path.join(runDir,'releases.json'); json(releases,[]);
 const decrypt=() => ['decrypt','--public',pub,'--box',boxId,'--cipher',cipher,'--releases',releases];
 cli(decrypt(),undefined,false);
 const ctx=await prepare(rpc);
 const setupTx=await dataTx(rpc,'VAULT2-SETUP',[fs.readFileSync(pub)]);
 const ciphertextTx=await dataTx(rpc,'VAULT2-CT',[Buffer.from(boxId,'hex'),Buffer.from(ct)]);
 const contentRef=crypto.createHash('sha256').update(ct).digest('hex');
 const {box,genesis}=await createBox(ctx,contentRef,boxId);
 await rpc.call('generate',[1]);
 const rpcFile=path.join(runDir,'rpc.json');
 // Credentials stay in ignored runtime, never stdout or evidence.
 const cfg=Object.fromEntries(fs.readFileSync(path.join(root,'.local/node/bitcoin.conf'),'utf8').split(/\r?\n/).filter(x=>x.includes('=')).map(x=>{const i=x.indexOf('=');return[x.slice(0,i),x.slice(i+1)];}));
 json(rpcFile,{url:'http://127.0.0.1:18483',username:cfg.rpcuser,password:cfg.rpcpassword});
 const configs=[0,1,2].map(i=>{const file=path.join(runDir,`watcher-${i}.json`);json(file,{rpcFile,genesis,boxId,operatorIndex:i,operatorFile:path.join(setup,`operator-${i}.json`),executable:exe,stateFile:path.join(runDir,`state-${i}.json`),confirmations:3});return file;});
 const assertNoReleases=()=>{for(let i=0;i<3;i++)assert.equal(fs.existsSync(path.join(runDir,`state-${i}.json`)),false);};
 await round(configs,'SEALED');assertNoReleases();
 const transfer=await transferBox(ctx,box); await rpc.call('generate',[1]);
 await round(configs,'SEALED');assertNoReleases();
 const opening=await openBox(ctx,transfer.box,transfer.key);
 await round(configs,'SEALED');assertNoReleases();
 await rpc.call('generate',[2]);
 await round(configs,'IMMATURE');assertNoReleases();cli(decrypt(),undefined,false);
 await rpc.call('generate',[1]);
 const first=await round(configs,'RELEASED');
 const again=await round(configs,'RELEASED');
 assert.deepEqual(again.map(r=>r.txid),first.map(r=>r.txid),'restart produced duplicate release transaction');
 await rpc.call('generate',[1]);
 const confirmedRestart=await round(configs,'RELEASED');
 assert.deepEqual(confirmedRestart.map(r=>r.txid),first.map(r=>r.txid));
 const records=[];
 for(let i=0;i<3;i++) {
  const tx=await rpc.call('getrawtransaction',[first[i].txid,1]);assert.ok(tx.confirmations>=1);
  const parsed=new bsv.Transaction(tx.hex),chunks=parsed.outputs[0].script.chunks;
  assert.equal(chunks.length,7);assert.equal(chunks[0].opcodenum,0);assert.equal(chunks[1].opcodenum,106);
  assert.equal(chunks[2].buf.toString(),'VAULT2-REL');
  const record={box_id:chunks[3].buf.toString('hex'),operator_idx:chunks[4].buf[0],ibe_key_share:chunks[5].buf.toString('hex'),operator_sig:chunks[6].buf.toString('hex')};
  assert.equal(parsed.outputs[0].script.toHex(),releaseScript(record));
  assert.equal(record.operator_idx,i);assert.equal(record.box_id,boxId);
  assert.equal(JSON.parse(cli(['verify','--public',pub],JSON.stringify(record))).valid,true);records.push(record);
 }
 for(let missing=0;missing<3;missing++){json(releases,records.filter((_,i)=>i!==missing));cli(decrypt(),undefined,false);}
 json(releases,records);assert.equal(cli(decrypt()),nft.toString());
 const forged={...records[0],ibe_key_share:'00'.repeat(48)};
 cli(['verify','--public',pub],JSON.stringify(forged),false);
 const info=await rpc.assertRegtest();
 const evidence={status:'PASS',network:info.chain,height:info.blocks,threshold:'3-of-3',boxId,artifactFingerprint,setupTx,ciphertextTx,genesis,transferTx:transfer.txid,openingTx:opening.txid,releaseTxs:first.map(r=>r.txid),checks:['sealed-no-release','transfer-no-release','mempool-no-release','two-confirmations-no-release','three-confirmations-release','three-distinct-operator-processes','restart-idempotent','confirmed-onchain-records-publicly-verified','all-two-share-subsets-fail','three-shares-exact-NFT','forged-share-rejected'],limitations:['single-process DKG setup','shared-host plaintext test shares','shared regtest node/wallet','no mix-net or issuer secrecy','one box only; Step3 deferred','3-of-3 cannot survive one operator loss'],runtime:path.relative(root,runDir)};
 json(path.join(runDir,'evidence.json'),evidence);console.log(JSON.stringify(evidence,null,2));
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});
