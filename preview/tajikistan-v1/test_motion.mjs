import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
for(let i=0;i<=80;i++){
 const p=i/80, a=pose(p);
 assert.ok(Math.abs(a.latch-(-80*Math.PI/180*Math.min(1,p/.25)))<1e-12);
 assert.ok(Math.abs(a.lid-(p<=.25?0:-105*Math.PI/180*(p-.25)/.75))<1e-12);
}
assert.throws(()=>validateAsset({lid:false,triangles:1,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:1,bounds:[NaN,1]}));
writeFileSync(new URL('./motion-check.json',import.meta.url),JSON.stringify({PASS:true,samples:81,latch_degrees:80,lid_degrees:105,negative_controls:3},null,2));
console.log('PASS motion: 81 samples; 3 invalid-asset negative controls rejected');
