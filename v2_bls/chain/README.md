# Local regtest watcher API

`rpc.cjs` exports `RegtestRPC`; `new RegtestRPC({url, username, password})` (also accepts `user`/`pass`), `.call(method, params=[])`, `.assertRegtest()`.

`node v2_bls/chain/operator.cjs --config <repo-local-json>` runs a polling operator. Config:
```json
{"rpcFile":".local/rpc.json","genesis":{"txid":"64 hex","vout":0},"boxId":"64 hex","operatorIndex":0,"operatorFile":".local/committee/operator-0.json","executable":".local/vault2.exe","stateFile":".local/operator-0-state.json","confirmations":3,"pollMs":1000}
```
Paths resolve relative to repository root; all runtime files must remain inside repo. `--once` performs one poll. Each operator uses its own state file and share file. RPC config is the same object accepted by constructor. Artifact/source are loaded from original `vault/`; no contract changes.

**Node prerequisite:** `getnetworkinfo.networkactive` must be literally `false`, `connections` zero and `getpeerinfo` empty. `-connect=0` alone is insufficient for this gate. Configure network-disabled startup externally; the adapter intentionally cannot bootstrap this by calling `setnetworkactive` while the gate is failing. Requires txindex and a funded wallet with multiple mature UTXOs (funding locks chosen inputs to avoid three-operator races). Uses BSV legacy `signrawtransaction`.

Validation: `node --test v2_bls/chain/chain.test.cjs` passes 15 tests. These are synthetic RPC/serialized-transaction fixtures, not consensus-valid openings or real chain release transactions. Separately, `node v2_bls/demo/milestone1.cjs` passed against BSV 1.2.3 regtest with networking explicitly disabled: actual covenant deployment/transfer/opening, three confirmed releases, public verification and exact NFT decryption. See the parent README and evidence file.

`watcher.cjs` exports `Watcher`, `traceOpening(rpc, genesis, boxId, confirmations=3)`, `decodeVault(hex)`, `releaseScript(record)`, `artifactFingerprint`. Watcher config is above; `await watcher.poll()` returns status, and `watcher.close()` releases its process lock.

The daemon rescans canonical blocks from pinned genesis on every poll, parses actual raw transactions, reconstructs the canonical artifact locking script, and checks every seal transition. Script validity is provided by the independent local consensus node, not caller booleans. Full-node trust is explicit; this is not SPV. Minimum depth is three. A persisted signed release is reused byte-for-byte after restart; a detected lost/changed opening after preparation halts as discrepancy rather than rereleasing. No quorum downgrade: intended committee is 3-of-3; killing one blocks aggregation.
