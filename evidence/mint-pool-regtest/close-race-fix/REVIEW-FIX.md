# Sponsor-pool shutdown race correction

Review reproduced release of the writer lock during an in-flight RPC, followed by descriptor reuse and duplicate dispense. The correction rejects synchronous `close()` while busy; callers must await the active operation and retry. Closed pools reject ledger appends before touching a descriptor. A private synchronous close path preserves fail-closed handling on ledger failure, which immediately aborts the operation before broadcast/delivery.

TDD: the four paused-RPC tests failed against the original code with `Missing expected exception.` (10 pass, 4 fail), then passed after correction. Coverage pauses prepare at chain check, source lookup and broadcast, plus dispense at UTXO lookup. Each checks lock retention, busy rejection, reopen, no closed-writer RPC/write, and exactly one durable dispense after replay. An additional disk-failure regression checks no broadcast and safe reopen.

Final gates (Hermes-run):

```
node mint/test/run.js
1..15
# tests 15
# suites 0
# pass 15
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 3614.780762

cd vault && npx mocha --no-config tests/*.test.js
  90 passing (8s)

node mint/scripts/regtest-pool.js evidence/mint-pool-regtest/close-race-fix
{"status":"PASS","preparations":3,"depth":5,"ledger":{"inputSats":300000,"prepFeeSats":1500,"preparedSats":298500,"dispensedSats":298500,"heldSats":0},"evidence":"/mnt/c/Users/futur/Desktop/bsv-vault-box/.worktrees/t_b6d09450/evidence/mint-pool-regtest/close-race-fix"}
```

All exits 0. Full test stdout is adjacent. Fresh integration evidence preserves the earlier committed run. Three preparations admitted and mined at depth 5; grammar and ledger checked against actual node data. Owned node shutdown exitCode 0. No mainnet, real-value keys, VPS or site changes.

During this correction PR #15 was independently merged at 160d8d8, including an unrelated LF-attributes change bd11776. The correction branch is based on that merged master, so its diff necessarily modifies the three newly introduced mint files rather than remaining additive relative to current master. No files predating phase 1 are changed by this correction, and prior evidence is preserved.

Known boundaries: regtest only; POSIX key-file custody; callers must handle busy close; caller-driven replenishment; manual ambiguous-broadcast/stale-lock reconciliation; downstream finality/unspentness revalidation. No production security or miner-policy claim. Independent correction review is required before phase 2 proceeds.
