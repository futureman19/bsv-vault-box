import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 staged poses: latch before lid, endpoints and reversal',()=>{
 for(let i=0;i<=80;i++){
  const p=i/80,v=pose(p);assert.ok(Number.isFinite(v.lid)&&Number.isFinite(v.latch));
  if(p<=.25)assert.equal(v.lid,0);else assert.ok(Math.abs(v.latch+80*Math.PI/180)<1e-12);
  assert.ok(Math.abs(v.lid+105*Math.PI/180*Math.max(0,(p-.25)/.75))<1e-12);
 }
 assert.deepEqual(pose(0),{lid:0,latch:0});assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('invalid actual geometry metadata rejected',()=>{
 assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
 assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
 assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN,1]}));
 validateAsset({lid:true,triangles:1,bounds:[0,1]});
});
