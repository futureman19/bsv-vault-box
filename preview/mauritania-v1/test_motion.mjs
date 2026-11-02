import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {pose,validateAsset} from './motion.mjs';
const rows=[];
for(let i=0;i<=80;i++) {const p=i/80,q=pose(p);assert.ok(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);if(p>=.25)assert.ok(Math.abs(q.latch+80*Math.PI/180)<1e-12);rows.push({progress:p,...q});}
assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(1).lid,-105*Math.PI/180);
assert.throws(()=>validateAsset({lid:false,triangles:0,bounds:[NaN]}));
writeFileSync(new URL('./motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples:rows,invalid_asset_rejected:true},null,2));
console.log('MOTION PASS: 81 staged poses, 80-degree latch then 105-degree lid; invalid asset rejected');
