'use strict';
const http = require('node:http');
// Unknown methods are treated as mutations, never an unguarded escape hatch.
const READ = new Set(['getblockchaininfo','getnetworkinfo','getpeerinfo','getblockcount','getbestblockhash','getblockhash','getblock','getblockheader','getrawtransaction','gettxout','getrawmempool','getmempoolinfo','getwalletinfo','listunspent','getbalance','decoderawtransaction','decodescript','gettransaction','validateaddress','getinfo']);
class RegtestRPC {
  constructor(config) {
    this.url = new URL(config.url);
    if (this.url.protocol !== 'http:' || !['127.0.0.1','[::1]'].includes(this.url.hostname) || this.url.username || this.url.password || this.url.hash || this.url.search) throw Error('RPC requires literal loopback HTTP URL without embedded credentials');
    this.auth = `${config.username ?? config.user ?? ''}:${config.password ?? config.pass ?? ''}`;
  }
  async _request(method, params) {
    const body = JSON.stringify({jsonrpc:'1.0',id:'vault2',method,params});
    return new Promise((resolve,reject) => {
      const req = http.request(this.url, {method:'POST',auth:this.auth,headers:{'Content-Type':'application/json','Content-Length':Buffer.byteLength(body)},timeout:30000}, res => {
        let text=''; res.on('data', b=> { text+=b; if(text.length>64000000) req.destroy(Error('RPC response too large')); });
        res.on('end',()=> { try {
          if(res.statusCode>=300 && res.statusCode<400) throw Error('RPC redirects forbidden');
          const data=JSON.parse(text); if(data.error) { const e=Error(`RPC ${method}: ${data.error.message}`);e.code=data.error.code;throw e; }
          if(res.statusCode!==200) throw Error(`RPC HTTP ${res.statusCode}`);
          resolve(data.result);
        } catch(e) {reject(e);} });
      });
      req.on('timeout',()=>req.destroy(Error('RPC timeout'))); req.on('error',reject);req.end(body);
    });
  }
  async assertRegtest() {
    const chain=await this._request('getblockchaininfo',[]);
    const network=await this._request('getnetworkinfo',[]);
    const peers=await this._request('getpeerinfo',[]);
    if(chain.chain!=='regtest' || network.networkactive!==false || network.connections!==0 || !Array.isArray(peers) || peers.length!==0) throw Error('Safety gate: regtest with P2P networkactive=false and no peers required');
    return chain;
  }
  async call(method,params=[]) {
    if(!READ.has(method)) await this.assertRegtest();
    return this._request(method,params);
  }
}
module.exports={RegtestRPC};
