import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,s=pose(p);
 assert.ok(Math.abs(s.lid+(p<=.25?0:105*Math.PI/180*(p-.25)/.75))<1e-12);
 assert.ok(Math.abs(s.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-12);
}
assert.throws(()=>validateAsset({lid:false,triangles:10,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:10,bounds:[NaN,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
console.log('MOTION PASS 81 poses; 3 invalid-asset controls rejected');
