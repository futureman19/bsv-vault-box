import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
const samples=[];
for(let i=0;i<=80;i++){
 const t=i/80,p=pose(t);assert(Number.isFinite(p.lid)&&Number.isFinite(p.latch));
 if(t<=.25)assert.equal(p.lid,0);else assert(Math.abs(p.latch+80*Math.PI/180)<1e-12);
 samples.push({t,...p});
}
assert.equal(pose(0).lid,0);assert.equal(pose(0).latch,0);
assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
for(const bad of [{lid:false,triangles:1,bounds:[0,1]},{lid:true,triangles:0,bounds:[0,1]},{lid:true,triangles:1,bounds:[NaN,1]}])assert.throws(()=>validateAsset(bad));
validateAsset({lid:true,triangles:1,bounds:[0,1]});
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalid_asset_negative_controls:3},null,2));
console.log('PASS motion: 81 staged poses, endpoints, 3 invalid-asset negative controls');
