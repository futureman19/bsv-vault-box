import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80, s=pose(p);
 assert.ok(Math.abs(s.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-12);
 assert.ok(Math.abs(s.lid+105*Math.PI/180*Math.max(0,(p-.25)/.75))<1e-12);
 if(p<=.25)assert.equal(s.lid,0);
}
assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('PASS motion: 81 staged poses, endpoints, clamps, invalid-asset negative controls');
