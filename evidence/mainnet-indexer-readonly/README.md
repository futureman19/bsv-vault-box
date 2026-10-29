# Phase 3b verification

No mainnet broadcast, real key generation, treasury or VPS access. Mainnet proof
uses public GETs only; offline tests use explicitly public/disposable fixture keys.
Mainnet prepare/transfer calls additionally fail before reservation/signing in
this phase. Funded operator composition/broadcast approval remains a later gate.

## Gate outputs

```
$ (cd vault && npx mocha --no-config tests/*.test.js)
90 passing (7s)

$ npm test --prefix mint
# tests 60
# pass 60
# fail 0
# cancelled 0
# skipped 0
# todo 0

$ node mint/scripts/mainnet-indexer-readonly.js
{"status":"PASS","proofs":[{"box":"A","state":"SEALED","confirmations":430},{"box":"B","state":"OPENED","confirmations":430}],"requests":26}

$ node mint/scripts/regtest-sale.js evidence/mint-canary-regtest
{"status":"PASS","saleState":"OPENED","transitions":5,"oldOwnerRejected":true}

$ shutdown.json
{"exitCode":0,"signalCode":null,"ownedPid":491467}
```

Full mint/vault gate output is alongside this file. Full guarded official-node
rehearsal evidence is `../mint-canary-regtest/`. Existing tests/harness/artifacts,
`vault/`, `docs/`, and pre-existing evidence were not edited. The deterministic
prep test compares serialized bytes under omitted/default and explicit regtest
policy. The full node rehearsal uses default regtest policy throughout the newly
threaded components; it is not a claim of matching txids across fresh blockchains.

## Live evidence

`run-2026-10-29T17-39-18-295Z.json` contains actual HTTP attempt statuses/timings,
raw bytes, decoded txs, blocks, tip and confirmed payment evidence. The real
HttpTransport validates raw txid, every output script/value, active block
membership, stable tip and exact `tip - height + 1`. Published covenant fingerprint,
SEALED/OPENED state, one-sat value, lineage and deployment commitment hashes also
match. Payment balance/unspent/details are exercised without an evidenceReader.

**Two HTTP 429s occurred**, recovered by bounded backoff; 26 attempts total.
A second run on the final source (`run-2026-10-29T17-50-25-240Z.json`) also
passed at depth 430: 31 GET attempts, including seven HTTP 429s recovered with
bounded backoff.
WoC uses `/v1/bsv`, not the legacy `/api/v1/bsv` prefix; raw hex is text/plain.
600ms spacing is not a proven sustainable quota; use serial >=15s polling with
bounded backoff and fail closed. Bananablocks itself was not separately tested.

These historical proofs are VAULT-0001, not mainnet ordinal-pair custody sale
acceptance. Indexer evidence is trusted, not SPV. Paid UTXOs must not be swept
before worker finality checks. Mainnet funding, fees/relay acceptance and new
ordinal-pair checker support remain unproven.

## Review notes

- Codex implementation lane deliberately skipped: this change edits signing/
  chain-policy safety boundaries. Hermes implemented and ran all gates directly.
- Existing dependency audit: 20 findings (1 low, 9 moderate, 9 high, 1 critical);
  pinned dependencies unchanged, no upgrades or claim of remediation.
- Phase-2 concurrent-box busy-guard finding remains: use sequential awaited worker
  calls; do not issue Promise.all. No unrelated worker scheduling change here.
- All owner refund/reconciliation decisions remain manual. The runbook includes
  exact proposed funding allocations but is explicitly NOT funding permission.
- `late-overpay-red.txt` records an intentionally failing regression before fixing
  late overpayment handling; current `mint-tests.txt` is the passing gate.
