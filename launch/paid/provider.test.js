'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {createProvider}=require('./provider');
const key='02'+'1'.repeat(64);
function result(){return {provider:'brc100',identityKey:key,disconnect(){this.closed=true;},wallet:{waitForAuthentication:async()=>({authenticated:true}),getNetwork:async()=>({network:'test'}),getPublicKey:async()=>({publicKey:key}),createSignature:async()=>({signature:[]})}};}
test('owner connection disabled by default and never runs on construction',async()=>{let calls=0;const p=createProvider({connectWallet:async()=>{calls++;}});assert.equal(calls,0);await assert.rejects(p.getWallet(),/disabled/);assert.equal(calls,0);});
test('uses pinned connect result shape and explicit auto-detect config',async()=>{const r=result();const p=createProvider({enabled:true,connectWallet:async config=>{assert.deepEqual(config,{autoDetect:true,providers:[]});return r;}});assert.equal(await p.getWallet(),r.wallet);p.disconnect();assert.equal(r.closed,true);});
test('late connect response is disconnected after cancellation',async()=>{let resolve;const r=result(),p=createProvider({enabled:true,connectWallet:()=>new Promise(done=>resolve=done)});const pending=p.getWallet();p.disconnect();resolve(r);await assert.rejects(pending,/cancelled/);assert.equal(r.closed,true);});
test('unexpected provider and identity mismatches fail closed',async()=>{for(const change of [r=>r.provider='popup',r=>r.identityKey='bad',r=>r.wallet.getPublicKey=async()=>({publicKey:'03'+'2'.repeat(64)}),r=>r.wallet.createSignature=null]){const r=result();change(r);const p=createProvider({enabled:true,connectWallet:async()=>r});await assert.rejects(p.getWallet());assert.equal(r.closed,true);}});
