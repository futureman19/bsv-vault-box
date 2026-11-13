import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
for(let i=0;i<=80;i++){let p=i/80,a=pose(p);assert.ok(Number.isFinite(a.lid)&&Number.isFinite(a.latch));if(p<=.25)assert.equal(a.lid,0);else assert.ok(Math.abs(a.latch+80*Math.PI/180)<1e-12);}
assert.deepEqual(pose(0),{lid:0,latch:0});assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
for(const bad of [{lid:false,triangles:1,bounds:[0]}, {lid:true,triangles:0,bounds:[0]}, {lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));
validateAsset({lid:true,triangles:1,bounds:[0,1]});
console.log('PASS: 81 staged poses, 80-degree latch, 105-degree lid, three negative geometry controls');
