import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
const samples=[];
for(let i=0;i<=80;i++){
 const p=i/80,v=pose(p);assert(Number.isFinite(v.lid)&&Number.isFinite(v.latch));
 if(p<=.25)assert.equal(v.lid,0);else assert(Math.abs(v.latch+80*Math.PI/180)<1e-12);
 assert(Math.abs(v.lid+105*Math.PI/180*Math.max(0,(p-.25)/.75))<1e-12);
 samples.push({progress:p,...v});
}
assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
writeFileSync(new URL('./motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalidAssetsRejected:true},null,2));
console.log('MOTION PASS: 81 staged samples, endpoints, clamping, invalid asset negatives');
