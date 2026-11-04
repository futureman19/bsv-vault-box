import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 staged finite monotonic poses and exact endpoints',()=>{let last={lid:0,latch:0};for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert.ok(Number.isFinite(q.lid)&&Number.isFinite(q.latch));assert.ok(q.lid<=last.lid&&q.latch<=last.latch);if(p<=.25)assert.equal(q.lid,0);if(p>=.25)assert.ok(Math.abs(q.latch+80*Math.PI/180)<1e-12);last=q;}assert.deepEqual(pose(0),{lid:0,latch:0});assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12)});
test('invalid geometry rejected',()=>{assert.throws(()=>validateAsset({lid:false,triangles:10,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:10,bounds:[NaN]}));});
