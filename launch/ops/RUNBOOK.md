# BoxSV operator runbook — offline drill, release HOLD

## Authority and scope

This is an exercised **nonsecret fixture** recovery procedure and a proposed operating policy, not a deployed service or approved launch. No keys were created/loaded, no node was run, no real funds or public chain were used, and no production files were changed. Production is GitHub Pages `master:/docs`; pushing master publishes. This card authorizes feature-branch publication only. Never treat a feature push as deployment authorization.

Source of truth: `feature/launch-rehearsal@01225c6aa893122525116dcfa793ac1f3d6885ae`, `evidence/rehearsal/REPORT.md`, `REVIEW.md` and `sha256.json` (SHA256 `8e4837ac5673a34dd170ebab7a27df1de32bfb83d1215af7de89fa284ee038a6`). Recovery validates all 96 inventory entries against that commit and adds the inventory itself: 97 archive files. Parent tests are historical evidence, NOT rerun consensus tests in this OPS card.

## What is actually available

- `launch/ops/recovery.py`: stdlib CLI, explicit hash-pinned nonsecret packet allowlist; deterministic ZIP, external archive hash verification, exact membership/size/hash checks, fresh-directory restore with byte readback. No network or live service controls.
- `launch/ops/exercise.py`: fresh-output-only drill including corrupt archive, wrong trust hash, traversal/extra members, existing destination rejection, restored SQLite replay, SQLite backup API, and local static release-pointer rollback.
- `launch/mint/dry_run.py`: fictional allocation ledger only. `build` does not construct transactions. There is no sale suspension command because there is no integrated live sale here. Do not invent one or run the funded runner as a substitute.
- Collection recovery is separate: `launch/collection/check_package.py` and its trusted inventory hash in `package-report.json`; see that README. This OPS ZIP does NOT contain all 201 model/source payloads or dependencies.

## Reproduce the bounded drill

From a fresh exact feature checkout with Python 3 and Git, choose a never-used card-local output path:

```
python launch/ops/exercise.py --output evidence/ops/my-new-drill
```

The script reads the historical pinned Git blobs and the currently fetched `origin/master` SHA for the second **simulation** release; it records both. It never checks out or writes master. Reproduction's candidate SHA can differ; compare the reported pins, not only PASS. Recorded final drill-03 passed 14 grouped checks in 4.676 seconds on this host, after adding portable-path guards; two additional unit tests cover 12 invalid path variants and duplicate/missing/tampered/symlink members. Earlier drill-02 passed in 5.31 seconds with the same archive hash. The committed archive lives at `evidence/ops/drill-03/rehearsal-backup.zip`; substitute drill-03 for drill-02 in the examples below when using the committed packet. That is local drill duration, not a production RTO measurement.

Initial drill-01 failed in the rollback setup because the harness guessed `docs/box.html` instead of actual `docs/box-demo.html` (and `collection.html` instead of `gallery.html`). Earlier recovery steps had executed. The correction used repository-discovered filenames and a fresh drill-02 directory; failed-run files are preserved locally, not relabeled as passing.

## Backup / restore steps

1. Verify the pinned source commit and obtain the expected inventory hash from a separately trusted record. A self-generated hash identifies bytes; it cannot authenticate its recorder or detect a coherent full-history rewrite.
2. Only the frozen nonsecret rehearsal directory is supported by this helper. Do NOT point it at a wallet, node datadir, home directory, credential store, or future production ledger. No `.env`, cookie, production key, password or private buyer data belongs in repository/evidence backups. Pinned fixture config is public, not permission to archive arbitrary configs.
3. Create a new archive (existing output is refused):

```
python launch/ops/recovery.py backup --source evidence/rehearsal --output evidence/ops/new-backup.zip --expected-manifest 8e4837ac5673a34dd170ebab7a27df1de32bfb83d1215af7de89fa284ee038a6
```

4. Record returned archive SHA256 outside the archive in an authenticated owner-approved channel. Transfer to separately controlled storage only after its funding, retention, encryption and access policy is approved. No external backup was provisioned here.
5. Verify, then restore to a NEW directory whose parent already exists. The recorded drill-02 archive uses:

```
python launch/ops/recovery.py verify --archive evidence/ops/drill-02/rehearsal-backup.zip --expected-sha256 c9a94473b506de18b498fa1a57393053e1113ca40ebc562bd0f002388d52e635
python launch/ops/recovery.py restore --archive evidence/ops/drill-02/rehearsal-backup.zip --expected-sha256 c9a94473b506de18b498fa1a57393053e1113ca40ebc562bd0f002388d52e635 --destination evidence/ops/recovery-new
python launch/mint/dry_run.py audit --db evidence/ops/recovery-new/operator.sqlite
python launch/mint/dry_run.py inspect --db evidence/ops/recovery-new/operator.sqlite
```

6. Preserve a partial directory if disk failure interrupts restore; do not serve it or overwrite it. Fix storage and retry into another fresh directory. Verification precedes extraction, but extraction is not transactional and no power-loss durability claim is made.
7. For future mutable SQLite state, stop admissions/writers through the actual supervised service before snapshotting; use SQLite backup API (exercised here on a read-only restored fixture), not a naked live `.sqlite` copy that omits WAL. Audit both snapshot and replay, record last durable event and external checkpoint. This exercise does not establish an online production backup integration.
8. Never restore an older allocation/sponsor ledger into an active service. Reconcile events after the checkpoint against exact persisted transaction bytes, chain observations and operator incident records first. Missing events/ambiguous reservations mean HOLD, not relisting. Restoring media or static HTML cannot restore keys or establish current chain ownership.

Proposed retention, requiring owner approval: immutable pre-release packet plus daily nonsecret snapshots; keep 30 daily and 12 monthly copies on two separately controlled stores with one offline/immutable copy. Monthly fresh-directory restore and before every release. Ledger safety target: zero acknowledged event loss; nightly backups alone cannot meet it—durable event replication/external checkpoints are unimplemented. Proposed incident RTO: static presentation 30 minutes; financial operations have no automatic resumption deadline and remain suspended until reconciled. Key recovery must be a separate owner-controlled encrypted/threshold procedure, tested separately with authorized custodians; this card does not claim key recoverability.

## Monitoring and error budgets — proposed, NOT provisioned

Named roles must be assigned before launch: incident commander (owner/delegate), operator, independent verifier, communications owner. No current paging integration/on-call coverage exists. Operator owns triage; verifier approves evidence; owner alone approves funding, sale and release decisions. Keep sanitized timestamps, exact code/artifact refs, event IDs and transaction IDs; never log keys, cookies, authorization headers or buyer PII.

| Signal / cadence when enabled | Threshold | Response |
|---|---|---|
| Static HTTPS entrypoints and asset hashes, every minute | Two consecutive failures, incorrect hash, or missing required asset | Page operator; stop release promotion; investigate CDN/Pages artifact; scoped rollback only with authorization |
| Static availability monthly target | 99.9%, at most 43.2 minutes unavailable per 30 days | Budget exhausted: freeze discretionary releases; repair only, owner review |
| Chain/indexer freshness every 30 seconds during future operations | Three transport failures, stale observation >120 seconds, disagreement in outpoint/block/depth | Immediately hold new allocations/payment-dependent transfers; retain read-only status; do not infer confirmations from balance |
| Chain progress | No new tip for 60 minutes | Investigate, retain payment-dependent holds; block intervals vary so this alone is not a proven outage |
| Ambiguous broadcast, finality loss, unexpected spender, duplicate allocation, journal integrity error | Any occurrence: zero safety budget | Suspend affected state-changing flow immediately; preserve ledger and exact bytes; incident reconciliation |
| Excess/partial/late receipts | Any occurrence | Durable refund/quarantine accounting; never drop receipt or auto-refund/relist |
| Backup verify / replay / external checkpoint age | Any mismatch or last planned daily backup >26 hours | Page operator, stop future financial admissions; do not roll back state to hide corruption |
| Key/auth exposure | Any suspicion | Suspend signing, preserve sanitized evidence; owner-led credential response, no automatic key rotation by this card |

Availability is a presentation goal, not a custody safety allowance. All financial integrity violations consume the entire safety budget immediately. Sampling and thresholds require integration tests and production approval; this document is not a working monitor. Error-budget definition: count scheduled minute probes unavailable, count missing observations as unavailable, report duration and denominator; never count cached HTML success as a successful payment path.

## Incident handling

**Chain/indexer outage:** record last trusted tip and observation time. Stop new admission and payment-dependent dispatch through the future service's tested maintenance control (currently unimplemented). Existing boxes/ownership do not depend on website uptime. Show neutral unavailable status, not 'payment failed'. Queue receipts durably without authorizing transfers. On recovery, compare raw txid, scripts/values, block membership, depth and current unspentness; single-indexer evidence is a remaining limitation. Require two fresh consistent observations and independent operator review before resuming; two observations are not independent sources or consensus certification.

**Ambiguous transaction:** persist exact raw bytes/txid, attempted count, payment and sponsor reservation before any transport. Timeout is unknown, not rejection. Quarantine the original reservation/funding parent. Query the exact txid and every input spend; preserve evidence if no definitive result. Never allocate another sponsor parent, mutate/re-sign a replacement, issue a second collectible, refund automatically or relist while uncertain. Existing guarded retry logic must revalidate finality and its budget; no ad-hoc broadcast commands in this runbook. Conflicting spend is escalation, not permission to forge ownership history.

**Finality loss after transfer/open:** retain TRANSFERRED/OPENED/WITHDRAWN history where that layer records it; attach a durable reconciliation hold. Payment reversal does not revoke buyer authority. The regtest service API ends OPENED even when captured transactions include withdrawal; do not rewrite its state label. Check inclusion-completion and later terminal observations, not only pre-broadcast retries.

**Sale suspension:** currently sale is disabled/unimplemented end-to-end; keep it that way. Future prerequisite: tested server-side admission/dispatch disable controls that leave receipt ingestion, persisted obligations and read-only status operational. Hiding a Buy button is insufficient. Stop signing/dispatch in a controlled manner after durable in-flight reconciliation, retain pool locks while operations drain, and never delete ledger/lock files to resume. Require fresh backup/replay, reconciled unknowns, fixed root cause, verifier and owner authorization before reopening. Public status should state affected function and next update time, without promising refunds or transaction reversal.

## Release and rollback plan (NOT executed)

1. Owner must authorize exact release scope/ref, destination and maintenance window; all release gates below remain HOLD. Fetch refs, record current remote master and candidate, clean isolated feature worktree, preserve concurrent edits. No force push/reset or rewriting another worktree.
2. Capture immutable whole-site `docs/` and asset manifest plus source/artifact pins before release. Verify all relative assets, gallery roster, fallback and browser acceptance. This card only exercises three HTML entrypoints in a local pointer simulation; it does not claim full production-site restoration.
3. Push feature first; exact `git ls-remote` SHA readback. Independent review. After explicit authorization only, integrate scoped change into current master without reverting unrelated work; GitHub Pages publication must be treated as a side effect of master push.
4. Read back actual live HTML/JS/CSS/GLB/image hashes after publication, not only HTTP 200. Exercise claw input/failure/replay, standalone and embedded Box interaction, mobile gallery and full asset decode. Keep a time-bounded verification window; if incorrect artifact persists, stop and escalate rather than repeatedly deploying blindly.
5. Rollback trigger: mismatched live artifact, startup failure, broken primary navigation or integrity/claim regression. Prepare a scoped revert of the specific release in a NEW feature branch; review against current master to preserve later concurrent edits. Obtain scoped rollback authorization, then follow the same release gate and live hash/browser readback. Do not roll back custody/receipt/sponsor/allocation databases, key material or chain transactions with website code. Preserve irreversible ownership and pending obligations.
6. Local drill uses immutable release directories plus fsync/atomic replacement of `active.json`, verifies hashes before selection, and proves corrupted candidate cannot replace the known-good pointer. Labels 'known-good'/'candidate' are drill labels, not production approval; GitHub Pages has different propagation and failure semantics, not tested here.

## Launch preflight — all must be evidenced, not inferred from this card

- [ ] Assign incident/on-call/verifier roles, maintenance controls, pagers, external checkpoint trust and owner-approved recovery targets; exercise a real service restart/suspension before funding.
- [ ] Continuous allocation → selected design → real issuer/origin → buyer → custody transaction binding implemented and independently tested. Uganda simulation, generic regtest ordinal and Iceland metadata proof remain separate.
- [ ] Real wallet signing/payment/custody integration; current four identity-only mocks are not signing evidence.
- [ ] Full-art admission/storage/preservation and exact package validation; legitimate issuer and independently chosen trust policy, miner/indexer/wallet compatibility, independent security review.
- [ ] All 201 one-of-ones reconciled (195 countries, five oceans, Moon); 73 art/package holds resolved, 128 limited candidates NOT silently approved, zero current final approvals. USA v9 wrapped-star continuation remains unresolved. Historical inner/source-archive discrepancies retained.
- [ ] Rights/provenance clearance, approved final art, collectible separated from outer vault and detached signed record (not extra certificate NFT); no accessories at launch.
- [ ] Price/currency/fees, reserves/odds, allocation fairness/entropy/buyer ordering, Moon-claimed disclosure, reveal, cancellation/refunds/tax/jurisdiction decisions approved; equal edition scarcity, no value guarantees.
- [ ] Funding/storage costs, mainnet, keys and release explicitly authorized separately. Production key custody/recovery remains untested here.
- [ ] Preserve public claims: claw is marketing demo; promo artwork may differ from model; reusable numbered seals UI-only until contract-proven; sequential payment/transfer is not atomic sale settlement; saved node proof is historical, not live unspentness.
- [ ] Address parent mobile prize-overlay interference, missing settled desktop prize capture and lazy-gallery screenshot limitations; physical-phone/Safari/deployed acceptance still absent.
- [ ] Independent final QA `t_85a25a3c` reviews actual files and evidence; this runbook completion does not approve launch.

Recommended next step: existing FINAL QA card consolidates implementation gaps separately from owner decisions, using the exact OPS feature SHA and parent pins. No new launch/deployment task is authorized by these passing local checks.
