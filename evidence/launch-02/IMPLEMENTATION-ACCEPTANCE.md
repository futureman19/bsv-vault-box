# CONTRACTS child — fixed acceptance milestone

Applies to existing task **t_4bd2681c**, following audit **t_52ee0956**. Deliver one local-only launch-construction proof plus finality/recovery hardening; stop when the gates below pass. Do not start a new protocol/reuse, sale allocation or production program.

## Inputs and integration ownership

Read `AUDIT.md` and raw logs, not merely the parent's completion message. Audit baseline master: `606147d6a1521adf635d79a70785ba7f82dbbf77`; funded machinery: `b11a382f197925fd011e8336575f8c90d7740107`; separate four-item evidence: `ff5d78f1e0d486af5c882c184fc08049996ebdc8`. Fetch latest refs and verify these objects. Bring only required reviewed source into the child's own feature worktree; do not assume master already includes either branch. Report integration commits and preserve unrelated website/art changes. Do not mutate the audit's snapshots or other worktrees.

The **pair covenant is the launch-proof baseline**, not the four-item certificate-NFT experiment. No contract-bytecode change is required for the narrow commitment-based proof below. If source or compiler changes do alter bytecode, provide fresh compile/typecheck, normalized artifact hashes and full relevant VM regressions; do not silently reuse old artifacts.

## Fixed product and record boundaries

* Exactly one independent collectible NFT inside the outer one-sat control construction. No extra certificate NFT, accessories, or object slots. Collection cap is 201 one-of-ones: 195 countries, five oceans, one Moon; equal edition scarcity. Roster source must be explicit, not inferred from a count.
* This milestone proves **one local fixture lifecycle**, not issuance/allocation of the 201 assets. Do not add random draw, price, odds, reservation sale rules or launch minting. Existing draw-at-open draft language is not approved allocation policy.
* Retain admitted narrow one-push text/plain grammar: one-sat original with a 64-character lowercase SHA256 digest of canonical metadata. Record the model/art byte hashes externally. This is a proposed/local launch representation, not approval of final storage or full-art inscription. If actual full-art admission is required instead, block with an exact grammar and cost proposal rather than widening silently.
* Detached authenticity record is signed data, not a separately inscribed NFT. Use domain `BOXSV-LAUNCH-CERT-1`; canonical signed statement fields in exact order: `protocol`, `collectionId`, `designId`, `collectibleOrigin`, `metadataSha256`. Strings only; `collectibleOrigin` is exact lowercase 64-hex txid plus `_0`; SHA256 is lowercase 64 hex. Reject extra/missing fields and noncanonical bytes.
* Metadata must be canonical and hashed **before** inscription; issuer signs the resulting original origin **after** inscription to avoid circular txids. Detached envelope fields: `statement` (canonical JSON string), `issuer` (compressed pubkey hex), `signature` (DER hex over SHA256 UTF-8 statement). Caller provides trusted issuer/collection/design policy separately; never infer trust from the envelope. Fixture scalars only, no production key creation/loading. Pin exact schema/examples in the child before tests; canonical metadata must bind the selected design and exact media hashes without claiming availability.
* Keep original issuance provenance separate from current custody integrity and original-manifest completeness. The verifier should return those checks explicitly, not one broad 'verified' flag.

## A. F-01 finality observations — required RED then GREEN

1. Turn the audit's white-box repro into ordinary regression tests around the existing worker/store and journal replay; preserve actual serialized fixture transfer bytes. Observe RED for missing-payment completion and ignored later transfer inclusion loss.
2. Maintain ownership history (TRANSFERRED/OPENED) and a separate durable `reconciliationRequired` flag with a reason, e.g. `PAYMENT_FINALITY_LOST` or `TRANSFER_FINALITY_LOST`. Do not relist inventory, erase historical transfers, change buyer authority or allocate a replacement parent in response. Uncertain RPC availability should be recorded distinctly from proven loss.
3. Revalidate payment when observing included transfers; recheck inclusion for completed monitored sales. Check caps and policy before any signing/broadcast as before. Persist holds so restart does not clear them. Do not silently retry a SUBMITTED sale with newly built bytes.
4. Test payment loss after send, transfer inclusion loss after completion, read errors, overpayment after TRANSFERRED and OPENED, repeated observation, restart, no second dispense, zero replacement broadcast, and unchanged buyer ownership history. Disclose mocked finality tests versus actual regtest reorg evidence.

## B. Single-item signed-record proof — required

1. New explicit local admission/certificate module and tests, using the unchanged pair construction. External trusted issuer policy is mandatory; no certificate NFT is created. Admit one deterministic metadata-commitment inscription independently, then Pack → Seal → Transfer → Open → Withdraw with fresh distinct valid sponsorship per operation.
2. Save exact raw transaction bytes, ordered outpoints and artifact hashes. Replay serialized bytes, not just builder booleans. Assert original NFT remains principal input/output zero and every principal stays one sat. Demonstrate unchanged immutable origin throughout.
3. Negative cases: copied-label/current-script counterfeit, forged/unknown issuer, tampered metadata/media digest/origin, unsupported admission grammar, missing/duplicate/substituted principal, sealed withdrawal, old-owner open/withdraw, unauthorized sponsor/change diversion, fee bounds and ledger conflicts. Retain existing pair/sponsor tests rather than replacing coverage with record-only tests.
4. Establish RED for the new record acceptance behavior before implementation. Do not claim each historical security test was newly observed RED.
5. Keep reusable seal behavior explicitly out of scope and failing in the chain model. No claim that two separately created controls are one stable reusable Box.

## C. Recovery classification — read-only, no new auto-resume service

1. Deliver a read-only command that accepts explicit local sale/pool evidence and captured chain observations, validates bytes and identifies RESERVING, BUILT, SUBMITTED, INCLUDED, uncertain-send and inconsistent/truncated evidence.
2. Never remove locks, dispense, sign, broadcast, refund, relist or edit journals. Ambiguous mapping stays quarantined, not guessed. Correlate exact outpoints/raw transaction IDs where available; describe the RESERVING-before-funding-ID crash window honestly.
3. Tests inject failure before/after reservation fsync, after dispense, after send but before stage persistence, and during a short write. Restart replay/classification must not issue a second parent and must report the same exact transaction or unresolved hold. Exercise file-custody tests on POSIX, not Windows mode-bit emulation.
4. Report that the existing funded CLI still has no automatic recovery if unchanged. A read-only classifier is not resumed paid fulfillment.

## Finish line and evidence

* Preserve raw RED/GREEN logs, named tests, exact command/exit codes, artifact hashes, source SHA and saved serialized proof. Rerun pair, sponsored pair, relevant client-record, finality/store/pool tests and typecheck. Run four-item regressions only if shared code changed; do not expand the product to match them.
* For a fresh node proof, only if necessary to satisfy the child's existing regtest acceptance: inspect all invoked helpers first, create a fresh datadir, regtest, wallet disabled, no P2P discovery/connections, cookie loopback RPC. No bare bitcoind help/version, no old harness version probe, no existing nodes. Capture exact owned PID/argv and shutdown. A repeat offline replay is not a fresh node run; report the distinction. No mainnet or testnet activity.
* Return a single fixed proof packet and request the review phase encoded in the child graph. Stop at this milestone. No further tests, new stages or new protocol should be invented after these gates are met.

## Release holds that this child does not waive

Production key custody, paid-run operational recovery, storage durability/cost, art approval (including unresolved USA v9), wallet/indexer support, miner fee policy, independent security review, sale terms/price/random allocation/legal review, mainnet authorization and release authorization remain explicit. Public reusable UI remains simulated. Branch push is not production deployment.
