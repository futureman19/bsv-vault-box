# BoxSV accidental mainnet startup — bounded read-only assessment

## Outcome

**Confirmed isolation failure and real mainnet peer activity; no affirmative evidence of wallet transaction rebroadcast, spending, or private-key disclosure in the bounded logs. This is not proof that no relay occurred.** The loaded wallet reported zero recorded transactions at startup, and the mempool was empty at import and shutdown. The process shut down cleanly according to its log. At assessment time the incident PID was absent and the only discovered bitcoind process was the untouched pre-existing regtest node.

## Scope and evidence

- Read first: `../../BOX-ORDINAL-FULLNODE-VALIDATION.md`, especially lines 71–77, and `../ordinal-fullnode-regtest/discovery-isolation-incident.json`.
- Source: WSL Ubuntu-24.04 `/home/futureman19/.bitcoin/bitcoind.log`.
- Inclusive window: **2026-10-28 15:58:37–16:04:00 UTC**. Actual first/last selected log times: 15:58:38–16:03:32. Selected 281932 timestamped lines; 193674 UpdateTip records. Source line references below are original log line numbers, not JSON line numbers.
- Saved sanitized excerpts, complete category-match counts, current file metadata, and full-argv process inventory: **`bounded-log-evidence.json`**. Collected **2026-10-28 17:56:00 UTC**.
- Finite local investigation: two streaming passes of this one debug log (inspection, then saved evidence); timestamp filtering preceded selection/output. No older log events or external address lookups investigated. Un-timestamped continuation lines were not analyzed. Category counts are keyword matches, not counts of transactions or proof of exhaustive semantic coverage. All matches in the four selected categories fit the output bounds.
- Wallet/config/database contents were not opened; wallet and chain files were stat-only. No RPC, node start/stop, network API calls, funding, repairs, deletions, commit or push. Source evidence was not overwritten. Log reads may affect access-time metadata according to filesystem policy; no explicit source writes were performed.

## Observations

### Wallet and transaction relay

- 15:58:38, lines 405–407: `Verifying wallet(s)...` / `Using wallet wallet.dat`.
- 15:58:41, lines 486–491: `Loading wallet...`, wallet load duration 13ms, `setKeyPool.size() = 2000`, **`mapWallet.size() = 0`**.
- This is direct evidence of an existing wallet load with zero recorded wallet transactions at that instant, not evidence of an empty balance on the current chain, absence of keys, or inability to receive/spend funds. The node was far behind the network.
- 15:58:41, lines 524–526: mempool TxDB found **0 transactions**; ordinary and non-final mempool import each reported **0 successes, 0 failed, 0 expired**.
- 16:03:28, lines 282270–282271: **`Dumped mempool ... (0 txs, 0 in txdb)`**, and `Dumped 0 txns to non-final mempool`.
- No matching Resend/Rebroadcast, AddToWallet, Commit/CreateTransaction, rescan, or explicit wallet-save event was found in the timestamped window. The seven transaction-relay-category matches were mempool storage/import/dump lines, not observed transaction announcements.
- These observations reduce the basis for conjecture that pre-existing wallet transactions were automatically rebroadcast. They do **not** establish no intervening relay: ordinary logging is not a packet trace, and empty endpoint snapshots do not prove intermediate emptiness. No wallet balance/history RPC was performed.

### Network and synchronization

- 15:58:38, lines 448–449: P2P listener bound, including `[::]:8333`; IPv4 address redacted in saved evidence. Binding does not by itself prove Internet reachability or an inbound connection.
- 15:58:41, lines 505, 513, 521: **1291 peer addresses loaded**, DNS seed lookup started, **16 seed addresses found**. These are peer addresses, not wallet addresses.
- 15:58:42–16:00:30: outbound peer connections explicitly logged (selected original lines 528–531, 1637–2329, 69341, 87608). Mainnet network contact was real, not merely enabled by configuration. This exposes ordinary node/network presence to peers; the log does not establish wallet-address or key exposure.
- 15:59:03–15:59:40: four `invalid-UA` ban-threshold events (lines 5088, 19260, 32734, 37698), not evidence of wallet compromise.
- 15:58:40, line 480: loaded best chain at **height 0**. UpdateTip records run from **height 1 at 15:58:45** (line 533) through **height 193674 at 16:03:28** (line 282181). The final tip's block date is 2012-08-13; this was not a synchronized current-mainnet wallet assessment. Some processing may have used already-present blocks; the log excerpts do not attribute every block to a fresh network download.

### Shutdown and storage

- 16:03:28, line 282221: **`Shutdown: In progress...`**.
- 16:03:32, line 282276: **`Shutdown: done`**. This supports orderly application shutdown, not independent database integrity verification.
- `wallet.dat`: current size **1392640 bytes**, mode **0600**, mtime/ctime **2026-10-28 16:03:32.459816 UTC**. Timestamp alignment is consistent with shutdown-time persistence; without a before-image/baseline it does not prove what wallet bytes changed. Linux ctime is metadata-change time, not creation time.
- Current chainstate log, block-index log, block/undo files, peers.dat, banlist.dat and mempool.dat have incident-window timestamps. Exact metadata is saved, with at most 12 newest children per chain directory. No chain/database file contents were read.
- Observed chain advancement and mempool dump are affirmative runtime effects. The exact newly written bytes, wallet save contents, and rollback delta remain unknown. A blank `db.log` (0 bytes by metadata) and the clean-shutdown message are not an integrity test.
- Chain/index/peer-cache data are generally reconstructible state; wallet data is not interchangeable with cache data. No deletion/rollback is warranted from this limited evidence, and no recovery was attempted. Wallet recoverability cannot be established without an authorized backup assessment.

### Process containment

At 17:56:00 UTC, `/proc/34313` was absent. Read-only enumeration of complete `/proc/*/cmdline` argv for bitcoind executable entries found only:

```text
PID 1762
/home/futureman19/bitcoin-sv-1.2.3/bin/bitcoind
-datadir=/home/futureman19/.bsv-regtest
-daemon
-reindex
```

No task-owned bitcoind remained in this inventory. This is a point-in-time executable/argv check, not a claim that all conceivable renamed executables or other WSL distributions were investigated. PID 1762 was not signaled, queried by RPC, or otherwise modified.

## Actionability, unknowns, and consent boundary

**Actionable evidence:** an accidental default-datadir wallet load, real DNS/outbound-peer activity, chain processing, persistence activity, and clean termination. Isolation/timeout/process-ownership controls should be addressed before any future execution; this assessment does not implement those changes.

**Not established:** wallet transaction broadcast, coin loss, secret/key disclosure, remote compromise, precise wallet byte changes, or verified database integrity. There is no affirmative exposure evidence here that justifies emergency key rotation or fund movement. Absence of such evidence is not a guarantee of safety.

Further investigation requires explicit user consent and a separately bounded plan: wallet/backup comparison or balance/history inspection; offline copied-database integrity checks; reading broader logs/configuration or network/firewall records; any node restart/RPC interaction; any external transaction/address lookup. A retrospective packet-level no-relay proof may be impossible if suitable capture logs never existed. Repairs, rollback/deletion, key rotation or fund movement would require separate authorization; none is recommended as an automatic response to conjecture.

## Files produced

- `evidence/incident-assessment/ASSESSMENT.md` — this report.
- `evidence/incident-assessment/bounded-log-evidence.json` — sanitized observed excerpts, metadata and process inventory.
- Scratch-only collector: `C:/Users/futur/.hermes/profiles/telegram2/cache/scratch/boxsv-incident-readonly.py`.

No original incident report, raw log, wallet, configuration, chain database or existing evidence file was intentionally modified.
