import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 staged poses and exact endpoints',()=>{for(let i=0;i<=80;i++){let p=i/80,s=pose(p);assert.ok(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(p<=.25)assert.equal(s.lid,0);else assert.equal(s.latch,-80*Math.PI/180);}assert.equal(pose(0).latch,0);assert.equal(pose(1).lid,-105*Math.PI/180);});
test('invalid geometry rejected',()=>{assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0]}));});
