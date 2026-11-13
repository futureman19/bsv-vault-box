import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
for(let i=0;i<=80;i++){
 const p=i/80,s=pose(p);
 assert.ok(Number.isFinite(s.lid)&&Number.isFinite(s.latch));
 if(p<=.25)assert.equal(s.lid,0);
 if(p>=.25)assert.ok(Math.abs(s.latch+80*Math.PI/180)<1e-12);
 assert.ok(s.lid<=0&&s.lid>=-105*Math.PI/180);
}
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN,1]}));
console.log('PASS motion: 81 samples, staged 80/105 endpoints, malformed asset rejection');
