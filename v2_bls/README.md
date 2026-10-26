# VAULT-0002 BLS prototype — Milestone 1

**Working local prototype, not a production graduation or Stable spec.** Real BLS12-381 IBE, real drand DKG, and three local operator processes have been exercised against an actual BSV 1.2.3 regtest node with the unchanged VAULT-0001 covenant. No substitute chain or cryptography is used by the integration demo.

**Safety exception:** initial node discovery accidentally started a default mainnet node and wrote outside this checkout; it was stopped. No transaction submission or spending was reported. This violated the mission's isolation constraints. See [SAFETY-INCIDENT.md](SAFETY-INCIDENT.md). All demonstrated vault/release transactions below are regtest transactions.

## Reproduce (Windows / Git Bash + WSL)

Prerequisites: Node/npm, Go, Git Bash, WSL `Ubuntu-24.04` with `curl`, `tar`, `sha256sum`, and Python 3. Tested with Go 1.27.1 and sCrypt compiler 1.20.0. No Docker, installed full node, funds, faucet, or public-network wallet is needed.

From the repository root:

```bash
bash v2_bls/scripts/check.sh
wsl.exe -d Ubuntu-24.04 -- bash /mnt/c/Users/futur/vault-0002-workspace/v2_bls/scripts/node.sh start
node v2_bls/demo/milestone1.cjs
wsl.exe -d Ubuntu-24.04 -- bash /mnt/c/Users/futur/vault-0002-workspace/v2_bls/scripts/node.sh stop
```

Replace only the checkout path for another location. `node.sh` downloads the official BSV 1.2.3 Linux archive, checks its pinned SHA-256, generates random local RPC credentials, and places downloads, configuration, chain data and wallet under `.local/node`. Go/npm caches, generated test shares and executable remain under ignored `.local/`. The existing covenant suite creates its ignored `vault/.env` test key; never fund it or commit it.

`check.sh` installs locked npm dependencies when absent (scripts disabled, then explicitly rebuilds the sCrypt transpiler), builds/compiles the unchanged covenant, executes its 8 tests, runs Go tests and `go vet`, builds the CLI, and runs the JS unit tests. The initial npm audit reported 20 inherited vulnerabilities, including one critical; these dependencies were not upgraded as part of this covenant-preserving change.

`milestone1.cjs` is bounded and repeatable. Each run generates fresh test keys, committee, box, and runtime directory. It mines regtest-only coins and performs:

1. Real DKG setup; encrypt a pre-assigned NFT before box creation.
2. Publish public setup and ciphertext data transactions; set the covenant `contentRef` to SHA-256 of the exact ciphertext JSON bytes.
3. Create a sealed covenant; start three independent watcher processes (`--once`) in parallel for each polling round.
4. Verify no release while sealed, after ownership transfer, while the opening is only in mempool, and at two confirmations.
5. At three confirmations, each operator publishes its own attributable `VAULT2-REL` transaction.
6. Restart all three watchers and verify identical transaction IDs, not new releases.
7. Mine and read back each release transaction; publicly verify its BLS share and Ed25519 attribution.
8. Reject all three possible two-share subsets; decrypt with three shares to the exact pre-assigned NFT; reject an altered share.

The output contains real regtest transaction IDs and writes `.local/milestone1-*/evidence.json`. Regtest IDs will not resolve on public explorers. A separate `node v2_bls/demo/chain-smoke.cjs` checks covenant plumbing only, explicitly without a crypto claim.

## Crypto and identity

Pinned dependencies: `github.com/drand/kyber v1.3.3` and `github.com/drand/kyber-bls12381 v0.3.5`; no Windows crypto fallback was required. The module uses drand's `share/dkg` with encrypted deals and authenticated responses, G2 polynomial commitments, and G1 threshold signatures. `ibe.EncryptCCAonG2` / `DecryptCCAonG2` implement the tlock-style Boneh–Franklin CCA construction. This is **not** the drand clock-round protocol: identity is exactly ASCII `VAULT2:` followed by the raw 32-byte box ID (not its hex encoding).

IBE wraps a random AES-256-GCM key; GCM encrypts arbitrary NFT bytes. A release is a 48-byte compressed G1 point. Public verification uses the operator's share of the G2 commitment polynomial. Recovery validates each share, distinct indices and the recovered signature before decryption. Tests also attempt direct under-threshold interpolation and direct IBE decryption, bypassing the wrapper's threshold guard.

The release record is:

```text
OP_FALSE OP_RETURN "VAULT2-REL" <box_id:32> <operator_idx:1> <G1_share:48> <Ed25519_sig:64>
```

Indices are zero-based. Attribution signs `ASCII("VAULT2-REL") || box_raw32 || index_byte || G1_share48`. Kyber's internal two-byte share prefix is not placed on chain. Public operator attribution keys are in `public.json`; pin this setup before verifying records.

## Operator policy and boundaries

Each watcher independently scans the local full node from its pinned genesis outpoint. It decodes and reconstructs canonical scripts, follows current outpoints through sealed transfers, checks immutable box/content identifiers and value, and requires SEALED→OPENED plus at least three canonical confirmations. The canonical compiler/template fingerprint is pinned in `chain/artifact-pin.json`. Genesis/default-state and later stateful-owner encodings are tested separately. Consensus validity is provided by the actual BSV full node; no caller-supplied `covenant_valid` flag is accepted. This is a full-node trust boundary, not an independent SPV implementation.

RPC is literal-loopback HTTP only, with redirects forbidden. Every mutation checks `chain=regtest`, `networkactive=false`, zero connections and zero peers. The node launcher disables listening, connecting, DNS seeds and discovery and then disables networking explicitly. No DefaultProvider, public indexer or network fallback exists in this adapter. The SDK's `testnet` address encoding is used because regtest shares it; transport remains exclusively the checked local regtest RPC.

The opening transaction itself is the request; no covenant format or flag change. Release state is locked per process, bound to box/operator/genesis/artifact, and signed transaction bytes are persisted before broadcasting. Unknown outcomes retry identical bytes. Restart rechecks the opening before rebroadcast; a disappeared/changed opening halts as `UNSEALED-DISCREPANCY`. A final check narrows, but cannot eliminate, the reorg race between observation and publication.

Continuous watcher command (the bounded demo uses `--once`):

```bash
node v2_bls/chain/operator.cjs --config .local/milestone1-RUN/watcher-0.json
```

See [chain/README.md](chain/README.md) for config fields. Each config receives one operator's secret file. The offline CLI's `release` command intentionally does **not** enforce chain policy: an operator with its secret can misbehave. Do not expose it as a public service.

## Tested versus unfinished

Verified locally:
- Unchanged covenant: **8/8** script-VM tests.
- JS chain/provider tests: **17/17**, including synthetic negative/reorg/crash-state fixtures.
- Go crypto/CLI tests and `go vet ./...`: pass, including wrong identity, malformed inputs, forged shares/attribution, tampered ciphertext, duplicate indices and direct two-share attacks.
- Actual regtest integration: passed on repeated fresh committee/box runs; three on-chain releases verified and exact NFT recovered.

Not implemented or claimed:
- **Process-isolated DKG.** The real DKG protocol is orchestrated in one setup process, which temporarily handles all participants. Runtime operators are separate processes, but same-user files are not a security boundary. No claim of issuer secrecy or independently administered operators.
- Secret files are plaintext test material; no Windows ACL hardening, HSMs, encrypted at-rest storage, proactive refresh, secure erasure, or complaint recovery. Never use real keys.
- Mix-net/shuffle proofs and hidden issuer assignments are absent. The demo's issuer knows its pre-assigned plaintext.
- Setup transaction contains the public committee, but does not yet implement the complete inventory/box-count anchor or independent setup discovery. The driver supplies the pinned setup locally.
- Random box ID bound in the actual covenant, matching its deployed v0.1 semantics; not the future outpoint-derived identity binding noted in VAULT-0001.
- One-box Milestone 1 integration, not Step 3's three-box lifecycle or independent-chain premature-release misbehavior scanner. Reorg negative tests use synthetic RPC; deep live-chain reorg handling is not demonstrated.
- The demo uses three concurrent process invocations per polling round, not a long-duration daemon soak. All operators share the local full node and funding wallet; fee-input locking/recovery needs further operational hardening.
- Golden vectors from the Feldman stand-in are preserved, not claimed byte-compatible with BLS. No second independent BLS implementation, audit, public testnet league, or mainnet deployment.
- **Threshold conflict:** this prototype is deliberately 3-of-3. Losing one operator prevents opening. Step 3(e) cannot pass without an explicitly approved different committee/threshold (for example 3-of-4 or 2-of-3). No silent switch was made.

`v2_ref.py`, `v2_vectors.json`, both spec documents, and all tracked `vault/` files remain unchanged. Do not run `v2_ref.py` in-place for verification: its main routine rewrites the baseline vector file.
