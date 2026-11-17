import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('staged 80 degree release and 105 degree opening at 81 samples',()=>{
 for(let i=0;i<=80;i++){let p=i/80,s=pose(p);assert(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(p<=.25)assert.equal(s.lid,0);else assert(Math.abs(s.latch+80*Math.PI/180)<1e-12);}
 assert.equal(pose(0).latch,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
 assert.deepEqual(pose(-2),pose(0));assert.deepEqual(pose(2),pose(1));
});
test('invalid actual-loader metrics rejected',()=>{
 const good={lid:true,triangles:10,bounds:[-1,0,1]};validateAsset(good);
 for(const patch of [{lid:false},{triangles:0},{bounds:[NaN]},{bounds:[]}])assert.throws(()=>validateAsset({...good,...patch}));
});
