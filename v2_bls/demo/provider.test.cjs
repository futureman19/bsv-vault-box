'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { RegtestProvider } = require('./provider.cjs');
const { bsv } = require('../../vault/node_modules/scrypt-ts');
test('provider has no synthetic UTXOs, network fallback or switching', async () => {
  const key = bsv.PrivateKey.fromRandom(bsv.Networks.testnet);
  let checked = false;
  const rpc = { assertRegtest: async () => { checked = true; }, call: async () => { throw Error('unexpected RPC'); } };
  const p = new RegtestProvider(rpc);
  await p.connect();
  assert.equal(checked, true);
  assert.deepEqual(await p.listUnspent(key.toAddress()), []);
  assert.throws(() => p.updateNetwork(bsv.Networks.mainnet), /forbidden/);
});
test('provider requires broadcast readback match before updating local coins', async () => {
  const rpc = { call: async method => method === 'sendrawtransaction' ? 'id' : 'other' };
  const p = new RegtestProvider(rpc);
  await assert.rejects(p.sendRawTransaction('0100'), /readback mismatch/);
  assert.deepEqual(p.coins, []);
});
