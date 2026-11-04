import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
let samples=[];
for(let i=0;i<=80;i++){let p=i/80,r=pose(p);assert(Number.isFinite(r.lid)&&Number.isFinite(r.latch));if(p<=.25)assert.equal(r.lid,0);else assert.equal(r.latch,-80*Math.PI/180);samples.push({p,...r});}
assert.equal(pose(1).lid,-105*Math.PI/180);assert.equal(pose(0).latch,0);
for(const bad of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));
validateAsset({lid:true,triangles:1,bounds:[0,1]});
writeFileSync(new URL('./motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalidGeometryRejected:3},null,2));console.log('MOTION_PASS samples=81 negative_controls=3');
