# Corrected feature handoff — local engineering verified; real-wallet gate blocked

## Identities and disposition

- Independently reviewed implementation: `bcab418120f063f62cd715ec450341dd471efee2`, review task `t_95a9e259`.
- Corrected implementation: `ca6181b608d42988b5d8801a156877239bb23e1b`.
- Feature branch: `feature/paid-finality-review-fix`; final evidence commit and independently read-back remote SHA are recorded in the task handoff (the evidence commit necessarily follows this report).
- One correction pass used. R1 is resolved by fresh behavioral tests, not by asserting the old reviewer reproduction is a passing safety test. No second independent review or external security certification is claimed.
- Local engineering acceptance passes. Actual installed-wallet compatibility remains **BLOCKED on owner action**, not proven by public-fixture signatures. No launch-ready claim or production authorization.

## R1 correction

The paid composition installs a trusted awaited `beforeAttempt` guard independently of fault-injection hooks. After buyer Open/Withdraw signatures and PREPARED persistence, and on prepared-only recovery, it rereads payment through the existing durable Delivery observer before ATTEMPT. Amount/depth loss, changed receipts, excess and unavailable evidence persist reconciliation holds and reject without sending. Exact prepared bytes and prior ownership history survive restart. Already attempted transactions still enter the existing interrupted-send quarantine; the guard cannot retry them. Transfer's existing payment guard is unchanged.

New `launch/continuous/paid-finality.test.js` exercises both buyer actions, five failure classes, both signing races and recovery races. Signing-race tests change persisted payment through a separate SQLite connection while valid authorization is in flight. Recovery tests lose evidence after the early observation to prove the new late guard executes. Every case asserts no additional send, unattempted pending bytes, durable hold, unchanged prior history and no new authorization after restart.

## Fresh results and evidence

All paths below are under `evidence/review-correction/` unless specified.

| Gate | Result | Evidence |
|---|---|---|
| Behavioral RED before correction | Expected missing-rejection failure | `red-focused.log` |
| R1 Open matrix | 10 pass, 0 fail | `green-open.log` |
| R1 Withdraw signing / recovery | 5 + 5 pass, 0 fail | `green-withdraw-signing.log`, `green-withdraw-recovery.log` |
| Integration, negative, process/server, wallet suites | 65 pass | `regressions-foreground.log` |
| Full POSIX mint suite, including delivery | 187 pass | `mint-foreground.log` |
| Adversarial security | 10 pass | `security.log` |
| Allocation | 19 pass | `allocation.log` |
| Pair/sponsored/native/detached-record Script VM | 111 pass | `vm.log` |
| TypeScript | exit 0 | `typecheck.log` (empty success output) |
| Actual isolated Edge desktop/mobile + ambiguous reload | 13 grouped checks pass | `browser/report.json`, screenshots, state DBs and exact downloaded JSON |
| Fresh exported desktop/mobile signed bytes | Five transitions each replay in VM; provenance passes | `replay-desktop.log`, `replay-mobile.log` |
| Read-only delivery inspection | exit 0, unchanged DB hash | `read-only-inspect.json`, `inspect-stderr.log` |

Read-only desktop delivery DB SHA-256 before/after: `8199a04795a5ac1f2022304705e0fd63fed5a71f66b7878247fe5643e815138c`.
Browser reports zero external requests and zero uncaught page errors. Eight deliberate negative-test HTTP 409 console errors are retained, not suppressed. The harness checked decoded images, overflow and closed owned ports. Screenshots were captured, but this correction worker's image-inspection tool failed with provider 402 insufficient balance; no new visual-quality judgment is claimed. No UI source was changed. Prior independent review's visual observation is historical, not a fresh screenshot inspection.

Execution caveats: initial full RED run hit 180s, the combined Withdraw run hit the tool wrapper's 420s limit, and background shell attempts failed before tests with `stdin is not a tty`. Raw failed/partial logs remain. Passing bounded foreground matrix splits supersede them. Dependency deprecation warnings and Node experimental SQLite warnings remain. No optional audit loop was opened.

## Exact local run

Use Node 24, Git; Python Playwright plus installed Edge for browser QA. From the feature checkout root:

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
npm ci --prefix launch/wallet-transport --ignore-scripts --no-audit --no-fund
mkdir -p launch/continuous/browser
node launch/wallet-transport/node_modules/browserify/bin/cmd.js launch/continuous/browser-wallet.js -o launch/continuous/browser/wallet.js
node launch/continuous/paid-cli.js demo launch/continuous/.paid-demo 8791
```

Open `http://127.0.0.1:8791`. Reserve → Pack → Seal → Observe fixture payment + deliver → Open → Withdraw. Stop with Ctrl+C. Reuse the same directory only for intentional recovery; never delete ledgers or holds to resume. For a separate run use a fresh directory.

Exact policy: `launch/continuous/paid-config.json`; full operating/config/recovery instructions: `launch/continuous/PAID.md`. Test price/depth/expiry constants are not approved economics. Wallet domain `testnet` is distinct from execution realm `offline-fixture`. Real send is not configurable in this runner; wallet signing defaults off except the explicitly started public-fixture harness, `WalletTransport.send()` throws, and low-level Delivery defaults disabled/rejects live-network sending.

```sh
node --test --test-name-pattern='Open' launch/continuous/paid-finality.test.js
node --test --test-name-pattern='Withdraw signing' launch/continuous/paid-finality.test.js
node --test --test-name-pattern='Withdraw prepared' launch/continuous/paid-finality.test.js
node --test launch/continuous/integrated.test.js launch/continuous/paid-security.test.js launch/continuous/test.js launch/continuous/security.test.js launch/continuous/server.test.js launch/continuous/process.test.js launch/wallet-transport/test.js launch/wallet-transport/security.test.js
node mint/test/run.js
node --test evidence/security/challenges.test.js
python launch/mint/test_dry_run.py
# In vault/:
npx mocha --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/native-custody.test.js tests/launch-record.test.js
npx tsc --noEmit
# Back at repository root; browser destination MUST be new:
python launch/continuous/paid_browser_qa.py evidence/review-correction/another-browser-run
node launch/continuous/paid-replay.js evidence/review-correction/browser/desktop-download.json
node launch/continuous/paid-replay.js evidence/review-correction/browser/mobile-download.json
node mint/scripts/delivery-inspect.js evidence/review-correction/browser/desktop-state/delivery.sqlite box-1 launch/continuous/paid-config.json
```

On Windows, `mint/test/run.js` invokes WSL and uses a fresh POSIX cache directory for file-mode tests. It launches tests, not a node daemon. Captured browser state deliberately retains crash locks; inspect exported bytes/read-only Delivery rather than restarting those captured stores. The owner recovery procedure requires confirming the exact old process is dead before removing only its stale SaleStore lock.

## Authoritative wallet contract and precise blocked requirement

Authoritative references retained and independently checked by the parent review:

- https://yours-wallet.gitbook.io/provider-api/ai-onboarding
- https://yours-wallet.gitbook.io/provider-api/low-level-brc-100/cryptography
- https://yours-wallet.gitbook.io/provider-api/low-level-brc-100/key-derivation
- https://yours-wallet.gitbook.io/provider-api/low-level-brc-100/blockchain-queries
- Yours source revision `ccdd6f480906c06cfa1481ad3a66f4abc8a5cc9e`, `src/cwi.ts`, `src/content.ts`, `src/background.ts`; exact excerpts/URLs/hashes: `evidence/wallet-transport/api/authoritative-excerpts.json`.
- Harness `@bsv/sdk@4.1.1`; exact interface and policy in `launch/wallet-transport/README.md`.

Use BRC-100 `createSignature({hashToDirectlySign})` with independently enrolled BRC-42 `[1,'boxsv custody']` / `testnet:owner:v1` / `self` owner key, not identity-key transaction signing or arbitrary-raw `signAction`. Verify returned DER and response envelope; assemble actual custody unlocks and independently replay Script. Pinned provider-source hashes in earlier evidence describe CRLF normalization; original source/evidence was not rewritten.

**Actual extension observation was only typeof on a documentation-origin CWI object. Zero provider methods or approvals were invoked.** It does not prove publisher/version, account/network, intended-origin permission behavior or direct-hash support. Fresh browser evidence here uses SDK ProtoWallet public deterministic signing, synthetic payments and local VM acceptance; no extension was discovered or called.

**BLOCKED OWNER GATE:** The owner must explicitly authorize and personally initiate one isolated, unfunded, no-send Yours compatibility session on the intended app origin; select account/testnet; personally approve identity and `[1,'boxsv custody']` / `testnet:owner:v1` / `self` derived-key access; independently enroll/pin both public keys; then approve exact synthetic transaction-hash and response-envelope signatures. Keep real sending disabled. If the installed provider rejects `hashToDirectlySign`, retain its actual version/error and fail closed; do not substitute broadcast-capable actions. This worker is not authorized to perform those approvals. No credentials should be sent in chat. This gate is not needed to run the local artifact, but it is indispensable to claim real installed-wallet compatibility, so the broad finish request is not closed on fixture-only evidence.

## Preserved production boundaries

Git comparison against reviewed `bcab418` leaves `launch/collection`, all previous `evidence/continuous`, `evidence/final-qa`, `evidence/integrated`, and production `docs/` unchanged. Other worktrees and old evidence/assets were not modified.

201 one-of-ones, one inner collectible NFT plus detached signed record, 73 historical art holds, full-art admission/storage limits and sub-5,000,000-byte standalone model-preview budget remain. No art approval, production randomness/fairness, economics/odds/legal decision, issuer authority, funding, release approval or prior public-copy hold is cleared. This remains sequential payment/delivery, not atomic settlement. Fixtures do not establish chain inclusion/unspentness, real funded ancestry, miner policy, real-wallet compatibility, external trust/checkpoints, rollback resistance, key recovery, full-art storage, arbitrary NFT support or reusable seals. Physical phones and Safari remain untested.

No deployment, master push, real funds, production keys, broadcast, permission approval, purchase, sale activation, refund, replacement funding, paid generation, external-profile change or live node was performed. Recommendation: resolve only the owner compatibility gate next if real-wallet proof is desired; do not fund or release based on this report.
