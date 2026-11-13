import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged mechanism endpoints and 81 samples',()=>{
 assert.deepEqual(pose(0),{lid:0,latch:0});
 for(let i=0;i<=80;i++){
  let p=i/80,a=pose(p);assert(Number.isFinite(a.lid+a.latch));
  if(p<=.25)assert.equal(a.lid,0);else assert.equal(a.latch,-80*Math.PI/180);
 }
 assert.equal(pose(.25).latch,-80*Math.PI/180);
 assert.equal(pose(1).lid,-105*Math.PI/180);
 assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('reject missing pivot, nonfinite bounds and empty mesh',()=>{
 const a={lid:true,triangles:3,bounds:[0,0,0,1,1,1]};validateAsset(a);
 for(const bad of [{...a,lid:false},{...a,triangles:0},{...a,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));
});
