'use strict';
// No public-network provider or fallback. Every RPC is routed through the
// regtest-only adapter, including reads used to construct/sign transactions.
const { Provider, bsv } = require('../../vault/node_modules/scrypt-ts');
class RegtestProvider extends Provider {
  constructor(rpc) { super(); this.rpc = rpc; this.coins = []; }
  isConnected() { return true; }
  async connect() { await this.rpc.assertRegtest(); return this; }
  updateNetwork() { throw new Error('network switching is forbidden'); }
  getNetwork() { return bsv.Networks.testnet; } // regtest shares address encoding, NOT transport
  async getFeePerKb() { return 500; }
  async getTransaction(id) { return new bsv.Transaction(await this.rpc.call('getrawtransaction', [id])); }
  async listUnspent(address) {
    const script = bsv.Script.buildPublicKeyHashOut(address).toHex();
    const available = [];
    for (const coin of this.coins.filter(c => c.script === script)) {
      if (await this.rpc.call('gettxout', [coin.txId, coin.outputIndex, true])) available.push(coin);
    }
    return available;
  }
  async getBalance(address) {
    return { confirmed: (await this.listUnspent(address)).reduce((s, c) => s + c.satoshis, 0), unconfirmed: 0 };
  }
  track(raw) {
    const tx = new bsv.Transaction(raw);
    const spent = new Set(tx.inputs.map(i => `${i.prevTxId.toString('hex')}:${i.outputIndex}`));
    this.coins = this.coins.filter(c => !spent.has(`${c.txId}:${c.outputIndex}`));
    tx.outputs.forEach((out, outputIndex) => {
      if (out.script.isPublicKeyHashOut()) this.coins.push({ txId: tx.id, outputIndex, script: out.script.toHex(), satoshis: out.satoshis });
    });
  }
  async sendRawTransaction(raw) {
    const id = await this.rpc.call('sendrawtransaction', [raw]);
    const fetched = await this.rpc.call('getrawtransaction', [id]);
    if (fetched !== raw) throw new Error('broadcast readback mismatch');
    this.track(raw);
    return id;
  }
}
module.exports = { RegtestProvider };
