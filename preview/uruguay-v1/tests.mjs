import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
for(let i=0;i<=80;i++){
 const p=i/80,a=pose(p);assert(Number.isFinite(a.lid)&&Number.isFinite(a.latch));
 if(p<=.25)assert.equal(a.lid,0);
 if(p>=.25)assert(Math.abs(a.latch+80*Math.PI/180)<1e-10);
}
assert.equal(pose(0).latch,0);assert.equal(pose(0).lid,0);
assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-10);
assert.throws(()=>validateAsset({lid:false,triangles:10,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:10,bounds:[NaN,1]}));
console.log('MOTION PASS: 81 poses, staged 80/105 degrees; three invalid-asset controls rejected');
