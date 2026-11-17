import assert from 'node:assert/strict';
import {test} from 'node:test';
import {pose,validateAsset} from './motion.mjs';
test('staged latch before lid, exact endpoints',()=>{assert.deepEqual(pose(0),{lid:0,latch:0});assert.equal(pose(.25).lid,0);assert.equal(pose(.25).latch,-80*Math.PI/180);assert.equal(pose(1).lid,-105*Math.PI/180);for(let i=0;i<=80;i++){let p=i/80;if(p<.25)assert.equal(pose(p).lid,0);else assert.equal(pose(p).latch,-80*Math.PI/180);}});
test('invalid asset negative controls are rejected',()=>{for(const x of [{lid:false,triangles:4,bounds:[1]},{lid:true,triangles:0,bounds:[1]},{lid:true,triangles:4,bounds:[NaN]}])assert.throws(()=>validateAsset(x));validateAsset({lid:true,triangles:4,bounds:[0,1]});});
