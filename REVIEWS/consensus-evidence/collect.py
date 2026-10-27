"""Read-only canonical regtest corpus export; run with WSL Python 3."""
import base64
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[2]
cookie = Path.home() / 'consensus-t_a71c39fc/replay-node/regtest/.cookie'
auth = base64.b64encode(cookie.read_bytes().strip()).decode()
def rpc(method, params=()):
    assert method in {'getblockchaininfo', 'getnetworkinfo', 'getrawtransaction', 'getblockheader'}
    req = Request('http://127.0.0.1:18445', data=json.dumps({'id': 1, 'method': method, 'params': list(params)}).encode(), headers={'Authorization': 'Basic ' + auth})
    result = json.loads(urlopen(req).read(), parse_float=Decimal)
    assert result['error'] is None, result['error']
    return result['result']
assert rpc('getblockchaininfo')['chain'] == 'regtest'
print('node', rpc('getnetworkinfo')['subversion'])
rows = []
for shape, txid in [('deploy','75736f4ef1b20c3b77c53bc47ac001e70d7b71123cb458962164b983b28b86e4'), ('sealed-transfer','bf1823bf3529b18e025b2ffdcfcfc0aeb0d92aa44f2c711d0bf415de5d59f847'), ('open','33c369ac3970c1f7321edccbe3581b37a27cc694fb5c0661f1cba85ca4ad7659')]:
    tx = rpc('getrawtransaction', [txid, True])
    assert hashlib.sha256(hashlib.sha256(bytes.fromhex(tx['hex'])).digest()).digest()[::-1].hex() == txid
    height = rpc('getblockheader',[tx['blockhash']])['height']
    prevouts = []
    for i in tx['vin']:
        prev = rpc('getrawtransaction', [i['txid'],True])
        out = prev['vout'][i['vout']]
        prevouts.append({'txid':i['txid'], 'vout':i['vout'], 'script':out['scriptPubKey']['hex'], 'satoshis':int(Decimal(out['value'])*100000000), 'height':rpc('getblockheader',[prev['blockhash']])['height']})
    rows.append({'id':'vault-'+shape, 'family':'vault/'+shape, 'rule':'vault.'+shape, 'tx':tx['hex'], 'prevouts':prevouts, 'params':{'spend_height':height,'era':'pre-genesis','consensus':True,'tx_version':tx['version']}, 'expect':{}, 'note':'Canonical mined regtest transaction from vault/evidence/regtest-cycle.txt; original bytes, no re-signing.'})
    print(shape, txid, 'height',height,'inputs',len(prevouts),'bytes',len(tx['hex'])//2)
assert len(rows) == 3
(root/'REVIEWS/consensus-evidence/vault.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))
