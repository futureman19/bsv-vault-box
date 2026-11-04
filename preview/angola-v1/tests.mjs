import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);assert.equal(pose(.25).latch,-80*Math.PI/180);
assert.equal(pose(1).lid,-105*Math.PI/180);
for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert.ok(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);else assert.equal(q.latch,-80*Math.PI/180);}
assert.throws(()=>validateAsset({lid:false,triangles:2,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:2,bounds:[NaN]}));
validateAsset({lid:true,triangles:2,bounds:[0,1]});
console.log('PASS motion: 81 poses, 80-degree latch then 105-degree lid; 3 negative controls rejected');
