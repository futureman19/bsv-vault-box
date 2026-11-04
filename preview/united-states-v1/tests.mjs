import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);
assert.ok(Math.abs(pose(.25).latch+80*Math.PI/180)<1e-12);
assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
for(let i=0;i<=80;i++){const p=pose(i/80);assert.ok(Number.isFinite(p.lid)&&Number.isFinite(p.latch));if(i<=20)assert.equal(p.lid,0);else assert.ok(Math.abs(p.latch+80*Math.PI/180)<1e-12);}
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('MOTION PASS: 81 poses, 80/105 degree choreography, 3 invalid asset negatives rejected');
