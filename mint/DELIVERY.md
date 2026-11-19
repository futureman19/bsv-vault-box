# Durable reservation → signed custody delivery (schema 1)

`mint/delivery.js` connects an existing reserved `SaleStore` record and its exact selected, already Pack/Seal-verified inventory to the **same** signed request/response and Script verifier used by `launch/continuous/engine.js`. It is sequential fulfillment, not atomic payment-versus-delivery. It does not choose a random allocation or a price. This is backend machinery for integration, not an activated sale.

**Real sending is disabled by default and remains hard-locked in this delivery phase.** Omitting `mode` disables `tick`. Only the explicitly selected `offline-rehearsal` + `offline-fixture` combination executes local transport; there is no mainnet override. `reconcile` can record independently supplied read-only inclusion evidence but cannot send. Do not point a rehearsal adapter at a live transport. The only supplied execution adapter is the existing no-network public fixture wallet/transport.

## Runnable artifact

Node 24 with `node:sqlite` (experimental warning expected):

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
node mint/scripts/delivery-rehearsal.js mint/.delivery-local japan
node mint/scripts/delivery-inspect.js mint/.delivery-local/delivery.sqlite box-1 mint/.delivery-local/config.json
node --test mint/test/delivery.test.js
node mint/test/run.js
```

Use a **new** directory for each rehearsal. The example uses public deterministic fixture keys and synthetic funding/receipts, a fictional 100-satoshi test amount, two-confirmation test thresholds, and a 500-satoshi test transition fee inherited from the existing fixture construction. None is an approved sale price, launch threshold, fee budget or economic decision. Never fund the fixture addresses. The example really calls `SaleStore.list/reserve`, `PaymentWatcher.poll`, the durable coordinator and the signed custody verifier. It returns `LOCAL_ACCEPTED`, not chain inclusion. Japan is selected to demonstrate this is not hardcoded to the earlier Iceland fixture; Morocco is also exercised in tests.

The recovery CLI opens SQLite with `readOnly:true`, validates the external issuer/configuration pin, manifest, detached signed record, custody and event hashes, and emits exact prepared bytes plus holds. It loads no keys/adapters, performs no network calls, changes no rows and removes no locks. Supply the config from a separately trusted copy, not a purported issuer inside an untrusted evidence bundle. Printed public buyer/payment identifiers may be sensitive in a real deployment; do not publish real customer records.

## Integration interfaces

```js
const {Delivery} = require('./mint/delivery');
const worker = new Delivery(absoluteDatabasePath, {
  config: {
    mode: 'disabled', // explicit offline-rehearsal ONLY in public-fixture tests
    network,         // offline-fixture | regtest | testnet | mainnet
    issuerPubkey,    // external trusted compressed issuer/seller key
    paymentDepth, deliveryDepth, termsRef // all required; no business defaults
  },
  payment, // read(address, depth) -> {satoshis, confirmations, refs}
  wallet,  // request(BOXSV-CONTINUOUS-REQUEST-1) -> authenticated signed response
  transport, // send(raw): no real implementation supplied/enabled
});
worker.enroll(reservation, sealedCustodyState, fundingPin);
// Only for explicitly configured offline rehearsal:
await watcher.poll(event => worker.onPayment(event));
await worker.tick(reservation.id);
// Separate trusted read-only observer; safe to run on ambiguous/terminal orders:
await worker.reconcile(reservation.id, evidenceReader);
worker.close();
```

- `reservation`: the actual output from `SaleStore.reserve`, or a trusted allocation bridge with **id, inventoryId (sealed transaction id), buyerPubkey, payAddress, priceSats, expiresAt**. Held/refund-required/expired upstream records are rejected. Importing a listed record without a buyer fails. Keep enrollment in the service's reservation path; a crash before enrollment is repaired by idempotently importing the same immutable reservation, never selecting another design. Do not expose enrollment, config or arbitrary state patches to unauthenticated clients.
- `sealedCustodyState`: **candidate, inventory, binding, policy, history** as used by the continuous workflow after Pack and Seal. A pending send or custody hold is rejected. `history` contains the original two signed raw responses and funding parents. Exactly one independently issued inner collectible plus outer container is accepted; no certificate/accessory NFT. The detached signed record, canonical metadata digest, exact manifest item/model/art hashes, immutable origin, buyer, issuer/seller and sealed owner are validated. The candidate manifest is pinned to `307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb`; no silent migration to a new art selection.
- `fundingPin`: **raw, root, amount, change**, for one externally prepared and exclusively assigned sponsor output. The actual serialized funding tx/root are pinned before signing; `amount-change` is an explicitly supplied fee, not a newly chosen budget. One-output sponsor preparation grammar remains narrow. No sponsor pool is replenished/dispensed inside this worker. In a future live integration, obtain this pin through the existing durable pool reservation API, persist the association before handing it to this worker, and prove unspentness/current depth separately; this phase has no funded ancestry/UTXO admission claim.
- Wallet request key is `delivery-<reservation-id>`, action **Transfer**, actionIndex **2**, and full immutable binding/source/inventory are signed. `verifyResponse` now accepts an optional explicit funding policy and uses `policy.network`; old fixture calls preserve their original synthetic funding validation. Recipient, phase, ordered one-satoshi custody outputs, sponsor change and anchored Script replay are still checked. The wallet never receives an order to Open or Withdraw the buyer's delivered package.
- Payment observation is **cumulative receipt evidence**, not spendable balance. It must continue to include previously received outpoints even after treasury spending. The existing `PaymentWatcher` callback is merely a trigger: this worker freshly reads `payment.read` before signing and again after signing/before the persisted attempt. The watcher skips zeros/depth loss and caches positive observations, so integration must also schedule `tick` (offline only in this phase) / `reconcile` independently for every enrolled order, including terminal ones. A balance-only production adapter is insufficient. `RegtestTransport` has cumulative scan semantics; the existing HTTP UTXO-based reader must be extended or replaced with retained historical receipt evidence before live treasury spending.
- `evidenceReader.transactionEvidence(txid)` follows the existing `HttpTransport.transactionEvidence` result shape: exact raw/txid, confirmations, block `{hash,height,confirmations,tx}`, detail `{blockhash,blockheight,confirmations}`, tip `{blocks,chain}`. Require the adapter's stable-tip and active-block checks; this is not SPV. Offline fixtures additionally require `kind: OFFLINE_INCLUSION_FIXTURE`, and result in `REHEARSED_CONFIRMED`, never `CONFIRMED`. Wrong bytes, depth, network or block evidence produce a monotonic hold. Later evidence cannot erase a hold or revoke recorded ownership history.

## Persistence and crash behavior

One shared SQLite database per collection/service is mandatory; do not create one database per invoice. Schema 1 contains immutable `orders`, hash-linked snapshot `events`, globally unique `receipts`, and pinned `configuration`. Unique constraints reserve design identity, original outpoint, payment address and sponsor funding tx. One design cannot be enrolled twice, even under a new order id. This enforces the pinned 201-design one-of-one roster; it does not implement fair randomized allocation.

Mutations use `BEGIN IMMEDIATE`, `synchronous=FULL`, a busy timeout and a compare-and-swap event head. Receipt claims and their observations commit together. Replay checks historical receipt registry mappings, hold monotonicity and prepared-byte immutability. Public source keys and the external issuer policy are rechecked on restart. Local hashes are corruption detection, **not** protection against a coherent database rewrite, rollback or a malicious operator. External checkpoints/backups remain required.

States:

1. `WAITING_PAYMENT`: partial or insufficient depth never signs.
2. `PREPARING`: persisted before wallet/funding handoff. A crash/failure leaves a hold; no second funding/signing attempt is allocated.
3. `PREPARED`: exact authenticated signed bytes persisted. A restart may use those same bytes only, after a fresh payment check.
4. `ATTEMPTED`: committed before transport. A lost response/process exit quarantines, with no automatic resend or replacement.
5. `LOCAL_ACCEPTED`: explicit no-chain receipt. `REHEARSED_CONFIRMED` is synthetic inclusion; `CONFIRMED` requires exact externally supplied nonfixture inclusion evidence. Payment or delivery finality loss adds a hold without resetting ownership history.

Ambiguity, unavailable evidence, excess/changed receipts, late payment/expiry, upstream custody holds and receipt conflicts never trigger refunds, relisting, release, replacement funding or a new allocation. A read-only operator can inspect and collect exact inclusion evidence. There is deliberately no clear-hold/retry/refund command. Business resolution needs a separately approved operation and policy.

## Migration and composition requirements

- No old ledger is rewritten. Provision a **fresh** schema-1 DB, back up the prior SaleStore/allocation/pool/continuous journals using their proper backup procedures, and import only exact reserved/sealed records through `enroll`. Preserve old evidence and all receipt/funding associations. A missing/incompatible schema or changed network/issuer/depth/terms pin refuses startup; no automatic destructive migrations.
- `Delivery` is the authoritative delivery ledger for enrolled records. Do **not** run legacy `TransferWorker` for them; that would create competing writers/sends. The old SaleStore is intentionally not marked TRANSFERRED by local fixture acceptance. A future projection to customer/order UI must be idempotent and distinguish real confirmation from simulation. The downstream integration card owns that UI/wallet bridge.
- Restart with the same external pins and the same database. Before changing terms/manifest/issuer or migrating active orders, write a reviewed explicit migration; don't delete the DB or restore financial state alongside static-site rollback. Coordinate filesystem ownership/permissions, external checkpointing and consistent SQLite backups with operations. Native-Windows tests do not establish POSIX file-mode security.
- The mint test runner's bounded timeout is now four minutes to accommodate signed-byte replay/crash tests; it still starts no node. Existing POSIX key/pool tests run on a real POSIX scratch filesystem through the established WSL runner.

## Unresolved external gates — deliberately not decided

Real extension/owner signing and wallet permissions; authenticated production reservation/buyer enrollment; final allocation entropy/order/reserves/odds/reveal/Moon disclosure; price/currency/fees and confirmation/expiry/refund rules; jurisdiction/legal and rights clearance; actual issuer/key custody/recovery; funded ancestry and input unspentness, miner/indexer acceptance, security review, cumulative production payment observer, and production transport authorization. No production worker or checkout is activated.

All **73 historical art holds**, all **201 final owner approvals**, full-art/storage/availability limits and owner/release holds remain intact. Metadata commitments do not store full art; the under-5,000,000-byte complete interactive-preview requirement is unchanged. No accessory/certificate NFT, arbitrary-file custody, reusable-seal covenant or permanent-storage claim is added. No deployment/master push, funds, live nodes, broadcasts, purchases or production keys are needed or used for this artifact.
