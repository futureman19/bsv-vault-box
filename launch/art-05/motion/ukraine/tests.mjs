import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {pose,validateAsset} from './motion.mjs';
const samples=[];
for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);else assert(Math.abs(q.latch+80*Math.PI/180)<1e-12);samples.push({p,...q});}
assert.deepEqual(pose(0),{lid:0,latch:0});assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
for(const bad of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,negative_invalid_assets_rejected:3},null,2));console.log('MOTION PASS: 81 staged poses; 3 invalid-asset controls rejected');
