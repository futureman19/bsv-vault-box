import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,s=pose(p);assert(Number.isFinite(s.lid)&&Number.isFinite(s.latch));
 if(p<=.25)assert.equal(s.lid,0);
 if(p>=.25)assert(Math.abs(s.latch+80*Math.PI/180)<1e-12);
}
assert.equal(pose(0).latch,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('MOTION PASS: 81 staged poses and 3 invalid-asset negative controls');
