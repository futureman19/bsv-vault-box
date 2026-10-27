'use strict';
// Exact ideal weighted-without-replacement marginals. Equal-weight designs
// are exchangeable, so enumerate counts per weight group rather than subsets.
const MAX_RETRIES=10000, MAX_TRANSITIONS=20000;
class DrawExhausted extends Error {
  constructor(message='Draw retry budget exhausted') { super(message); this.name='DrawExhausted'; this.code='DRAW_EXHAUSTED'; }
}
class OddsUnavailable extends Error {
  constructor(bound) { super('Exact slot_odds exceeds reference resource budget; sampled bounds are not publication odds'); this.name='OddsUnavailable'; this.bound=bound; }
}
const gcd=(a,b)=>{while(b){[a,b]=[b,a%b];}return a;};
function fraction(n,d=1n) { const g=gcd(n,d); return [n/g,d/g]; }
const add=(a,b)=>fraction(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,n,d)=>fraction(a[0]*n,a[1]*d);
const show=a=>`${a[0]}/${a[1]}`;
const cache=new Map();
function retryBudget(table,slots) {
  if(slots<2)return;
  let min=BigInt(table[0].weight),max=min;
  for(const row of table){const w=BigInt(row.weight);if(w<min)min=w;if(w>max)max=w;}
  if(max*BigInt(slots)>BigInt(MAX_RETRIES)*min)throw new DrawExhausted('Manifest expected retry bound exceeds 10000');
}
// Diagnostic only: deterministic xorshift32 sampling, Hoeffding + union bound.
// Never accepted as exact disclosure. Finite PRNG samples are not a proof.
function sampledBound(table,slots) {
  const samples=Math.max(1,Math.min(4096,Math.floor(1000000/(slots*table.length)))), counts=Array.from({length:slots},()=>new Uint32Array(table.length));
  let seed=0x5641554c;
  const random=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)/4294967296;};
  for(let k=0;k<samples;k++){
    const used=new Set(); let total=table.reduce((s,d)=>s+d.weight,0);
    for(let slot=0;slot<slots;slot++){
      let r=random()*total, chosen=-1;
      for(let i=0;i<table.length;i++)if(!used.has(i)){chosen=i;r-=table[i].weight;if(r<0)break;}
      used.add(chosen);total-=table[chosen].weight;counts[slot][chosen]++;
    }
  }
  const total=table.reduce((s,d)=>s+d.weight,0);
  let deviation=0;
  for(const row of counts)for(let i=0;i<table.length;i++)deviation=Math.max(deviation,Math.abs(row[i]/samples-table[i].weight/total));
  const epsilon=Math.sqrt(Math.log(2*slots*table.length/1e-6)/(2*samples));
  return {method:'fixed-seed diagnostic; IID Hoeffding assumption',seed:'5641554c',samples,confidence:0.999999,maxDeviation:deviation,lower:Math.max(0,deviation-epsilon),upper:Math.min(1,deviation+epsilon)};
}
function tableOdds(table,slots) {
  if(!slots)return [];
  const key=JSON.stringify([table.map(d=>[d.id,d.weight]),slots]);
  if(cache.has(key))return cache.get(key);
  const groups=[];const byWeight=new Map();
  for(const d of table){let g=byWeight.get(d.weight);if(g===undefined){g=groups.length;byWeight.set(d.weight,g);groups.push({weight:BigInt(d.weight),count:0});}groups[g].count++;}
  const total=groups.reduce((s,g)=>s+g.weight*BigInt(g.count),0n);
  let states=new Map([[groups.map(()=>0).join(','),[1n,1n]]]), transitions=0;
  const result=[];
  for(let slot=0;slot<slots;slot++){
    const marginal=groups.map(()=>[0n,1n]), next=new Map();
    for(const [state,p] of states){
      const used=state.split(',').map(Number);
      const remaining=total-groups.reduce((s,g,i)=>s+g.weight*BigInt(used[i]),0n);
      for(let i=0;i<groups.length;i++){
        const left=groups[i].count-used[i];if(!left)continue;
        if(++transitions>MAX_TRANSITIONS)throw new OddsUnavailable(sampledBound(table,slots));
        if(p[1].toString(2).length>8192)throw new OddsUnavailable(sampledBound(table,slots));
        const q=mul(p,groups[i].weight*BigInt(left),remaining);
        marginal[i]=add(marginal[i],q);
        if(slot+1<slots){const u=used.slice();u[i]++;const k=u.join(',');next.set(k,add(next.get(k)||[0n,1n],q));}
      }
    }
    result.push(table.map(d=>{const i=byWeight.get(d.weight);return {id:d.id,probability:show(mul(marginal[i],1n,BigInt(groups[i].count)))};}));
    states=next;
  }
  // Bound cache memory and never hand mutable cached objects to callers.
  if(cache.size>=8)cache.delete(cache.keys().next().value);
  cache.set(key,result);return result;
}
function computeSlotOdds(m) {
  if(!Number.isSafeInteger(m.pack_size)||m.pack_size<1||m.pack_size>100||m.designs.length>10000)throw new RangeError('Reference odds limit: 100 slots and 10000 designs');
  const mainSlots=m.pack_size-Object.keys(m.slots||{}).length;
  const main=tableOdds(m.designs,m.allow_pack_duplicates?Math.min(mainSlots,1):mainSlots);
  let index=0;
  return Array.from({length:m.pack_size},(_,slot)=>{
    const cfg=m.slots?.[String(slot)];
    return structuredClone(cfg?tableOdds(cfg.table,1)[0]:main[m.allow_pack_duplicates?0:index++]);
  });
}
function materiallyDeviates(m,odds) {
  return odds.some((rows,slot)=>{
    const cfg=m.slots?.[String(slot)],table=cfg?cfg.table:m.designs;
    const total=BigInt(cfg?cfg.total_weight:m.total_weight);
    return rows.some((row,i)=>{const [n,d]=row.probability.split('/').map(BigInt);let delta=n*total-BigInt(table[i].weight)*d;if(delta<0n)delta=-delta;return delta*100n>d*total;});
  });
}
module.exports={MAX_RETRIES,DrawExhausted,OddsUnavailable,retryBudget,computeSlotOdds,materiallyDeviates};
