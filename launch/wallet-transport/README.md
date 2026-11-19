# Yours / BRC-100 no-send wallet transport

This is the signing boundary for integration task `t_31e507ba`, **not a replacement continuous demo or a completed purchase**. It signs caller-prepared transactions through the real BRC-100 provider contract and independently verifies both the transaction signature and a request-bound response signature. No provider methods that fund, construct, process or broadcast transactions are called. `send()` always throws `SEND_DISABLED`; signing is also disabled unless explicitly configured. No secrets, credentials or real accounts are required for the public-fixture harness.

## Reproduce

From the repository root, Node 24 and Python with Playwright/Edge for the optional browser smoke:

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
npm ci --prefix launch/wallet-transport --ignore-scripts --no-audit --no-fund
npm test --prefix launch/wallet-transport
npm run harness --prefix launch/wallet-transport
npm run build:browser --prefix launch/wallet-transport
python launch/wallet-transport/browser_smoke.py
# Optional complete bounded recapture; destination MUST NOT exist and must be inside repo:
python launch/wallet-transport/capture.py evidence/wallet-transport/my-fresh-run
```

Browser build creates ignored `browser/adapter.js` exposing `window.BoxSVWalletTransport`. It contains verifier code, not fixture private keys. Integrate using the selected wallet's `WalletInterface` object (e.g. `useWallet().wallet`); do not automatically select a different installed provider. The existing product's CWI generation can supply its explicitly selected `window.CWI`. The adapter neither detects nor authenticates the extension publisher. Same-origin compromised JavaScript cannot be made safe merely by checking an injected object.

The Node harness uses **public scalar 2**, SDK `ProtoWallet`, real BRC-42 derivation and real BRC-100 signatures. It assembles a P2PKH unlocking script and runs the repository Script VM. Its parents are synthetic, binding hashes are illustrative, and no network request is made. The isolated browser smoke replays those fresh fixture signatures through the compiled adapter; it is not fresh extension signing or a custody lifecycle proof.

## Authoritative provider decision

Existing product choice: `docs/claw.js:56-100` and `docs/index.html` use Yours / BRC-100 CWI, not RockWallet. Inspected the exact continuous implementation at `d02b279d8ea41871c4f4af6760576a3926617fb6`, final-QA report at `db4760ddcb33108da563b1df84a7e308205de3ec`, and collection decisions/ledger at `f0a54d9b3e80338fbe34c869987a45d6d23ae25c`. The feature branch starts from the continuous implementation, preserving prior evidence.

Authoritative sources (retrieved before implementing):

- https://yours-wallet.gitbook.io/provider-api/ai-onboarding — recommends `@1sat/react` discovery and low-level WalletInterface for unsupported high-level actions. Documentation says no injected global; do not blindly infer the installed generation from that claim.
- https://yours-wallet.gitbook.io/provider-api/low-level-brc-100/cryptography — `createSignature`, byte-array results and protocol/key/counterparty binding.
- https://yours-wallet.gitbook.io/provider-api/low-level-brc-100/key-derivation — derived keys, not identity-key transaction signing.
- https://yours-wallet.gitbook.io/provider-api/low-level-brc-100/blockchain-queries — read-only network method.
- Yours source pinned at **ccdd6f480906c06cfa1481ad3a66f4abc8a5cc9e**: `src/cwi.ts` actually injects `createEventCWI()`; `src/content.ts` transports requests with page host as originator; `src/background.ts:2660-2686` forwards `CreateSignatureArgs` intact to the underlying wallet. This resolves the docs/source generation discrepancy without inventing a custom extension protocol.
- `@bsv/sdk@4.1.1`, npm integrity `sha512-s/ComOkwz/Z8pyC2JOJUqazSwNNNJIxgb+UuULfsuTcJKzw3DUoXYA5HLzN7Bj+nYILUGAqc1CSwSMF7g22ZSw==`: `Wallet.interfaces.d.ts` explicitly defines `hashToDirectlySign?: Byte[]`; `ProtoWallet.createSignature` signs it directly, or SHA256-hashes `data`. Exact excerpts, source hashes and URLs are retained in `evidence/wallet-transport/api/authoritative-excerpts.json`. Yours source declares SDK `^2.5.0`; the installed extension's resolved version was **not established**. The harness SDK is an explicitly pinned verifier/reference implementation, not an assertion about installed-wallet version.

No `signRawTransaction` method is assumed. `signAction` is deliberately unused: it takes a reference from a wallet-created action, not an arbitrary maker transaction. No high-level send/ordinal action is called.

## Interface and caller trust boundary

```js
const { WalletTransport, requestHash, verifyResponse } = require('./adapter');
const adapter = new WalletTransport(selectedProvider, {
  network: 'testnet',              // exactly 'mainnet' or 'testnet'; no regtest relabeling
  identityKey: trustedIdentityKey, // compressed public key, separately enrolled/pinned
  signingKey: trustedOwnerKey,     // separately enrolled derived public key
  allowSigning: false,            // default; live permission gate stays closed
  timeoutMs: 60000
});
// Only an explicitly authorized harness or future owner-initiated session sets allowSigning:true.
const response = await adapter.request(preparedRequest, {
  expectedRequestHash: trustedPreparedRequestHash,
  signal: abortController.signal
});
verifyResponse(preparedRequest, response, trustedPolicy);
// provider removal / account switch / sign-out / navigation:
adapter.disconnect(); // terminal local disconnect; construct a new session after re-enrollment
```

`expectedRequestHash` MUST come from the trusted preparation/journal boundary, **not be recomputed from untrusted browser JSON and then called trusted**. `requestHash` is the shared canonical serializer/digest helper. It covers every field, exact raw transaction, ordered parents, input index, action, binding, outputs, fee and expiry. The fixture computes it locally only because the fixture owns its preparation.

`preparedRequest` is a closed JSON object; see the complete executable example in `fixture.js`:

- `version:1`, unique `id` (8–128 ASCII letters/digits/underscore/hyphen), `expiresAt` epoch milliseconds (future, maximum five minutes), exact `network`, `identityKey`, `signingKey`.
- `action`: Reserve, Pack, Seal, Transfer, Open or Withdraw. No resealing support.
- `binding`: exact manifestSha256, designId (canonical slug), metadataSha256, origin (`txid_vout`), buyerPubkey. These are application commitments, not an invented wallet payload. Reserve/Open/Withdraw must use the bound buyer **derived ownership key**, not the account identity key.
- Except Reserve: `transaction:{raw,parents,inputIndex}`. `parents` are complete raw transactions in input order (one per input); IDs, output indices, values, duplicates and fee conservation are checked. The selected input must have an empty unlocking script. All outputs/inputs and sequence/locktime are committed by ALL|FORKID (`0x41`); no caller-selected sighash weakening. The digest is computed locally from exact bytes and parent script/value, never accepted from a caller or extension.
- Except Reserve: `intent:{outputs:[{script,satoshis}],maxFee}`. Every ordered output must exactly match; no hidden wallet change/reselection. These expected outputs must be independently prepared from the intended action/recipient. The adapter does not invent covenant outputs or decide that a design belongs to an authenticated issuer.

The actual provider calls are ONLY:

1. `waitForAuthentication({})`, then `isAuthenticated({})`, `getNetwork({})`, `getPublicKey({identityKey:true})`.
2. Derived-key read: `getPublicKey({protocolID:[1,'boxsv custody'],keyID:'testnet:owner:v1',counterparty:'self',forSelf:true})`. Mainnet has a distinct `mainnet:owner:v1` keyID. Protocol and counterparty are fixed, not caller-controlled.
3. For transactions: `createSignature({protocolID,keyID,counterparty,hashToDirectlySign:[...32DigestBytes]})` → `{signature:number[]}`. Convert strict low-S DER to transaction signature by appending `41` **after verification**.
4. Response attestation: `createSignature({protocolID,keyID,counterparty,data:[...UTF8CanonicalEnvelopeBytes]})` → `{signature:number[]}`. The envelope includes the requestHash and exact transactionSignature, network, identityKey and signingKey.
5. Recheck authentication, network, identity and derived key after each signature, before returning.

Response is a closed object `{version:1,kind:'VERIFIED_SIGNATURES_NOT_SENT',requestHash,network,identityKey,signingKey,transactionSignature,signature}`. Reserve has `transactionSignature:null`. Signing ownership is proven under the externally pinned derived key; `getNetwork` is a provider assertion, not independent chain evidence. Network is also domain-bound through derivation and signed request. Identity trust comes from enrollment, not merely a self-reported key.

## Integration worker obligations

This is intentionally a new **prepared-request → verified-signatures** interface, not a dishonest drop-in for `FixtureWallet.request`, which currently constructs transactions internally using keys. Separate construction from authorization. Enroll the derived public owner key before generating the buyer's ownership outputs; the new provider cannot sign as the old fixture scalar or an arbitrary identity key. Seller/sponsor construction and keys remain separately scoped.

1. Construct and stabilize transaction/preimage bytes and funding parents. Persist the complete request and trusted digest with expected journal head/action/buyer/design/origin. Never rebuild from wallet-selected inputs or use createAction as a substitute.
2. Hand the prepared request to this adapter. For each needed input, use a unique request ID and appropriately pinned role key. Fill the contract-specific unlocking script using its verified `transactionSignature`; **do not use the P2PKH harness assembler for a covenant**.
3. Verify the complete assembled transaction with the existing anchored provenance, intended transition/recipient and compiled Script replay. This adapter verifies signatures and outputs; it does not certify full custody semantics, chain inclusion, unspentness or admission. Persist exact accepted bytes before any hypothetical send attempt, preserving existing quarantine rules.
4. Verify `response` again at the receiving boundary against the original persisted request and immutable role policy. For historical audit only, supply the recorded acceptance timestamp via `verifyResponse(...,{now: acceptedAt})`; live acceptance must not backdate expiry.
5. Maintain durable request-ID/action/head replay protection in the engine. Adapter IDs are session-local and consumed even on rejection/timeout; no automatic retries. A new ID after rejection requires a new user action and current journal validation. Recreating an adapter is not a durable replay defense.
6. On selected-wallet status/account changes, sign-out, navigation or provider replacement call `disconnect()`. No speculative provider event API is assumed. Local cancellation/timeout cannot close the extension prompt or revoke a signature already generated; late results are discarded and may never update custody. Funds cannot move here because no send method exists.

## Actual extension observations versus fixture evidence

Read-only attached-browser observation at the Yours documentation origin: `typeof window.CWI === 'object'`; `createSignature`, `getPublicKey`, `getNetwork`, `isAuthenticated`, `waitForAuthentication`, `createAction`, and `signAction` were functions. `window.yours` and `window.panda` were undefined. **No method was invoked.** No connect, identity read, permission approval or signature was requested. This establishes only a visible CWI surface on that page, not publisher authenticity, version, account, network or transaction compatibility. The isolated browser smoke is a separate browser context with no extension provider usage.

**Exact indispensable live gate:** the owner must explicitly authorize and personally initiate one isolated, unfunded, no-send Yours compatibility session on the intended local app origin; select the account/network; approve identity/derived-key access for `[1,'boxsv custody']`, `<network>:owner:v1`, `self`; independently enroll/pin those public keys; then personally approve the prepared synthetic transaction-hash signature and request-envelope signature. Keep real sending disabled. If `hashToDirectlySign` is unsupported/rejected by that installed generation, fail closed and retain the exact provider/version error; do not replace it with a broadcast-capable action or claim compatibility. This worker was prohibited from opening/approving that gate. It is NOT required to run the delivered harness.

## Holds retained

201 one-of-ones (195 countries, five oceans, one Moon), one inner collectible plus detached signed record, historical 73 art holds/final-approval gates, full-art admission/storage limits, issuer/economics/legal/odds/funding/release and independent-security holds all remain. No old evidence or artwork was edited, no node launched, no master push/deployment performed. Dependency warnings and fixture tests do not establish dependency-security or commercial miner compatibility.
