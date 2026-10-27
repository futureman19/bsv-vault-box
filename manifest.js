'use strict';
const { createHash } = require('node:crypto');
const {retryBudget,computeSlotOdds,materiallyDeviates}=require('./odds');
const own = (o,k) => Object.prototype.hasOwnProperty.call(o,k);
function integer(n, min=0) {
  if (!Number.isSafeInteger(n) || n < min) throw new TypeError('Expected safe integer >= '+min);
  return n;
}
function object(o) {
  if (!o || typeof o !== 'object' || ![Object.prototype,null].includes(Object.getPrototypeOf(o))) throw new TypeError('Expected plain JSON object');
}
// Python sorts Unicode code points, not UTF-16 code units or numeric JS keys.
function compareKeys(a,b) {
  const aa=Array.from(a,c=>c.codePointAt(0)), bb=Array.from(b,c=>c.codePointAt(0));
  for(let i=0;i<Math.min(aa.length,bb.length);i++) if(aa[i]!==bb[i]) return aa[i]-bb[i];
  return aa.length-bb.length;
}
function quote(s) {
  return JSON.stringify(s).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
}
function canonicalSerialize(value) {
  const active=new Set();
  function encode(v) {
    if(v===null) return 'null';
    if(typeof v==='string') return quote(v);
    if(typeof v==='boolean') return String(v);
    if(typeof v==='number') { if(!Number.isSafeInteger(v)) throw new TypeError('Canonical numbers must be safe integers'); return String(v); }
    if(typeof v!=='object') throw new TypeError('Unsupported JSON value');
    if(active.has(v)) throw new TypeError('Cyclic JSON');
    active.add(v);
    let result;
    if(Array.isArray(v)) {
      const parts=[];
      for(let i=0;i<v.length;i++) { if(!own(v,i)) throw new TypeError('Sparse array'); parts.push(encode(v[i])); }
      result='['+parts.join(',')+']';
    } else {
      object(v);
      if(Object.getOwnPropertySymbols(v).length) throw new TypeError('Symbol keys unsupported');
      result='{'+Object.keys(v).sort(compareKeys).map(k=>quote(k)+':'+encode(v[k])).join(',')+'}';
    }
    active.delete(v); return result;
  }
  return encode(value);
}
function manifestRoot(m) { return createHash('sha256').update(canonicalSerialize(m),'utf8').digest('hex'); }
function tableWeight(table, catalog) {
  if(!Array.isArray(table)||!table.length) throw new TypeError('Empty weight table');
  const ids=new Set(); let total=0;
  for(const d of table) {
    object(d); integer(d.id); integer(d.weight,1);
    if(ids.has(d.id)) throw new TypeError('Duplicate design id');
    if(catalog&&!catalog.has(d.id)) throw new TypeError('Slot design absent from catalog');
    ids.add(d.id); total=integer(total+d.weight,1);
  }
  return total;
}
function validateStructure(m) {
  object(m); canonicalSerialize(m);
  if(typeof m.name!=='string'||m.manifest_version!==1||typeof m.allow_pack_duplicates!=='boolean') throw new TypeError('Invalid manifest fields');
  integer(m.pack_size,1);
  if(tableWeight(m.designs)!==m.total_weight) throw new TypeError('Incorrect main total_weight');
  for(const d of m.designs) if(typeof d.ref!=='string') throw new TypeError('Missing design ref');
  const catalog=new Set(m.designs.map(d=>d.id));
  const slots=m.slots===undefined?{}:m.slots; object(slots);
  for(const [key,cfg] of Object.entries(slots)) {
    if(!/^(0|[1-9][0-9]*)$/.test(key)||!Number.isSafeInteger(Number(key))||Number(key)>=m.pack_size) throw new TypeError('Invalid slot key');
    object(cfg);
    if(tableWeight(cfg.table,catalog)!==cfg.total_weight) throw new TypeError('Incorrect slot total_weight');
  }
  // Each explicit slot is its own table key, even if its table equals another.
  if(!m.allow_pack_duplicates && m.designs.length < m.pack_size-Object.keys(slots).length) throw new TypeError('Not enough designs for main-table slots');
  if(!m.allow_pack_duplicates) retryBudget(m.designs,m.pack_size-Object.keys(slots).length);
  return m;
}
function validateManifest(m) {
  validateStructure(m);
  if(m.per_slot_odds_published!==undefined && typeof m.per_slot_odds_published!=='boolean') throw new TypeError('Invalid odds attestation');
  if(!m.allow_pack_duplicates || m.slot_odds!==undefined) {
    const odds=computeSlotOdds(m);
    if(materiallyDeviates(m,odds) && m.per_slot_odds_published!==true) throw new TypeError('Per-slot odds deviate > 1 percentage point: explicit attestation required');
    if(m.slot_odds===undefined || canonicalSerialize(m.slot_odds)!==canonicalSerialize(odds)) throw new TypeError('Missing or incorrect slot_odds');
  }
  return m;
}
function buildManifest(input) {
  // Copy JSON values without allowing JSON.stringify to drop unsupported data.
  object(input);
  const m=JSON.parse(canonicalSerialize(input));
  if(m.manifest_version===undefined) m.manifest_version=1;
  if(m.total_weight===undefined) m.total_weight=tableWeight(m.designs);
  if(m.slots!==undefined) {
    object(m.slots);
    for(const cfg of Object.values(m.slots)) {
      object(cfg);
      if(cfg.total_weight===undefined) cfg.total_weight=tableWeight(cfg.table);
    }
  }
  validateStructure(m);
  if(!m.allow_pack_duplicates && m.slot_odds===undefined) m.slot_odds=computeSlotOdds(m);
  return validateManifest(m);
}
module.exports={buildManifest,validateManifest,canonicalSerialize,manifestRoot,computeSlotOdds};
