'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const {ids,manifest,root,script,tagged,chain}=require('./checker-fixtures');
const {drawPack}=require('../draw');
function harness(data=chain(),rateLimit=false){
 const calls=[],waits=[];
 const context=vm.createContext({crypto:globalThis.crypto,TextEncoder,TextDecoder,Uint8Array,setTimeout:(f,ms)=>{waits.push(ms);f();},fetch:async url=>{
  const p=url.replace('https://api.whatsonchain.com/v1/bsv/main','');calls.push(p);
  if(rateLimit&&p==='/tx/'+ids.manifest){rateLimit=false;return {status:429};}
  const value=p.includes('/script/')?[{tx_hash:ids.sealed,tx_pos:0}]:data[p];
  return {status:value?200:404,ok:!!value,json:async()=>JSON.parse(JSON.stringify(value))};
 }});
 vm.runInContext(fs.readFileSync(require.resolve('../docs/vaultcheck'),'utf8')+';globalThis.checker=VaultCheck;',context);
 return {check:async(id=ids.open,options={manifestTxid:ids.manifest,mintTxid:ids.mint})=>JSON.parse(JSON.stringify(await context.checker.checkBox(id,3,options))),calls,waits};
}
test('recomputes pack from committed manifest, opening height +1, and validates mint',async()=>{
 const h=harness();const r=await h.check();assert.deepEqual(r.outputs[0].pack.designs,drawPack(manifest,ids.box,ids.seed).designs);assert.equal(r.outputs[0].mintStatus,'VALID');assert.equal(r.verdict,'OPENED-VERIFIED');assert.ok(r.evidence.some(e=>e.includes('pack:')));
});
test('tampered ordered designs are INVALID-MINT',async()=>{const d=chain();d['/tx/'+ids.mint].vout=[tagged('VAULT3-MINT',{manifest_root:root,box_id:ids.box,designs:[999,999,999]})];assert.equal((await harness(d).check()).verdict,'INVALID-MINT');});
test('missing draw block is pending, never invalid mint',async()=>{const d=chain();delete d['/block/height/101'];const r=await harness(d).check();assert.equal(r.outputs[0].packStatus,'PENDING');assert.equal(r.outputs[0].mintStatus,'PENDING');assert.ok(r.evidence.includes('pack pending — one more block'));assert.equal(r.verdict,'OPENED-VERIFIED');});
test('opened transfer uses original opening, not transfer height',async()=>{const h=harness();const r=await h.check(ids.transfer);assert.equal(r.outputs[0].openingTxid,ids.open);assert.ok(h.calls.includes('/block/height/101'));assert.ok(!h.calls.includes('/block/height/106'));});
test('unconfirmed opening never draws',async()=>{const d=chain();d['/tx/'+ids.open].confirmations=0;const h=harness(d);const r=await h.check();assert.equal(r.outputs[0].packStatus,'PENDING');assert.ok(!h.calls.includes('/block/height/101'));});
test('mismatched manifest commitment fails closed',async()=>{const d=chain();d['/tx/'+ids.manifest].vout=[tagged('VAULT3-MANIFEST',{...manifest,name:'tampered'})];await assert.rejects(harness(d).check(),/commitment/i);});
test('unrelated mint cannot validate even with correct designs',async()=>{const d=chain();d['/tx/'+ids.mint].vin=[{txid:ids.sealed,vout:0}];assert.equal((await harness(d).check()).verdict,'INVALID-MINT');});
test('manifest fetch retries 429 with backoff',async()=>{const h=harness(chain(),true);await h.check();assert.equal(h.calls.filter(x=>x==='/tx/'+ids.manifest).length,2);assert.ok(h.waits.includes(3000));});
test('legacy verdicts remain unchanged without a manifest locator',async()=>{const h=harness();assert.equal((await h.check(ids.sealed,{})).verdict,'SEALED-VERIFIED');assert.equal((await h.check(ids.open,{})).verdict,'OPENED-VERIFIED');});
test('missing ancestry fails closed instead of using transfer height',async()=>{const d=chain();delete d['/tx/'+ids.sealed];await assert.rejects(harness(d).check(),/opening|ancestor/i);});
test('compiler genesis-state parent is resolved',async()=>{const d=chain();d['/tx/'+ids.sealed].vout[0].scriptPubKey.hex=script(0).replace(/6a00010021[0-9a-f]{66}2500000000$/,'6a01010001000500000000');assert.equal((await harness(d).check()).outputs[0].openingTxid,ids.open);});
test('missing mint and locator are unverified errors',async()=>{const d=chain();delete d['/tx/'+ids.mint];await assert.rejects(harness(d).check(),/unavailable/);await assert.rejects(harness().check(ids.open,{mintTxid:ids.mint}),/Manifest txid required/);});
test('invalid manifest weight and duplicate payload are rejected',async()=>{const d=chain();d['/tx/'+ids.manifest].vout=[tagged('VAULT3-MANIFEST',{...manifest,total_weight:999})];await assert.rejects(harness(d).check(),/weight/);d['/tx/'+ids.manifest].vout=[tagged('VAULT3-MANIFEST',manifest),tagged('VAULT3-MANIFEST',manifest)];await assert.rejects(harness(d).check(),/exactly one/);});
test('inline draw matches library over 25 seeded catalogs',async()=>{
 const {buildManifest,manifestRoot}=require('../manifest');
 for(let i=0;i<25;i++){
  const m=buildManifest({name:'Unicode é 😀 '+i,pack_size:4,allow_pack_duplicates:i%2===0,per_slot_odds_published:true,designs:Array.from({length:6},(_,j)=>({id:j,ref:'r',weight:(j+1)*(i+1)})),slots:{3:{table:[{id:0,weight:1},{id:5,weight:2}]}}});
  const d=chain();const hash=manifestRoot(m);d['/tx/'+ids.manifest].vout=[tagged('VAULT3-MANIFEST',m)];
  for(const [id,state] of [[ids.sealed,0],[ids.open,1]])d['/tx/'+id].vout[0].scriptPubKey.hex=script(state,hash);
  const r=await harness(d).check(ids.open,{manifestTxid:ids.manifest});assert.deepEqual(r.outputs[0].pack,drawPack(m,ids.box,ids.seed));
 }
});
test('draw block must link to the opening block',async()=>{const d=chain();d['/block/height/101'].previousblockhash=ids.seed;await assert.rejects(harness(d).check(),/block|reorg/i);});
