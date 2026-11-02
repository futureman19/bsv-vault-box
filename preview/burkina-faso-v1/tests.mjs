import test from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 poses: staged latch 80 then lid 105; clamp and reverse endpoints',()=>{
 for(let i=0;i<=80;i++){const t=i/80,p=pose(t);assert(Number.isFinite(p.lid)&&Number.isFinite(p.latch));assert(Math.abs(p.latch-(-80*Math.PI/180*Math.min(t/.25,1)))<1e-12);assert(Math.abs(p.lid-(-105*Math.PI/180*Math.max(0,(t-.25)/.75)))<1e-12);if(t<=.25)assert.equal(p.lid,0);else assert.equal(p.latch,-80*Math.PI/180);}
 assert.deepEqual(pose(-1),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('invalid-asset negative controls throw instead of passing',()=>{
 const good={lid:true,triangles:1,bounds:[0,0,0,1,1,1]};assert.doesNotThrow(()=>validateAsset(good));
 for(const bad of [{lid:false},{triangles:0},{bounds:[NaN]},{bounds:[]}])assert.throws(()=>validateAsset({...good,...bad}));
});
