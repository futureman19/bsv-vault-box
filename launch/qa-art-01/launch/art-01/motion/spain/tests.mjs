import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged latch then lid: 81 poses',()=>{for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert.ok(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);else assert.ok(Math.abs(q.latch+80*Math.PI/180)<1e-12);}assert.deepEqual(pose(0),{lid:0,latch:0});assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);});
test('clamp and reject missing/invalid asset',()=>{assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));validateAsset({lid:true,triangles:1,bounds:[0,1]});});
