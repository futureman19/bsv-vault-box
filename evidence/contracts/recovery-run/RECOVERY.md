# Bounded interrupted-run completion

The existing staged implementation and original raw evidence were retained without source redesign. All entries in `../hashes.json` matched the working files before verification. The single-flight fix was already present: all three `run()` observation returns await `observeFinality()` before releasing the lock. The actual async regression passed in the fresh POSIX suite.

## Fresh execution

`commands.json` in this directory records the seven actual commands and exit codes; every command exited 0. Logs are separate from prior evidence:

- VM pair/sponsored/native/launch-record suites: 111 passing.
- Mint suite via WSL/POSIX: 122 passing, zero failed or skipped, including async single-flight and crash/recovery tests.
- TypeScript noEmit: pass.
- Pair and sponsor vectors: pass; no tracked vector change.
- Saved serialized proof: five lifecycle transactions and five sponsor preparations replayed; conflicting spend rejected; liveChainChecked false.
- Read-only recovery CLI: UNCERTAIN_SEND, quarantined true, mayResume false.

No contract, production source or test changes were required during this recovery run. A directory-local `.gitattributes` disables newline conversion for captured evidence: four previously staged files otherwise differed from the recorded byte hashes under core.autocrlf=true. Raw logs, including original whitespace, are not reformatted to satisfy source whitespace checks. Source-only `git diff --cached --check -- mint vault` passed.

## Review and release boundary

This fulfills only the fixed acceptance plan from audit commit `3c5906783e86e5f56b05702c143eec7c95edade2`. The new source delta relative to funded pin `b11a382f197925fd011e8336575f8c90d7740107` is the finality worker plus launch-record/recovery modules and their tests; pair covenant source and compiled bytecode remain unchanged. Compiler reproducibility is not newly established.

Existing security child `t_31e30c41` must review the resulting feature commit; it remains uncompleted by this card. Mint child `t_545a3a30` also remains uncompleted and retains its own scope/holds. Its assets parent is now done, so the earlier report's statement about waiting for its other parent is historical.

All limitations in `../REPORT.md` remain: mocked finality rather than real reorg; digest-only single fixture, not full-art admission or all-201 issuance; read-only diagnosis, not automatic paid-run recovery; reusable numbered seals unsupported; single-indexer trust and non-atomic settlement. No art changes/visual approval, live node, funds, production keys, chain broadcast, sale activation, master push or deployment. Existing public fixture signing in offline tests is not production key work.
