# Independent local security challenge — changes required before launch

## Verdict and scope
Review completed against `6dbcd54bcb254d51b3edb847af0035316f3d4aef` (`feature/launch-contracts-hardening`), remotely read back at review time. The earlier audit is `3c5906783e86e5f56b05702c143eec7c95edade2`; funded adapter comparison is `b11a382f197925fd011e8336575f8c90d7740107`. This is a new local review session, with an additional read-only static reviewer, not third-party security certification.

Existing gates pass, but focused adversarial tests reproduce three findings. **Do not treat this card's completion as approval of the implementation or launch.** The card delivers the review, failing acceptance controls and repair handoff; it does not alter production implementation. Repair and independent recheck must precede integrated rehearsal approval.

## Findings

### S-01 — Medium, new: recovery replay can erase finality history and holds
`mint/recovery.js:88–95,187–201` replaces each sale snapshot after checking only inventory, buyer and raw transfer continuity. It does not preserve historical INCLUDED or reconciliation facts. A later snapshot with identical valid signed transaction bytes can regress INCLUDED/TRANSFERRED to BUILT/PAID_PENDING; with a captured zero-confirmation observation the classifier reports BUILT and `reconciliationRequired:false`. Likewise a later snapshot clearing an earlier PAYMENT_FINALITY_LOST hold reports false.

Both are runtime reproduced in `challenges-red.txt`. They undermine the advertised contradiction diagnosis and monotonic operator holds. They do **not** authorize spending: `quarantined:true` and `mayResume:false` remain intact. Input is local captured journal data; no remote attacker mutation or normal worker path producing these snapshots was established. Treat as an operator-recovery integrity acceptance blocker, not demonstrated theft.

Required repair: preserve historical inclusion/ownership and monotonic hold facts, or reject regressive/contradictory snapshots as INCONSISTENT. Preserve legitimate BUILT/UNCERTAIN retry transitions. Add durable-history controls for cleared reasons, not just cleared flags. Never remove locks, relist, resume, or dispense replacement funding from this classifier.

### S-02 — Medium, pre-existing: inclusion accepts contradictory block evidence
`mint/transfer.js:102–118` validates transaction-detail depth but accepts a block with any positive `confirmations` and matching txid in its list. It does not require block hash equality, integer block confirmations, or block depth >= configured depth. Three negative controls reproduce acceptance of (1) detail depth 3/block depth 1 when policy depth is 2, (2) a different block hash, (3) fractional block depth 0.5. Consistent inclusion and missing-membership controls behave correctly.

The same predicate exists in the pinned funded ancestor (`included` before this change), so this is **not introduced by the hardening commit**. Inconsistent/stale RPC responses can prematurely satisfy transfer/open inclusion or conceal finality loss; this does not defeat signatures or create chain ownership. A consistently malicious indexer remains a separate known trust assumption even after repair.

Required repair: validate block identity, safe-integer depth >= policy depth, membership and response shape; fail closed on contradictions. Test actual worker PAID_PENDING and terminal branches plus observeOpen, without broadcasts or replacement funding. Existing mocks lacking block hashes should become realistic, not weaken the checks. This is a finality-policy launch blocker.

### S-03 — Low, new: exact object schema admits inherited fields
`vault/src/launch-record.js:8–17` checks own-key count but reads expected fields through prototypes. A valid envelope with inherited signature and an unrelated own `extra` property is accepted. Runtime reproduction retains a valid external-policy signature: no forgery or issuer-trust bypass was established. Ordinary JSON-parsed objects do not exhibit this inherited-field shape.

Required repair: require each expected field to be an own property along with exact own-key count and string types; cover envelope, policy and media objects. Low-risk direct-JavaScript API schema hardening, not an independent critical launch risk.

## Actual execution
- Locked dependency install: `npm ci --ignore-scripts --no-audit --no-fund` in vault, exit 0; deprecation warnings retained as a limitation, no dependency-security clearance claimed.
- `python evidence/security/run-gates.py`: all seven parent gate commands exit 0. Fresh **111 VM tests**; **122 POSIX mint tests**, zero skipped; typecheck; pair and sponsor vectors; saved serialized proof replay; read-only recovery CLI. Exact commands and logs are here, not overwritten parent evidence.
- VM suites cover pair/native/sponsored custody, old-owner authorization, sealed withdrawal, missing/duplicate/substituted assets, counterfeit/parent proofs, sponsor auth/change/fee and conflict handling. No unauthorized genuine-custody withdrawal found in this bounded review.
- Saved proof replay: five lifecycle transactions and five sponsor preparations; conflicting spend rejected; `liveChainChecked:false`. One collectible metadata commitment plus detached signed record, not a certificate NFT or full artwork inscription.
- `node --test evidence/security/challenges.test.js`: **10 cases, 4 positive/control passes, 6 expected-security failures (exit 1)** proving the three findings above. These are deliberately RED acceptance tests, not a passing security suite. Raw output is `challenges-red.txt`.
- Source review read actual covenant, verifier, transfer worker, recovery, launch record, parent audit and corresponding tests. Additional static reviewer findings S-01/S-03 were independently reproduced by this worker before inclusion.
- No compiler rebuild; unchanged compiled artifact exercised and fingerprinted. No node/harness invocation, live reorg, network chain call, real funds, production keys, issuance, sale, or production release. Existing POSIX unit suites use only public deterministic fixture material and temporary test files.

## Remaining launch limits
Parent F-01's invoked-worker finality reconciliation and single-flight tests pass; this is not an ongoing monitoring daemon. S-02 limits the quality of inclusion observations. Recovery stays read-only, not automatic paid fulfillment/refund/lock recovery. Original-collection provenance, manifest completeness and custody integrity remain distinct.

Full-art admission/storage durability, issuance of all 201 one-of-ones, wallet/indexer/miner compatibility, single-indexer trust and sequential non-atomic settlement remain unproven or explicitly limited. Reusable numbered seals are unsupported on-chain; OPENED-to-SEAL rejection remains tested and public reuse is simulation. No visual review or artwork change was undertaken; USA v9 remains unapproved. Price/odds/allocation/legal terms, storage cost, funding, mainnet and release require their existing approvals. No arbitrary NFT support or production readiness is inferred.

## Handoff
Repair S-01/S-02 and harden S-03 in a separately assigned bounded implementation card, using this exact review branch and retained RED controls. Independently rerun the complete existing gates and make all ten challenge cases pass; include worker-level finality and historical-reason monotonicity controls. Keep repair evidence separate from the immutable RED output. Do not merge or push master. Rehearsal must consume the repaired, reviewed SHA rather than the parent SHA alone.
