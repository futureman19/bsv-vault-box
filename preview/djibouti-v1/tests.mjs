import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){const p=i/80,r=pose(p);assert(Number.isFinite(r.lid)&&Number.isFinite(r.latch));if(p<=.25)assert.equal(r.lid,0);if(p>=.25)assert(Math.abs(r.latch+80*Math.PI/180)<1e-12);}
assert.equal(pose(0).latch,0);assert.equal(pose(1).lid,-105*Math.PI/180);
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
console.log('PASS: 81 staged motion poses, exact endpoints, 3 rejected invalid assets');
