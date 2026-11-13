import {pose} from './motion.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs';
let samples=[];
for(let i=0;i<=80;i++){let p=i/80,a=pose(p);assert(Math.abs(a.lid+(p<=.25?0:105*Math.PI/180*(p-.25)/.75))<1e-12);assert(Math.abs(a.latch+80*Math.PI/180*Math.min(1,p/.25))<1e-12);if(p<=.25)assert.equal(a.lid,0);samples.push({p,...a});}
fs.writeFileSync(new URL('motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples},null,2));console.log('MOTION PASS 81 samples, latch 80 degrees before lid 105 degrees');
