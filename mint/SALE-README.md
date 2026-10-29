# Phase 2 — isolated regtest sale loop

No deployment, real keys, live funds or production readiness. Existing tracked files are unchanged.

## Gates
`node mint/test/run.js` runs existing pool/RPC and new sale, watcher, transfer and HTTP tests in WSL/POSIX custody.
`cd vault && npx mocha --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/native-custody.test.js` runs the 90 covenant tests.
`node mint/scripts/regtest-sale.js [NEW_ABSOLUTE_EVIDENCE_DIR]` runs the official checksum-pinned v1.2.3 node through the existing guard. Default evidence must not already exist. Public fixture scalars only; no actual wallet is loaded. The harness calls the real API and watcher, transfers inventory, rejects the prior owner's open against an unspent pair, then mines the buyer's open and withdrawal and verifies ancestry and final one-sat outputs. Owned node shutdown and RPC journals are recorded.

## Composition/API
Import `SaleStore`, `PaymentWatcher`, `RegtestTransport`, `TransferWorker`, and `createService`; see the integration harness for runnable composition. The service exposes only a loopback listener, default 8090. Its inventory is operator-configured, never accepted from HTTP clients.
- GET /health: ok, service=boxsv-mint, version, uptimeSec.
- GET /v1/boxes: {boxes:[...]}.
- Empty POST /v1/boxes: list the next configured inventory item; 201 box. If inventory empty, 409.
- POST /v1/boxes with {id,buyerPubkey}: bind an unreserved listing to a compressed public key and expiration; 201 box.
- GET /v1/boxes/:id: box or 404. Box retains skeleton id/state/payAddress/buyerPubkey fields and adds price/expiry/refund/transfer id. No raw journal, funding, or keys are exposed.
The shapes were recovered from the original provisioning session, not by accessing the VPS. Browser-origin requests are denied; public authentication, wallet ownership proof and rate limiting are future deployment gates.

Poll explicitly: `store.expire(); await watcher.poll(e => store.payment(e.id,e));` then run the worker for PAID_PENDING entries on each bounded scheduler tick. The harness owns these ticks. No daemon/timer is silently started. OPENED is recorded only after `observeOpen` validates a confirmed buyer-authored direct open; the buyer key is never passed to the worker.

## Safety and limitations
- One testnet xpub-derived address per box. Buyer binding is immutable. Expired addresses/inventory are quarantined, not automatically relisted; late and partial funds are flagged for manual refund, never automatically spent. Payer must reserve before paying; possession of a payment address does not authenticate the payer.
- Synchronous append/fsync journal and exclusive writer lock preserve allocations and transfer bytes. Local journal/inventory are trusted operator inputs, not arbitrary uploads. Crash locks and ambiguous RESERVING states require manual reconciliation with the pool ledger; never delete a lock while a process is alive. Stop and await worker operations before closing the store. Back up the journal/xpub together. No automatic corrupted-journal repair or distributed worker support.
- Before dispense and broadcast, payment finality is re-read; network must be regtest. Funding remains held after ambiguity. Retry budget and exact signed bytes are persisted before send; retries never create replacement spends. Inclusion requires matching raw bytes and active block membership. SUBMITTED waits for inclusion; eviction/reorg after inclusion needs operator reconciliation. No eternal polling loop or fee bumping.
- Actual covenant builder enforces three inputs, principal outputs 0/1 each one sat, sponsor last, 0x41 signatures and 1..10000-sat fees. Default is 500 sats, not a miner quote.
- HTTP transport is read-only and uses WoC-shaped main balance/unspent/chain-info/transaction endpoints. Balance alone fails closed. It checks outpoint value/script and confirmation depth against detailed indexer data. It trusts the indexer (not SPV), requires unswept payments, and is tested with fixtures only; no external HTTP or mainnet broadcast was exercised. Alternate indexers can inject an evidenceReader. The local RPC transport rescans bounded blocks and includes spent receipt outputs, detecting a changed tip during the scan.
- No payout sweep, automatic refunds, testnet run, mainnet run, VPS access, miner-policy acceptance, UI integration or security audit. Existing dependency vulnerabilities reported by npm are unchanged; no dependency upgrades were authorized.
