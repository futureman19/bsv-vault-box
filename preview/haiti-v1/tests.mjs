import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,r=pose(p);assert.ok(Number.isFinite(r.lid)&&Number.isFinite(r.latch));
 if(p<=.25)assert.equal(r.lid,0);else assert.ok(Math.abs(r.latch+80*Math.PI/180)<1e-12);
}
assert.equal(pose(0).latch,0);assert.equal(pose(1).lid,-105*Math.PI/180);
assert.equal(pose(1).latch,-80*Math.PI/180);
assert.throws(()=>validateAsset({lid:null,triangles:0,bounds:[NaN]}));
console.log('MOTION PASS: 81 staged poses, exact 80/105 endpoints; invalid-asset negative control rejected');
