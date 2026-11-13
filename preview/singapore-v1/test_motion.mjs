import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
const samples=[];
for(let i=0;i<=80;i++){const p=i/80,v=pose(p);assert(Number.isFinite(v.lid)&&Number.isFinite(v.latch));if(p<=.25)assert.equal(v.lid,0);if(p>=.25)assert(Math.abs(v.latch+80*Math.PI/180)<1e-12);samples.push({p,...v});}
assert.equal(pose(0).lid,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalid_assets_rejected:true},null,2));console.log('MOTION PASS: 81 staged samples; invalid geometry rejected');
