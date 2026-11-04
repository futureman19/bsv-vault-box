import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);assert.equal(pose(.25).latch,-80*Math.PI/180);
assert.equal(pose(1).lid,-105*Math.PI/180);
for(let i=0;i<=80;i++){let p=i/80;let a=pose(p);assert(Number.isFinite(a.lid)&&Number.isFinite(a.latch));if(p<=.25)assert.equal(a.lid,0);else assert.equal(a.latch,-80*Math.PI/180);}
assert.throws(()=>validateAsset({lid:false,triangles:0,bounds:[NaN]}));
console.log('PASS: 81 staged motion samples; endpoints; invalid-asset negative control');
