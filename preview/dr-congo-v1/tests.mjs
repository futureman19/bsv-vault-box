import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);
assert.equal(pose(.25).latch,-80*Math.PI/180);
assert.equal(pose(1).lid,-105*Math.PI/180);
for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert.ok(s.lid<=0&&s.lid>=-105*Math.PI/180);assert.ok(s.latch<=0&&s.latch>=-80*Math.PI/180);if(p<=.25)assert.equal(s.lid,0);else assert.equal(s.latch,-80*Math.PI/180);}
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('MOTION PASS: 81 staged poses; 3 invalid asset controls rejected');
