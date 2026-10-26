'use strict';
// Real-chain plumbing check only; no encryption/committee claim.
const assert = require('node:assert/strict');
const { localRPC, prepare, createBox, transferBox, openBox } = require('./covenant.cjs');
const { traceOpening } = require('../chain/watcher.cjs');
(async () => {
 const rpc = localRPC(), ctx = await prepare(rpc);
 const { box, boxId, genesis } = await createBox(ctx, require('node:crypto').randomBytes(32).toString('hex'));
 await rpc.call('generate', [1]);
 assert.equal((await traceOpening(rpc, genesis, boxId)).status, 'SEALED');
 const transferred = await transferBox(ctx, box);
 await rpc.call('generate', [1]);
 const sealed = await traceOpening(rpc, genesis, boxId);
 assert.equal(sealed.status, 'SEALED');
 assert.equal(sealed.current.txid, transferred.txid);
 const opened = await openBox(ctx, transferred.box, transferred.key);
 assert.equal((await traceOpening(rpc, genesis, boxId)).status, 'SEALED');
 await rpc.call('generate', [2]);
 assert.equal((await traceOpening(rpc, genesis, boxId)).status, 'IMMATURE');
 await rpc.call('generate', [1]);
 const ready = await traceOpening(rpc, genesis, boxId);
 assert.equal(ready.status, 'READY');
 assert.equal(ready.opening.txid, opened.txid);
 console.log(JSON.stringify({status:'PASS',network:'regtest',genesis,transfer:transferred.txid,opening:opened.txid,confirmations:ready.opening.confirmations}));
})().catch(e => { console.error(e.stack); process.exitCode = 1; });
