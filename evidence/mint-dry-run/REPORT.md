# MINT dry-run delivery — bounded milestone

Branch `feature/launch-mint-dry-run`; asset parent `d9de7e9562a1a3f69650cff04b6883bf7e4bcdaa` and repaired security source `10acb9dfa127862b20172f4ce12f1dee32901b88` merged into isolated assigned worktree. No inherited vault/mint implementation changes. New implementation lives only in `launch/mint/`.

## Delivered

Offline Python CLI, exact pinned 201-design roster, proposal-only deterministic allocation, exact remaining-pool fractional odds and Moon allocation visibility. SQLite serialized writers, append-only API history, atomic snapshot/events, restart replay, uniqueness/idempotence, receipt deduplication, partial/late/excess-payment accounting, expiry/refund and ambiguous-send holds. Finality-loss holds preserve confirmed ownership state. No automatic unlock/refund/reallocation; no transaction builder or live sender exposed.

Fixture config uses 100 fictional units and public seed. Neither price, reserves, allocation nor reveal/sale policy is approved. Build outputs an unsigned detached-record plan, not a certificate NFT or serialized mint. `launchReady:false`, `mayBroadcast:false` always. CLI run selected Uganda, progressed through simulated WITHDRAWN, retained 200 available, 7 ledger events. Actual DB and command output are preserved.

## Fresh verification

- `python launch/mint/test_dry_run.py`: **19 passed**, covering all 201 unique reservations, 202nd rejection, repeated-request behavior, concurrency, restart via separate CLI processes, rollback before/after write, tamper rejection, canonical Moon odds, holds and live-action denial.
- Real CLI init + six fixture actions + inspect + audit: all exit 0. Saved operator.sqlite read back and verified WITHDRAWN, mayBroadcast false.
- Inherited compiled Script suites: **111 passed**; retained security challenges: **10 passed**; TypeScript noEmit: pass.
- Saved parent proof replay: **5 lifecycle transactions + 5 sponsor preparations**, conflict rejected, `liveChainChecked:false`. This is historical serialized replay, not fresh node acceptance or all-201 issuance.
- Read-only isolated review approved bounded simulation, with one nonblocking malformed-action issue reproduced/fixed and full suite rerun; details in REVIEW.md.

Exact gate invocations in commands.json and run-gates.py. Separate replay command: `node evidence/contracts/replay-proof.js evidence/contracts/proof.json evidence/contracts/fixture-trusted-policy.json`. Locked install used `npm ci --ignore-scripts --no-audit --no-fund` in vault; dependency deprecation warnings are preserved, no dependency-security clearance claimed. Full POSIX funded-mint suite was NOT rerun on this card; prior 167-pass evidence is inherited historical evidence, not included in fresh counts.

Original attempt unexpectedly left scaffold/tests despite provider failure report; preserved tests-red.txt and stale temp fixture untracked rather than trusting prior status. Fresh scaffold RED in recovery-red.txt; initial implementation had a fixture-slug mismatch (moon vs canonical the-moon), retained first-green.txt is actually a failed run. Explicit Moon positive test reproduced the output bug in moon-red.txt; repaired. Reviewer issue RED in action-red.txt. Other added concurrency/CLI controls were regression verification, not individually observed RED. Historical raw logs untouched.

## Readiness boundary

No live node, mainnet/testnet, real keys/funds, sale activation, minting, production docs changes, master push or deployment. VM tests use existing public deterministic fixtures. No additional art generation, visual edits or approval. USA v9 remains unapproved with wrapped-star continuation unresolved. Promotional illustrations remain distinct from interactive models.

This milestone is local allocation/operator rehearsal only. Full-art admission/storage/all-201 transaction generation, issuer authentication, buyer/outpoint binding, production fairness, independent checkpointing, ongoing paid fulfillment/refunds, wallet/indexer/miner integration and external security certification remain absent or unproven. Parent one-collectible narrow commitment custody does not establish arbitrary NFT support or numbered reusable seals. Single-indexer and sequential payment/transfer limitations persist. Full unresolved operator/sale approval checklist is in `launch/mint/README.md`.

Next: existing dependent rehearsal `t_35cdff45`, after its other required parents. No new test program or launch authorization implied. `sha256.json` pins exact staged bytes for source and this evidence packet; self-generated hashes establish byte identity, not recorder authenticity.
