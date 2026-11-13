import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose, validateAsset} from './motion.mjs';
test('latch releases before lid; reverses safely; endpoints clamp',()=>{
 assert.deepEqual(pose(0),{lid:0,latch:0});
 assert.equal(pose(.2).lid,0); assert.ok(pose(.2).latch<0);
 assert.equal(pose(1).lid,-105*Math.PI/180);
 assert.deepEqual(pose(-2),pose(0)); assert.deepEqual(pose(3),pose(1));
 for(let i=0;i<=100;i++){let p=pose(i/100);assert.ok(Number.isFinite(p.lid));if(p.lid<0)assert.equal(p.latch,-80*Math.PI/180);}
});
test('asset contract rejects missing lid, nonfinite and empty geometry',()=>{
 assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
 assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
 assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[0,NaN]}));
 assert.doesNotThrow(()=>validateAsset({lid:true,triangles:10,bounds:[-2,0,-1,2,2,1]}));
});
