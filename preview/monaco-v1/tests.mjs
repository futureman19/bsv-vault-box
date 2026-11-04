import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
const samples=[];
for(let i=0;i<=80;i++){
 const p=i/80,q=pose(p);assert(Number.isFinite(q.lid)&&Number.isFinite(q.latch));
 if(p<=.25)assert.equal(q.lid,0);else assert(Math.abs(q.latch+80*Math.PI/180)<1e-12);
 assert(q.lid<=0&&q.lid>=-105*Math.PI/180);samples.push({progress:p,...q});
}
assert.equal(pose(0).latch,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN,1]}));
validateAsset({lid:true,triangles:1,bounds:[0,1]});
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,negative_controls_rejected:3},null,2));
console.log('MOTION_PASS 81 poses; three invalid-asset negatives rejected');
