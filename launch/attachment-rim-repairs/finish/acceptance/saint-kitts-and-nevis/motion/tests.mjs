import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,v=pose(p);
 assert.ok(Number.isFinite(v.lid)&&Number.isFinite(v.latch));
 if(p<=.25)assert.equal(v.lid,0);
 else assert.ok(Math.abs(v.latch+80*Math.PI/180)<1e-12);
}
assert.equal(pose(0).latch,0);
assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
assert.throws(()=>validateAsset({lid:false,triangles:50,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:50,bounds:[NaN,1]}));
console.log('MOTION PASS: 81 staged poses, endpoints/clamps, 3 malformed-asset negative controls');
