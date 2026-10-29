#!/usr/bin/env bash
# bitcoind invocation guard — added after the 2026-10-28 accidental mainnet
# startup (see evidence/incident-assessment/ASSESSMENT.md).
#
# Refuses to exec bitcoind unless:
#   1. an explicit -datadir=... argument is present, AND
#   2. that datadir is NOT the default ($HOME/.bitcoin), AND
#   3. -regtest or -testnet is present (mainnet node work is out of scope here).
#
# Usage: bash bitcoind-guard.sh <bitcoind-binary> [bitcoind args...]
set -euo pipefail
if [ "$#" -lt 1 ]; then
  printf '%s\n' 'Usage: bash bitcoind-guard.sh BITCOIND_BIN [args...]' >&2
  exit 2
fi
BIN=$1; shift
DATADIR=''
NETWORK=''
for a in "$@"; do
  case "$a" in
    -datadir=*) DATADIR=${a#-datadir=} ;;
    -regtest)   NETWORK=regtest ;;
    -testnet)   NETWORK=testnet ;;
  esac
done
if [ -z "$DATADIR" ]; then
  printf '%s\n' 'GUARD: refusing — no explicit -datadir given (bare invocations hit the default datadir)' >&2
  exit 2
fi
case "$DATADIR" in
  "$HOME/.bitcoin"|"$HOME/.bitcoin/"|~/.bitcoin)
    printf '%s\n' 'GUARD: refusing — the default datadir is off-limits on this host' >&2
    exit 2 ;;
esac
if [ -z "$NETWORK" ]; then
  printf '%s\n' 'GUARD: refusing — pass -regtest or -testnet explicitly; mainnet is out of scope' >&2
  exit 2
fi
# Hard wall-clock ceiling so a forgotten node cannot run for days (default 30 min).
exec timeout "${BOXSV_NODE_TIMEOUT:-1800}" "$BIN" "$@"
