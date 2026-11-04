import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert(s.lid<=0&&s.latch<=0);if(p<=.25)assert.equal(s.lid,0);else assert.equal(s.latch,-80*Math.PI/180);}
assert.equal(pose(1).lid,-105*Math.PI/180);assert.equal(pose(0).latch,0);
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('PASS 81 motion poses, endpoints, invalid-asset negative controls');
