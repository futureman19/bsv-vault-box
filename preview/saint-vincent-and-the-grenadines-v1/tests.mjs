import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
import {writeFileSync} from 'node:fs';
const samples=[];
test('81 staged release poses and endpoints',()=>{
 for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert(Number.isFinite(q.lid)&&Number.isFinite(q.latch));if(p<=.25)assert.equal(q.lid,0);else assert(Math.abs(q.latch+80*Math.PI/180)<1e-12);samples.push({p,...q});}
 assert.equal(pose(0).lid,0);assert(Math.abs(pose(1).lid+105*Math.PI/180)<1e-12);assert.equal(pose(-1).lid,0);assert.deepEqual(pose(2),pose(1));
 writeFileSync(new URL('./motion-check.json',import.meta.url),JSON.stringify({status:'PASS',samples},null,2));
});
test('asset validator rejects missing hierarchy and nonfinite bounds',()=>{
 assert.throws(()=>validateAsset({lid:false,triangles:5,bounds:[0,1]}));assert.throws(()=>validateAsset({lid:true,triangles:5,bounds:[NaN]}));assert.throws(()=>validateAsset({lid:true,triangles:0,bounds:[0]}));validateAsset({lid:true,triangles:5,bounds:[0,1]});
});
