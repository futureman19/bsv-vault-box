import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){let p=i/80,q=pose(p);assert(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);if(p>=.25)assert(Math.abs(q.latch+80*Math.PI/180)<1e-12);}
assert.equal(pose(0).lid,0);assert.equal(pose(0).latch,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
for(const a of [{lid:false,triangles:5,bounds:[0,1]},{lid:true,triangles:0,bounds:[0,1]},{lid:true,triangles:5,bounds:[NaN,1]}])assert.throws(()=>validateAsset(a));
console.log('PASS motion: 81 poses, staged 80/105 endpoints; missing hinge, zero triangles and nonfinite bounds rejected');
