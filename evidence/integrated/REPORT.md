# Integrated continuous wallet and paid delivery — local milestone

## Delivered

The existing continuous browser page now has a runnable paid-fixture mode using the parent **real BRC-100 adapter contract**, browser-side SDK signatures, existing SaleStore allocation, PaymentWatcher, durable Delivery coordinator and existing signed custody verifier. One fixed Iceland candidate retains its manifest/metadata/origin, derived buyer key and identity enrollment through Reserve → Pack → Seal → synthetic payment observation → Transfer → Open → Withdraw.

This is **not a real-wallet purchase, production readiness, random sale, atomic settlement or chain inclusion**. No production sending exists. Source/run instructions: **`launch/continuous/PAID.md`**. Exact fixture recovery configuration: `launch/continuous/paid-config.json`.

## Exact source basis

- Delivery parent: `d894303ece772cdb7674ab8208201cacd794baad`, branch `feature/durable-paid-delivery`.
- Wallet parent: `7685b0e085619dc6784f8a7c297cb2b2480ceb48`, branch `feature/authoritative-wallet-transport`.
- Both remote tips were fetched, merged and read back unchanged before publication. Merge baseline: `b3dde1e`.
- Read exact final-QA report at `db4760ddcb33108da563b1df84a7e308205de3ec`, continuous report at `d02b279d8ea41871c4f4af6760576a3926617fb6`, and collection decisions/independent report at `f0a54d9b3e80338fbe34c869987a45d6d23ae25c`. Those reports and the complete collection tree remain byte-identical in Git.
- Work is confined to assigned worktree `t_31e507ba`, branch `feature/integrated-wallet-paid-demo`. No sibling worktree, production `docs/` or old evidence/assets were edited. Historical art pins were not promoted to later candidates.

## Actual execution

| Gate | Result | Retained evidence |
|---|---|---|
| New integrated flow/security/restart/HTTP tests | **11 pass, zero failed/skipped** | `final-tests.txt` |
| Parent continuous + wallet adversarial suites | **54 pass** (22 continuous, 32 wallet) | `parents-regression.txt` |
| POSIX mint/payment/delivery/pool/recovery | **187 pass, zero skipped** | `mint-posix.txt` |
| Existing independent security challenges | **10 pass** | `security-regression.txt` |
| Allocation/restart/receipt/hold regressions | **19 pass** | `allocation.txt` |
| Compiled pair/sponsored/native/detached-record Script suites | **111 pass** | `vm.txt` |
| TypeScript noEmit | exit 0 | `typecheck.txt` |
| Fresh CLI full pipeline and separate-process restart | WITHDRAWN; five verified transitions | `run-01.txt`, `restart-01.txt`, `run-01/` |
| Read-only saved-byte VM replay | CLI + actual desktop/mobile browser exports pass | `replay-cli.txt`, `replay-browser-desktop.txt`, `replay-browser-mobile.txt` |
| Actual isolated Edge continuous page | desktop 1365×1000, mobile 390×844, ambiguous-send flow | `browser-02/report.json`, screenshots and downloads |
| Read-only delivery inspection | exact persisted binding/bytes; no DB changes | `readonly-delivery.json`, `verification.json` |

Browser-02 is the final capture after transport-sharing and testnet observer-domain corrections. Browser-01 remains retained. Both complete desktop/mobile flows execute buyer BRC signatures inside the browser through SDK `ProtoWallet` and `WalletTransport`; server receives/verifies the original persisted request responses and assembles actual covenant scripts. This is not the parent's standalone P2PKH smoke test or a replay-only mock. Each successful journey has five verified buyer requests: reservation plus two inputs each for Open and Withdraw. Seller/sponsor construction remains a separately labeled public deterministic service fixture.

Browser negative cases reject malformed signatures, provider rejection, wrong identity/buyer, wrong network and disconnect before allocation. Ambiguous paid delivery retains the exact signed bytes/funding across reload without promoting ownership. No external requests or uncaught page errors occurred. Expected HTTP 409 console errors from deliberate negative tests are retained, not represented as a clean-console run. Owned servers were terminated and their ports checked closed. Browser capture directories retain SaleStore crash locks from forced teardown; use exported JSON for read-only replay.

The actual mobile completion image was visually inspected: no obvious clipping or overlap, but small hexadecimal evidence and long disclosures remain less comfortable on a phone. Existing prominent withdrawal wording is qualified by the adjacent fixture/no-chain text; this is not a public production UX acceptance or a physical-phone/Safari test. No optional visual redesign was undertaken.

## What was joined and protected

- Existing `Engine` remains the page's lifecycle state machine; legacy mode tests still pass. It now accepts a separately supplied enrolled policy and independently verifies BRC authorization records alongside the legacy service-signed responses.
- `ordinal-pair.transition` gained an optional owner-signature callback, allowing public-key-only construction and real external input signatures rather than requiring the buyer private key. Covenant/output/ordinal enforcement is unchanged.
- Buyer identity differs from BRC-42 derived custody key. Network domain is consistently **testnet** for derivation, payment-address and observer policy. The inherited **offline-fixture** label is separately retained as execution realm and local-receipt type, never testnet inclusion.
- Durable exact requests/hashes precede browser handoff. Rejected IDs stay consumed; pending authorization after actual child exit 75 blocks progress after operator handling of the existing stale SaleStore lock. No automatic lock reclaim, hold clear or replacement order is provided.
- SaleStore fixes one design's sealed inventory ID/address to the signed buyer reservation. The existing Delivery ledger independently binds reservation, buyer, design, metadata, original outpoint and sponsor parent. Its watcher callback is a trigger, not receipt truth; current cumulative synthetic evidence is reread before sending and later buyer actions.
- Delivery's exact prepared Transfer/local receipt are projected into the continuous journal without a second send. Payment loss preserves historical transfer but blocks subsequent signing. Ambiguity, reconciliation loss, binding mismatch, malicious response, duplicate payment, prepared-only restart and abrupt authorization crash are exercised. Reconciled synthetic inclusion stays `REHEARSED_CONFIRMED` and does not clear ambiguity or relist anything.
- Serialized VM replay proves the same original ordinal/manifest and derived buyer through five transitions. One inner NFT and detached signed record remain distinct. No full-art custody or reusable-seal support was added.

## RED/GREEN record and limitations

`constructor-red.txt` records a public-key-only owner failing because construction required its private key; the callback correction passes actual Script. `reservation-red.txt` and `paid-red.txt` record missing integration entrypoints, not behavioral security REDs. `server-red.txt` records absent paid-mode page behavior. `transport-red.txt` records the real failure to share ambiguous transport behavior with the existing Pack action. `network-red.txt` records the initially regtest-labeled observer policy; final composition consistently uses the testnet derivation/address/observer domain with an explicitly separate offline execution realm. Other security cases are regression assertions, not individually observed RED.

Dependencies emitted inherited deprecation warnings and Node reports experimental SQLite. No dependency security audit, fresh node consensus, live input unspentness/depth, funded ancestry, commercial miner/indexer compatibility, actual extension signature, trusted production issuer, production funding/fees, external checkpoints, physical power-loss certification or coherent rollback/rewrite protection is established. Deterministic preview construction on restart regenerates identical public fixture Pack/Seal/funding bytes for pin checks; it is not a new allocation or actual UTXO creation. Random paid allocation/fairness remains unimplemented and unapproved.

## Fresh extension observation and exact external gate

`extension-observation.json` records a **typeof-only** read of the existing Yours documentation tab: CWI object and expected method names visible; `yours`/`panda` absent. **Zero provider methods, permission approvals, identity reads, account/network reads or signatures were invoked in that attached browser.** It proves neither extension authenticity/version nor intended local-origin compatibility. Isolated Edge signing uses public fixtures only.

Authoritative provider basis remains the parent's pinned Yours source `ccdd6f480906c06cfa1481ad3a66f4abc8a5cc9e` and source/API excerpts. Only BRC-100 direct-hash signatures and signed request envelopes are used; no arbitrary-raw `signAction` assumption or broadcast-capable action.

**One real-wallet gate remains:** the owner must explicitly authorize and personally initiate an isolated unfunded no-send session on the intended app origin, select account/testnet, approve identity plus `[1,'boxsv custody']` / `testnet:owner:v1` / `self` derived-key access, independently enroll/pin those keys, and approve the exact synthetic transaction-hash and response-envelope signatures. The installed provider must support `hashToDirectlySign`; otherwise retain its exact error and stop. This task does not open or approve that gate, and it is not required for the delivered runnable fixture milestone.

## Recovery verification

The continuation reran all 11 integrated/security tests and read-only five-transition VM replay successfully (`recovery-tests.txt`, `recovery-replay.txt`). The interrupted evidence verifier had incorrectly parsed merged Node warning/JSON output as pure JSON; it now accepts only the two known SQLite warning lines before strict JSON parsing and checks each serialized VM result. Original logs were not rewritten. `verification.json` records newline-only checkout differences for inherited `vault/src/launch-record.js` and `mint/delivery.js`, with both executed and Git hashes; neither inherited file was changed. Evidence hashes are checked against staged Git blobs before publication.

## Preserved holds and handoff

All 201 one-of-ones, 73 historical art holds, one-inner-NFT/detached-record structure, full-art/storage/sub-5MB model-preview limits, issuer/key-custody, rights/legal/economics/odds/funding and owner/release holds remain. No funds, broadcasts, live nodes, production keys, purchases, refunds, replacement funding, paid generation, master push, deployment or sale activation occurred.

Hotspot: `launch/continuous/engine.js` composes explicit delivery funding pins with external wallet authorization. Existing review child `t_95a9e259` owns the independent read-only verdict; correction child `t_eb1741f9` owns any bounded review-blocker pass. No tasks were spawned and no independent review is claimed by this implementation report.

**Recommended next step:** run the pre-created read-only review against this exact feature commit and retained evidence; do not activate a sale or treat fixture success as launch approval.
