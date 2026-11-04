import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged latch then lid, endpoints and all 81 samples',()=>{
 assert.deepEqual(pose(0),{lid:0,latch:0});
 assert.equal(pose(.25).lid,0);assert.equal(pose(.25).latch,-80*Math.PI/180);
 for(let i=0;i<=80;i++){const p=i/80,a=pose(p);assert.ok(Number.isFinite(a.lid)&&Number.isFinite(a.latch));assert.ok(a.lid<=0&&a.lid>=-105*Math.PI/180);if(p<=.25)assert.equal(a.lid,0);else assert.equal(a.latch,-80*Math.PI/180);}
 assert.equal(pose(1).lid,-105*Math.PI/180);assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('real invalid geometry negative controls',()=>{for(const bad of [{lid:false,triangles:1,bounds:[1]},{lid:true,triangles:0,bounds:[1]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));validateAsset({lid:true,triangles:1,bounds:[0,1]});});
