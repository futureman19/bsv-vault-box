# Continuous wallet + paid-delivery rehearsal

**Local fixture only. No real send path, wallet permissions, purchase, funded ancestry or chain inclusion.** This extends the existing `launch/continuous` page and engine; it is not the wallet lane's unrelated P2PKH smoke page.

## Exact runnable setup

Use Node 24 (built-in `node:sqlite`), Git, and this feature checkout:

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
npm ci --prefix launch/wallet-transport --ignore-scripts --no-audit --no-fund
mkdir -p launch/continuous/browser
node launch/wallet-transport/node_modules/browserify/bin/cmd.js launch/continuous/browser-wallet.js -o launch/continuous/browser/wallet.js
node launch/continuous/paid-cli.js demo launch/continuous/.paid-demo 8791
```

Open **http://127.0.0.1:8791**. Reserve → Pack → Seal → Observe fixture payment + deliver → Open → Withdraw. The buyer signs in the browser using the actual `WalletTransport` and SDK `ProtoWallet`, not server-produced signature replay. Service issuer/sponsor signatures remain public fixture scalars 1/3. The buyer identity is public scalar 2, but custody uses its **separately derived BRC-42 key**, not its identity public key. The page never discovers or calls an installed extension. Only the explicitly started fixture runner enables fixture signing; `WalletTransport` defaults to `allowSigning:false` and `send()` always throws.

Stop with Ctrl+C; resume the same directory and port. Do not delete or replace state to bypass a hold. Use a fresh directory for an independent rehearsal. Legacy `cli.js demo --dir ...` is unchanged and remains the earlier fixture flow.

Fresh CLI execution and replay:

```sh
node launch/continuous/paid-cli.js run launch/continuous/.paid-run
node launch/continuous/paid-cli.js replay launch/continuous/.paid-run
# Truly read-only exported-byte replay (does not open or update a DB):
node launch/continuous/paid-replay.js launch/continuous/.paid-run/evidence.json
# Read-only durable delivery inspection with EXTERNALLY pinned fixture policy:
node mint/scripts/delivery-inspect.js launch/continuous/.paid-run/delivery.sqlite box-1 launch/continuous/paid-config.json
```

`paid-config.json` is the exact explicit rehearsal policy; its price/depth/expiry/terms constants are test inputs, **not approved economics or operational policy**. The runner does not accept a config switch that enables live sending. The low-level Delivery class still defaults to disabled, and rejects live-network sends even in offline-rehearsal mode.

## Bindings and persistence

- The pinned 201-candidate manifest selects the same Iceland candidate, metadata digest, independently issued ordinal origin, buyer and detached issuer-signed record for the full journey. This is a fixed-design allocation, not random paid allocation or approved odds.
- `testnet` is the consistent **wallet derivation/address/observer network domain**. `offline-fixture` is the separate **execution realm** on legacy custody requests, delivery configuration and local receipts. It is not a claimed third blockchain or testnet inclusion. No node/indexer is consulted. The policy and exported evidence carry both explicitly; the buyer identity and derived key are pinned before construction and rechecked on replay.
- `journal.sqlite`: existing hash-chained custody lifecycle, prepared bytes, attempted markers, and holds.
- `authorizations.sqlite`: exact browser requests and independently calculated hashes persisted before handoff; globally unique request IDs and verified/rejected status. Pending authorization after a process crash stops further work. Rejected IDs remain consumed across restart. This database also stores the explicitly simulated payment observation.
- `sales.jsonl`: existing SaleStore allocation/address/buyer, fixed to the deterministic preview's sealed inventory ID. The preview builds the same public-fixture Pack/Seal bytes; it does not claim they have already been accepted. The legacy sale state is deliberately **not promoted to TRANSFERRED** by local VM receipts.
- `delivery.sqlite`: existing shared order/address/design/origin/funding/receipt registry; watcher triggers are rechecked against durable cumulative observation. Preparation claim, prepared bytes and send attempt precede the local transport. The accepted Transfer is projected into the continuous journal using exactly the saved response and receipt, not sent twice.
- Buyer Open/Withdraw use two independently verified BRC-100 input signatures, assembled into the actual `ordinalPair` covenant unlocks. The assembler checks exact raw transaction and parent bytes, outputs, fee and anchored serialized Script history. The existing former-owner/sealed-withdrawal protections are not replaced by UI checks.

Signing and payment are sequential, **not atomic payment-versus-delivery**. A fixture `Pay` writes synthetic receipt `sha256("public simulated payment:" + sealedInventoryId):0`, 100 test satoshis/depth 2; it neither sends funds nor observes an actual payment. Payment observation is reread before delivery and before later buyer actions, then again after Open/Withdraw signature preparation immediately before the durable send attempt (also on prepared-only recovery). A lost/depth-reduced/changed/excess/unavailable observation persists a delivery hold, retains prepared bytes and prior ownership, and prevents transport. Holds never refund, clear, relist, retry an attempted send, or allocate replacement funding.

## Crash/recovery boundary

An unclean process exit leaves the existing SaleStore `.lock`; startup fails closed. An operator must first verify that the exact owning process is dead and review the retained journal, then remove only that stale lock to inspect/resume. Do **not** add automatic name-based process kills or ledger resets. The test performs this step only for its own child after observing exit 75. A pending BRC authorization remains an `INTERRUPTED_WALLET_HANDOFF` hold afterward; there is intentionally no hold-clear command.

A prepared custody transaction can resume with the same bytes and no new wallet call. Attempted/ambiguous sends require manual reconciliation and retain their hold even if exact synthetic inclusion is subsequently recorded. Coherent database rollback/rewrite, physical power-loss guarantees, external backups/checkpoints, production recovery and issuer key custody remain unproven.

## Bounded regression commands

```sh
node --test launch/continuous/integrated.test.js launch/continuous/paid-security.test.js
# R1 race/recovery matrix (split for bounded tool timeouts):
node --test --test-name-pattern='Open' launch/continuous/paid-finality.test.js
node --test --test-name-pattern='Withdraw signing' launch/continuous/paid-finality.test.js
node --test --test-name-pattern='Withdraw prepared' launch/continuous/paid-finality.test.js
node --test launch/continuous/test.js launch/continuous/security.test.js launch/continuous/server.test.js launch/continuous/process.test.js launch/wallet-transport/test.js launch/wallet-transport/security.test.js
node mint/test/run.js
node --test evidence/security/challenges.test.js
python launch/mint/test_dry_run.py
# from vault/:
npx mocha --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/native-custody.test.js tests/launch-record.test.js
npx tsc --noEmit
# from repository root, with Python Playwright + installed Edge:
python launch/continuous/paid_browser_qa.py evidence/integrated/NEW-browser-run
```

Browser output directory must be new. The harness starts/stops only its own loopback servers; blocks external requests; tests desktop/mobile, negative signatures, exact downloads and ambiguous-send reload. Its forced termination deliberately leaves crash-lock evidence; use exported JSON for read-only replay, not an accidental restart of the captured directory. Real physical phones, Safari and installed-extension signing are not covered.

## Authoritative wallet API and exact owner-only gate

See `../wallet-transport/README.md` and the pinned source/excerpts in `evidence/wallet-transport/api/authoritative-excerpts.json`: Yours source **ccdd6f480906c06cfa1481ad3a66f4abc8a5cc9e**, BRC-100 `createSignature({hashToDirectlySign})`, BRC-42 protocol `[1,'boxsv custody']`, keyID `testnet:owner:v1`, counterparty `self`. SDK harness version is 4.1.1, not a claim about the installed extension's version. No `createAction`, `signAction`, send, or broadcast method is used.

Fresh attached-browser observation in `evidence/integrated/extension-observation.json` only reads `typeof` on the existing documentation page's CWI surface. **Zero provider methods or wallet permissions were invoked.** This is separate from isolated Edge fixture signing and does not establish origin compatibility, account/network, publisher/version authenticity, or extension support for direct-hash signing.

**One indispensable gate for real-extension compatibility:** the owner must explicitly authorize and personally initiate an isolated, unfunded, no-send session on the intended app origin; select account/testnet; personally approve identity and `[1,'boxsv custody']` / `testnet:owner:v1` / `self` derived-key access; independently enroll those two public keys; then approve the exact prepared synthetic transaction-hash and response-envelope signatures. Fail closed if the installed provider rejects direct-hash signing. The fixture UI intentionally has no button to open that permission gate. No worker approval is authorized. This gate is not needed to run the delivered local rehearsal.

## Preserved boundaries

201 one-of-ones (195 countries, five oceans, Moon); one inner NFT and detached signed record; all 73 historical art holds and final owner/release gates; full-art admission/storage and sub-5,000,000-byte standalone model-preview limits remain unchanged. This developer browser signing bundle is separate from that model-preview payload. No art/assets/old evidence were rewritten. No price/odds/legal decision, new asset promise, deployment/master push, funds, live node, production key, refund, replacement funding, purchase, paid generation or sale activation is included.
