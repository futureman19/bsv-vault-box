import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pose,validateAsset} from './motion.mjs';
test('81 ordered poses and exact endpoints',()=>{for(let i=0;i<=80;i++){const p=i/80,q=pose(p);assert.ok(Number.isFinite(q.lid));if(p<=.25)assert.equal(q.lid,0);else assert.ok(Math.abs(q.latch+80*Math.PI/180)<1e-12);}assert.equal(pose(0).latch,0);assert.equal(pose(1).lid,-105*Math.PI/180);});
test('invalid geometry negative controls reject',()=>{for(const x of [{lid:false,triangles:1,bounds:[0]},{lid:true,triangles:0,bounds:[0]},{lid:true,triangles:1,bounds:[NaN]}])assert.throws(()=>validateAsset(x));});
