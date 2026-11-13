import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,a=pose(p);assert(Number.isFinite(a.lid)&&Number.isFinite(a.latch));
 if(p<=.25)assert.equal(a.lid,0);
 else assert(Math.abs(a.latch+80*Math.PI/180)<1e-10);
}
assert.equal(pose(0).latch,0);assert.equal(pose(0).lid,0);
assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-10);
for(const a of [{lid:false,triangles:1,bounds:[0,1]},{lid:true,triangles:0,bounds:[0,1]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(a));
console.log('MOTION PASS: 81 staged poses; endpoints; 3 invalid-asset negative controls rejected');
