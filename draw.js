'use strict';
const { createHash } = require('node:crypto');
const { validateManifest } = require('./manifest');
const D=1;
function natural(n) { if(!Number.isSafeInteger(n)||n<0) throw new TypeError('Expected nonnegative safe integer'); return n; }
function text(s) { if(typeof s!=='string'||!s.length||!s.isWellFormed()||s.includes('|')) throw new TypeError('Expected nonempty well-formed text without pipe delimiter'); }
function drawIndex(boxId,seed,slot,retry,totalWeight) {
  text(boxId); text(seed); natural(slot); natural(retry); natural(totalWeight);
  if(!totalWeight) throw new TypeError('Zero total weight');
  // Executed v3_ref.py baseline: textual fields, separators, decimal nonces.
  const h=createHash('sha256').update(`VAULT3-DRAW|${boxId}|${seed}|${slot}|${retry}`,'utf8').digest('hex');
  return Number(BigInt('0x'+h)%BigInt(totalWeight));
}
function drawPack(manifest,boxId,seed) {
  validateManifest(manifest); text(boxId); text(seed);
  const designs=[], trace=[], seen=new Map(); let retries=0;
  for(let slot=0;slot<manifest.pack_size;slot++) {
    const cfg=manifest.slots?.[String(slot)];
    const table=cfg?cfg.table:manifest.designs, total=cfg?cfg.total_weight:manifest.total_weight;
    const key=cfg?`slot${slot}`:'main';
    if(!seen.has(key)) seen.set(key,new Set());
    const used=seen.get(key); let retry=0;
    while(true) {
      const index=drawIndex(boxId,seed,slot,retry,total);
      let cumulative=0, id;
      for(const d of table) { cumulative+=d.weight; if(index<cumulative) { id=d.id; break; } }
      if(id===undefined) throw new Error('Weight walk overflow');
      if(manifest.allow_pack_duplicates||!used.has(id)) {
        designs.push(id); used.add(id); trace.push({slot,table:key,retry,design:id}); break;
      }
      retry=natural(retry+1); retries=natural(retries+1);
    }
  }
  return {designs,retries,trace};
}
function drawBlockHeight(openHeight,delay=D) { natural(openHeight); natural(delay); return natural(openHeight+delay); }
// Pure synchronous adapter. Caller supplies already-validated chain evidence.
function drawPackForOpen(manifest,boxId,openHeight,blockHashAtHeight,delay=D) {
  if(openHeight===null||openHeight===undefined) return null;
  const height=drawBlockHeight(openHeight,delay);
  if(typeof blockHashAtHeight!=='function') throw new TypeError('Expected synchronous block hash lookup');
  const seed=blockHashAtHeight(height);
  if(seed===null||seed===undefined) return null;
  return drawPack(manifest,boxId,seed);
}
module.exports={D,drawIndex,drawPack,drawBlockHeight,drawPackForOpen};
