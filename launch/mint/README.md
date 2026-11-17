# BoxSV offline allocation rehearsal

**SIMULATION ONLY — no sale, mint, signing, chain connection or broadcast.** Python 3 standard library. `build` produces a plan, NOT serialized transactions. No switch can enable mainnet. This CLI never imports the live mint runner. The repository still contains separately guarded experimental chain tooling; this is not a repository-wide removal of those tools.

## Exact inputs / supported boundary

- Asset source: `d9de7e9562a1a3f69650cff04b6883bf7e4bcdaa`, `launch/assets/candidate-manifest.json`, SHA256 `307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb`.
- Reviewed custody/recovery source merged: `10acb9dfa127862b20172f4ce12f1dee32901b88` (security repair), not superseded parent-only source.
- Exactly 201 one-of-ones: 195 Country, 5 Ocean, 1 Moon. Reserves subtract from this cap, never add editions. Canonical Moon slug is `the-moon`.
- Inner collectible is distinct from functional outer custody Box. Certificate is a detached record, NOT another NFT. Here it remains unsigned. No accessories.
- Parent narrow supported admission uses a metadata-hash text ordinal; full-art all-201 issuance, storage, arbitrary NFTs, automatic paid fulfillment and reusable numbered seals remain unproven. This allocation ledger does not bind a real buyer, payment address or NFT outpoint and cannot establish custody. Existing transaction/VM proofs remain separate evidence.

## Commands (run from repository root)

Use a fresh card-local directory. Do not put credentials or personal buyer data in fixture requests. The example price is **100 fictional units, not satoshis or an approved price**. Empty reserves are an example, not approved allocation terms. All seeds in this tool are public test data, never secrets.

```
python launch/mint/test_dry_run.py
python launch/mint/dry_run.py init --db evidence/mint-dry-run/operator.sqlite --config launch/mint/fixture-proposal.json --manifest launch/assets/candidate-manifest.json
python launch/mint/dry_run.py apply --db evidence/mint-dry-run/operator.sqlite --request launch/mint/fixtures/01-reserve.json
python launch/mint/dry_run.py apply --db evidence/mint-dry-run/operator.sqlite --request launch/mint/fixtures/02-receipt.json
python launch/mint/dry_run.py apply --db evidence/mint-dry-run/operator.sqlite --request launch/mint/fixtures/03-build.json
python launch/mint/dry_run.py apply --db evidence/mint-dry-run/operator.sqlite --request launch/mint/fixtures/04-included.json
python launch/mint/dry_run.py apply --db evidence/mint-dry-run/operator.sqlite --request launch/mint/fixtures/05-open.json
python launch/mint/dry_run.py apply --db evidence/mint-dry-run/operator.sqlite --request launch/mint/fixtures/06-withdraw.json
python launch/mint/dry_run.py inspect --db evidence/mint-dry-run/operator.sqlite
python launch/mint/dry_run.py audit --db evidence/mint-dry-run/operator.sqlite
```

`init` refuses existing paths. Requests require unique `key`, `reservation` and `action`; receipt additionally requires globally unique `receipt` and positive integer `units`. Supported actions: reserve, receipt, expire, build, simulate-send (outcome included/ambiguous), simulate-open, simulate-withdraw, finality-loss. All unexpected fields/actions fail. `expire` is an explicit simulated operator event, not a real clock or approved reservation duration.

## Safety / restart semantics

SQLite BEGIN IMMEDIATE serializes writers; synchronous FULL commits event and snapshot together before returning. Every read/write replays the hash-linked history and compares the snapshot. Reopen the same DB after restart, inspect/audit, and retry only the identical request/key; it returns its original result without a second event. That historical receipt may precede a later hold: inspect current status before any decision. Failed writes roll back; corrupted or partially initialized DBs fail closed, never auto-reinitialize. Keep evidence and obtain review; never delete a questionable ledger to resume selling. Do not place SQLite on shared network filesystems.

Expiry permanently retains the reservation/design; partial and late receipts accrue REFUND_HOLD. Overpayment is retained for manual refund accounting and prevents further progression. Ambiguous send permanently holds the same plan/design; no automatic retries, refunds, unlock or relisting exist. Finality loss adds a durable hold without demoting TRANSFERRED/OPENED/WITHDRAWN history. An unpaid expiry also stays held. This conservative policy can exhaust availability; production cancellation/reallocation policy is deliberately not chosen. There is no refund execution command.

Hash chains establish local consistency, not recorder authenticity: an attacker able to rewrite the entire database can recompute it, and a coherent older copy is not detectable. SQLite durability is subject to OS/filesystem guarantees; tests are not power-loss certification. Protect and independently checkpoint any future real ledger before considering production.

## Allocation / odds proposal, NOT an approved sale

Sorted eligible roster -> Fisher-Yates -> SHA256 counter rejection sampling (avoids modulo bias). `permutationCommitment` commits the exact ordered array; public fixture seed/config + manifest reproduce it. The proposal's theoretical probability of each **remaining eligible** design is exactly 1/N, and Moon 1/N while unallocated/eligible, otherwise 0/1. Reserved and already allocated designs have zero remaining availability. Holds do not restore odds. `moonAllocated` changes on reservation, not a real claim/mint. All designs have identical edition scarcity.

This is deterministic rehearsal, **not unpredictable randomness**: fixture outcomes are publicly knowable. A future fair sale needs externally anchored roster/reserves/order commitments before reservations, non-grindable independent entropy with an abort policy, an auditable buyer ordering rule, reveal timing and public claimed/held-Moon updates. A server-selected seed plus a self-generated hash alone does not prove fairness. Production randomness/commit-reveal services are not implemented. The CLI intentionally does not simulate live probability claims using its known seed.

## Unresolved approval / readiness gates

User decisions: actual price/currency/fees; reserves and who receives them; allocation mechanism/entropy and independent audit; buyer ordering, per-buyer limits/bots; mint timing and maximum packages; reveal timing; reservation duration, cancellation and relisting; partial/excess/late-payment refunds and refund fees; ambiguous-send/finality dispute handling; sold-out/Moon-claimed disclosure; geographic eligibility, tax and jurisdiction-specific legal review. No demand/value guarantees.

Engineering/release: all art approvals and collection QA (USA v9 NOT approved; wrapped-star continuation unresolved); provenance/rights; authentic issuer and origins; full-art admission and all-201 transaction construction; storage funding/preservation/recovery; independently reviewed custody and wallet/indexer/miner integration; durable external checkpoints and real operator authentication; sequential payment/transfer is not atomic settlement; funds, keys, mainnet and deployment need separate authorization. Promotional illustrations may differ from actual models. No visuals edited or newly approved here.

Next consumer: existing rehearsal `t_35cdff45`, using this exact feature commit plus its other required parents. No production deployment.
