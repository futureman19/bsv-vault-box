import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);assert.equal(pose(.25).latch,-80*Math.PI/180);
assert.equal(pose(1).lid,-105*Math.PI/180);
for(let i=0;i<=80;i++){const p=pose(i/80);assert(p.lid<=0&&p.lid>=-105*Math.PI/180);assert(p.latch<=0&&p.latch>=-80*Math.PI/180);if(i<=20)assert.equal(p.lid,0);}
assert.throws(()=>validateAsset({lid:false,triangles:10,bounds:[1,2]}));
assert.throws(()=>validateAsset({lid:true,triangles:10,bounds:[NaN]}));
console.log('MOTION PASS: 81 poses, 80-degree latch / 105-degree lid; invalid assets rejected');
