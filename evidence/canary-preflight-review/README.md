# Phase 3b preflight follow-up verification

Fresh evidence; existing phase-3b evidence was not changed. No mainnet broadcasts,
random private keys, funded wallets, treasury, VPS, deployment or mainnet node.

Commands executed from repository root:

- `npm test --prefix mint`: **76 tests passed**, 0 failed/skipped. Original tests unchanged.
- `(cd vault && npx mocha --no-config tests/*.test.js)`: **90 passing**.
- `node mint/scripts/mainnet-indexer-readonly.js evidence/canary-preflight-review/indexer`:
  **PASS**, A SEALED/B OPENED, confirmation depth 430; 24 GETs, no 429s in this run.
- `node mint/scripts/regtest-sale.js evidence/canary-preflight-review/regtest`:
  **PASS**, OPENED, five transitions, buyer withdrawal, old-owner rejection;
  `regtest/shutdown.json` records exitCode 0. Official guarded isolated regtest only.
- Linux/WSL: `node mint/test/preflight-live-readonly.js /ABSOLUTE/NEW/report.json`:
  **READ_ONLY_PREFLIGHT_PASS**, eight real WoC GETs, all HTTP 200, all three public
  fixture addresses UNFUNDED. The committed final run is `live-public-fixture-retry.json`.
  This helper creates only public deterministic scalar 101/102 WIF fixtures,
  public seed byte 103 xpub and scalar 104 buyer pubkey, removes the temporary
  fixture key/config directory afterward, and invokes the actual CLI main function.
  **NEVER FUND THESE FIXTURE ADDRESSES.**

`live-public-fixture.json` is an earlier passing live run with the same fixtures.
`live-public-fixture-final.json` records an intermediate FAIL_CLOSED run. That
version did not retain HTTP traces on failure, so the cause is unconfirmed (not
claimed to be a rate limit). The final entrypoint now preserves public GET
URL/status traces on failure while redacting config/error values. The retry
passed. Unit tests separately verify a 429 fails closed with status evidence.

The funded-shape path is tested with explicitly synthetic serialized transaction,
block and UTXO fixtures (not represented as real funding). Tests cover exact
3x50000 sponsor, 2x60000 inventory, 10000 payment, wrong/partial/extra shapes,
duplicate outpoints, unconfirmed/wrong-value/wrong-script evidence, wrong chain,
changing tip, custody failure, unsupported options, disallowed HTTP methods/routes,
secret redaction, new-file-only reports, and a signing-call trap.

Limitations: read-only budget composition, not inventory provisioning, signed
transactions, durable reservation, refund machinery or miner-policy admission.
Owner key generation and actual funding remain separately authorized steps.
