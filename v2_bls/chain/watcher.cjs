'use strict';
const fs=require('node:fs'), path=require('node:path'), crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const {bsv}=require(path.join(root,'vault/node_modules/scrypt-ts'));
const {Vault}=require(path.join(root,'vault/dist/contracts/vault.js'));
const artifact=JSON.parse(fs.readFileSync(path.join(root,'vault/artifacts/vault.json'),'utf8'));
Vault.loadArtifact(artifact);
const artifactFingerprint=crypto.createHash('sha256').update(JSON.stringify({hex:artifact.hex,abi:artifact.abi,stateProps:artifact.stateProps})).digest('hex');
const pin=require('./artifact-pin.json');
if(artifactFingerprint!==pin.artifactFingerprint || artifact.compilerVersion!==pin.compilerVersion)throw Error('Canonical VAULT-0001 artifact fingerprint mismatch');
function hex(s,n) {if(typeof s!=='string'||!new RegExp(`^[0-9a-f]{${n*2}}$`).test(s))throw Error(`Expected canonical ${n}-byte hex`);return s;}
function local(p) {const full=path.resolve(root,p);if(!full.startsWith(root+path.sep))throw Error('Path outside repository');let parent=full;while(!fs.existsSync(parent))parent=path.dirname(parent);if(!fs.realpathSync(parent).startsWith(fs.realpathSync(root)+path.sep)&&parent!==root)throw Error('Symlink escapes repository');return full;}
function decodeVault(script) {
 const d=Vault.fromLockingScript(script);
 if(d.boxState!==0n&&d.boxState!==1n)throw Error('Invalid state');
 hex(d.boxId,32);hex(d.contentRef,32);
 if(!/^(02|03)[0-9a-f]{64}$/.test(d.owner))throw Error('Invalid compressed owner');
 // Constructor pushes stay immutable even when stateful owner/state change.
 // Rebuild the original template arguments, then the decoded state trailer.
 const args=d.delegateInstance.ctorArgs().map(a=>a.value);
 const fresh=new Vault(...args);
 fresh.boxState=d.boxState; fresh.owner=d.owner;
 if(d.delegateInstance.isGenesis)fresh.markAsGenesis();
 if(fresh.lockingScript.toHex()!==script)throw Error('Noncanonical artifact reconstruction');
 return {state:Number(d.boxState),boxId:d.boxId,contentRef:d.contentRef,owner:d.owner};
}
function parseRaw(raw,id) {const tx=new bsv.Transaction(raw);if(tx.id!==id || tx.toString()!==raw)throw Error('Raw transaction hash/encoding mismatch');return tx;}
async function traceOpening(rpc,genesis,boxId,confirmations=3) {
 hex(genesis.txid,32);hex(boxId,32);
 if(!Number.isInteger(genesis.vout)||genesis.vout<0||!Number.isInteger(confirmations)||confirmations<3)throw Error('Invalid pin/depth');
 const info=await rpc.assertRegtest();const tip=info.bestblockhash;const height=info.blocks;
 const g=await rpc.call('getrawtransaction',[genesis.txid,1]);
 if(!g.blockhash || g.confirmations<1)throw Error('Genesis not confirmed');
 const gh=await rpc.call('getblockheader',[g.blockhash]);
 if(await rpc.call('getblockhash',[gh.height])!==g.blockhash)throw Error('Noncanonical genesis');
 const gt=parseRaw(g.hex,genesis.txid),out=gt.outputs[genesis.vout];if(!out)throw Error('Missing genesis output');
 let state=decodeVault(out.script.toHex());if(state.state!==0||state.boxId!==boxId)throw Error('Genesis pin does not identify sealed box');
 let current={...genesis},amount=out.satoshis,opening=null;
 for(let h=gh.height;h<=height;h++) {
   const bh=await rpc.call('getblockhash',[h]);const block=await rpc.call('getblock',[bh,1]);
   for(const item of block.tx) {
     const id=typeof item==='string'?item:item.txid;
     if(id===genesis.txid)continue;
     const raw=await rpc.call('getrawtransaction',[id,0]);const tx=parseRaw(raw,id);
     const spends=tx.inputs.filter(i=>i.prevTxId.toString('hex')===current.txid&&i.outputIndex===current.vout);
     if(!spends.length)continue;
     if(spends.length!==1||!tx.outputs[0])throw Error('Invalid lineage spend');
     const next=decodeVault(tx.outputs[0].script.toHex());
     if(next.boxId!==boxId||next.contentRef!==state.contentRef||tx.outputs[0].satoshis!==amount)throw Error('Lineage immutable/value mismatch');
     if(state.state===1&&next.state!==1)throw Error('Reseal');
     if(state.state===0&&next.state===1) {
       if(next.owner!==state.owner)throw Error('Artifact open changed owner');
       if(opening)throw Error('Multiple openings');
       opening={txid:id,blockhash:bh,height:h,confirmations:height-h+1};
     }
     // The normative artifact permits only a vault at output zero and optional P2PKH change.
     if(tx.outputs.length>2 || (tx.outputs[1]&&!tx.outputs[1].script.isPublicKeyHashOut()))throw Error('Invalid covenant output shape');
     state=next;current={txid:id,vout:0};
   }
 }
 if(await rpc.call('getbestblockhash')!==tip)throw Error('Chain changed during lineage scan');
 if(opening&&await rpc.call('getblockhash',[opening.height])!==opening.blockhash)throw Error('Opening reorg');
 return {status:opening?(opening.confirmations>=confirmations?'READY':'IMMATURE'):'SEALED',opening,current,artifactFingerprint,tip};
}
function releaseScript(r) {
 hex(r.box_id,32);hex(r.ibe_key_share,48);hex(r.operator_sig,64);
 if(!Number.isInteger(r.operator_idx)||r.operator_idx<0||r.operator_idx>255)throw Error('Invalid operator index');
 const s=new bsv.Script().add(bsv.Opcode.OP_FALSE).add(bsv.Opcode.OP_RETURN);
 for(const b of [Buffer.from('VAULT2-REL'),Buffer.from(r.box_id,'hex'),Buffer.from([r.operator_idx]),Buffer.from(r.ibe_key_share,'hex'),Buffer.from(r.operator_sig,'hex')])s.add(b);
 return s.toHex();
}
function save(file,value) {const tmp=file+'.tmp';const fd=fs.openSync(tmp,'w',0o600);try{fs.writeFileSync(fd,JSON.stringify(value));fs.fsyncSync(fd);}finally{fs.closeSync(fd);}fs.renameSync(tmp,file);}
class Watcher {
 constructor(config,rpc) {
   this.c=config;this.rpc=rpc;this.file=local(config.stateFile);this.operator=local(config.operatorFile);this.exe=local(config.executable);
   hex(config.boxId,32);if(!Number.isInteger(config.operatorIndex)||config.operatorIndex<0||config.operatorIndex>255)throw Error('Invalid operator index');
   fs.mkdirSync(path.dirname(this.file),{recursive:true});this.lock=this.file+'.lock';
   if(fs.existsSync(this.lock)) {const pid=Number(fs.readFileSync(this.lock,'utf8'));if(!Number.isInteger(pid)||pid<1)throw Error('Invalid lock');let alive=true;try{process.kill(pid,0);}catch(e){if(e.code==='ESRCH')alive=false;else throw e;}if(alive)throw Error('Operator state locked');fs.unlinkSync(this.lock);}
   fs.writeFileSync(this.lock,String(process.pid),{flag:'wx',mode:0o600});
 }
 close(){if(this.lock){fs.unlinkSync(this.lock);this.lock=null;}}
 async trace(){return traceOpening(this.rpc,this.c.genesis,this.c.boxId,this.c.confirmations??3);}
 async poll() {
   let saved=fs.existsSync(this.file)?JSON.parse(fs.readFileSync(this.file,'utf8')):null;
   if(saved&&(saved.boxId!==this.c.boxId||saved.operatorIndex!==this.c.operatorIndex||saved.artifactFingerprint!==artifactFingerprint||JSON.stringify(saved.genesis)!==JSON.stringify(this.c.genesis)))throw Error('Persistent release identity mismatch');
   const view=await this.trace();
   if(saved&&(view.status!=='READY'||view.opening.txid!==saved.opening.txid||view.opening.blockhash!==saved.opening.blockhash))throw Error('UNSEALED-DISCREPANCY: prepared/released opening changed; halted');
   if(view.status!=='READY')return view;
   if(!saved) {
     let rec;
     try { rec=JSON.parse(execFileSync(this.exe,['release','--operator',this.operator,'--box',this.c.boxId],{encoding:'utf8',timeout:30000,windowsHide:true,stdio:['ignore','pipe','pipe']})); }
     catch { throw Error('Local share signer failed (output suppressed)'); }
     if(rec.box_id!==this.c.boxId||rec.operator_idx!==this.c.operatorIndex)throw Error('Signer identity mismatch');
     const script=releaseScript(rec);
     const raw=new bsv.Transaction().addOutput(new bsv.Transaction.Output({script:bsv.Script.fromHex(script),satoshis:0})).uncheckedSerialize();
     const funded=await this.rpc.call('fundrawtransaction',[raw,{changePosition:1,lockUnspents:true}]);
     const signed=await this.rpc.call('signrawtransaction',[funded.hex]);
     if(!signed.complete)throw Error('Wallet signing incomplete');
     const tx=new bsv.Transaction(signed.hex);
     if(tx.outputs[0].satoshis!==0||tx.outputs[0].script.toHex()!==script||tx.outputs.length>2)throw Error('Wallet mutated release');
     saved={boxId:this.c.boxId,operatorIndex:this.c.operatorIndex,genesis:this.c.genesis,artifactFingerprint,opening:view.opening,raw:signed.hex,txid:tx.id,status:'prepared'};
     // Durable bytes BEFORE send: unknown broadcast outcomes only retry identical tx.
     save(this.file,saved);
   }
   const check=await this.trace();
   if(check.status!=='READY'||check.opening.txid!==saved.opening.txid||check.opening.blockhash!==saved.opening.blockhash)throw Error('UNSEALED-DISCREPANCY: reorg before publication');
   let known=null;try{known=await this.rpc.call('getrawtransaction',[saved.txid,0]);}catch(e){if(e.code!==-5)throw e;}
   if(known && known!==saved.raw)throw Error('Release readback mismatch');
   let present=false;
   if(known) {
     present=(await this.rpc.call('getrawmempool')).includes(saved.txid);
     if(!present) {
       const meta=await this.rpc.call('getrawtransaction',[saved.txid,1]);
       if(meta.blockhash && meta.confirmations>0) {
         const header=await this.rpc.call('getblockheader',[meta.blockhash]);
         present=header.confirmations>0 && await this.rpc.call('getblockhash',[header.height])===meta.blockhash;
       }
     }
   }
   // Indexed orphan bytes are historical availability, not publication.
   if(!present) {const id=await this.rpc.call('sendrawtransaction',[saved.raw]);if(id!==saved.txid)throw Error('Broadcast txid mismatch');const back=await this.rpc.call('getrawtransaction',[saved.txid,0]);if(back!==saved.raw)throw Error('Broadcast readback mismatch');}
   saved.status='published';save(this.file,saved);
   return {status:'RELEASED',txid:saved.txid,opening:check.opening};
 }
}
module.exports={Watcher,traceOpening,decodeVault,releaseScript,artifactFingerprint,local,bsv,Vault,parseRaw};
