'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { RegtestRPC } = require('../chain/rpc.cjs');
const { RegtestProvider } = require('./provider.cjs');
const { Vault, bsv } = require('../chain/watcher.cjs');
const { TestWallet, findSig } = require('../../vault/node_modules/scrypt-ts');
const root = path.resolve(__dirname, '../..');
function localRPC() {
  const entries = fs.readFileSync(path.join(root, '.local/node/bitcoin.conf'), 'utf8').split(/\r?\n/)
    .filter(line => line.includes('=')).map(line => { const i = line.indexOf('='); return [line.slice(0, i), line.slice(i+1)]; });
  const conf = Object.fromEntries(entries);
  if (conf.regtest !== '1' || conf.rpcport !== '18483') throw Error('Unexpected node configuration');
  return new RegtestRPC({ url: 'http://127.0.0.1:18483', username: conf.rpcuser, password: conf.rpcpassword });
}
async function prepare(rpc) {
  await rpc.assertRegtest();
  // Newly mined coins have no value outside this isolated regtest chain.
  await rpc.call('generate', [105]);
  const key = bsv.PrivateKey.fromRandom(bsv.Networks.testnet);
  const provider = new RegtestProvider(rpc);
  const funding = await rpc.call('sendtoaddress', [key.toAddress().toString(), 0.01]);
  await rpc.call('generate', [1]);
  provider.track(await rpc.call('getrawtransaction', [funding]));
  const signer = new TestWallet(key, provider);
  return { key, provider, signer };
}
async function createBox(ctx, contentRef, boxId = crypto.randomBytes(32).toString('hex')) {
  const box = new Vault(0n, boxId, contentRef, ctx.key.publicKey.toHex());
  await box.connect(ctx.signer);
  const tx = await box.deploy(1);
  return { box, boxId, genesis: { txid: tx.id, vout: 0 } };
}
async function transferBox(ctx, box) {
  const next = box.next();
  const newKey = bsv.PrivateKey.fromRandom(bsv.Networks.testnet);
  ctx.signer.addPrivateKey(newKey);
  next.owner = newKey.publicKey.toHex();
  const call = await box.methods.transfer(r => findSig(r, ctx.key.publicKey), next.owner, {
    pubKeyOrAddrToSign: ctx.key.publicKey, next: { instance: next, balance: 1 }
  });
  return { box: next, key: newKey, txid: call.tx.id };
}
async function openBox(ctx, box, key = ctx.key) {
  const next = box.next(); next.boxState = 1n;
  await box.connect(ctx.signer);
  const call = await box.methods.open(r => findSig(r, key.publicKey), {
    pubKeyOrAddrToSign: key.publicKey, next: { instance: next, balance: 1 }
  });
  return { box: next, txid: call.tx.id };
}
module.exports = { localRPC, prepare, createBox, transferBox, openBox, root };
