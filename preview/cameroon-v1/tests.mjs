import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('80-degree release precedes 105-degree opening',()=>{assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(.25).lid,0);assert.equal(pose(.25).latch,-80*Math.PI/180);assert.equal(pose(1).lid,-105*Math.PI/180);assert.equal(pose(1).latch,-80*Math.PI/180);for(let i=0;i<=80;i++){let p=i/80,s=pose(p);assert.ok(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(p<=.25)assert.equal(s.lid,0);else assert.equal(s.latch,-80*Math.PI/180);}});
test('clamping and invalid asset rejection',()=>{assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));validateAsset({lid:true,triangles:1,bounds:[0,1]});});
