#!/usr/bin/env bash
# Linux/WSL only; never use the default Bitcoin datadir or an existing RPC.
set -euo pipefail
if [ "$#" -ne 2 ]; then
  printf '%s\n' 'Usage: bash fullnode-regtest.sh ABS_SCRATCH_BASE ABS_NEW_EVIDENCE_DIR' >&2
  exit 2
fi
BASE=$1
EVIDENCE=$2
case "$BASE:$EVIDENCE" in /*:/*) ;; *) printf '%s\n' 'Absolute Linux paths required' >&2; exit 2;; esac
if [ -e "$EVIDENCE" ]; then printf '%s\n' 'Evidence directory must not exist' >&2; exit 2; fi
mkdir -p "$BASE"
INSTALL=$(mktemp -d "$BASE/boxsv-bin-XXXXXX")
URL=https://download.bitcoinsv.io/bitcoinsv/1.2.3
curl --fail --location --silent --show-error --max-time 120 "$URL/bitcoin-sv-1.2.3-x86_64-linux-gnu.tar.gz" -o "$INSTALL/node.tar.gz"
curl --fail --location --silent --show-error --max-time 30 "$URL/SHA256SUMS.asc" -o "$INSTALL/SHA256SUMS.asc"
ACTUAL=$(sha256sum "$INSTALL/node.tar.gz")
EXPECTED=13f222f5b466fe4af2bb867628354e4ae9711a10019e89fc7bf018b90e30b3c8
if [ "${ACTUAL%% *}" != "$EXPECTED" ]; then printf '%s\n' 'Archive checksum mismatch' >&2; exit 1; fi
# PGP signature is retained, not claimed independently authenticated.
tar -xzf "$INSTALL/node.tar.gz" -C "$INSTALL"
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
node "$HERE/fullnode-regtest.js" "$INSTALL/bitcoin-sv-1.2.3/bin/bitcoind" "$BASE" "$EVIDENCE"
