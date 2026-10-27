'use strict';
const assert = require('node:assert/strict');
const {buildManifest,validateManifest,computeSlotOdds}=require('../manifest');
const {drawPack,DrawExhausted,drawIndex}=require('../draw');
const input=(weights)=>({name:'test',pack_size:2,allow_pack_duplicates:false,designs:weights.map((weight,id)=>({id,ref:'x',weight}))});
assert.throws(()=>buildManifest(input([99,1])),/attestation/);
assert.throws(()=>drawPack({...input([100000,1]),manifest_version:1,total_weight:100001},'box','seed'),DrawExhausted);
const m=buildManifest({...input([99,1]),per_slot_odds_published:true});
assert.deepEqual(m.slot_odds,[[{id:0,probability:'99/100'},{id:1,probability:'1/100'}],[{id:0,probability:'1/100'},{id:1,probability:'99/100'}]]);
assert.deepEqual(computeSlotOdds(m),m.slot_odds);
const bad=structuredClone(m); bad.slot_odds[1][0].probability='99/100';
assert.throws(()=>validateManifest(bad),/slot_odds/);
const absent=structuredClone(m); delete absent.slot_odds;
assert.throws(()=>validateManifest(absent),/slot_odds/);
assert.equal(drawPack(m,'box','seed').designs.length,2);
assert(buildManifest(input([101,99])).slot_odds); // exactly 1 pp: allowed
assert.throws(()=>buildManifest(input([102,98])),/attestation/);
assert.throws(()=>buildManifest({...input([1,1]),per_slot_odds_published:'true'}),/attestation/);
console.log('PASS hardening odds guard, disclosure integrity, unsafe budget');
// Real hash and literal preimage, independently obtained with Python hashlib.
const crypto=require('node:crypto'),fs=require('node:fs'),vm=require('node:vm');
const preimage='VAULT3-DRAW|'+'00'.repeat(32)+'|'+'11'.repeat(32)+'|2|3';
const digest='a3ae26ffa23407ba3010b78262b0bd33b3453527012c4f34ff3e0b6658a3bdbb';
assert.equal(crypto.createHash('sha256').update(preimage,'utf8').digest('hex'),digest);
assert.equal(drawIndex('00'.repeat(32),'11'.repeat(32),2,3,100),91);
const spec=fs.readFileSync(require.resolve('../VAULT-0003-draw-at-open.md'),'utf8');
assert(spec.includes(preimage));assert(spec.includes(digest));
for(const field of ['a|b','',null,'\ud800'])assert.throws(()=>drawIndex(field,'seed',0,0,100));
for(const arg of [-1,0.5,NaN,Number.MAX_SAFE_INTEGER+1])assert.throws(()=>drawIndex('box','seed',arg,0,100));
// Instrument crypto in a VM only: no production hash override or skipped validator.
const uniform=buildManifest(input([1,1]));
function capped(acceptAt){
 let calls=0;
 const sandbox={module:{exports:{}},require:name=>name==='node:crypto'?{createHash:()=>({update:text=>({digest:()=>{calls++;const parts=text.split('|');return parts[3]==='1'&&Number(parts[4])===acceptAt?'1':'0';}})})}:require(name==='./manifest'?'../manifest':'../odds')};
 vm.runInNewContext(fs.readFileSync(require.resolve('../draw'),'utf8'),sandbox);
 return {run:()=>sandbox.module.exports.drawPack(uniform,'box','seed'),calls:()=>calls};
}
const cap=capped(-1);assert.throws(cap.run,DrawExhausted);assert.equal(cap.calls(),10002);
const edge=capped(10000);assert.equal(edge.run().trace[1].retry,10000);assert.equal(edge.calls(),10002);
const last=capped(9999);assert.equal(last.run().trace[1].retry,9999);
const atLimit=buildManifest({...input([5000,1]),per_slot_odds_published:true});assert(atLimit.slot_odds);
assert.throws(()=>buildManifest({...input([5001,1]),per_slot_odds_published:true}),DrawExhausted);
const overridden=buildManifest({...input([1,1]),slots:{1:{table:[{id:0,weight:1},{id:1,weight:3}]}}});
assert.deepEqual(overridden.slot_odds[1],[{id:0,probability:'1/4'},{id:1,probability:'3/4'}]);
// Cache isolation: mutating returned odds cannot alter future verification.
const mutable=computeSlotOdds(uniform);mutable[0][0].probability='0/1';assert.deepEqual(computeSlotOdds(uniform),uniform.slot_odds);
// Too many distinct weights: bounded deterministic diagnostic, never false exact odds.
const large={...input(Array.from({length:20},(_,i)=>i+1)),pack_size:8,per_slot_odds_published:true};
let diagnostic;
assert.throws(()=>buildManifest(large),e=>{diagnostic=e.bound;return e.name==='OddsUnavailable'&&e.bound.upper>=e.bound.lower;});
assert.throws(()=>buildManifest(large),e=>{assert.deepEqual(e.bound,diagnostic);return true;});
console.log('PASS encoding, actual retry cap and boundary, table scope, cache safety, bounded sampling');
