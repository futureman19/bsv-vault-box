import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
const deg=x=>x*Math.PI/180;
for(let i=0;i<=80;i++){
 const p=i/80,q=pose(p);
 assert.ok(Math.abs(q.latch+deg(80)*Math.min(1,p/.25))<1e-12);
 assert.ok(Math.abs(q.lid+(p<=.25?0:deg(105)*(p-.25)/.75))<1e-12);
 if(p<=.25)assert.equal(q.lid,0);
 else assert.equal(q.latch,-deg(80));
}
assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
for(const x of [{lid:false,triangles:1,bounds:[0,1]},{lid:true,triangles:0,bounds:[0,1]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(x));
validateAsset({lid:true,triangles:1,bounds:[0,1]});
console.log('PASS motion: 81 staged poses, clamped endpoints, 3 invalid-asset negatives');
