# Bounded payment → continuous delivery integration

## API

```js
const {configure, poll, ConfirmedReceiptObserver} = require('../../launch/paid/payment');
// Use the SAME continuous Engine / SQLite Journal that will Reserve and deliver.
configure(engine, {
  id: 'fixture-invoice-1',
  binding: engine.inspect().binding,
  address: explicitTestnetP2PKHAddress,
  amount: 1000,                 // synthetic test amount, NOT selected launch terms
  expiresAt: explicitEpochMilliseconds,
  network: 'offline-fixture',
  minimumDepth: 2               // synthetic test depth, NOT selected launch terms
});
await engine.reserve('reserve');
// HttpTransport is explicitly injected; no public endpoint is chosen here.
const observer = new ConfirmedReceiptObserver({
  transport: explicitlyInjectedHttpTransport, // regtest policy, mocked HTTP in tests
  network: 'offline-fixture',
  clock: Date.now,
  maxTransactions: 100
});
await poll(engine, observer);
// Pack/Seal may precede payment. Transfer cannot.
await engine.advance('transfer', 'Transfer');
```

`configure` is synchronous and returns inspect state; `poll` is async and returns inspect state. Neither polls automatically nor delivers automatically. Read-only replay uses `new Engine(new Journal(existingFile))`; no wallet is needed. State is `inspect().payment` with invoice, observations, fingerprints, qualified, acceptedReceipts. Custody stage and history remain authoritative and are never replaced by payment status.

## Durable semantics

- PAYMENT_CONFIG must precede Reserve. It pins exact invoice fields and the entire immutable Iceland binding, including manifest/metadata hashes and original outpoint. requestFor includes the invoice in the signed intent and subsequent requests.
- PAYMENT_OBSERVATION persists complete validated receipts, including raw bytes, decoded outputs, block membership/height and stable tip supplied by the injected observer. Same existing SQLite transaction and head CAS; no second reservation/allocation store.
- Gate is in engine.advance and reducer PREPARED, ATTEMPT, and ACCEPTED for Transfer. Zero, partial and insufficient-depth payment cannot unlock it.
- Consecutive identical observations are idempotent; historically identical snapshots after intervening changes MUST replay, so zero → paid → zero detects finality loss.
- EXCESS_PAYMENT, PAYMENT_EXPIRED, FINALITY_LOST and PAYMENT_UNAVAILABLE are monotonic holds. They do not erase TRANSFERRED/OPENED/WITHDRAWN or receipt history. No automatic refund/reallocation/retry recovery is implemented.
- Deadline is first fully-qualified observation time; merely broadcasting before expiry does not suffice. Already qualified unchanged receipts remain qualified after expiry.
- Observer unavailability, invalid proof, true unconfirmed transactions lacking a block, and backwards clocks fail closed. An unavailable observation records an error, not manufactured confirmations. Unconfirmed transactions consequently create a manual-reconciliation hold, rather than automatically recovering when mined.

## Evidence boundary and limits

The observer reads address HISTORY, never balance/unspent, then calls existing HttpTransport.transactionEvidence for each transaction and validates the receipt again in reducer replay. Merchant spending does not remove a historic receipt. History must be a complete array within maxTransactions (default 100, maximum 1000), with at most 1000 matching outputs; pagination/object envelopes or excess size fail closed, not truncate. Raw script, exact sats, txid/output index, block identity/membership/depth and same-tip scan are validated. An endpoint silently omitting history remains an indexer trust limitation; this is NOT SPV or independent chain consensus proof. All tests use explicit mocked HTTP and deterministic public fixtures. No mainnet adapter, live chain, wallet credentials, broadcast, or production sale terms were introduced.

PaymentWatcher is intentionally not reused: its poll skips zero and insufficient-depth results and fingerprints only amount/refs, which can hide finality loss or block replacement. HttpTransport.transactionEvidence is reused safely while its unspent/balance read is not.

## Verification

Command:
`node --test launch/paid/payment.test.js launch/paid/custody-wallet.test.js launch/paid/wallet.test.js launch/continuous/test.js launch/continuous/security.test.js launch/continuous/process.test.js launch/continuous/server.test.js mint/test/watcher.test.js`

Final output: **69 tests passed, 0 failed**, `payment-final.txt`. Includes full same-engine lifecycle and restart, duplicate/no-double-delivery, raw/binding/address/tx/block/outpoint rejection, partial/excess/expiry/depth loss, terminal preservation, unavailable holds, and existing non-paid continuous/BRC100/watcher regressions. `git diff --check` passed. Node emits the existing experimental SQLite warning.

TDD logs: payment-red.txt (missing public API), payment-clock-red.txt (backwards-clock availability bug), payment-reorg-red.txt (historical-snapshot dedup regression). Earlier green/regression files preserve intermediate runs; payment-final.txt is authoritative.

Only source files owned/changed here: launch/paid/payment.js, launch/paid/payment.test.js, launch/continuous/engine.js. No commits/pushes, wallet/custody/browser edits, live network or broadcast.
