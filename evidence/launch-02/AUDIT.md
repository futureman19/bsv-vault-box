# LAUNCH-02 — custody and launch architecture audit

## Verdict

**Audit complete; sale activation remains blocked.** The existing compiled custody prototypes enforce their narrow rules in the rerun VM tests. No unauthorized-withdrawal exploit was found in this bounded review. The approved launch package is **not yet implemented end to end**: existing one-item custody accepts tiny text inscriptions, the separate four-item experiment includes a certificate NFT and two objects that are outside current launch scope, and the funded service has a reproduced finality-observation defect plus deliberate manual-recovery limitations.

This is an internal bounded audit, not independent security certification. No node was started or contacted, no real signing key loaded or generated, no chain transaction broadcast, no funds moved, and no production file changed. Tests used existing public deterministic fixture keys, including temporary POSIX fixture files created and removed by the established unit runner. No artwork was changed or visually approved.

## Exact sources and branch separation

| Surface | Pinned commit | Status in this audit |
|---|---|---|
| `origin/master` | `606147d6a1521adf635d79a70785ba7f82dbbf77` | Feature branch baseline; public gallery/site left unchanged |
| `origin/feature/four-item-custody-proof` | `ff5d78f1e0d486af5c882c184fc08049996ebdc8` | Extracted to `.audit-sources/bundle`; contains four-item VM and sponsored node evidence |
| `origin/codex/mint-funded-adapter` | `b11a382f197925fd011e8336575f8c90d7740107` | Extracted to `.audit-sources/funded`; contains latest funded runner, adapters and unit suites |

These are **different branches**, not one integrated launch release. Files cited below refer to the named snapshot. Reproduction scripts fetch nothing, extract exact Git objects, and operate inside this task's worktree. Dependencies were installed from each pinned `vault/package-lock.json` with `npm ci --ignore-scripts --no-audit --no-fund`; package deprecation warnings occurred. No dependency-security clearance is claimed. Compiled artifacts were executed and fingerprinted, **not rebuilt by a compiler in this audit**. TypeScript typecheck passed.

Current docs read include BOX-MINT-1, BOX-ORDINAL-PAIR-1, BOX-ORDINAL-SPONSOR-1, BOX-ORDINAL-FULLNODE-VALIDATION, the two BOX-FOUR-ORDINAL drafts, and mint README/SALE-README plus actual funded implementation. Some draft prose predates subsequent evidence: e.g. sponsor draft says no native-node execution, while the full-node report supplies it. Do not turn either historical text into present production approval. The old full-node report also discloses a historical isolation incident; this audit did not run that harness or touch its nodes.

## What the code actually supports

### Single-ordinal pair — closest existing custody primitive to launch

`vault/src/contracts/ordinalPair.ts:5–7,18–85`, `vault/src/ordinal-pair.js:117–135`:

* One independently existing **one-satoshi**, canonical P2PKH-before-envelope `text/plain` inscription, a single direct content push of **1–75 bytes**, and one separately created one-satoshi EMPTY control.
* Immutable origin is the original outpoint. Deposit inputs are original NFT then control; subsequent principal inputs/outputs are parent indices 0/1 in that order. Both continuation outputs are identical compiled covenant scripts, but identity is **positional sat ancestry**, not a copied label or envelope.
* Phases: EMPTY(0) → PACKED(1) → SEALED(2) → OPENED(3) → withdrawal to two owner P2PKH outputs. Sealed transfer changes both owners and leaves phase sealed. There is no EMPTY reset, numbered seal, or covenant surviving withdrawal.
* Both principals preserve one sat. Optional sponsor input is third; optional sponsor change is output 2. Owner and sponsor covenant authorization require SIGHASH_ALL|FORKID (`41`), and the funding input independently requires its P2PKH signature.
* The funding parent must be one-input/one-output index zero, scriptSig at most 108 bytes, precisely parsed and hashed. Positive custody fee is capped at 10,000 sats. Sponsor-only change is enforced. Arbitrary wallet funding and direct reuse of service change are not supported; preparation incurs a separate fee.
* Admission/replay authenticates the original inscription and initial code/owner/anchor; consensus supplies actual UTXO existence and spentness. A hash-only parent witness is not arbitrary sibling-script introspection. Copied-code parents can have VM-valid standalone spends but fail anchored provenance.

### Four-item construction — genuine experiment, not approved launch package

`bundle/vault/src/contracts/fourOrdinalSponsored.ts:18–78` commits exactly four origins, five principal sats and six inputs including sponsorship. Ordered assets are collectible, **certificate NFT**, object one, object two, control. Its canonical detached certificate names three other origins; a fourth inscription stores the envelope digest. The client requires an externally chosen issuer policy; Script does not verify provenance. The older unsponsored `four-ordinal.js:104–133` has an anchored verifier; its five-input verifier must not be reused for six-input sponsored evidence.

Historical node bytes plus current offline replay support this fixed tiny-text construction. They do **not** support arbitrary artwork, interchangeable bundle lengths, the approved signed-record-only certificate, or reuse. Do not merge the four-item protocol into launch merely because its tests pass.

### Mint/service

The funded branch implements bounded funding preparation, append/fsync journals, exact-UTXO checks, reservations, watcher, persisted transfer bytes/retry budget, buyer-offline signing, and an owner-gated runner. Unit coverage exercises mainnet POST behavior only through mocks. Payment then transfer is **sequential fulfillment**, not atomic payment-versus-delivery. The service has hot authority over unsold inventory, not sold genuine outputs after confirmation. Reorg/finality and trusted indexer assumptions remain relevant.

## Threat model

| Actor/boundary | Attack or failure | Existing defense / remaining exposure |
|---|---|---|
| Former owner or copied seller key | Open/withdraw after transfer; competing sale | New actual outputs require new owner; old-owner VM cases pass. Pre-confirmation conflicts and reorgs require finality handling. |
| Current owner while sealed | Withdraw without opening; replace one item | Phase checks and exact ordered prevouts/outputs reject it. Owner may legitimately open; sealing is not secrecy. |
| Counterfeit issuer or evidence supplier | Clone code, origin label, certificate, or trust key | Full genesis-anchored admission/replay and external issuer policy required. Current VM validity alone is insufficient. |
| Sponsor/caller | Divert principal/change, fake funding amount, fee overflow, omit auth | Authenticated bounded parent and full-output commitments; principal, fee and signature adversarial cases rerun. |
| Local service crash/storage | Dispense twice, partial journal, lost send response | Persist/fsync before dispense/send, exclusive lock, byte-stable retries, RESERVING quarantine. Availability/recovery remains manual. |
| Indexer or reorg | False confirmation/unspentness, disappeared payment, orphaned transfer | Raw-byte/output checks and block membership reduce inconsistency, but single-indexer data is trusted; F-01 misses later observations. |
| Operator/inventory configuration | Wrong or counterfeit origins offered as genuine launch collectible | Local inventory is trusted; collection roster and issuer binding must be checked before distribution. No proof of all 201 issuance slots exists. |
| Storage/provider loss | Missing art/model or detached signed record | Hashes establish integrity, not availability; no storage purchasing or durability guarantee in scope. |

Assumptions: secp256k1/hash security, correct SDK/compiled Script behavior, honest actual UTXO lookup at consensus, trusted local operator journal directory and external issuer policy. Audit did not establish arbitrary malicious-block rejection, SPV/header verification, miner economics, wallet/indexer recognition, or secure production key operations.

## Risk-ranked findings and reproducible gaps

### F-01 — HIGH: transfer completion and terminal status miss finality loss

**Confirmed implementation defect**, not demonstrated theft. `funded/mint/transfer.js:192–196` sets TRANSFERRED on transfer inclusion before checking payment; payment revalidation is at 205 on the broadcast path. The terminal return at 118 prevents subsequent inclusion checks. `watcher.js:48–53` suppresses below-depth events, so a missing payment does not repair this.

Executable: `node evidence/launch-02/reproduce-findings.js` after setup. The white-box persisted-SUBMITTED fixture calls real run/guard/included methods with saved serialized transfer bytes, mocked RPC and a payment reader reporting zero funds/depth. Constructor is deliberately bypassed to avoid any key loading. Observed: TRANSFERRED with **zero payment reads**; simulated later inclusion loss is ignored, total inclusion reads remains one. This is a control-flow repro, **not a live reorg**.

Fix: independently persist ownership observation and payment/finality health. Preserve TRANSFERRED/OPENED ownership history when a payment disappears or excess payment arrives; flag durable reconciliation rather than relist or revoke ownership. Recheck inclusion for monitored completed sales. Never allocate replacement funding or reverse a confirmed transfer automatically.

### F-02 — HIGH launch blocker: approved package/art admission and signed record are not integrated

**Explicit scope gap**, not a covenant bypass. Pair verifier rejects the saved genuine `model/gltf-binary` example as `unsupported inscription grammar` (reproduced). Four-item fixture solves a different package: extra certificate NFT plus two objects. Pair path has no launch certificate/201-roster authenticity policy.

The supported launch construction today is therefore only a **single tiny-text test collectible in a one-seal pair**, not the full saleable collection. A single ordinal carrying a digest can represent a deliberately specified metadata commitment, but it does not store the model, prove storage availability, or become broad artwork admission. Recommended bounded child uses this narrow commitment form and detached signed record in local proof only; any choice to inscribe full artwork or pay for storage remains separately authorized.

### F-03 — HIGH operational launch blocker: no exercised paid-run recovery workflow

**Documented fail-closed limitation**, not duplicate issuance. `funded/mint/funded-runner.js:128–131` refuses any pre-existing evidence directory, `492–497` explicitly disclaims automatic resume/replacement/refund. `transfer.js:140–146` records RESERVING before dispense; funding identity appears only at BUILT (`178–188`). The established unit tests verify ambiguous reservation does not dispense again, truncated records fail closed, and short writes prevent broadcast. This audit reran those tests successfully.

A paid crash may require manual cross-journal reconciliation and strand fulfillment. Do not weaken the lock or RESERVING guard. Child must provide a read-only recovery classification and executable interruption tests before any later decision to authorize a resumable runner.

### F-04 — MEDIUM product-claim blocker: reusable Box identity/numbered seals unimplemented

`ordinalPair.ts:64–84` has no reseal/repack path and withdrawal releases the control to P2PKH. Repro freshly signs an OPENED → SEAL transaction; VM rejects with `SCRIPT_ERR_NUMEQUALVERIFY`. Four-item contracts likewise have no reuse. Keep reusable UI explicitly simulated. No new reuse protocol is authorized by this audit's implementation plan.

### F-05 — MEDIUM security assumption: single-indexer finality, non-atomic payment

`funded/mint/watcher.js:103–150` checks raw txid/output details and returned block membership but does not validate a header chain/Merkle proof. A consistently false indexer response can pass those checks. This is documented trust, not evidence of an actual compromise. Payment followed by transfer exposes a settlement interval; F-01 hardening does not make it atomic. Keep independent public-chain/indexer/miner validation and a production settlement policy as release holds, not implicit child work.

## Actual execution and evidence

All files below are card-local under `evidence/launch-02/`.

| Gate | Actual result |
|---|---|
| `run-audit.py`: original pair, sponsor, native and both four-item VM suites | **156 passing**, exit 0 (`vm-tests.txt`) |
| Pair, sponsored-pair, four-item golden vectors | All exit 0, exact comparisons unchanged (`*-vectors.txt`) |
| TypeScript `tsc --noEmit` | Exit 0 (`typecheck.txt`) |
| Existing stored node replay | **16 accepted, 20 rejected, 8500 sats** recomputed historical fees, exit 0 (`node-evidence-replay.txt`) |
| Independent raw RPC-journal cross-check | 16 successful submissions matched bytes + block membership; 20 mandatory Script failures; **240 before/after input UTXO value/script checks**; five final one-sat outputs (`captured-node-crosscheck.txt`) |
| Funded mint suite via supplied WSL/POSIX runner | **90 passed, 0 failed, 0 skipped**, exit 0 (`mint-tests.txt`) |
| Focused finding reproduction | Reuse rejection, real model grammar rejection, F-01 terminal/finality defect all observed (`reproduce-findings.txt`) |

The node replay is a **new offline check of historical captured execution**, not a new full-node run. Its fee total concerns the captured four-item local-regtest experiment only, not a launch quote. Capture authenticity is not established by a self-generated hash manifest. Two installed SDK copies emitted a duplicate-BSV warning in the mixed-snapshot repro; all assertions completed. No compiler run, wallet compatibility run, UI/browser/visual QA, actual reorg, full-art inscription, mainnet canary, sale, or independent security audit was performed.

## Reproduce without live services

From this audit feature branch at the repository root:

```sh
python evidence/launch-02/prepare-audit.py
(cd .audit-sources/bundle/vault && npm ci --ignore-scripts --no-audit --no-fund)
(cd .audit-sources/funded/vault && npm ci --ignore-scripts --no-audit --no-fund)
python evidence/launch-02/run-audit.py
node .audit-sources/funded/mint/test/run.js
node evidence/launch-02/reproduce-findings.js
node evidence/launch-02/check-captured-node.js
```

On Windows the mint runner invokes WSL login-shell Node and creates/removes its fixture custody files on the Linux filesystem. Only these offline/unit entrypoints are allowed here; do not substitute deploy, default npm test, funded runner, node harness, key utility or live preflight commands.

## Bounded implementation handoff

See `IMPLEMENTATION-ACCEPTANCE.md` for the fixed next milestone on existing child `t_4bd2681c`. Completion of this audit releases that child; it does not approve launch or certify art. No additional task was created.
