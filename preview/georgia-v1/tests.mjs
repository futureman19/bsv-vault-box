import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged latch 80 then lid 105 over 81 poses',()=>{for(let i=0;i<=80;i++){let p=i/80,a=pose(p);assert.equal(a.lid,p<=.25?0:-105*Math.PI/180*((p-.25)/.75));assert.ok(Math.abs(a.latch-(-80*Math.PI/180*Math.min(1,p/.25)))<1e-12);}assert.equal(pose(1).lid,-105*Math.PI/180);assert.equal(pose(1).latch,-80*Math.PI/180);});
test('invalid geometry genuinely rejects',()=>{assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0]}));assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0]}));assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));validateAsset({lid:true,triangles:1,bounds:[0,1]});});
