# Durable reservation-to-custody delivery — implementation handoff

## Delivered

`mint/delivery.js` provides a shared SQLite reservation/payment/delivery ledger around the existing signed custody workflow. It consumes the actual `SaleStore.reserve` shape, validates the exact selected design/metadata/origin and buyer, receives `PaymentWatcher` triggers, freshly verifies cumulative payment evidence, requests **Transfer** through the existing authenticated wallet interface, and replays the serialized transaction through the existing custody verifier. The new funding-pin option in `launch/continuous/engine.js` removes reliance on fixture-only fee/root assumptions for that verification boundary while preserving existing fixture behavior.

The runnable example uses **Japan**, not the earlier hardcoded Iceland selection; Morocco is also tested. One inner NFT and the detached signed authenticity record remain the package boundary. This is sequential fulfillment, not atomic settlement. The 201 one-of-ones, 73 art holds, full-art/storage/preview-size limits and all owner/release holds are unchanged.

**Real sends remain disabled.** The default mode rejects execution; only explicit offline rehearsal can use the supplied no-network public-fixture adapter. No production transport is enabled, and no economics are approved by config labels. No deployment/master push, funds, broadcasts, live nodes, production keys, wallet approvals, purchases or paid generation occurred.

## Source pins and isolation

Implementation base: `d02b279d8ea41871c4f4af6760576a3926617fb6`.
Read exact prior reports at `db4760ddcb33108da563b1df84a7e308205de3ec` (final QA), `d02b279` (continuous implementation), and `f0a54d9b3e80338fbe34c869987a45d6d23ae25c` (collection decisions/ledger reference). This branch does not promote later art candidates or overwrite old evidence. Work was confined to assigned worktree `t_8cbaabe5` on `feature/durable-paid-delivery`; production and sibling worktrees were untouched.

Hotspot for downstream integration: **launch/continuous/engine.js** changes `requestFor` to use `policy.network`, and adds optional explicit funding pins to `verifyResponse`. Merge any wallet-lane verifier changes deliberately. New coordinator, scripts, tests and documentation otherwise live under `mint/`; evidence is new `evidence/delivery/` only.

## Reproduce

See `mint/DELIVERY.md` for complete API shapes, migration/configuration and recovery semantics.

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
node mint/scripts/delivery-rehearsal.js mint/.delivery-local japan
node mint/scripts/delivery-inspect.js mint/.delivery-local/delivery.sqlite box-1 mint/.delivery-local/config.json
node --test mint/test/delivery.test.js
node mint/test/run.js
```

The destination must be fresh. `delivery-inspect` opens SQLite read-only, verifies exact bindings/signed bytes and reports holds without keys, network activity or state changes. Do not silently create a new DB for restart. SQLite schema version is 1; incompatible schema or changed issuer/network/depth/terms pins refuse startup. Use one shared registry across invoices, not per-invoice databases. Never run the legacy `TransferWorker` for enrolled records. No destructive migration of old journals was attempted.

## Executed verification

| Gate | Actual result | Evidence |
|---|---|---|
| Complete POSIX mint suite including 20 new delivery cases | **187 passed, 0 failed, 0 skipped** | `mint-final.txt` |
| Existing continuous engine/security/server/process suites | **22 passed** | `continuous.txt` |
| Existing allocation/restart/hold tests | **19 passed** | `allocation.txt` |
| Existing pair/sponsored/native/detached-record Script suites | **111 passed** | `vm.txt` |
| Retained independent security challenges | **10 passed** | `security.txt` |
| TypeScript noEmit | exit 0 | `typecheck.txt` |
| Fresh SaleStore → watcher → selected Japan signed custody rehearsal | `LOCAL_ACCEPTED`, one wallet request, one local transport call, zero real broadcasts | `rehearsal.txt`, `run-japan/` |
| New-process operator recovery | exact saved binding/bytes and local receipt recovered, no chain-inclusion claim | `recovery-final.json` |

New cases cover duplicate/replayed observations, partial/insufficient confirmations, immutable buyer/design/source/address/economics conflicts, globally shared receipt ownership, exact funding retention, expiry/excess, post-signing payment loss, terminal finality loss, genuine process exit after claim/preparation/attempt, two simultaneous DB connections, issuer pin changes, upstream holds, malformed signatures/metadata, inclusion reconciliation and subsequent loss, read-only byte preservation, and receipt-index tampering. Confirmed synthetic evidence remains `REHEARSED_CONFIRMED`, never a real chain receipt; ambiguous holds remain even after exact inclusion is later observed.

The runner timeout was increased from 60 to 240 seconds to accommodate signed-byte replay and three child-process crash cases. It uses the existing POSIX key/pool test entrypoint and starts no node. Native Windows also ran the initial 18-case expanded suite and the final two targeted hold/registry cases. Native Windows permissions are not claimed as POSIX key-custody evidence.

## RED/GREEN history and limits

`red.txt` captures the missing delivery entrypoint. `trust-red.txt` records a real failure to require the external issuer pin again on restart; fixed by persisting/comparing the pin and checking it during import/replay. `hold-registry-red.txt` records two real failures: dropping upstream custody holds during import, and failure to detect deleted historical receipt mappings; both fixed and rerun GREEN. Other negative cases were added as regression assertions, not individually observed RED. Earlier output files are retained, not overwritten with final results.

Dependency installation emitted inherited deprecation warnings; no dependency-security audit is claimed. Node's SQLite experimental warning remains. The checksum/event chain identifies bytes and accidental corruption, not recorder authenticity or resistance to coherent database rollback/rewrite. Actual child-process crashes are tested, not physical power loss. No fresh full-node, miner, real-wallet or browser acceptance is claimed by this backend task; the existing downstream integration/QA cards own that work.

## Precise remaining gates

1. **Downstream integration:** merge wallet adapter and this coordinator into the continuous browser flow using the same buyer/design/origin/source tuple. Backend API and runnable CLI are delivered; browser wiring and real extension compatibility are not claimed here.
2. **Live payment observer:** supply cumulative historical receipts with stable finality; the existing HTTP UTXO-balance reader alone cannot safely observe receipts after treasury spending. Watcher callback deduplication is not terminal reconciliation. Schedule independent payment and exact delivery evidence reads.
3. **Live send/funding:** no live transport is enabled. Actual input unspentness/depth, funded ancestry, pre-reserved sponsor pins, signer/issuer custody, external checkpoints, production monitoring and operator recovery need authorized integration. No replacement funding is allocated by this worker.
4. **Owner decisions:** price/currency/fee budgets, thresholds/expiry/refunds, randomness/buyer order/reserves/odds/reveal/Moon disclosure, rights/legal, art approval, storage/retention and exact release/funding authority remain unset/unapproved. The explicit fixture constants are not decisions.
5. **Claims:** no certificate/accessory NFT, full-art inscription/permanent hosting, arbitrary assets, reusable-seal covenant or production readiness is added. Reconciliation records evidence but provides no automatic refund, resend, relist, release or hold-clear command.

**Recommended next step:** the pre-created integration child should consume this branch plus the wallet-lane handoff, retaining the disabled real-send gate and the named external limitations. No new tasks were spawned.
