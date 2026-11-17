import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,q=pose(p);
 assert.ok(Math.abs(q.lid+(p<=.25?0:105*Math.PI/180*(p-.25)/.75))<1e-12);
 assert.ok(Math.abs(q.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-12);
 if(p<=.25)assert.equal(q.lid,0);
}
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
console.log('MOTION PASS: 81 staged poses; invalid geometry controls rejected');
