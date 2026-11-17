import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {pose,validateAsset} from './motion.mjs';
const samples=[];
for(let i=0;i<=80;i++){const p=i/80,v=pose(p);assert(Number.isFinite(v.lid)&&Number.isFinite(v.latch));if(p<=.25)assert.equal(v.lid,0);else assert(Math.abs(v.latch+80*Math.PI/180)<1e-10);samples.push({progress:p,...v});}
assert.equal(pose(0).lid,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-10);assert.throws(()=>validateAsset({lid:false,triangles:0,bounds:[NaN]}));
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples,invalid_asset_rejected:true},null,2));console.log('MOTION PASS: 81 staged poses, endpoint and invalid-asset checks');
