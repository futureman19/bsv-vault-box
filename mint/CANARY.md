# Mainnet canary — phase 3b (READ ONLY)

**Do not fund anything or generate real keys in this phase.** This release proves
chain-policy plumbing and public indexer reads. `canary: true` is necessary to
construct mainnet components; it is NOT broadcast authorization.
`Canary.broadcast()` unconditionally rejects mainnet preparation/transfer before
reservation or signing. No environment variable/config option disables this lock.
The funded run requires a separate owner-approved implementation/review that adds
a mainnet chain/broadcast adapter and operator composition. The current loopback
RPC adapter is for the guarded regtest node, not a mainnet-node launch recipe.

## Commands that are runnable now

From the repository root (Node >=22, pinned `vault` dependencies installed):

```sh
npm ci --prefix vault --ignore-scripts
npm test --prefix mint
(cd vault && npx mocha --no-config tests/*.test.js)
node mint/scripts/mainnet-indexer-readonly.js
node mint/scripts/regtest-sale.js /ABSOLUTE/NEW/evidence-directory
```

The last command runs only isolated regtest with public disposable fixture keys,
wallet disabled and no peers. It refuses an existing evidence directory. On
Windows the harness uses WSL and keeps key files on its POSIX home filesystem.
Do not execute `vault/scripts/mainnet-cycle.ts`: that is an old, different,
spending workflow, not this canary's entrypoint.

## Fixed policy (not configurable upwards)

Pass the same `{chain:'mainnet', canary:true}` to SaleStore, SponsorPool,
TransferWorker, HttpTransport, PaymentWatcher and createService. Omission defaults
to regtest. RPC reports `main`, `test`, `regtest`; public options are exactly
`mainnet`, `testnet`, `regtest`. Testnet/regtest accept only testnet WIF/tpub;
mainnet accepts only mainnet WIF/xpub. Owned 0600 single-link regular key files,
absolute paths, no symlinks, POSIX only; never keys in argv/env/logs.

Hard limits live exclusively in `mint/canary.js`:
- Pool: 250000 sats held maximum; smaller configured caps allowed.
- Preparation: source AND prepared output <=100000 sats (conservative).
- Transition/prep fee: positive and <=10000 sats.
- Listed price: 1..10000 sats.
- Receipt >2x listing price: EXPIRED + refundRequired, never PAID_PENDING.
  Already TRANSFERRED/OPENED records retain their ownership state and flag review.
- Inventory: <=2 lifetime allocations per journal, including expired/sold entries.
  Start the first funded experiment with exactly ONE box. Do not rotate journals
  to evade limits. No replenishment or automatic top-ups in the canary.

Checks run at construction/replay and operation boundaries. A cap failure is an
abort, not permission to edit the journal or increase a limit. Components must
agree on policy. The HTTP adapter retains the legacy `/api/v1/bsv` prefix by
default; WoC requires `apiPrefix:'/v1/bsv'`. Its `regtest` default retains the
legacy main-route behavior for compatibility; **use RegtestTransport for regtest**,
never the HTTP adapter as local-chain evidence.

## Future owner-gated funded rehearsal (NOT authorized now)

### 1. Freeze the experiment

Obtain explicit owner approval of the exact commit, one box, owner as buyer,
10000-sat price, intended 1000-sat transfer fee, 500-sat prep fee, payout/refund
wallet and maximum loss. These fees are proposed budgets, NOT miner quotes.
Stop if admission needs >10000 sats per transition. Public sales, VPS/treasury,
remote listeners and third-party buyers remain out of scope.

The named operator entrypoint is `mint/scripts/canary-preflight.js`. It checks
custody, constructs the mainnet canary policy, derives the first payment address,
reads all three funding addresses using the real HttpTransport, checks exact
confirmed/unspent funding output shapes against serialized transactions and a
stable tip, and emits a dry-run composition report. It has no broadcast adapter,
listener, signing call or RPC client. Its network wrapper allows only specific
WoC GET routes with redirects disabled. No flag can arm it.

This is the approved **preflight-entrypoint path**, not a funded execution engine.
A funded release still needs inventory provisioning and a reviewed broadcast
adapter under a separate owner gate. Preflight does not build/sign transactions,
create a buyer reservation, or prove miner admission. Do not remove the guard.

### 2. Generate isolated keys only after that approval

**Future owner-only commands; do not execute key generation in phase 3b.**
Use Node >=22 and this repository's lockfile-pinned `bsv` dependency (via
`vault/src/ordinal-pair`), not an unspecified web key generator. On Linux/WSL,
with the repo path substituted, generate service keys directly to exclusive files:

```sh
export BOXSV_REPO=/absolute/path/to/bsv-vault-box
umask 077
mkdir -m 700 "$HOME/boxsv-canary-service"
node -e 'const fs=require("node:fs"),p=require("node:path"),{bsv}=require(process.env.BOXSV_REPO+"/vault/src/ordinal-pair"); for(const name of ["inventory","sponsor"]){const k=new bsv.PrivateKey(bsv.Networks.livenet); fs.writeFileSync(p.join(process.env.HOME,"boxsv-canary-service",name+".wif"),k.toWIF()+"\n",{flag:"wx",mode:0o600});}'
```

Never rerun into an existing directory or overwrite keys. On a **separate offline
owner wallet machine** with the same pinned dependency, generate the isolated
payment HD wallet; only the public xpub may be copied to the service machine:

```sh
umask 077
mkdir -m 700 "$HOME/boxsv-canary-owner"
node -e 'const fs=require("node:fs"),p=require("node:path"),{bsv}=require(process.env.BOXSV_REPO+"/vault/src/ordinal-pair"); const hd=bsv.HDPrivateKey.fromSeed(require("node:crypto").randomBytes(32),bsv.Networks.livenet),d=p.join(process.env.HOME,"boxsv-canary-owner"); fs.writeFileSync(p.join(d,"payment.xprv"),hd.toString()+"\n",{flag:"wx",mode:0o600}); fs.writeFileSync(p.join(d,"payment.xpub"),hd.hdPublicKey.toString()+"\n",{flag:"wx",mode:0o600});'
```

Back up private files offline and verify recovery/public-address derivation before
funding. This HD wallet is not automatically imported into the buyer's wallet;
the owner must retain a reviewed recovery/spend path before funding it. The buyer
uses the owner's existing BSV wallet, exporting only the compressed buyer public
key. Neither buyer private key nor payment xprv enters the service. Never use
fixture scalars/seeds for funds. These commands have not been executed with random
keys in phase 3b; custody/derivation/preflight are tested with public fixture keys.

### 3. Exact funding plan (owner wallet pays all miner fees separately)

| Destination | Exact receipts | Purpose |
|---|---:|---|
| Fresh inventory-key P2PKH address | **120000 sats**, preferably two 60000-sat outputs | Inventory inscription + empty-box setup budget; record change, principal and fees separately |
| Fresh sponsor-key P2PKH address | **150000 sats as three separate 50000-sat outputs** | Three bounded prep sources for deposit, seal and transfer |
| Reserved box's derived payment address | **10000 sats once**, from owner's own wallet | Owner-buyer payment; wait >=1 confirmation |

Do NOT send one 150000-sat sponsor UTXO directly to `prepare`: it exceeds the
100000-sat prep-source cap. With the planned three outputs and 500-sat prep fee,
each prepared parent is 49500 sats; total prep fee is 1500 sats. Each 1000-sat
transition leaves 48500 sponsor-change sats, excluding the preserved pair's two
principal sats. This is arithmetic, not a chain result. Deposit/seal need their
actual builders' input/output accounting checked before signing.

Do not automatically recycle sponsor change. Buyer open/withdraw are separately
owner-authorized wallet actions; obtain their fee quotes and funding plan before
funding the sale. The 10000-sat purchase receipt must not be swept to pay them.
These 270000 service-funding sats are not the pool cap: 120000 are inventory,
150000 sponsor; pool hold cap is independently 250000.

### 4. Run the operator preflight (no broadcast, no listener)

After future key-custody approval, create `~/boxsv-canary-service/preflight.json`
using this exact schema. Replace placeholders with absolute POSIX paths and public
values; `$HOME` is not expanded inside JSON. No WIF/xprv belongs in this file:

```json
{
  "inventoryKeyPath": "/home/OPERATOR/boxsv-canary-service/inventory.wif",
  "sponsorKeyPath": "/home/OPERATOR/boxsv-canary-service/sponsor.wif",
  "paymentXpub": "REPLACE_WITH_OWNER_PAYMENT_XPUB",
  "buyerPubkey": "REPLACE_WITH_OWNER_COMPRESSED_PUBLIC_KEY"
}
```

From the repo root on Linux/WSL (not a Windows-mounted directory for secret files):

```sh
node mint/scripts/canary-preflight.js --help
node mint/scripts/canary-preflight.js "$HOME/boxsv-canary-service/preflight.json" "$HOME/boxsv-canary-service/preflight-before-funding.json"
```

Exit 0 means **read-only checks passed**, NOT permission to fund. Inspect the
report's three addresses offline against backed-up keys/xpub; payment derivation
is exactly `xpub/0`, matching SaleStore's first allocation in a fresh journal.
Unfunded addresses are explicitly `UNFUNDED`. Once the separate funded phase is
approved, use the exact output plan above (inventory now strictly two 60000-sat
outputs). Repeat with a **new** report filename after funding confirmations:

```sh
node mint/scripts/canary-preflight.js "$HOME/boxsv-canary-service/preflight.json" "$HOME/boxsv-canary-service/preflight-after-funding.json"
```

Nonempty addresses must match the exact planned output count and amounts; partial,
unconfirmed, spent-during-read, duplicate, extra or inconsistent receipts fail
closed. A 429/5xx, changing tip or timeout also fails; wait at least 15 seconds,
reconcile, then rerun to a new report. No automatic broadcast/retry/refund exists.
Payment should remain UNFUNDED until a later release actually creates the durable
buyer reservation. **Do not pay based on this preflight's address alone.**
The report's prepared amounts/change are verified budget arithmetic, not signed
transactions. No journal or server is started and no inventory ancestry is proved
by this funding-only preflight. The full regtest command in §Commands exercises
actual inventory creation, reservation and signing without touching mainnet.

After the separately reviewed funded release, bind only 127.0.0.1:8090 (or ::1),
no tunnels or VPS. Use one process/one journal and explicitly serial scheduler ticks:

1. Validate sealed inventory ancestry, phase, owner and both 1-sat outputs.
2. List one inventory item; reserve using owner's buyer public key BEFORE payment.
3. Check returned payment address against offline xpub derivation; owner pays once.
4. Poll indexer serially >=15 seconds apart; expire reservations, deliver confirmed
   receipt events to SaleStore, then `await worker.run(id)` **sequentially** for
   each pending box. Never use Promise.all: phase-2 worker's store-wide busy guard
   drops concurrent calls. This known behavior is unchanged here.
5. Wait for exact serialized transfer bytes in an active block, not just send
   success. No second preparation after an ambiguous reservation.
6. Buyer independently verifies ownership, opens and withdraws from their wallet.
   Never give the worker the buyer key. Check old-owner authority is invalid.

### 5. Verify publicly

- Existing A: https://boxsv.com/check.html?txid=f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39
- Existing B: https://boxsv.com/check.html?txid=2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f
- New transaction: `https://whatsonchain.com/tx/<txid>` and
  `https://api.whatsonchain.com/v1/bsv/main/tx/<txid>`.
- Use the checker input if the page ignores query parameters. A/B are historical
  **VAULT-0001** seals, not the newer ordinal-pair sale contract. Their GET proof
  establishes indexer decoding/confirmation math, NOT sale-contract miner policy.
  Do not expect the legacy checker to certify a new ordinal-pair box; verify that
  contract with the custody/history verifier plus chain UTXOs and evidence.

### 6. Abort, reconcile, refund

Stop scheduler and new reservations on inconsistent indexer responses, 429/5xx,
reorg, cap failure, unknown broadcast outcome or unexpected output. Await all
in-flight work before closing store/pool. Retain journal, exact bytes, attempts
and reservations. Never delete a live lock or automatically clear RESERVING.
Cross-check every input/outpoint before resuming; do not create a replacement
spend or new funding reservation to cure uncertainty.

Expired, partial, unassigned and >2x payments require manual refund review.
Confirm no transfer has been submitted/included, identify actual payer ownership
out of band (do not trust a claimed return address), reconcile UTXOs, then owner
wallet signs a refund minus the disclosed miner fee. No automatic refunds or
payout consolidation exists here. If transfer happened, do not refund as if it
failed; ownership cannot be revoked. Quarantine post-inclusion reorgs manually.

### 7. Fee-accounting and stop checklist

- Preserve raw bytes, txid, block/hash/height, timestamps and indexer responses.
- For EVERY transaction: sum actual input values - sum output values = miner fee.
- Track funding-wallet fee, inventory setup fees/change, each prep fee, each
  transition fee, sponsor change, buyer payment fee and later open/withdraw fees.
- Never count dispensed/held principal as miner fees. Verify both pair outputs
  remain one sat and sponsor change returns to sponsor.
- Independently reconcile the three 50000-sat sources, three 49500-sat parents,
  journal reservations and any leftover coins. Do not rely on totals alone.
- Record admission/inclusion latency. One successful transfer is not commercial
  miner-policy proof; the specification's independent broadcast observations and
  fee-policy assessment remain funded-phase gates.
- Finish after one owner-buyer lifecycle. No scale-up until owner reviews evidence.

## Observed indexer constraints

The committed `evidence/mainnet-indexer-readonly/run-*.json` records actual GETs,
HTTP status/timing, raw transactions, outputs, blocks, tip and computed depths.
The initial run passed A SEALED and B OPENED at depth 430 with 26 GET attempts;
**two HTTP 429 responses** recovered with bounded backoff.
At 600-ms spacing this is not a rate-limit capacity measurement. Use conservative
15-second polling and bounded backoff, never infer an unlimited quota. WoC raw
hex is text/plain, not JSON; `/v1/bsv` differs from the bananablocks-style prefix.
Payment reads require unswept receipts and trust indexer consistency, not SPV.
