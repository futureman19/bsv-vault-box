# Incident follow-up — wallet disposition and implemented controls

Follow-up to `ASSESSMENT.md` (2026-10-28 accidental mainnet startup). Performed 2026-10-29 UTC with the owner's explicit consent.

## Wallet disposition: provably empty, quarantined, keys burned

The wallet loaded during the incident was inspected on a **copy** inside a fresh
regtest datadir (wallet RPC over loopback only; original file never opened by a node):

- Unencrypted HD wallet, created **2026-10-26 20:21:40 UTC** (two days before the
  incident — the first, unnoticed default-datadir launch). Keypool 1000 + 1000 internal.
- `txcount = 0`, zero labels, zero recorded transactions — nothing ever received or spent
  as far as the wallet itself knows.
- All **2001** derivable mainnet P2PKH addresses were computed from the regtest dump
  (hash160 re-encoded to mainnet, no keys exported from WSL) and checked against the
  bananablocks indexer: **all balances 0 satoshis**. Address-list SHA-256:
  `0d2f9d344411dfdb1a9beb8e6d387b41a43aa1933488fd03201bbd9dfed7abd6`
  (list retained locally, not published — the wallet is empty and retired, but there is
  no reason to publicly link its addresses).

Nothing of value was ever at risk. **However**: during inspection the dump (including the
HD master key) transited a live terminal — treat the key material as **burned**.
The wallet and every key in it must never be funded or used again.

## Controls implemented

1. **Quarantine**: `~/.bitcoin/wallet.dat` moved to
   `~/backups/boxsv-incident-2026-10-28/wallet.dat.original-quarantined` (sha256
   `cfa43dd5…a8012`, three identical copies incl. one Windows-side). Any future
   accidental default-datadir launch now creates a fresh empty wallet — nothing existing
   can be loaded. A `README-QUARANTINE.txt` marks the datadir.
2. **Invocation guard**: `vault/scripts/bitcoind-guard.sh` refuses any bitcoind call
   without an explicit non-default `-datadir`, requires `-regtest`/`-testnet`, and runs
   under a hard `timeout` (30 min default, `BOXSV_NODE_TIMEOUT` to override).
3. **Inspection hygiene**: the transient regtest datadir and wallet dump used for the
   balance audit were shredded/removed the same session; the inspection node ran with
   `connect=0 listen=0 dnsseed=0 discover=0 upnp=0` and was verified stopped.

## What was NOT done

- The pre-existing regtest node (PID 1762, `-datadir=.bsv-regtest -reindex`) was not
  touched.
- The incident-window chain data in `~/.bitcoin` (blocks/chainstate synced to height
  193674) was left in place per the assessment's "no deletion warranted".
- No key rotation was needed: no keys from this wallet protect anything, anywhere.
