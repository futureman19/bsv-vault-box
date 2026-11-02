import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert.ok(Math.abs(q.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-12);assert.ok(Math.abs(q.lid+105*Math.PI/180*Math.max(0,(p-.25)/.75))<1e-12);if(p<=.25)assert.equal(q.lid,0);}
assert.throws(()=>validateAsset({lid:false,triangles:0,bounds:[NaN]}));
writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples:81,latch_degrees:80,lid_degrees:105,negative_invalid_asset_rejected:true},null,2));console.log('MOTION PASS: 81 staged poses; invalid asset rejected');
