import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged latch 80 then lid 105 across 81 poses and reverse',()=>{
 for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert.ok(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(p<=.25)assert.equal(s.lid,0);else assert.ok(Math.abs(s.latch+80*Math.PI/180)<1e-12);assert.ok(s.lid<=0&&s.latch<=0);}
 assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(1).lid,-105*Math.PI/180);assert.equal(pose(1).latch,-80*Math.PI/180);assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('real validation rejects absent pivots, empty mesh and NaN bounds',()=>{
 for(const a of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(a));
 validateAsset({lid:true,triangles:1,bounds:[0,1]});
});
