import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 staged poses and exact endpoints',()=>{
 for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert.ok(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(p<=.25)assert.equal(s.lid,0);else assert.ok(Math.abs(s.latch+80*Math.PI/180)<1e-12);}
 assert.deepEqual(pose(0),{lid:0,latch:0});assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('actual fail-closed negative controls',()=>{
 const good={lid:true,triangles:100,bounds:[-1,0,-1,1,2,1]};assert.doesNotThrow(()=>validateAsset(good));
 for(const bad of [{...good,lid:false},{...good,triangles:0},{...good,bounds:[NaN]},{...good,bounds:[]}])assert.throws(()=>validateAsset(bad));
});
