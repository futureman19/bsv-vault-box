import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const samples=[];
for(let i=0;i<=80;i++){const p=i/80,s=pose(p);assert(Number.isFinite(s.lid)&&Number.isFinite(s.latch));if(p<=.25)assert.equal(s.lid,0);else assert(Math.abs(s.latch+80*Math.PI/180)<1e-12);samples.push({progress:p,...s});}
assert.equal(pose(0).latch,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);
for(const x of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(x));
fs.writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',negativeControlsRejected:3,samples},null,2));
console.log('MOTION PASS: 81 poses; staged 80/105 degrees; 3 invalid-asset negative controls rejected');
