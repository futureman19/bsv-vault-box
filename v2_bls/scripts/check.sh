#!/usr/bin/env bash
# Run from Git Bash on Windows. Go/Node/WSL Ubuntu-24.04 must already exist.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
ROOT="$(pwd -W 2>/dev/null || pwd)"
export GOMODCACHE="$ROOT/.local/go-mod" GOCACHE="$ROOT/.local/go-cache" GOPATH="$ROOT/.local/go"
export TMP="$ROOT/.local/tmp" TEMP="$ROOT/.local/tmp" TMPDIR="$ROOT/.local/tmp"
export npm_config_cache="$ROOT/.local/npm-cache" HUSKY=0 NETWORK=local
mkdir -p .local/tmp .local/go-mod .local/go-cache .local/go .local/npm-cache
if [[ ! -d vault/node_modules ]]; then
  npm --prefix vault ci --ignore-scripts
  npm --prefix vault rebuild scrypt-ts-transpiler
fi
# build's prebuild removes artifacts; compile must follow it.
npm --prefix vault run build
npm --prefix vault run compile
npm --prefix vault run test:mocha
(cd v2_bls && go test -count=1 -v ./... && go vet ./... && go build -o "$ROOT/.local/vault2.exe" ./cmd/vault2)
node --test v2_bls/chain/chain.test.cjs v2_bls/demo/provider.test.cjs
git diff --exit-code -- v2_ref.py v2_vectors.json VAULT-0001-sealed-boxes.md vault/src/contracts/vault.ts vault/scripts/mainnet-cycle.ts
echo 'Offline checks passed. Run node.sh start and demo/milestone1.cjs for real regtest integration.'
