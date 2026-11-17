import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 staged motion samples and exact endpoints',()=>{
 for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);else assert(Math.abs(q.latch+80*Math.PI/180)<1e-12);}
 assert.deepEqual(pose(0),{lid:0,latch:0});assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
 assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('invalid runtime asset negative controls reject',()=>{
 const good={lid:true,triangles:1,bounds:[0,0,0,1,1,1]};validateAsset(good);
 for(const bad of [{...good,lid:false},{...good,triangles:0},{...good,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));
});
