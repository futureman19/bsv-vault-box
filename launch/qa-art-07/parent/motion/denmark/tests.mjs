import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import fs from 'node:fs';
assert.deepEqual(pose(0),{lid:0,latch:0});
assert.equal(pose(.25).lid,0);
assert.ok(Math.abs(pose(.25).latch+80*Math.PI/180)<1e-10);
assert.ok(Math.abs(pose(1).lid+105*Math.PI/180)<1e-10);
for(let i=0;i<=80;i++){const p=pose(i/80);assert.ok(Number.isFinite(p.lid)&&Number.isFinite(p.latch));if(i<=20)assert.equal(p.lid,0);}
assert.throws(()=>validateAsset({lid:false,triangles:3,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0,1]}));
assert.throws(()=>validateAsset({lid:true,triangles:3,bounds:[NaN,1]}));
fs.writeFileSync(new URL('./motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples:81,latch_degrees:80,lid_degrees:105,invalid_asset_controls_rejected:3},null,2));
console.log('MOTION PASS: 81 samples; 3 invalid-asset controls rejected');
