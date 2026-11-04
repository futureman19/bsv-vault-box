import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 staged poses and exact endpoints',()=>{
 for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert.ok(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);else assert.equal(q.latch,-80*Math.PI/180);}
 assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(1).lid,-105*Math.PI/180);assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('reject absent/invalid actual geometry',()=>{for(const a of [{lid:false,triangles:3,bounds:[1]},{lid:true,triangles:0,bounds:[1]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(a));});
