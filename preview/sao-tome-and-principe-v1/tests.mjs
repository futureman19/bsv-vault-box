import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
for(let i=0;i<=80;i++){
 const p=i/80,v=pose(p);assert(Math.abs(v.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-10);
 assert(Math.abs(v.lid+105*Math.PI/180*Math.max(0,(p-.25)/.75))<1e-10);
 if(p<=.25)assert.equal(v.lid,0);else assert.equal(v.latch,-80*Math.PI/180);
}
assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('PASS 81 staged poses; endpoints; invalid geometry negative controls');
