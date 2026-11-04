import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,s=pose(p);
 assert.ok(Math.abs(s.latch+Math.min(p/.25,1)*80*Math.PI/180)<1e-12);
 assert.ok(Math.abs(s.lid+Math.max(0,(p-.25)/.75)*105*Math.PI/180)<1e-12);
 if(p<=.25)assert.equal(s.lid,0);
}
assert.throws(()=>validateAsset({lid:null,triangles:1,bounds:[1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('MOTION PASS: 81 staged poses; invalid geometry negative controls rejected');
