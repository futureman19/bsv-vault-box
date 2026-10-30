# Mainnet canary — owner-gated funded machinery

**This implementation is NOT authorization to fund or execute on mainnet.**
Build/review evidence uses only guarded local regtest broadcasts and live mainnet
GETs with public fixtures. Never fund a fixture address. A later owner decision
must approve the exact reviewed commit, one owner-buyer box, maximum loss,
10000-sat price, fee budgets, payout/refund wallet and recovery plan.
No public sale, VPS, treasury access or production-readiness claim is implied.

## Verification commands (safe during build)

From the repository root with Node >=22 and pinned dependencies:

```sh
npm ci --prefix vault --ignore-scripts
npm test --prefix mint
(cd vault && npx mocha --no-config tests/*.test.js)
node mint/scripts/regtest-sale.js /ABSOLUTE/NEW/official-sale-evidence
node mint/scripts/canary-run.js --owner-authorized --regtest-rehearsal /ABSOLUTE/NEW/funded-rehearsal-evidence
# Linux/WSL only; public deterministic unfunded fixtures, GET-only:
node mint/test/preflight-live-readonly.js /ABSOLUTE/NEW/live-preflight.json
```

The regtest command launches the checksum-pinned official v1.2.3 node through the
existing guard: fresh datadir, regtest, wallet disabled, loopback cookie RPC, no
P2P peers/discovery. Windows delegates to WSL; keys live on the POSIX filesystem.
It executes the **same `runCanary` implementation** as mainnet, differing in
chain policy/transport and local mining/payment callbacks. Buyer completion is a
separate offline-wallet process after the runner has stopped. It also proves
missing-gate refusal and an actual on-chain wrong funding shape refusal. The
harness corrects disposable local funding only; the runner never repairs funding.
Never run the unrelated historical `vault/scripts/mainnet-cycle.ts` workflow.

## Gate design and fixed policy

`canary: true` constructs mainnet components but DOES NOT authorize broadcasts.
`Canary.broadcast()` still rejects every ordinary mainnet policy, including
`ownerAuthorized:true`, copied policies, JSON roundtrips, fake capabilities and
regtest capabilities. `authorizeRunner()` issues a process-local capability only
after an explicit CLI flag **and interactive TTY confirmation** of a freshly
random 128-bit challenge. The prompt displays the hash binding the config,
preflight report and evidence destination. The authorization is never stored in
an environment variable, config, report or journal. No unattended mainnet mode,
stdin pipe, replayable approval file or default unlock exists.

Only the runner and separate signed-only buyer publisher call that gate in
production. Mainnet constructors receive its capability explicitly; a private
WeakMap/WeakSet brands their immutable policies. The adapter repeats
`Canary.broadcast()` immediately before its only POST. Local rehearsal's explicit
`--owner-authorized --regtest-rehearsal` attestation creates a **regtest-only**
capability, never a mainnet one. This is an application guard, not a sandbox
against someone modifying JavaScript or monkey-patching the runtime.

The runner checks the exact frozen constants at startup:

| Limit | Sats/count |
|---|---:|
| Pool held maximum | 250000 |
| Prep source/prepared output maximum | 100000 |
| Any prep/transition fee maximum | 10000 |
| Price maximum (this run uses exactly this) | 10000 |
| Excess-payment quarantine threshold | >2x price |
| Lifetime inventory per journal | 2 (this run allocates 1) |

No replenishment, journal rotation to evade caps, sponsor-change recycling,
automatic refund, fallback broadcaster or automatic broadcast retry. The funded
runner sets `maxAttempts:1`. Existing ordinary regtest behavior is unchanged.

## 1. Owner generates isolated keys AFTER separate funded approval

**Do not execute these random-key commands during implementation/review.**
Use Linux/WSL and owned 0600 single-link regular files, absolute paths, no symlinks.
Never put WIF/xprv in argv, environment variables, logs, evidence or git.

On the service machine, with the repository path substituted:

```sh
export BOXSV_REPO=/absolute/path/to/bsv-vault-box
umask 077
mkdir -m 700 "$HOME/boxsv-canary-service"
node -e 'const fs=require("node:fs"),p=require("node:path"),{bsv}=require(process.env.BOXSV_REPO+"/vault/src/ordinal-pair"); for(const name of ["inventory","sponsor"]){const k=new bsv.PrivateKey(bsv.Networks.livenet); fs.writeFileSync(p.join(process.env.HOME,"boxsv-canary-service",name+".wif"),k.toWIF()+"\n",{flag:"wx",mode:0o600});}'
```

On a **separate offline owner wallet machine**, with the same pinned dependency:

```sh
export BOXSV_REPO=/absolute/path/to/bsv-vault-box
umask 077
mkdir -m 700 "$HOME/boxsv-canary-owner"
node -e 'const fs=require("node:fs"),p=require("node:path"),{bsv}=require(process.env.BOXSV_REPO+"/vault/src/ordinal-pair"); const d=p.join(process.env.HOME,"boxsv-canary-owner"),hd=bsv.HDPrivateKey.fromSeed(require("node:crypto").randomBytes(32),bsv.Networks.livenet),buyer=new bsv.PrivateKey(bsv.Networks.livenet); for(const [name,value] of [["payment.xprv",hd.toString()],["payment.xpub",hd.hdPublicKey.toString()],["buyer.wif",buyer.toWIF()],["buyer.pub",buyer.publicKey.toString()],["buyer.address",buyer.toAddress().toString()]]) fs.writeFileSync(p.join(d,name),value+"\n",{flag:"wx",mode:0o600});'
```

Only copy `payment.xpub` and `buyer.pub` to the service. Neither buyer WIF nor
payment xprv enters the funded runner/service. Back up and verify key recovery
and public derivation offline before funding. The payment HD wallet is not
automatically imported anywhere; retain a reviewed recovery/spend path. These
commands have not been executed with real random keys for this delivery.

Create `~/boxsv-canary-service/config.json` with this exact schema (literal
absolute paths; JSON does not expand `$HOME`):

```json
{
  "inventoryKeyPath": "/home/OPERATOR/boxsv-canary-service/inventory.wif",
  "sponsorKeyPath": "/home/OPERATOR/boxsv-canary-service/sponsor.wif",
  "paymentXpub": "REPLACE_WITH_OFFLINE_PAYMENT_XPUB",
  "buyerPubkey": "REPLACE_WITH_OFFLINE_BUYER_PUBKEY"
}
```

## 2. Inspect addresses, then make exact owner-wallet funding sends

```sh
node mint/scripts/canary-preflight.js --stage inspect "$HOME/boxsv-canary-service/config.json" "$HOME/boxsv-canary-service/inspect.json"
```

Inspect PASS is read-only discovery, NOT funded readiness or permission to pay.
Verify the printed report addresses against offline key backups. The owner uses
their existing wallet to send these exact outputs, paying that wallet's miner
fees separately. No universal wallet-specific send command is assumed:

| Destination | Exact receipts | When |
|---|---:|---|
| Inventory address from inspect | **2 separate 60000-sat outputs** | Before startup |
| Sponsor address from inspect | **3 separate 50000-sat outputs** | Before startup |
| Offline buyer address | **2 separate 1500-sat outputs** | Before offline open/withdraw; record both parent raw transactions and indexes |
| Reserved payment address (`xpub/0`) | **1 output of 10000 sats** | ONLY after runner prints `PAY_ONLY_NOW` and reservation ID |

The inventory setup spends each 60000 source into one principal sat + 59499 change
+ 500 fee. Sponsor preps each spend 50000 → 49500 with 500 fee. Deposit, seal and
transfer each use one prep, preserve the two 1-sat pair outputs and return 48500
sats to the sponsor with a 1000-sat fee. Inventory setup total fee = 1000;
three prep fees = 1500; three transition fees = 3000. Service funding = 270000,
not the independently enforced 250000 pool cap (only 150000 enters the pool).

Buyer funding is **3000 total**, split into two 1500 sources, not a single 1–2k
output: each open/withdraw action needs its own canonical prep (500 fee) and
1000 transition fee. Each prep leaves exactly 1000 and its action consumes it,
with zero sponsor change. Two actions × (500 + 1000) = 3000. Fees are frozen
budgets, not miner quotes. If not admitted, HALT rather than silently raise fees.
No purchase proceeds or service sponsor change are recycled into buyer fees.

## 3. Fresh startup preflight and one mechanical funded command

Wait for all five service funding outputs to be confirmed. Payment MUST still
be unfunded, including mempool receipts. Run:

```sh
node mint/scripts/canary-preflight.js --stage startup "$HOME/boxsv-canary-service/config.json" "$HOME/boxsv-canary-service/startup.json"
# LATER owner-approved mainnet execution ONLY, from a real interactive terminal:
node mint/scripts/canary-run.js --owner-authorized "$HOME/boxsv-canary-service/config.json" "$HOME/boxsv-canary-service/startup.json" "$HOME/boxsv-canary-service/run-001"
```

Type the exact one-time challenge only after checking the reviewed commit and
composition. The report must be <=5 minutes old, not future-dated, startup PASS,
matching chain, buyer and addresses, inventory/sponsor EXACT_CONFIRMED_UNSPENT,
payment UNFUNDED. The runner independently repeats live startup preflight and
requires identical outpoints before creating the new run directory. An edited
PASS report cannot override fresh chain evidence. Wrong shape, early payment,
partial/extra/duplicate/unconfirmed funding or mempool spends fail closed.

Staged mainnet checks use WoC `/address/.../unspent/all`, reject pagination,
validate actual raw output values/scripts and active-block membership under a
stable tip, and reread UTXOs. `--stage inspect` preserves the earlier read-only
public-fixture path; it is never accepted as startup readiness.

Serial funded sequence (no `Promise.all` chain operations):

1. Owner gate → exact cap verification → fresh startup preflight → composition.
2. Prepare three sponsor parents; require five confirmations for each.
3. Inscribe the restricted `BoxSV-test` text NFT and create the anchored empty box.
4. Deposit → seal, verifying actual inputs, fee conservation and custody history.
5. Persist sealed manifest and its SHA-256 root commitment. This is a **local
   evidence commitment**, not a new on-chain Merkle/root protocol transaction.
6. Create one listing and durable owner-buyer reservation; then start service on
   `127.0.0.1:8090`. Print `PAY_ONLY_NOW`, exact 10000 sats and reservation ID.
7. Owner verifies address against offline xpub/0 and sends once. Serial WoC
   payment polling waits 15 seconds between polls. Pending exact payment waits;
   any wrong amount/shape halts for manual reconciliation. Exact confirmed
   payment stage is independently rechecked before transfer signing/submission.
8. Persist a 3-input transfer intent → submit once → prove active-block inclusion
   with exact bytes → mark TRANSFERRED → export buyer bundle → clean shutdown.

`--stage payment` reads **only the reserved payment role**, because startup
inventory/sponsor sources have now been spent. It requires exactly one confirmed
unspent 10000-sat output. Never weaken startup checks to allow early payment.
Both reservation and inclusion waits are bounded (240 polls; reservation one
hour). Preflight/indexer inconsistency, timeout, 429/5xx or changing tip halts;
there is no permissive fallback. Between ordinary HTTP reads the mainnet runner
paces requests at 1.5 seconds; periodic polling is >=15 seconds. Revalidation at
transaction boundaries is additional, not an independent polling scheduler.

## 4. Separate offline buyer open and withdrawal

The funded runner ENDS at confirmed transfer. Copy `run-001/buyer-bundle.json` to
the offline owner machine. Independently inspect its original inscription,
anchored box, complete history, sealed transfer owner and fees. Obtain parent
raw hex for the two confirmed 1500-sat buyer P2PKH fee outputs using GET-only
wallet/indexer reads. Create `fee-sources.json` (public data only):

```json
[
  {"raw":"RAW_PARENT_TRANSACTION_HEX_FOR_FIRST_1500_OUTPUT","index":0},
  {"raw":"RAW_PARENT_TRANSACTION_HEX_FOR_SECOND_1500_OUTPUT","index":1}
]
```

Indexes must be the actual output indexes; the outputs may share a parent but
must be distinct outpoints. On the offline wallet machine:

```sh
node mint/scripts/canary-buyer.js "$HOME/boxsv-canary-owner/buyer-bundle.json" "$HOME/boxsv-canary-owner/buyer.wif" "$HOME/boxsv-canary-owner/fee-sources.json" "$HOME/boxsv-canary-owner/signed.json"
```

This tool performs no networking. It verifies genesis-anchored history, buyer
ownership, fee source amounts and both covenant actions before emitting four
signed transactions: open prep → open → withdrawal prep → withdrawal.
Copy **only signed.json** back to an online operator machine. Independently
review it, then use a second deliberate owner-gated publication:

```sh
# LATER owner action, not part of build verification:
node mint/scripts/canary-publish.js --owner-authorized /ABSOLUTE/signed.json /ABSOLUTE/NEW/buyer-publication-evidence
```

The publisher has no keys. It rechecks UTXOs, local signatures, exact fees and
serial predecessor links, writes each intent before submission and waits for
confirmed inclusion before the next. It uses the same gated WoC adapter and
requires a new interactive challenge. Verify both final 1-sat outputs belong to
the buyer. Abnormal interruption requires manual reconciliation, never rerunning
the whole file blindly. The regtest rehearsal performs these buyer actions on
its guarded node, separately from the stopped funded runner.

## Adapter and reconciliation boundaries

WoC is pinned to `https://api.whatsonchain.com/v1/bsv/main/`. Raw `/hex` replies
are text/plain; broadcasting sends JSON `{txhex:...}` to `POST /tx/raw`, accepts
only the matching plain/JSON-string txid, uses a bounded timeout and refuses
redirects. All other adapter operations are allowlisted GETs. Covenant UTXOs use
reversed SHA-256 script hashes and complete unspent responses with explicit
mempool-spend rejection. ARC fallback is deliberately absent: an ambiguous
primary response must NOT become another submission path.

On any failure: stop scheduling, preserve intents, raw bytes, journal locks and
funding reservations, reconcile every input/outpoint and active-chain result.
Never delete a live lock, allocate a replacement sponsor parent or change fees
to cure uncertainty. Normal cleanup closes the listener/store/pool; abnormal
process death may leave locks for manual investigation. Late/partial/excess or
unassigned payments require manual owner refund review. A transferred box cannot
be revoked or refunded as though delivery never happened. Payment finality is
indexer evidence, not SPV or atomic delivery-versus-payment.

Per-transaction evidence separates actual fees, preserved principal and change;
never report pool held/dispensed sats as fees. `pool.jsonl` and `sales.jsonl` are
write-ahead/fsynced. Inventory/deposit/seal signed intents and submission budgets
are fsynced before POST; uncertain transfer stays quarantined with one attempt.
The run is never auto-resumed or expanded beyond one box.

Existing public A/B URLs are historical **VAULT-0001**, not this newer ordinal
pair contract. The legacy checker does not certify these new boxes. Verify with
`verifyHistory`, active chain raw bytes, both UTXOs and the evidence pack. Regtest
PASS and public GET PASS establish neither commercial miner admission nor an
independent security audit. Actual funded execution remains a later owner gate.
