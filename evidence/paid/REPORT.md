# Wallet/payment integration: no-send engineering delivered; owner compatibility gate open

Task t_bc4da8be; feature/wallet-paid-delivery, based on continuous implementation d02b279d8ea41871c4f4af6760576a3926617fb6. Read final QA db4760ddcb33108da563b1df84a7e308205de3ec and retained collection ledger/decisions from f0a54d9b3e80338fbe34c869987a45d6d23ae25c. This is not production publication or full task completion.

## Working deliverable

`launch/paid/README.md` contains exact install/run/replay commands and configured API. Browser demo signs buyer requests in the browser through the same BRC100 transport, using explicitly public scalar-2 fixtures. Separate connect and per-digest approve controls, cancellation/disconnect, account/network verification, malicious response rejection and signed-byte VM replay are integrated into payment-to-custody progression.

The configured API now completes all five custody transitions rather than rejecting advance. It binds externally supplied buyer (tested scalar 4), network, metadata/origin, funding bytes, shared receipt registry and payment observer in the same durable engine. Dry-run mode is explicit, cannot be turned into a network send, and bypasses send transport entirely. Testnet/mainnet labels are intent binding, not actual chain execution. Configured API and fixture browser UI are separate compositions of that engine; no claim of installed-extension end-to-end completion.

Payment checks include complete empty history before reservation, fresh receipts before Transfer preparation and again after signing, restart/PREPARED handling, unique network/address and receipt outpoint attribution across invoice journals, and durable reconciliation holds. No refunds, relisting, replacement funding or automatic ambiguous-send retries.

## Fresh parent execution

- `node --test --test-reporter=spec launch/paid/*.test.js launch/continuous/*.test.js`: **108 passed, zero failed**, `final-tests.txt`.
- `python launch/paid/browser_qa.py evidence/paid/browser-final`: desktop/mobile complete flow and ambiguous-held case, **six grouped checks**, zero external requests/page errors; owned ports closed. This uses Playwright Edge with no user extension profile.
- `node launch/paid/cli.js run --dir evidence/paid/run-02` and `replay`: WITHDRAWN, five transitions, seven signature calls, 23 events; chainInclusion false. `run-02.txt`, `replay-02.txt` and actual saved journal/evidence.
- Provider/bundle targeted tests: **10 passed**, `provider-final.txt` (also included in final 108).
- Mobile screenshot `browser-04/mobile-withdrawn.png` inspected: no visible horizontal clipping; small supporting copy and long vertical layout retained. Final same-layout captures are in browser-final. No physical phone/Safari claim.

Two browser harness defects were corrected: a five-second expectation was too short for full VM/journal replay under concurrent load, and an intermediate disabled button could disappear before the harness saw it. The harness now waits for the actual pending request ID to change and bounded final status. Failed runs browser-02/browser-03 and their logs remain preserved; neither failure is represented as a passing run.

## Independent review and two bounded correction passes

Prior `REVIEW-1.md` found stale-payment authorization and cross-invoice receipt reuse; corrected in pass 1 with regression tests and shared registry. Independent reviewer deleg_77aa48bc confirmed those fixes and independently ran **27 plus eight targeted tests**; it correctly identified configured delivery was still a stub.

Pass 2 implemented explicit no-send configured full custody, caller-pinned distinct funding parents, network/identity binding and restart validation. Final read-only reviewer **deleg_f35c9d4c** independently ran configured/provider suites: **11 passed**. Verdict: no security blocker found within this bounded no-send scope; NOT full task or launch readiness. It verified send-sentinel refusal, complete lifecycle, exact pins, pre/post-sign payment checks and disabled provider default. No further correction/audit loop was started. Review summaries are human-readable records, not third-party certification.

## Provider evidence and exact gate

Official onboarding refreshed successfully as Markdown (HTTP 200), stored in `provider/onboarding-refresh.txt`; HTML/extraction attempts failed and were not used as evidence. @1sat/connect 0.1.2 published types/implementation inspected; wrapper consumes its real result shape. Default provider access is disabled; no connection/permission/signature was requested from the user's wallet. Browser target inspection did not verify an installed Yours version; access to chrome://extensions was blocked. No extension absence claim is made.

**Owner action needed:** identify the exact installed Yours build and provide an owner-operated test-only connection/signature compatibility session. Do not provide private keys or seed phrases. The agent must not approve wallet permissions. The adapter's generic BRC100 detection may discover a localhost wallet rather than Yours, so brand/version must be established rather than inferred.

Beyond that gate, live funding/unspentness and chain inclusion/finality transport reconciliation, hosted multiuser authentication, and nonfixture configured browser composition remain unverified/not delivered as a live purchase. Those are engineering/operational boundaries, not things owner permission alone proves. Fixed funding amounts and a frozen single Iceland candidate remain scope restrictions; no production randomness or price was selected. Indexer completeness remains trusted rather than SPV.

npm optional peer conflict in transitive @sigma-auth/better-auth-plugin (^2 SDK versus pinned 4.1.1) remains disclosed. No dependency security clearance is claimed. Root pins are not proof of chain ancestry/unspentness. Hash chains do not prevent coherent full-ledger rollback. No node, real funds, production key, broadcast, sale/mint activation, production deployment or master push occurred.

201 one-of-ones and existing 73 art holds/full-art storage limits are preserved. One inner collectible with detached signed record; no certificate NFT, accessories, arbitrary asset admission or proven reusable covenant. Rights, economics/legal, storage, external audit and release gates remain open. Recommended next step: owner-operated test-only wallet compatibility check, not funding or launch.
