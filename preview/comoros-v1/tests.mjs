import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){const p=i/80,v=pose(p);assert.equal(v.lid,p<=.25?0:-105*Math.PI/180*((p-.25)/.75));assert.equal(v.latch,p===0?0:-80*Math.PI/180*Math.min(1,p/.25));}
assert.throws(()=>validateAsset({lid:false,triangles:10,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:10,bounds:[NaN]}));
validateAsset({lid:true,triangles:10,bounds:[0,1]});
console.log('PASS motion: 81 staged poses; missing-pivot and nonfinite negative controls rejected');
