# Paid delivery integration — no-send build

This local app joins one exact Iceland candidate, buyer, independent origin, signed record, reservation, confirmed-payment observation and Pack → Seal → Transfer → Open → Withdraw. **It is not an activated sale or a proven installed-Yours checkout.** No network broadcast path is enabled. Never fund public test keys.

## Run

Node 24, Python Playwright + local Edge for browser QA. From repository root:

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
npm ci --prefix launch/paid --ignore-scripts --no-audit --no-fund
npm run build:wallet --prefix launch/paid
node launch/paid/cli.js demo --dir launch/paid/.local-demo --port 8790
```

Open http://127.0.0.1:8790. Connect **public fixture buyer**, click Reserve, then explicitly approve its pending signature. Pack and Seal use the supplied seller adapter. Observe partial/shallow/exact mocked payment to exercise the delivery gate. Transfer requires exact qualified payment. Open and Withdraw each need three separate browser approvals (two covenant input signatures and the response attestation). The browser never contacts an extension in this mode. Cancel/disconnect rejects pending signatures; reconnect is explicit. No automatic approval loop is present in application code.

Use the same directory to resume. There is no reset/relist/refund command. Old pre-registry journals fail closed; retain them rather than migrate away evidence. Fresh independent fixture universes are not new collectible supply.

CLI reproduction and read-only recovery (fresh run directory):

```sh
node launch/paid/cli.js run --dir launch/paid/.reproduction
node launch/paid/cli.js inspect --dir launch/paid/.reproduction
node launch/paid/cli.js replay --dir launch/paid/.reproduction
```

`inspect` and `replay` open existing fixture SQLite read-only and verify unchanged file hashes. Replay re-executes signed bytes in the compiled Script VM, not a node. Ambiguous/interrupted sends retain exact prepared bytes and funding; there is no retry/replacement-funding recovery command. Keep terminal ownership history when payments later lose finality or excess receipts appear.

## Real transport, explicit configuration

`wallet.js` implements BRC-100 WalletInterface calls: authenticate, network, identity key, derived self key under `[1,'boxsv covenant']` / `paid-delivery-v1`, and `createSignature({hashToDirectlySign: 32 bytes, ...derivation})`. It rechecks identity/network/derived key before and after signatures, rejects malformed/wrong signatures, and fences cancellation, duplicate calls and late results. It never uses createAction/signAction or broadcasts.

`provider.js` pins `@1sat/connect` **0.1.2** and consumes its published `ConnectWalletResult`. `BoxSVBrowserWallet.createProvider()` is disabled by default. After the owner has chosen and verified a test wallet, a host can explicitly create it with `{enabled:true}` and pass `getWallet:()=>provider.getWallet()` to the browser mount. Connect is a user gesture, not startup discovery. Pair local `client.disconnect()` with `provider.disconnect()` on host teardown/cancellation. Auto transport identifies **BRC100**, not the Yours brand, and can discover localhost wallets as well as extensions. Do not assume a CWI global proves current Yours compatibility. Provider response identity is checked; `YoursTransport` independently checks key/network and signatures.

Official onboarding was retrieved from https://yours-wallet.gitbook.io/provider-api/ai-onboarding.md; current docs describe @1sat APIs rather than legacy injected `window.yours`. Published connect types and implementation were inspected before writing the wrapper. SDK is pinned at 4.1.1. npm reports an optional peer SDK ^2 conflict in transitive @sigma-auth/better-auth-plugin; successful bundle tests do **not** clear dependency security or installed-wallet compatibility.

### Configured full no-send API

`createConfigured(file, options)` in `configured.js` accepts:

- `dryRun:true`, `sendEnabled:false` (any send opt-in rejected).
- Externally trusted `policy`: network `testnet` or `mainnet`, seller/buyer/sponsor public keys, and `fundingByAction` with exact `{funding,fundingRoot}` raw hex for **each** Pack/Seal/Transfer/Open/Withdraw. Repeated funding outpoints rejected.
- `genesis`: exact independently issued inventory, metadata and detached issuer envelope; frozen candidate manifest and binding are verified.
- `binding`: exact design/manifest/metadata/origin/buyer tuple, never adopted from wallet responses.
- Already connected `bridge` and matching `session`; explicit `sponsor`, `getFunding(request)` and `sellerWallet.request(request)` adapters.
- `invoice` with explicit address, amount, deadline, network, depth, and identical binding. These are caller decisions, no production defaults.
- `paymentObserver`: `ConfirmedReceiptObserver` over `HttpTransport` with explicit URL/network. GET-only transaction history, raw bytes, decoded values/scripts, block membership and stable tip are checked.
- `paymentRegistry`: one persistent shared `ReceiptRegistry` file across every invoice/journal/process. No independent per-invoice registries in a deployment.

The returned Engine executes the entire lifecycle and signed-byte VM replay with local dry-run receipts. It **never invokes a send transport**. Testnet/mainnet labels only bind intent; they do not establish real network execution. `configured.test.js` is the runnable full example with a different public buyer (scalar 4), explicit external funding pins, same observer and registry, and supplied seller adapter. Neither synthetic nor externally pinned roots establish chain ancestry/current unspentness. The fixed 100000 funding / 99500 change / 500 fee shape remains an engineering restriction, not approved economics.

The caller must supply the same trusted initialization on restart. Configured read-only inspection can use `Journal.prototype` with a read-only `DatabaseSync` and `trustedInitial`, then `new Engine(journal).inspect()`; do not reuse the fixture-only inspect CLI with arbitrary trusted policy. Never promote a dry-run journal into a live ledger.

## Persistence and reconciliation

Reserve performs a fresh empty-address-history check. Transfer re-observes before preparation **and after signing before the durable attempt**, also when resuming PREPARED. Cached qualification alone never authorizes delivery. Receipt registry allocates unique network/address and network/outpoint mappings before journal commits, with orphan allocations held rather than released. Unconfirmed receipts wait; missing or inconsistent evidence holds. Excess, expired, unavailable and finality-loss states retain ownership history. Indexer history completeness and chain assertions remain trusted, not SPV. Shared-registry backup/restore must be coordinated with invoice journals; hashes alone cannot detect coherent rollback.

## Tests and boundaries

```sh
node --test --test-reporter=spec launch/paid/*.test.js launch/continuous/*.test.js
python launch/paid/browser_qa.py evidence/paid/a-new-browser-run
```

Latest parent run: **108 pass**, desktop/mobile complete flow plus ambiguous hold, zero external browser requests/page errors. Browser and CLI fixture paths use public scalar 2; configured API tests use scalar 4 and both network labels. These are separate bounded assertions, not an installed-extension transaction.

**Next owner gate:** identify the exact installed Yours version and provide an owner-operated test-only connection/signature session for compatibility verification. No agent may approve that permission. This build has not exercised a real extension or real funded origin. Live broadcaster, authoritative UTXO/inclusion reconciliation, production hosting/auth, external audit, storage/rights/economics/legal and release authorization remain outside verified delivery. Preserve all 201 one-of-ones (195 countries, five oceans, Moon), existing art holds and full-art/storage limits. One inner collectible plus detached signed record; no accessory/certificate NFT, arbitrary-asset or reusable-covenant claim.
