import {pose,validateAsset} from './motion.mjs';
import assert from 'node:assert/strict';
for(let i=0;i<=80;i++){const p=i/80,r=pose(p);assert(Math.abs(r.lid+105*Math.PI/180*Math.max(0,(p-.25)/.75))<1e-9);assert(Math.abs(r.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-9);}
assert.throws(()=>validateAsset({lid:false,triangles:10,bounds:[0,0,0,1,1,1]}));
console.log('MOTION PASS: 81 poses; missing pivot rejected');
