import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 poses stage latch before lid and stay bounded',()=>{for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert(q.lid<=0&&q.lid>=-105*Math.PI/180);assert(q.latch<=0&&q.latch>=-80*Math.PI/180);if(p<=.25)assert.equal(q.lid,0);else assert.equal(q.latch,-80*Math.PI/180);}assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(1).lid,-105*Math.PI/180);});
test('invalid geometry genuinely rejected',()=>{assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));validateAsset({lid:true,triangles:1,bounds:[0,1]});});
