#!/usr/bin/env bash
# WSL Ubuntu-24.04; all node state is kept inside this checkout.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BASE="$ROOT/.local/node"
export TMPDIR="$BASE/tmp"
mkdir -p "$TMPDIR" "$BASE/data" "$BASE/downloads"
umask 077
VERSION=1.2.3
SHA=13f222f5b466fe4af2bb867628354e4ae9711a10019e89fc7bf018b90e30b3c8
ARCHIVE="$BASE/downloads/bitcoin-sv-$VERSION-x86_64-linux-gnu.tar.gz"
BIN="$BASE/bitcoin-sv-$VERSION/bin"
CONF="$BASE/bitcoin.conf"
if [[ ! -x "$BIN/bitcoind" ]]; then
  curl -fsSL --retry 2 "https://releases-svnode.bsvblockchain.org/svnode-$VERSION/bitcoin-sv-$VERSION-x86_64-linux-gnu.tar.gz" -o "$ARCHIVE"
  printf '%s  %s\n' "$SHA" "$ARCHIVE" | sha256sum -c -
  tar -xzf "$ARCHIVE" -C "$BASE"
fi
if [[ ! -f "$CONF" ]]; then
  python3 - "$CONF" <<'PY'
import pathlib,secrets,sys
pathlib.Path(sys.argv[1]).write_text('''regtest=1
server=1
listen=0
connect=0
dnsseed=0
discover=0
upnp=0
listenonion=0
maxconnections=0
txindex=1
genesisactivationheight=1
rpcbind=127.0.0.1
rpcallowip=127.0.0.1
rpcport=18483
excessiveblocksize=100000000
maxstackmemoryusageconsensus=100000000
minminingtxfee=0.00000001
'''+ 'rpcuser=regtest_' + secrets.token_hex(8) + '\nrpcpassword=' + secrets.token_hex(32) + '\n')
PY
fi
# Safety flags cannot be overridden by config. Never accept extra daemon flags.
COMMON=(-datadir="$BASE/data" -conf="$CONF" -regtest -rpcport=18483)
cli() { "$BIN/bitcoin-cli" "${COMMON[@]}" -rpcconnect=127.0.0.1 "$@"; }
verify() {
  cli getblockchaininfo > "$BASE/blockchain-info.json"
  cli getnetworkinfo > "$BASE/network-info.json"
  python3 - "$BASE" <<'PY'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); b=json.loads((p/'blockchain-info.json').read_text()); n=json.loads((p/'network-info.json').read_text())
assert b['chain']=='regtest', b['chain']
assert n['connections']==0, n['connections']
assert n['networkactive'] is False, 'P2P must be disabled'
print(json.dumps({'chain':b['chain'],'blocks':b['blocks'],'connections':n['connections'],'subversion':n['subversion'],'rpc':'127.0.0.1:18483'}))
PY
}
case "${1:-start}" in
  start)
    if ! cli getblockchaininfo >/dev/null 2>&1; then
      "$BIN/bitcoind" "${COMMON[@]}" -daemon -listen=0 -connect=0 -dnsseed=0 -discover=0 -upnp=0 -listenonion=0 -maxconnections=0 -rpcbind=127.0.0.1 -rpcallowip=127.0.0.1 -txindex=1 -genesisactivationheight=1
    fi
    for _ in {1..60}; do
      if cli getblockchaininfo >"$BASE/start-chain.json" 2>/dev/null; then
        python3 -c 'import json,sys; assert json.load(open(sys.argv[1]))["chain"] == "regtest"' "$BASE/start-chain.json"
        cli setnetworkactive false >/dev/null
        verify
        exit 0
      fi
      sleep 1
    done
    printf 'RPC did not become ready; inspect .local/node/data/regtest logs\n' >&2
    exit 1;;
  status) verify;;
  stop) verify >/dev/null; cli stop;;
  rpc) shift; verify >/dev/null; cli "$@";;
  *) printf 'Usage: node.sh {start|status|stop|rpc METHOD [ARGS...]}\n' >&2; exit 2;;
esac
