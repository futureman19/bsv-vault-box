import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert(Math.abs(s.lid-(p<=.25?0:-105*Math.PI/180*(p-.25)/.75))<1e-12);assert(Math.abs(s.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-12);if(p<=.25)assert.equal(s.lid,0);}
assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('MOTION PASS: 81 poses, clamp endpoints, invalid-asset negatives');
