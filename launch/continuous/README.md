# Continuous buyer → design → origin → custody demo

**SIMULATION ONLY. Never fund the public fixture keys.** This is a runnable local application and CLI, not a report combining unrelated fixture runs. It does not connect an extension, request user signatures, query a chain, broadcast, accept money, activate a sale or modify production `docs/`.

## Run the browser demo

Requirements: Node **24** (built-in `node:sqlite`), Git with this repository's referenced history, and the pinned vault dependencies. From the repository root:

```sh
npm ci --prefix vault --ignore-scripts --no-audit --no-fund
node launch/continuous/cli.js demo --dir launch/continuous/.local-demo --port 8789
```

Open **http://127.0.0.1:8789**. Reserve Iceland, then Pack → Seal → Transfer → Open → Withdraw. Every click invokes the application engine, signs through the separate public fixture adapter, validates the signed response, replays compiled Script and persists the actual serialized transaction. The displayed IDs come from that journal, not a canned browser progression. Evidence JSON can be downloaded after any stage. The image is the exact promotional-art Git blob in the candidate manifest, hash-checked before serving.

Reload/restart with the **same directory** to resume the saved state. Do not delete or overwrite a held journal to pretend recovery succeeded. There is deliberately no reset/relist command. For a distinct independent demonstration, choose a fresh directory and understand it is a new isolated fixture universe, not new collection supply. Stop the local server with Ctrl+C. This is loopback HTTP only, not a hosted preview or `file://` app.

The optional fixture-error disclosure covers rejection, disconnect, wrong buyer/network, bad signature and ambiguous send. A rejected response changes no custody. An ambiguous send permanently holds the exact signed bytes and funding; no automatic resend/replacement funding is allowed. Browser/server errors never infer success. The UI displays only one fixed candidate; no random-allocation policy or launch price is chosen.

## One-command integration / saved-byte reproduction

After dependency installation, use a never-used output directory:

```sh
node launch/continuous/cli.js run --dir launch/continuous/.reproduction
node launch/continuous/cli.js replay --dir launch/continuous/.reproduction
```

`run` starts from a signed independent fixture issuance, reserves it for the fixture buyer, then executes the complete five-transition lifecycle. It saves `journal.sqlite`, `evidence.json` and source hashes. `replay` opens the same ledger, verifies its event chain and cryptographic bindings, and executes the saved transactions in the VM again. It refuses incomplete journeys. No node is started. Replay of the committed run:

```sh
node launch/continuous/cli.js replay --dir evidence/continuous/run-01
```

## Architecture and trust boundaries

- `common.js`: exact 201-entry manifest pin, canonical request encoding, signature checks. Selected design `iceland`; full immutable identity `urn:boxsv:collection:impossible-places:v1:iceland`. Manifest SHA256 `307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb`.
- `fixture-wallet.js`: the **only signing adapter**. Published scalars 1/2/3 serve seller, buyer and sponsor. Separately signed issuance spends establish the tiny text metadata-hash origin and initial outer Box from assumed synthetic roots. A detached authenticity statement binds that actual origin to the metadata/design; it is not another NFT. Buyer signs the reservation and their Open/Withdraw transactions; seller signs Pack/Seal/Transfer; sponsor signs funding and covenant authorizations.
- `engine.js`: application orchestration and durable reservation/allocation for **one fixed inventory item**, not the old disconnected allocation report. It reuses the actual `vault/src/ordinal-pair.js` transaction/compiled-Script implementation and `launch-record.js` verifier. The same design identity, manifest hash, buyer, digest and original outpoint are asserted in each event. Signed wallet-response envelopes bind the complete request and exact transaction/funding bytes; trusted role keys are external policy, never adopted from the response.
- `Journal`: SQLite `BEGIN IMMEDIATE` and `synchronous=FULL`; hash-linked events are cryptographically replayed on read, with compare-and-swap head checks for concurrent writers. Prepared bytes commit before a send attempt; the attempt commits before transport. A crash after preparation can resume exact bytes with no wallet request. A crash after an attempt is quarantined without resend. Partial/corrupt DBs fail closed. This is local consistency, not external checkpointing or protection from coherent full-history rollback/rewrite.
- `FixtureTransport`: returns an explicitly named **local VM acceptance**, not a block/confirmation receipt. The engine independently checks the returned txid and raw-byte digest. There is no public-chain adapter exposed by the CLI or server. The new orchestration is a production-shaped integration seam, **not an integration into the separately guarded paid `TransferWorker`/watcher**. Payment, production randomness, clocks and sale economics are not part of this fixed-item milestone.
- `server.js`: loopback-only, exact Host/Origin checks, no CORS, allowlisted routes, explicit action and idempotency key. It does not serve the repository or local files by arbitrary path. Stale browser actions cannot advance the next phase accidentally.

The inscription commits 64 ASCII hash characters under the existing narrow `text/plain` grammar. Neither model nor artwork bytes are inscribed. Metadata hashes are verified against the exact candidate manifest; only the promotional image bytes are served/decoded in this UI. This is not fresh verification of every model file or the historical source archive. Public fixture issuer signatures prove mathematical consistency, not a trustworthy real issuer.

Principal ordinal input/output ordering stays zero throughout. Two one-sat outputs are held together; output zero is the inner collectible and output one is the control companion—not a second collectible/certificate. Fees are fixture values: each transition uses an independently prepared 100,000-sat synthetic sponsor output, with 99,500-sat sponsor change and a 500-sat transition fee; preparation costs 500 fixture sats. This is neither a price quote nor real expenditure. Funding uses the contract's restricted one-input/one-output preparation grammar. Service sponsor change is not recycled.

Finality-loss/excess simulation holds preserve confirmed-local ownership history and prevent advancement/reallocation. Existing paid watcher/finality/recovery paths are unchanged and their regressions are rerun. These local holds do not implement real payment observation, accounting, refunds or reorg detection.

## Tests

```sh
node --test launch/continuous/test.js launch/continuous/security.test.js launch/continuous/server.test.js launch/continuous/process.test.js
python launch/continuous/browser_qa.py launch/continuous/.browser-run
```

The browser test requires Python Playwright and local Edge. It creates fresh desktop/mobile/ambiguous fixtures, blocks external traffic, executes the complete UI flow and errors, checks exact evidence downloads, and stops its owned servers. It is emulated mobile viewport coverage, not physical-phone/Safari acceptance.

Recorded results: **22 integration/security/server/process tests**, **111 existing contract tests**, **167 POSIX mint tests**, **10 security challenges**, **19 allocation regressions**, TypeScript pass; desktop/mobile complete flows and durable ambiguous error state pass. See `../../evidence/continuous/REPORT.md` for exact commands, failures and review scope.

## Still blocked

Real extension transaction construction/signing transport and compatibility; authentic funded origins and issuer; chain confirmation/finality; wallet/indexer/miner interoperability; full-art admission/storage; external security audit/checkpoints/key recovery; physical devices; production paid allocation/payment/settlement. This is not a complete production purchase, atomic settlement, fresh node run or proof of seal reuse.

All **201 final approvals and 73 art/package decisions remain unresolved**. All edition counts remain one: 195 countries, five oceans, one Moon. Rights, economics, pricing/odds/reveal/reserves, legal, storage/funding, sale/mint activation and release remain blocked. No master push or deployment is authorized by this milestone.
