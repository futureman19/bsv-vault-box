# BoxSV launch rehearsal — executed, launch remains HOLD

## Verdict

Bounded **layered rehearsal PASS with integration holds**. This is NOT a passing continuous production mint. Allocation, generic-node custody, signed metadata and browser demo are separate evidence layers. The existing implementation does not bind them into one buyer/design/origin transaction flow; no such success is claimed. Independent read-only file/image review passed this bounded scope (`REVIEW.md`, deleg_9e60f944). No production deployment, master push, paid generation, testnet/mainnet broadcast, real funds, production key creation/loading or sale activation.

## Exact integrated candidates

Integration base c03e2925d01897cd5351383833d959b7a29ba1ad, branch `feature/launch-rehearsal`:
- allocation: edcdd5954439ba3b183b157bd52777a17b722b41
- security repair: 10acb9dfa127862b20172f4ce12f1dee32901b88
- collection: f0a54d9b3e80338fbe34c869987a45d6d23ae25c
- web/claw: e5003341b4d503ac1d04f0a852e0570939e68bac

`verify-integration.py` confirms ancestry and unchanged relevant production trees against these pins; ledger SHA256 ea68d8c34af0e4158fd4f6b9c5ef77727f34ca5c34d66c317303ecf7b21ee796. Only existing test change is an optional output-directory environment variable, preserving parent evidence. New harnesses/evidence are card-local. No art altered or approved.

## Freshly executed

| Gate | Result | Evidence |
|---|---|---|
| Offline allocation / restart, idempotence, tamper and holds | 19 pass | allocation.txt |
| Collection packaging regression | 12 pass | collection-corrected.txt |
| Compiled Script VM suites | 111 pass | vm.txt |
| POSIX mint, recovery/finality/adapters/failure injections | 167 pass, zero skips | mint-posix.txt |
| Retained security challenges S-01/02/03 | 10 pass | security.txt |
| TypeScript | pass | typecheck.txt |
| Signed Iceland fixture saved-byte replay | 5 lifecycle + 5 preparations, conflict rejected | proof.txt |
| Claw unit | 4 pass | claw-unit.txt |
| Served gallery/Box browser suite | 10 grouped checks pass | web/report.json, web.txt |
| Authored-claw browser suite | 13 pass, no uncaught errors | claw/report.json |
| Browser wallet identity mocks | 4 pass: success/reject/empty/absent | wallet.json |
| Fresh official-node regtest lifecycle | 5 custody transitions, old owner rejected | regtest/result.json |
| Independent raw node capture replay | pass | regtest-audit.json |
| Source/artifact/ledger pins and secret scan | pass | integration.json |

`commands.json` intentionally retains the first collection command's exit 2 (wrong filename test_consolidate.py); corrected `python launch/collection/test_consolidation.py` passed. It is not a product failure or a hidden all-green initial run. An initial secret-scan expression matched its own PEM-pattern source; anchoring real PEM/config headers corrected this harness false positive. No key leak was found. The launcher script now names the correct test. Do not rerun into frozen evidence; use a new output root.

### Buyer journey layers and fail-closed boundaries

1. Real CLI invocations, with a new process for each step, initialized a fresh SQLite fixture and applied reservation, fictional receipt, build plan, simulated inclusion, open, withdrawal; inspect/audit then passed. Result: **Uganda, WITHDRAWN, 7 events, 200 available**. 100 units are fictional, not satoshis or approved price. `operator-*.json` / `operator.sqlite` retain all outputs. Plan has `serializedTransaction:null`, `custodyVerifiedByThisSimulation:false`, `DETACHED-UNSIGNED-NOT-NFT`, `mayBroadcast:false` and `launchReady:false`. Automatic mint/real-origin binding is not implemented.
2. Separate unchanged regtest sale harness exercised actual inscription + outer Box, pack, seal, loopback reservation, local payment depth, transfer, old-owner failure, buyer open and withdrawal. This is a **generic text ordinal**, not issuance of the allocated Uganda art. Node service state ends OPENED because its API has no withdrawal state; actual transaction history reaches withdrawal. Do not relabel the API state.
3. Separate signed Iceland metadata commitment proof replays in VM with externally chosen public-fixture issuer policy. It is not the generic regtest asset, not full-art issuance and not a separate certificate NFT.
4. Actual browser pages exercise simulated seal inspection/open/transfer/reuse, resets and input isolation. Wallet mocks only authenticate/read public identity. No extension signing, payment or custody integration is claimed. Unknown signing/payment methods are forbidden in the mock. Missing/rejected identities allow only explicit demo fallback.

### Node safety and evidence

Inspected unchanged `mint/scripts/regtest-sale.js`, `regtest-node.js`, and `vault/scripts/bitcoind-guard.sh` before running. Fresh POSIX datadir, explicit regtest, wallet disabled, connect/listen/discovery disabled, cookie-only loopback RPC. Version queried through owned node getnetworkinfo, executable hashed, no bare version/help invocation. Public deterministic fixture scalar keys only, ephemeral fixture files removed by harness; no owner keys or secrets in packet. Archive download is software retrieval, not public-chain traffic.

Saved exact RPC submissions, mined block membership, final UTXOs, config, binary provenance and clean shutdown. `audit-regtest.js` reparses saved bytes and independently verifies five custody transactions and six sponsor preparations in VM; checks raw submission equality and mined membership, mandatory Script rejection and unspent principals before/after the former-owner attempt. Captured final outputs 0 and 1 are one satoshi each to buyer script; origin cba0434bda8c869bef408613a48541d3b2ac543dcc43d0f72ea48b48c31e1d21_0, final txid 308d87e060fa716abc7451c2b027fb336efdb0279da7f15d82b72388514728eb. Positional ancestry, not node-native NFT recognition.

Fees: **2,500 local custody sats + 3,000 sponsor preparation sats**, excluding inscription/funding/payment setup. Invalid attempt pays no mined fee; pool dispensed amount is not fees. Node shutdown exit 0; subsequent process inventory found no bitcoind process. Only the owned node was stopped. This proves local acceptance under recorded policy, not commercial miner/indexer/wallet compatibility. Final UTXOs are captured historical regtest state, not current public-chain unspentness. Controlled crash/finality simulations are not real reorg/power-loss certification.

Compiled ordinalPair artifact file SHA256 **36e436e97844dfcf60c912072447c5b1e03bcd0c5490f0e07dded3c81cedaccd**, source SHA256 **a8d2f5252b02509cb4f35001942432eb8aab847ca1befdb0c71779be4050d660**. Matches signed proof and current source; existing bytecode exercised without compiler rebuild. No new compiler reproducibility claim.

## Visual limits and preserved decisions

Independent reviewer inspected six actual fresh images. Mobile controls/disclosures readable, but dimmed game text interferes behind the prize overlay. `claw/desktop-reveal.png` was overwritten by later race-phase capture and is NOT settled desktop prize evidence. Full-page blank gallery areas can reflect lazy capture timing; these captures do not prove all images decoded. Fresh web suite tests recovery/lazy loading; parent all-402 decode evidence remains historical, not rerun here. No physical-phone/Safari/deployed-site acceptance. Small promotional captions remain; illustration may differ from interactive model.

All **201 one-of-ones: 195 countries, five oceans, Moon** remain equal edition scarcity. **73 art/package holds, 128 limited candidates, zero final approvals**. Exact collection ledger preserved, not a new full 201-model visual inspection. USA v9 remains unapproved; wrapped-star continuation unresolved. Historical archive discrepancies (Iceland/Morocco/Rwanda) and inner-inventory holds (Iceland/Morocco/Namibia/New Zealand/Paraguay) remain. Outer package tests do not clear them. Reusable numbered seals remain UI-only; covenant refuses opened-to-seal reuse.

## Handoff and unresolved launch blockers

Existing OPS child `t_b85cf2b2` is next: use this exact feature ref and packet for fixture backup/restore/runbook work. It must preserve these distinctions, not present a working integrated sale. Real allocation->NFT binding, real issuer/origins, full-art admission/storage, wallet transaction signing, durable external checkpoints/automatic recovery, miner/indexer compatibility and independent security certification remain unresolved. Price/odds/allocation/reveal/reserves/refunds/legal terms, all art approvals, funding/storage costs, mainnet and release require separate authorization. Single-indexer and sequential payment/transfer limits remain; no atomic settlement claim.

`sha256.json` identifies packet bytes, not recorder authenticity. Deliverable archive contains only this card's evidence and scripts, not full 201 model payloads or dependencies. Reproduction requires the exact integrated feature checkout. No other assigned card is completed by this handoff.
