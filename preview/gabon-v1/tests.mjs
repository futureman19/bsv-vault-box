import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
for(let i=0;i<=80;i++){let p=i/80,s=pose(p);assert.equal(s.lid,p<=.25?0:-105*Math.PI/180*((p-.25)/.75));assert.equal(s.latch,p===0?0:-80*Math.PI/180*Math.min(1,p/.25));}
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('PASS: 81 motion poses and 3 invalid-asset negative controls');
