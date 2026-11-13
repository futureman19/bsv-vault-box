import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
const samples=[];
for(let i=0;i<=80;i++){
 const p=i/80,a=pose(p);
 assert.ok(Number.isFinite(a.lid)&&Number.isFinite(a.latch));
 if(p<=.25)assert.equal(a.lid,0);
 else assert.ok(Math.abs(a.latch+80*Math.PI/180)<1e-12);
 samples.push({p,...a});
}
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
assert.ok(Math.abs(pose(1).latch+80*Math.PI/180)<1e-12);
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN]}));
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalid_geometry_rejected:3},null,2));
console.log('MOTION_PASS 81 staged poses; 3 invalid geometry cases rejected');
