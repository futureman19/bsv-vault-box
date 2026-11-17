# Continuous buyer–design–origin custody: local integration PASS

## Delivered

A working loopback browser application and integration CLI follow **one pinned Iceland candidate and one public fixture buyer** from signed reservation/allocation through **Pack → Seal → Transfer → Open → Withdraw**. The same application engine persists and asserts the design identity, candidate manifest hash, metadata digest, buyer key and independently issued original outpoint at every step. It is not a report joining separate fixtures.

The engine calls the existing serialized transaction/compiled Script and detached-record verifiers, through a separate deterministic fixture wallet adapter. Every browser action drives this engine and shows actual saved IDs. The exact manifest promotional image is retrieved from its pinned Git blob and hash-checked. Production `docs/`, artwork and the other worktrees were untouched.

**Launch remains blocked.** This is not a real-wallet purchase or chain inclusion. No node, testnet/mainnet, funds, user/production keys, service purchase, mint/sale activation, master push or deployment occurred.

## Runnable delivery

Repository branch: `feature/continuous-custody-demo`, based on final-QA integration `db4760ddcb33108da563b1df84a7e308205de3ec`.

Entry point: `launch/continuous/README.md`.

From the exact feature checkout, after `npm ci --prefix vault --ignore-scripts --no-audit --no-fund`:

```sh
node launch/continuous/cli.js demo --dir launch/continuous/.local-demo --port 8789
```

Open **http://127.0.0.1:8789**. Resume the same persisted fixture by restarting with the same directory. The delivery does not leave a server running or publish a hosted preview.

One-command fresh full-flow reproduction:

```sh
node launch/continuous/cli.js run --dir launch/continuous/.reproduction
```

Saved-byte verification of delivered evidence:

```sh
node launch/continuous/cli.js replay --dir evidence/continuous/run-01
```

The attached archive contains the new source/harnesses and evidence, not the full repository, dependencies or all model assets. Use the feature checkout for execution. Node 24's SQLite experimental warning and inherited dependency deprecation warnings remain; installation is not a dependency audit.

## Actual immutable binding

- Design: `urn:boxsv:collection:impossible-places:v1:iceland`
- Exact 201-candidate manifest SHA256: `307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb`
- Metadata SHA256: `45f26e3f26153fe3562949d7a98fc5ea023fa290cbdfecee0edab4bea58045ca`
- Buyer public key, public fixture only: `02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5`
- Independently issued collectible origin: `0580a374ee024525808f19b99f7dca91f3d86880207c3deb3ffa90bbd0206a36_0`
- Final withdrawal txid: `a6a76545443ee590f86107fce49a52dedbccc209cb71e28deb777ec9b783e697`

`run-01/evidence.json` and `journal.sqlite` retain the signed origin/Box issuance, assumed roots, detached authenticity statement, wallet request/response signatures, all five raw custody transactions, funding preparations and acceptance receipts. Final stage **WITHDRAWN**, **17 journal events**. Both final outputs pay the fixture buyer; original ordinal remains output zero. The detached record is not a certificate NFT. The inscription contains only the supported 64-character metadata digest, not model/artwork bytes.

## Real execution

| Gate | Result | Retained output |
|---|---|---|
| Continuous integration, wallet/security, HTTP, child-process crash tests | **22 passed; zero failed/skipped** | `green-final.txt` |
| Existing pair/sponsored/native/launch-record VM suites | **111 passed** | `vm-regression.txt` |
| Existing POSIX mint/finality/pool/recovery/adapters | **167 passed; zero skipped** | `mint-posix.txt` |
| Existing independent security challenges | **10 passed** | `security-regression.txt` |
| Existing allocation/restart/hold regressions | **19 passed** | `allocation-regression.txt` |
| TypeScript `--noEmit` | exit 0 | `typecheck.txt` |
| Fresh connected CLI flow | WITHDRAWN; five Script-verified transitions | `run-01.txt`, `run-01/` |
| New-process saved-byte replay | WITHDRAWN; all provenance/custody predicates true | `replay-01.txt` |
| Desktop 1365×1000 + mobile 390×844 | Complete UI flow, rejection, reload, exact evidence download, no overflow | `browser-02/report.json` |
| Ambiguous-send browser error | Exact bytes retained across reload, hold disables progress | `browser-02/ambiguous-held-reloaded.png` |
| Read-only independent agent review | No scoped blockers; independently reran initial 20-test suite | `REVIEW.md` |

Actual regression commands:

```sh
node --test launch/continuous/test.js launch/continuous/security.test.js launch/continuous/server.test.js launch/continuous/process.test.js
# from vault/; NOT npm test (which invokes unrelated build/compile hooks)
npx mocha --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/native-custody.test.js tests/launch-record.test.js
npx tsc --noEmit
# from repository root
node mint/test/run.js
node --test evidence/security/challenges.test.js
python launch/mint/test_dry_run.py
python launch/continuous/browser_qa.py evidence/continuous/browser-02
```

Browser output directories must be fresh; do not rerun over `browser-02`. Edge ran with external requests blocked and reduced motion. There were no external requests or uncaught page errors. Expected fixture rejection responses are intentional HTTP errors, not hidden success. Parent inspected actual desktop-initial and mobile-complete screenshots: no visible blocking defect; dense small hexadecimal evidence remains less comfortable on a phone. Physical-phone/Safari and deployment were not tested. Owned browser servers were stopped and all three test ports independently refused connections afterward.

## Failure and recovery controls

- Wrong design, metadata digest, origin and buyer mutations are rejected, even when the local event hash is recomputed. A correctly signed response to a changed binding is rejected at the application boundary.
- Signed responses are checked against expected role key, network, entire canonical request and actual transaction/funding bytes. An authentic envelope around a changed transaction is rejected before send. Signature rejection, disconnect, wrong buyer/network and malformed signature cannot allocate or change custody.
- Duplicate IDs do not sign, send or dispense again; reuse for a different action fails. Explicit action prevents stale browser requests from silently advancing the next phase. Two concurrent connections cannot both spend the same phase.
- Prepared raw bytes are committed before transport; an attempt marker commits before send. Tests reopen after exceptions **and abrupt child `process.exit(75)`** at both boundaries. Prepared-only recovery reuses exact bytes without a wallet call; attempted/ambiguous recovery quarantines without resend or replacement funding. This is process-crash coverage, not physical power-loss certification.
- Finality/excess holds are monotonic and retain TRANSFERRED ownership history. No automatic relisting, refund, replacement allocation or authority revocation. New local hold injection is not real payment/finality observation; reviewed production-intended watcher/recovery code is unchanged and its suite passes.

## TDD and honest rerun history

`red.txt` records the continuous-flow assertion failing because orchestration did not exist. `server-red.txt` similarly records the missing connected server. `stale-action-red.txt` records a real behavioral failure: a stale Pack request advanced the next phase; explicit-action validation fixes it. Individual remaining negative cases were added as security regression checks and **were not each observed RED**.

Two harness defects were retained rather than hidden:
1. `security-first.txt`: the first concurrency test awaited a rejection before starting the second connection, allowing a legitimate next-phase action. It was changed to pause the first wallet so both requests actually overlap; product code was not changed for that harness correction.
2. `browser-01.txt`: string `wait_for_function` evaluation hit the strict page CSP. Locator waits fixed the harness; CSP was not weakened. Failed-run files remain under `browser-01/`.

The initial implementation also needed a synthetic root's input-output fixture descriptor before its first green run. Final green output and the two named behavioral RED logs are retained. No independent-review blocking findings required a correction pass, and no optional extra review cycle was started.

## Source-byte provenance

All new implementation and evidence bytes are preserved with directory-local `-text` attributes and verified against staged Git blobs. One unchanged inherited dependency, `vault/src/launch-record.js`, has CRLF working-tree bytes versus LF Git bytes. The first cross-tree byte assertion caught this; no existing source or captured logs were rewritten. `source-provenance.json` records both hashes and newline-only equivalence; `executed-launch-record.js` retains the exact executed dependency bytes. The runtime source inventory intentionally records executed bytes, so a fresh LF checkout must account for this disclosed newline difference. Raw RED/VM logs retain captured trailing whitespace; the source-only whitespace check passes.

## What remains unproven / blocked

- **Exact remaining wallet boundary:** no real extension transport, real user transaction signatures, wallet compatibility or production payment/custody purchase. The adapter is separate and verifies real serialized signatures, but public-fixture success cannot establish any extension's behavior.
- New orchestration integrates fixed-item reservation with custody; it does **not** activate or wire production paid allocation, watcher, pricing, randomness/odds or atomic sale settlement. No launch economics were chosen. Synthetic roots are assumed, not funded ancestry; local acceptance receipts are explicitly not block evidence.
- Script VM replay is not fresh full-node consensus, commercial miner policy, indexer recognition or external security certification. Existing historical node evidence was neither relabeled nor rerun.
- Artwork/model hashes are pinned metadata commitments, not full-art inscription/storage approval. The promotional image was byte-verified and decoded; no new 201-model/art review or archive-issue clearance occurred. Reuse unsupported.
- No trusted real issuer, external checkpoint, protection from coherent journal rewrite/rollback, key recovery, production monitoring, rights/legal/storage/funding clearance or release authorization.
- All **201 final approvals and 73 art/package decisions remain unresolved**; supply remains 195 countries + five oceans + one Moon, each 1-of-1.

**Recommended next step:** review this runnable local journey, then scope one explicitly authorized real-wallet compatibility sandbox—without funding or activating a sale. This milestone closes the local continuous-binding gap only.
