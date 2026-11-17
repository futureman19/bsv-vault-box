# Bounded security repair — S-01 / S-02 / S-03

## Delivery
Base: `feature/launch-security-review@4ed20c7266e1ca7247e750d37d255896b467bcca`, superseding the initial evidence-only pin per parent comment. Delivery branch: `feature/launch-security-fix`. No production merge or deployment.

- S-01: replay returns INCONSISTENT on regressed INCLUDED stage, TRANSFERRED/OPENED state, changed historical open identity, cleared reconciliation flag or removed reasons. Legitimate retry progression remains accepted; preserved reasons appear in classification output. All classifications remain quarantined with mayResume false.
- S-02: transaction and block observations require valid shapes, exact block hash identity, safe-integer depth at least configured depth, and tx membership. Malformed/contradictory evidence throws into observation-unavailable holds, preventing an eligible BUILT retry on contradictory block evidence. Valid below-depth observations and absent membership retain existing false/non-included semantics.
- S-03: exact schema requires each expected field to be an own string property. Envelope, issuer policy and media hashes have prototype-adversary coverage.

No covenant, compiled artifact, package dependency, production website or protocol redesign.

## Evidence and verification
`python evidence/security-fix/run-gates.py red` reproduced original challenge failures and new controls before implementation. Original `evidence/security/challenges-red.txt` is untouched. Fresh RED mint run: 167 tests, 135 passed, 32 failed, zero skipped. Some new negative controls passed on the baseline; do not interpret every new case as individually RED. Original ten challenges again reproduced four passes/six failures.

`python evidence/security-fix/run-gates.py green` ran eight commands, all exit 0:
- VM: **111 passing** (pair, sponsored pair, native custody, launch records).
- Full established POSIX mint entrypoint: **167 passed, zero failed/skipped**, versus 122 baseline; 45 additional controls.
- Existing immutable security challenges: **10 passed**, zero failures.
- TypeScript typecheck; pair vectors; sponsor vectors.
- Saved proof replay: five serialized lifecycle transactions, five sponsor preparations, conflicting spend rejected. `liveChainChecked:false`.
- Recovery CLI: UNCERTAIN_SEND, quarantined true, mayResume false.

`commands-green.json` contains exact commands/working directories and corresponding output files. Native dependency install used locked `npm ci --ignore-scripts --no-audit --no-fund`; deprecation warnings occurred, no dependency-security clearance claimed. POSIX suite creates only public deterministic fixture keys in private temporary test directories via its existing runner; no production keys or live chain access. No bitcoind invocation.

`REVIEW.md` records isolated independent bounded code review approval, its attributed targeted verification and retained limitation. No implementation changes followed review. Source diff whitespace gate passed. Directory-local -text preserves captured evidence bytes. `sha256.json` hashes evidence and reviewed source as staged Git blobs, avoiding Windows CRLF ambiguity; manifest verifier compares actual committed blobs after commit. Self-generated hashes establish byte identity, not external recorder authenticity.

## Remaining boundaries / next step
This approves only the bounded repair for downstream integration, not launch. Rehearsal `t_35cdff45` must consume the repaired reviewed feature SHA from the completion handoff, not just the earlier green parent. Other rehearsal dependencies remain effective.

Missing block membership can permit a bounded retry of the exact existing BUILT/UNCERTAIN transaction; SUBMITTED/terminal observations do not rebroadcast. This is unchanged behavior, not replacement funding. Single-indexer trust and sequential, non-atomic payment/transfer settlement remain limitations. Recovery is read-only, not automatic fulfillment/refund/lock recovery. Reusable numbered seals remain UI-only; full-art admission/storage, arbitrary NFT support, miner/wallet/indexer compatibility and production readiness are not established.

Launch scope remains 201 one-of-one collectible designs (195 countries, five oceans, Moon), with detached signed authenticity record, not an extra certificate NFT. No art changed; USA v9 remains unapproved. Price, odds/allocation, storage/funding costs, legal terms, mainnet and release require separate user approval. No purchases, sale/mint activation, testnet/mainnet broadcast or master push occurred.
