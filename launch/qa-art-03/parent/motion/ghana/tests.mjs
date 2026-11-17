import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {pose,validateAsset} from './motion.mjs';
const samples=Array.from({length:81},(_,i)=>({progress:i/80,...pose(i/80)}));
for(const s of samples){assert(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(s.progress<=.25)assert.equal(s.lid,0);else assert(Math.abs(s.latch+80*Math.PI/180)<1e-12);}
assert.equal(pose(0).latch,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
for(const bad of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(bad));
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalidAssetNegativesRejected:3},null,2));console.log('MOTION PASS: 81 staged poses; 3 invalid-asset negative controls rejected');
