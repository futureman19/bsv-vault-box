import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);
assert.equal(pose(.25).latch,-80*Math.PI/180);
assert.equal(pose(1).lid,-105*Math.PI/180);
for(let i=0;i<=80;i++){const p=pose(i/80);assert(Number.isFinite(p.lid)&&Number.isFinite(p.latch));if(i<=20)assert.equal(p.lid,0);else assert.equal(p.latch,-80*Math.PI/180);}
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('MOTION PASS: 81 samples; endpoints, staging, invalid-asset negatives');
