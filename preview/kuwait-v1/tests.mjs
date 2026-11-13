import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged endpoints, holds, monotonicity and inverse sampling',()=>{
 assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(.25).lid,0);
 assert.equal(pose(.25).latch,-80*Math.PI/180);assert.equal(pose(1).lid,-105*Math.PI/180);
 for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert.ok(Number.isFinite(s.lid+s.latch));if(p<=.25)assert.equal(s.lid,0);else assert.equal(s.latch,-80*Math.PI/180);if(i)assert.ok(s.lid<=pose((i-1)/80).lid&&s.latch<=pose((i-1)/80).latch);}
 assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('real invalid-geometry controls reject',()=>{
 validateAsset({lid:true,triangles:1,bounds:[0,1]});
 for(const v of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(v));
});
