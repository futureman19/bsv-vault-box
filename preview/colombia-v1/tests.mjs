import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged latch then lid, 81 poses',()=>{for(let i=0;i<=80;i++){const p=i/80,a=pose(p);assert.ok(Math.abs(a.latch-(-80*Math.PI/180*Math.min(1,p/.25)))<1e-12);assert.ok(Math.abs(a.lid-(p<=.25?0:-105*Math.PI/180*(p-.25)/.75))<1e-12);}assert.equal(pose(0).lid,0);});
test('real invalid geometry rejected',()=>{for(const bad of [{lid:false,triangles:10,bounds:[0,1]},{lid:true,triangles:0,bounds:[0,1]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));});
