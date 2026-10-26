# VAULT-0003 regtest lifecycle

## Passed

Two full final executions are recorded verbatim in `evidence/regtest-cycle.txt` and `evidence/regtest-cycle-repeat.txt` (BSV v1.2.3, local isolated regtest). Each execution publishes the 1,000-design manifest, deploys three unchanged VAULT-0001 covenants, transfers box 0 to a different ephemeral owner while sealed, opens boxes 0 and 1, and mines two child transactions with valid pack inscriptions. Box 2 stays sealed; opened covenant outputs remain unspent and independent of pack inscriptions.

All five acceptance checks pass on each execution:

- (a) After the opening is confirmed but before the next block is mined, `drawPackForOpen` returns null using actual chain height/hash availability (D=1).
- (b) Two fresh Node child processes independently fetch the manifest and opening from RPC, resolve the draw hash, and compute identical ordered packs and retry traces. They receive only transaction IDs, not manifests, seeds or packs. This is independent execution of the same library, not independent algorithm implementations. Different newly created boxes/runs intentionally have different packs.
- (c) The second child transaction also carries a deliberately forged inscription at output 1 (first design ID 1000). It is actually mined. `verifyMint` accepts output 0 and rejects output 1, proving client-level rejection, not consensus rejection.
- (d) Slots 0–8 are mutually unique in each pack.
- (e) Slot 9 is in the legendary table (IDs 990–999).

Raw broadcasts are read back byte-for-byte. Confirmation block hashes are compared with the canonical chain. The script checks manifest-root binding, prior sealed state, immutable covenant fields, direct mint ancestry to opening change, and post-mint unspent covenant outputs.

## Transaction invariants

| Stage | Input | Outputs |
|---|---|---|
| Manifest | ephemeral P2PKH funding | 0: zero-sat `OP_FALSE OP_RETURN VAULT3-MANIFEST <canonical JSON>`; P2PKH change |
| Deploy | per-box ephemeral P2PKH funding | 0: one-sat SEALED covenant; fee change |
| Transfer/open | input 0: previous one-sat covenant; separate P2PKH fee funds | 0: one-sat successor covenant, same ID/root; P2PKH change |
| Mint | opening's P2PKH change, never covenant output | 0: one-sat pack ord envelope + P2PKH; optional forged one-sat envelope at 1; ordinary change |

The covenant artifact/source and checker remain unchanged. The current covenant has no ord metadata mirror; the new pack inscription carries `protocol: VAULT3-MINT`, `manifest_root`, `box_id`, and ordered `designs`.

## Reproduce

Node 20+ and a locally running BSV regtest node with wallet/mining RPC, txindex, and Genesis enabled **before deployment** are required. No mainnet/testnet connection is used. The transport accepts only literal loopback ports 18443 or 18445, rejects redirects, and checks `chain === regtest` before every mutation. It never instantiates DefaultProvider or loads `.env`.

One-time build from repository root (no source or artifact changes are committed):

```bash
cd vault
npm ci --ignore-scripts
npm rebuild scrypt-ts-transpiler
npx tsc
npx scrypt-cli compile
```

The compile must report one passing contract. Do not use `npm run build` here: its prebuild removes artifacts.

For a **dedicated disposable** regtest node, one-time setup on Linux/WSL is:

```bash
mkdir -p .regtest-node
/path/to/bitcoin-sv-1.2.3/bin/bitcoind \
  -datadir="$(pwd)/.regtest-node" -regtest -genesisactivationheight=1 \
  -txindex=1 -server -rpcuser=YOUR_LOCAL_USER -rpcpassword=YOUR_LOCAL_PASSWORD \
  -rpcport=18445 -port=18446 -listen=0 -dnsseed=0 -connect=0 -daemon \
  -excessiveblocksize=1000000000 \
  -maxstackmemoryusageconsensus=100000000 -maxstackmemoryusagepolicy=100000000 \
  -minminingtxfee=0.00000001
```

The data directory is ignored and must never be committed/shared (contains regtest wallet keys). Actual verification used the node executable at `/home/futureman19/bitcoin-sv-1.2.3/bin/bitcoind` in WSL Ubuntu-24.04, with the task-local `vault/.regtest-node` datadir. The originally provisioned port-18443 node was left unchanged. The isolated node was stopped after verification; restart with the above options to replay its retained data.

Set `REGTEST_RPC_AUTH` to the local node's user:password without committing it. Then **one command runs the whole demo**, including fresh-chain coinbase maturation when needed:

```bash
REGTEST_RPC_PORT=18445 node scripts/regtest-cycle.js
```

Read-only replay of any logged manifest/open pair:

```bash
REGTEST_RPC_PORT=18445 node scripts/regtest-cycle.js --replay MANIFEST_TXID OPEN_TXID
```

The replay path never generates a key, funds, mines or broadcasts. The RPC credential can be restricted to read-only methods for replay. Each lifecycle run intentionally mints new test boxes and is not idempotent. Keys for boxes and pack outputs exist only in process memory, so these outputs become intentionally unspendable by the demo after it exits.

Additional gates from repo root:

```bash
node test/vault3.test.js
python -B test/python-parity.py
```

Both pass, including 50 independent Python differential cases. Final runtime safety smoke checks reject an unapproved port and missing RPC authentication before broadcasting.

## Failed during development / fixed

- The supplied node on port 18443 rejected the first covenant transfer with `mandatory-script-verify-flag-failed (Push value size limit exceeded)`: Genesis was not enabled at its low regtest height. Manifest and deployment transactions from that failed attempt remain in that disposable chain. A separate Genesis-enabled task-local node resolved this without touching the original node or covenant.
- Default TestWallet fee splitting left only one satoshi of opening change. An initial zero-fee mint entered mempool but was not mined; later input/output accounting assertions correctly stopped insufficient-budget attempts. Disabling splitting preserves enough opening change; explicit conservative fees and assertions now precede publish. Failed-run test outputs/mempool entries are not represented as successful evidence.
- Dependency install reported 20 existing audit vulnerabilities (1 low, 9 moderate, 9 high, 1 critical). Dependencies were not upgraded in this bounded lifecycle task.

## Faked or skipped / review caveats

Nothing in the recorded final runs is a simulated transaction, block hash, or confirmation. Design refs (`design:N`) are deliberately synthetic catalog labels, not hosted artwork. Regtest mining is controlled locally; this does not demonstrate production miner-resistance, unpredictable entropy against the node operator, SPV, reorg resilience, or external ordinal-indexer compatibility.

**Existing VAULT-0001 identity limitation:** the deployed v0.1 covenant requires immutable `boxId` before its own transaction ID exists. This demo uses SHA256d of a public funding outpoint (wire txid + uint32le vout), recorded beside each deployment. It does NOT claim the draft v0.2 definition of a hash of the covenant's own genesis outpoint, which would need a separately specified binding mechanism. No covenant change was made to hide this mismatch. Review this limitation before calling the entire draft protocol production-complete.

The verifier here is a bounded lifecycle adapter, not a general adversarial lineage/indexer implementation. It delegates consensus validity to the local node, checks the immediate opening predecessor and mint linkage, and uses the parent library for exact pack contents. Both replays use the same algorithm; separate Python algorithm parity is covered by the library gate. No mainnet or testnet broadcasts, real funds, committed private keys, external indexer tests, or CI-pass claims.
