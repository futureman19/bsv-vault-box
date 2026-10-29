# BOX-MINT-1 — Draft: mint/sale backend specification

## Status and scope

Draft specification for the service that turns the verified prototype into sales.
**No implementation in this document's commit.** Inputs: `BOX-ORDINAL-SPONSOR-1-DRAFT.md`
(contract + sponsorship rules), `BOX-ORDINAL-FULLNODE-VALIDATION.md` (independent BSV
v1.2.3 node acceptance: deposit/seal/transfer/open/withdraw mined; 3 owner-confusion
attacks rejected), `VAULT-0003-draw-at-open.md` (manifest/draw/verify protocol).

This spec closes gate item "no production funding preparation/replenishment service"
and defines the remaining path to a mainnet canary. It does NOT authorize mainnet
value, change any deployed artifact, or resolve the owner decisions listed in §7.

## 1. Sale model (recommended)

**Pre-deployed sealed boxes; ownership transfer on payment.**

- The service mints an inventory of sealed boxes ahead of time: each is the verified
  covenant pair (1-sat ordinal companion + 1-sat box), owner = service inventory key,
  phase = SEALED, contents committed by manifest (draw-at-open, VAULT-0003).
- Buyer connects wallet on boxsv.com (already present), picks a box, pays the listed
  price to that box's unique payment address (§3).
- On confirmed payment the service broadcasts a **transfer** transition to the buyer's
  public key (owner field), sponsored per the bounded funding grammar.
- Buyer opens whenever they want; open/withdraw are signed client-side by their wallet.
  The covenant rejects any old-owner (service) open/withdraw — verified on the native
  node, so inventory keys cannot rug a sold box.

Fallback when inventory is empty: deploy-on-payment (deposit+seal with buyer as owner
at creation). Slower (two-stage confirmation) but no inventory lockup. Same builder.

Why transfer-based: every byte of this flow is already node-verified; the only new
machinery is operational (watching, signing, broadcasting, pooling), not contractual.

## 2. Components

1. **Payment watcher** — per-box HD-derived payment addresses; detection via indexer
   polling (bananablocks/WoC-compatible API) with N-confirmation finality before
   transfer broadcast. No local full node required (post-incident rule: node runs
   only via `vault/scripts/bitcoind-guard.sh`; mainnet node work stays out of scope).
2. **Transfer worker** — given (box UTXO pair, buyer pubkey), builds the sponsored
   transfer with the existing `vault/src/ordinal-pair.js` builder, signs with inventory
   + sponsor keys, broadcasts via ARC, tracks inclusion, retries with bounded backoff.
3. **Sponsor pool manager** — the piece the sponsor draft explicitly did not automate:
   maintains a queue of qualifying one-input/one-output P2PKH funding parents
   (≤108-byte scriptSig), replenishes from a capped hot wallet, enforces the
   in-Script fee cap (1..10000 sat; tests used 500), and accounts every sat.
4. **Mint worker** — inventory replenishment: inscribes the collectible ordinal,
   builds deposit+seal with manifest commitment, lands the pair on the inventory key.
5. **Sale API** — box listing (from inventory), price/address assignment, sale state
   machine (`LISTED → PAID_PENDING → TRANSFERRED → OPENED`), buyer-facing status for
   the site; the public checker stays zero-dependency and read-only.

## 3. Payment association and payout

- One fresh address per listed box (HD derivation from a service xpub) — no
  amount-based matching, no memo requirements, clean refunds on timeout.
- Payment finality: transfer only after 1 confirmation minimum (canary),
  revisit for volume. Unpaid reservations expire (address reuse is safe: expiry
  frees the box back to LISTED; late payments are refunded minus miner fee).
- Payout consolidation: proceeds sweep to the owner payout address on a schedule.
  **Payout address is an owner decision (§7).**

## 4. Key custody boundaries

| Key | Held by | Exposure |
|---|---|---|
| Buyer key | buyer wallet only | never touches the service |
| Inventory key | service (hot) | bounded: unsold inventory only; covenant blocks misuse of sold boxes (native-node verified) |
| Sponsor key | service (hot) | bounded: pool cap + per-tx fee cap enforced in Script; top-ups manual at canary |
| Payment xpub | service (watch-only) | no spending ability |

Precedent for hot-key handling on this machine: WIF via file only, 0600, never in
shell history or env dumps (same rule as the gryd sponsor key).

## 5. Mainnet fee policy — open risk

Tests used `minminingtxfee=0.00000001` locally; **that is not a miner quote**
(stated in both predecessor docs). A ~15.8 KB transfer at 500 sat is ~0.03 sat/byte
and may sit under real relay/mining policy. Before any sale:

1. Canary probe: one real mainnet transfer at the intended fee; measure admission +
   inclusion latency across at least two independent broadcasts.
2. If relay is slow/refused, raise the fee budget (still inside the 10000-sat Script
   cap) and re-probe. Price must absorb: transfer fee + one sponsor-prep fee + margin.

## 6. Test plan (no real money until the last step)

1. Extend `vault/scripts/fullnode-regtest.js` into a mint-backend integration run:
   watcher → payment detection (regtest-mined) → sponsored transfer → buyer-key
   open/withdraw, all against the official v1.2.3 binary, evidence captured.
2. Testnet pass with the real watcher/API path.
3. Mainnet canary: exactly one box, minimum price, owner as the buyer. Full evidence
   pack (txids, checker verdicts, fee accounting) before inventory scale-up.

## 7. Owner decisions required (not made here)

1. **Box price** (drives fee budget + inventory size).
2. **Payout address** (where proceeds consolidate).
3. **Launch inventory size** (sats locked as 1-sat pairs are trivial; ordinal
   collectibles + sponsor prep fees are not).
4. **Hosting** — idle Hetzner VPS vs fly.io (both available; VPS keeps BSV work off
   the gryd deploy path).
5. **Who sponsors buyer open/withdraw fees** — default assumption: buyer's wallet
   funds its own open (standard wallet behavior); service sponsoring those too is a
   product choice, not a technical gate.

## 8. Explicit non-goals for this milestone

No general inscription grammar, no covenant bytecode upgrade path, no SPV proof
service for buyers (checker stays WoC/bananablocks-backed), no security audit claim,
no marketing site changes. The demo on boxsv.com keeps working unchanged until the
sale API is proven on testnet.
