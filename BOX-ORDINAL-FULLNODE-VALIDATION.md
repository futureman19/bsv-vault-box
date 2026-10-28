# BoxSV sponsored external-ordinal custody — independent BSV node validation

## Outcome

**Functional regtest acceptance passed on Bitcoin SV v1.2.3, using the exact compiled artifact and transaction builder from `fbea77dd6a1e339d37eaa906d35209622ebe0e6e`.** No contract, artifact, builder, package dependency, public website or deployment was changed. This remains a Draft one-ordinal prototype, not production approval.

**Operational exception: the discovery phase violated the requested isolation boundary.** A mistaken help invocation opened the existing WSL default mainnet data directory and wallet. Details below are material; this task cannot be described as having left all existing node data untouched. The subsequent acceptance runs themselves used fresh regtest datadirs, disabled wallets and P2P, and loopback-only cookie-authenticated RPC.

## Independent execution and evidence

Primary final run: `evidence/ordinal-fullnode-regtest/run-4-reproduction/`. `run-3-chronicle/` independently repeated the same current-epoch configuration. Earlier `run-1/` and `run-2/` used Genesis activation only; all evidence is retained, not rewritten. Each run has `bitcoin.conf`, `provenance.json`, `network.json`, `rpc.jsonl`, raw transaction `.hex` files, node stdout/debug logs and `result.json`.

Per run, the native C++ node admitted and mined **16 non-coinbase transactions**: funding split, independent inscription, initial empty box, eight sponsor preparations (including attack funding), and five custody lifecycle transactions. **Three freshly signed attacks were rejected.** A fresh chain reached height 126: 110 maturity blocks plus 16 transaction-containing blocks. `verifychain(4,0)` returned true. The existing JS VM also executes inside the unmodified builder, but **its boolean result is not the acceptance gate**: raw serialized transactions are submitted to the independent executable and its responses/chain queried. Separate unchanged VM regressions: 90 passing, in `vm-regressions.log`.

The fixture mines to the published disposable Alice scalar-1 address (wallet disabled), spends a matured coinbase, and mints a supported one-sat P2PKH-before-envelope `text/plain` inscription in its own confirmed transaction. Only afterward is the anchored EMPTY box created and the existing inscription deposited. No synthetic input ancestry is submitted to the node. Sponsor preparations are actual confirmed one-input/one-output P2PKH transactions paying Bob (disposable scalar 2), each with a 500-sat preparation fee. Each custody transaction uses 999500 sponsor satoshis, returns 999000 to Bob, pays a 500-sat fee, and preserves both one-sat principal outputs. These amounts are test parameters, not miner fee quotes. Never fund these keys outside this disposable regtest.

| Lifecycle | Serialized bytes (final run) | Node result |
|---|---:|---|
| Deposit | 11726 | mempool present, mined, raw bytes equal |
| Seal | 15854 | mempool present, mined, raw bytes equal |
| Transfer Alice → Bob | 15855 | mempool present, mined, raw bytes equal |
| Open by Bob | 15855 | mempool present, mined, raw bytes equal |
| Withdraw to Bob | 8814 | mempool present, mined, raw bytes equal |

The harness checks `sendrawtransaction` txid, `getrawmempool`, `getrawtransaction` confirmations/raw bytes, and containing `getblock` membership for every accepted non-coinbase transaction. It queries both final principal UTXOs and checks one sat each and exact Bob P2PKH script. It also checks the initial inscription output is spent, authenticated anchored history replay, and first-input/first-output one-sat ancestry at every transition.

Origin: `15e5c81167db43379ae9dbc43289eb41befbe402dfc6c08d971cb10406cb33bb_0`.
Final ordinal UTXO: `817641232c7760deb069940fe3d638e4b99f861f7628f8f7b8136db04de51a40:0`.
The companion is output 1. Node consensus checks scripts/UTXOs; the **ordinal identity interpretation is positional ancestry checked by this harness**, not a claim of indexer or wallet recognition. These deterministic transaction IDs repeat across runs; block hashes differ.

## Adversarial node results

Each attack is built with fresh full-transaction owner and sponsor signatures, stabilized preimages, and an independently confirmed genuine sponsor UTXO. Both pair inputs are still unspent when submitted. The harness verifies they remain unspent afterward, so failures are not hidden by missing inputs or prior valid-spend conflicts.

- Sealed withdrawal signed by current Alice: RPC error `-26`, `16: mandatory-script-verify-flag-failed (Script failed an OP_VERIFY operation)`.
- Former-owner Alice opening after transfer to Bob: RPC error `-26`, `16: mandatory-script-verify-flag-failed (Signature must be zero for failed CHECK(MULTI)SIG operation)`.
- Former-owner Alice withdrawing after Bob opens: same mandatory CHECKSIG failure.

Former-owner signatures are valid signatures by the **wrong owner**, not blank/stale signatures. All attack bytes and exact node replies are retained. These are native-node mandatory-script failures on the mempool admission path. **No invalid candidate block was constructed/submitted**, so this does not separately demonstrate invalid-block rejection. Successful transactions were actually mined, rather than merely passing `testmempoolaccept` or a local interpreter.

## Node provenance and consensus/policy scope

- Official release metadata: https://github.com/bitcoin-sv/bitcoin-sv/releases/tag/v1.2.3 (saved `release.json`). GitHub release assets list was empty.
- Official archive: https://download.bitcoinsv.io/bitcoinsv/1.2.3/bitcoin-sv-1.2.3-x86_64-linux-gnu.tar.gz
- Publisher manifest: https://download.bitcoinsv.io/bitcoinsv/1.2.3/SHA256SUMS.asc (retained). Archive SHA-256 verified against its checksum: `13f222f5b466fe4af2bb867628354e4ae9711a10019e89fc7bf018b90e30b3c8`.
- Executed `bitcoind` SHA-256: `70b36ab04b1bdd5712e58cf43957e21f6d02dd890f0cce6d0acae16e97783610`.
- Canonical compact-JSON artifact SHA-256: `b63258bcda50691ea871f33e89723c4a22b429a3a9f7636dadd9c2ea36a75a84`.
- Builder file SHA-256: `4c0a7597a054c9508032392b766f4b51a807280f1e929ff682deb69546186426`.
- Manifest was fetched over HTTPS and hash-matched. **Its PGP signature was not independently authenticated against a trusted maintainer key.** No reproducible-source-build claim.
- Host: Windows 11 with Ubuntu-24.04 WSL2, Linux `6.6.87.2-microsoft-standard-WSL2`; Linux Node v22.22.1. Windows Docker absent; WSL Docker installed but default-user socket access denied. Native official Linux binary ran under WSL without installing system packages or modifying existing Docker services.

Final configuration: regtest; Genesis at height 1 and Chronicle at height 2; 100 MB excessive block/consensus stack limits, 10 MB block construction limit; 32 MB coins cache and 16 MB DB cache; `assumevalid=0`; wallet disabled; `listen=0`, `connect=0`, DNS/discovery/UPnP disabled; RPC bound to `127.0.0.1:19483` with a freshly generated cookie. Start/end connection count zero. Node `networkactive` remains true internally but no peers/listener/discovery are configured.

Upstream v1.2.3 `chainparams.cpp` (retained) defaults Genesis/Chronicle to regtest heights **10000/15000**, versus mainnet **620538/943816**. Overrides let the small chain execute the modern eras. Current transaction signatures remain `SIGHASH_ALL|FORKID` (`0x41`), not Chronicle opt-in sighash; scripts/builders are unchanged. Earlier runs did not activate Chronicle; final two did and passed.

Policy: `acceptnonstdtxn=0`, `acceptnonstdoutputs=1` (the latter is the documented post-Genesis default). No general nonstandard-transaction bypass, unlimited stack setting, or script-validation timeout increase was used. Required `minminingtxfee=0.00000001` BSV/kB is an intentionally permissive local mining policy, **not evidence that a commercial miner accepts the chosen fee**. `getnetworkinfo.relayfee` reports zero. Initial runs specified removed `minrelaytxfee`; node logged it as ignored. Final configuration removes that obsolete option. Config and actual RPC values are authoritative, not assumed defaults.

## Reproduce

Requires existing `vault/node_modules` from the repository lockfile, Linux/WSL Node, curl, tar and sha256sum. Use a fresh evidence directory and an explicitly approved scratch location. The wrapper fetches the pinned official archive, checks its exact checksum, extracts into a fresh directory, and invokes the harness. It does not use any existing node RPC or wallet.

```bash
# From Linux/WSL, adjust only absolute repository/scratch/evidence paths:
bash /mnt/c/Users/futur/Desktop/bsv-vault-box/vault/scripts/fullnode-regtest.sh \
  /mnt/c/Users/futur/.hermes/profiles/telegram2/cache/scratch/boxsv-fullnode \
  /mnt/c/Users/futur/Desktop/bsv-vault-box/evidence/ordinal-fullnode-regtest/new-run
```

That exact wrapper was exercised for `run-4-reproduction`, exit 0. Fresh datadir/evidence creation prevents reuse of prior acceptance. The process is stopped through its own cookie RPC; only the spawned child can receive fallback SIGTERM. Scratch binary/data remain for inspection and are not committed. Cookie and wallet files are not copied into evidence. Raw transactions/public disposable keys are intentionally public fixture material.

## Discovery isolation incident — not hidden by the successful test

During binary discovery, `bitcoind -help-debug` was mistaken for a help-only command. After supplying mandatory runtime parameters, it instead started the downloaded binary **without the required isolated datadir/regtest/offline flags**, opening `/home/futureman19/.bitcoin/bitcoin.conf` and `wallet.dat`. Correct syntax is `bitcoind -help -help-debug`.

It ran from approximately 15:58:38 to 16:03:32 UTC on 2026-10-28. The Windows tool timed out but its WSL child survived. Name-only `pgrep bitcoind` missed it because BSV changes process/thread names. Full-argv `ps` identified owned PID 34313; explicit SIGTERM stopped it, and `/proc/34313` absence was verified. Its debug log records default-mainnet chain activity through height 193674 and clean shutdown. No transaction submission, signing or wallet RPC was issued to that process, but **incidental existing-wallet rebroadcast was not assessed, and unchanged wallet/database state cannot be claimed**. Existing data was not deleted or rolled back.

A separate pre-existing node PID 1762, `/home/futureman19/bitcoin-sv-1.2.3/bin/bitcoind -datadir=/home/futureman19/.bsv-regtest -daemon -reindex`, was identified and left running. `discovery-isolation-incident.json` retains selected startup/shutdown lines and bounded tip summaries without copying private wallet data. The final process inventory confirms only that pre-existing node remains; no task-owned node is left running. This is an operational failure, not a covenant-construction failure. Future probes must use explicit isolation even during discovery and full-argv ownership checks after timeouts.

## Remaining boundaries

This closes a finite independent-native-node **functional regtest** gate. It does not establish public-chain inclusion, arbitrary miner fee/policy compatibility, broad NFT grammar support, SPV/indexer/wallet compatibility, security audit completeness, malicious-block rejection, reorg behavior, mainnet deployment, or production sponsor replenishment. No push/deploy or public fixture broadcast was performed. The overall requested no-existing-data-touch guarantee was **not met**, as disclosed above.
