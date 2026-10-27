# VAULT-0003: Draw-at-Open — Trustless Mystery Layer
**Status:** DRAFT · **Version:** 0.1.0 · **Date:** 2026-10-26
**Depends on:** VAULT-0001 · **Companion:** `v3_ref.py` (reference PoC, executed), `v3_vectors.json`
**Supersedes:** VAULT-0002 (committee key-release) for products where no trusted third party is acceptable. VAULT-0002 remains the only path for *fixed-before-sale hidden contents*; VAULT-0003 is the trustless alternative that trades "fixed" for "no trust."

---

## 1. Abstract

A VAULT-0003 box is a VAULT-0001 sealed vault whose contents are **not assigned at creation**. The full inventory — every design, its rarity weight, its metadata — is committed on-chain before the first box sells. Opening draws the assignment deterministically from the box ID and the hash of a block that does not exist until the opening is already broadcast. Nobody — issuer, owner, or miner below 51% cost — can know or influence the outcome beforehand, and anyone can recompute it afterward. No committee, oracle, server, or trusted party of any kind.

This is the "Copenhagen" box: no hidden fact of the matter exists until opening collapses it. (The physical-Pokémon, fixed-contents version requires VAULT-0002's trusted keepers or future witness-encryption math.)

## 2. Draw semantics — Version A (with replacement), pack model

Each box contains a **pack of N cards** (default N = 10). Each card is derived from a per-slot seed (§6); draws are independent only when duplicates are allowed. Committed weights are **FIRST-SLOT marginals** for each table: `weight / total_weight`. No-duplicate later slots have different marginal probabilities, not the original weight ratios. Duplicates of a design can exist across boxes; each minted instance is unique by construction (identity = `(design_id, box_id, slot)`).

**Within-pack duplicates** are configurable per manifest:
- `allow_pack_duplicates: true` (simplest) — slots fully independent; a pack may contain two of the same design.
- `false` (physical-pack feel) — verifiable **rejection sampling**: a slot that draws a design already in the pack re-draws with an incrementing retry nonce until unique. Fully deterministic — any verifier replays the identical process and must land on the identical pack.

**Per-slot weight tables** (optional, physical-pack mechanics): the manifest may give some slots their own table — e.g. slots 0–8 draw from the common/uncommon table, slot 9 draws from a rares-only table ("guaranteed rare"). Each slot's table is committed in the manifest, so the guarantee is auditable before purchase.

Consequences, stated honestly:
- Opening all boxes does NOT populate the collection exactly once — expect ~63% of designs to appear across 1,000 single-draw equivalents.
- A true no-duplicates-across-boxes case (Version B) requires shared on-chain pool state, serializing all opens through one covenant. Out of scope here.

## 3. Trust model

None beyond BSV's own honest-majority mining assumption. There is no key material, no keeper, no oracle. The issuer's only powers end at creation (§4), after which the issuer is disappearable. Miner manipulation is priced at a block reward per reroll attempt (§9).

## 4. Inventory manifest and commitment

Before any box is sold, the issuer publishes on-chain:

1. **Manifest** (JSON, OP_RETURN, tagged `VAULT3-MANIFEST`):
   ```
   { "name": "...", "pack_size": 10,
     "allow_pack_duplicates": false,
     "designs": [
       {"id": 0, "ref": "<content hash/URL>", "weight": 500},
       {"id": 1, "ref": "<...>", "weight": 300}, ... ],
     "total_weight": 100000,
     "slots": { "9": { "table": [ {"id": 7, "weight": 90}, {"id": 8, "weight": 10} ],
                       "total_weight": 100 } },        // optional per-slot tables ("guaranteed rare")
     "slot_odds": [ ... ],                         // required exact rows, see §4.1
     "per_slot_odds_published": true,              // required if deviation > 1 percentage point
     "manifest_version": 1 }
   ```
   Weights are integers and specify FIRST-SLOT marginals, not universal per-slot rarity. The manifest is PUBLIC by design — buyers must be able to audit the odds (and any per-slot guarantees) before paying.
2. **Manifest root** = SHA-256 of the canonical manifest bytes. Every box's covenant `content_ref` field carries this root (repurposing VAULT-0001's field: for mystery boxes it commits the catalog, not a specific content).

Immutability follows from VAULT-0001: `content_ref` can never change, so every box is welded to the manifest it was born under.

### 4.1 Normative odds disclosure

Every no-duplicate manifest MUST additionally contain `slot_odds`, computed by the reference `computeSlotOdds` in `manifest.js`/`odds.js`. This is an array indexed by absolute slot, each containing `{ "id": <integer>, "probability": "<numerator>/<denominator>" }` rows in that slot's table order. Fractions MUST be reduced nonnegative base-10 integers with positive denominator (including `0/1` and `1/1`); no JSON floating-point values. They specify exact ideal weighted-without-replacement marginals, before the finite retry cap; modulo bias below `total_weight / 2^256` is not represented as advertised precision. Exhaustion is a failed draw, never a substitute card, and can affect the distribution conditional on successful packs. These fractions are not a claim of zero exhaustion probability.

For `[99,1]` and two main slots, the rows are `[99/100,1/100]` then `[1/100,99/100]`. A deviation of **more than 1 percentage point** from that table's first-slot weights requires explicit `per_slot_odds_published: true`; absent/false attestation MUST fail validation. Attestation alone is insufficient: missing or forged `slot_odds` MUST fail. The builder fills missing odds but never supplies attestation for the issuer. The fields are inside the manifest commitment; adding them changes its root, not the draw preimage.

The reference enumerates selected-count states grouped by equal weights (singleton groups are subset enumeration). A transition from state S to selecting group g has probability `remaining_count[g] * weight[g] / remaining_weight`; sum incoming probability mass, then divide a group's marginal equally among its designs. Thus the 1000-design Genesis table has only three weight groups and is computed exactly, not sampled. Main-slot index advances only for main-table slots. Every explicit slot has its own single-use table scope.

Resource limits: at most 100 slots, 10000 catalog designs, 20000 state transitions per table, and an 8192-bit incoming rational denominator. If exact computation exceeds a state/rational limit, the implementation supplies fixed-seed (`0x5641554c`, xorshift32) sampling diagnostics and rejects with `OddsUnavailable`. Sample count is `max(1,min(4096,floor(1000000/(slots*designs))))`; the reported simultaneous Hoeffding radius is `sqrt(log(2*slots*designs/1e-6)/(2*samples))`. This is a diagnostic confidence bound under an IID assumption, not a proof for a fixed PRNG. Estimates MUST NOT be published as exact odds or accepted via attestation. Such catalogs must be simplified before publication. Size-limit violations fail immediately. These conservative limits keep validation finite without mislabelling sampled probabilities as exact.

## 5. Box creation and minting of boxes

Boxes are ordinary VAULT-0001 covenant UTXOs: `box_id` (from genesis outpoint, per VAULT-0001 v0.2), state SEALED, `content_ref` = manifest root, owner = buyer. Claw-machine UI = the mint interface; the covenant is the box.

## 6. The draw function (per pack)

```
draw_block_height  = height(block containing the opening tx) + D      (D = 1 recommended)
seed               = blockhash(draw_block_height)

for slot in 0 .. pack_size-1:
    table          = slots[slot].table if defined, else designs
    table_key      = slot if slot has own table, else "main"
    retry          = 0
    loop:
        draw_index = SHA256(UTF8("VAULT3-DRAW|" + boxId + "|" + seed + "|" + slot + "|" + retry)) mod table.total_weight
        design     = walk table weights in order until cumulative > draw_index
        if allow_pack_duplicates or design not already drawn FROM THIS TABLE: accept, break
        if retry == 10000: throw DrawExhausted                            // never return a partial pack
        retry += 1                                                        // deterministic rejection sampling
```

- **Dedup scope is per-table** (prevents non-termination): main-table slots dedup among themselves; a slot with its own table (e.g. guaranteed-rare) dedups only against slots sharing that table — its card may coincide with a main-table pull, exactly like a physical pack's rare slot.
- **Manifest validity rule:** with `allow_pack_duplicates: false`, every table must contain at least as many designs as the number of slots bound to it. For a table bound to k >= 2 slots, reject when `(max_weight / min_weight) * k > 10000`, using exact integer comparison. After j < k accepted designs, rejected mass is at most `j*max_weight`, while remaining mass is at least `(n-j)*min_weight`, so expected retries are at most `j*max_weight/((n-j)*min_weight) <= (k-1)*max_weight/min_weight < k*max_weight/min_weight`. This is a conservative per-slot expectation bound, not a guarantee; geometric tails still require the runtime cap. Single-use explicit tables and duplicate-allowed draws do not reject duplicates and need no ratio constraint. An unsafe table raises typed `DrawExhausted` during validation, before hashing.

**Normative byte encoding:** hash UTF-8 bytes of exactly `"VAULT3-DRAW|" + boxId + "|" + seed + "|" + slot + "|" + retry`. Do not hash binary concatenation, reverse hashes, add spaces, BOM or a newline. Production `boxId` and `seed` are lowercase hexadecimal strings representing 32-byte hashes; slot and retry are zero-based unsigned decimal integers with no leading zeros except `0`. Fields containing `|` are invalid. The digest is interpreted as an unsigned big-endian integer, then reduced modulo table weight. Historical simulation APIs also accept nonempty well-formed text IDs such as `box-alpha`; callers MUST enforce production hash format at the chain boundary. This compatibility does not change any encoded bytes or historical vectors.

**Conformance vector (literal UTF-8 preimage, no trailing newline):**
```
VAULT3-DRAW|0000000000000000000000000000000000000000000000000000000000000000|1111111111111111111111111111111111111111111111111111111111111111|2|3
```
SHA-256 = `a3ae26ffa23407ba3010b78262b0bd33b3453527012c4f34ff3e0b6658a3bdbb`; modulo 100 = **91**. Inputs: boxId = 32 zero bytes rendered as hex, seed = 32 `11` bytes rendered as hex, slot = 2, retry = 3. This literal vector was independently hashed with Python hashlib and is asserted in JS and Python tests.

**Retry cap:** attempt nonce 0 followed by at most 10000 retries (nonces 1 through 10000). If nonce 10000 also repeats an already-selected design, throw `DrawExhausted` (`code: DRAW_EXHAUSTED` in JS); no partial pack or alternate seed is valid. A valid manifest can still exhaust at runtime.

- **Everything is replayable:** box_id, block hash, slot, retry are all public or derivable — any verifier recomputes the entire pack bit-for-bit.
- **D = 0** (hash of the open block itself) is acceptable for low-value boxes; the including miner could orphan-and-remine for a reroll at block-reward cost.
- **D = 1** (the *next* block) is the default: the miner who includes the opening cannot know the outcome at inclusion time, and manipulating it requires mining two consecutive blocks. The reveal finalizes one block after opening — a small, honest delay.
- The draw is **client-verified**, not script-enforced: Bitcoin Script cannot read block headers, so the covenant enforces the state machine (VAULT-0001, unchanged) and the pack contents are a deterministic public function of chain data. Every wallet, indexer, and marketplace computes the same pack; a wrong claim is objectively refutable.

## 7. Opening and pack minting

1. Owner broadcasts VAULT-0001 `open` — seal breaks on-chain, irreversible.
2. After the draw block exists, anyone computes the full pack from §6.
3. The opener mints the pack in one child transaction of the opening tx, tagged `VAULT3-MINT`, carrying `{manifest_root, box_id, designs: [d0..dN-1]}` — one inscription per card (each its own 1Sat ordinal, individually tradable) or a single pack inscription with the ordered list (cheaper; cards tradable as a unit). Validity rule (client-enforced): **the mint is valid iff the design list equals the recomputed pack, in slot order, including retry replays.** Any deviation = invalid, MUST be rejected by indexers and marketplaces.
4. Opened box, pack, and individual cards are independent collectibles; all transferable (VAULT-0001 opened-transfer for the box).

Both mint encodings below are normative for a single ordered pack payload:

- **Tradable inscription:** `OP_FALSE OP_IF <"ord"> OP_1 <"application/vnd.vault3-mint+json"> OP_0 <JSON> OP_ENDIF <locking script>`. JSON includes `protocol: "VAULT3-MINT"` plus `manifest_root`, `box_id`, and `designs`. The envelope precedes the spendable locking script; a single 1Sat pack inscription trades as a unit.
- **Lightweight record:** `[OP_FALSE] OP_RETURN <"VAULT3-MINT"> <JSON>`, with the same root, identity, and ordered designs. This is a non-spendable record, not itself a tradable ordinal.

The public checker supports exactly one pack payload across these encodings per mint transaction, rejects ambiguous duplicates (including mixed encodings), and applies identical child-transaction and recomputation checks. Split per-card inscriptions require separate aggregation support and are not supported by this checker.

## 8. Seal-check extension

VAULT-0001 §7 stands unchanged. For opened boxes, the checker additionally: fetches the opening block height, waits for draw block, recomputes the assignment, and verifies any presented mint matches. New verdict: `INVALID-MINT` (mint disagrees with the deterministic draw).

## 9. Adversarial analysis

| Adversary | Capability | Result |
|---|---|---|
| Owner | precompute outcomes | Cannot: draw block hash doesn't exist until after the open tx is buried (D≥1) or included (D=0). Withholding after broadcast is impossible — the tx is already public. |
| Owner grinding | try many openings | Each box is one UTXO; opening is irreversible and the box ID is fixed at creation. No free-choice input remains at open time. |
| Miner (D=0) | orphan + remine for reroll | Costs a block reward per attempt and risks losing to competing miners; priced defense. D=1 raises this to mining two consecutive blocks. |
| Issuer | rig the inventory | Manifest committed before sale; every box's content_ref welds it in. Changing odds post-launch is consensus-impossible. |
| Issuer | cherry-pick good boxes | All sealed boxes are identical (superposition). Nothing to pick. |
| Previous owner | retain influence | Draw depends on box_id + future block only. Nothing retained matters. |
| Reorg | open tx reorged out | Box reverts to sealed (UTXO unspent); a later re-open draws fresh. The NFT mint, being a child of the opening, dies with it — consistent by construction. |

## 10. Implementation boundaries

- **Consensus (covenant):** seal state machine, box_id immutability, content_ref = manifest root weld — all inherited from VAULT-0001, **no contract change required**.
- **Protocol/client validation:** manifest parsing, draw recomputation, mint validity — the same trust model as 1Sat ordinal metadata.
- **Off-chain:** claw-machine animation, odds display, reveal UX.

## 11. Graduation (Draft → Stable)

1. Reference PoC executed: `v3_ref.py` — simulated chain + manifest + draws (see test output). **DONE.**
2. `vaultcheck` extension: recompute draws for opened boxes, `INVALID-MINT` verdict, live against the two mainnet boxes' successors.
3. Regtest lifecycle: manifest → mint 3 boxes → sealed transfer → open → draw → mint instance → verify → invalid-mint rejection.
4. Mainnet: one manifest + a small genesis run of boxes with a public odds table.

## Appendix A — PoC scope note

`v3_ref.py` simulates the chain (block hashes as deterministic stand-ins) and executes: manifest immutability, pack-draw determinism and replay-verification, un-openable-before-collapse, no-duplicates-within-pack via deterministic rejection sampling, guaranteed-rare slot tables, rarity distribution sanity over many packs, cross-box duplicate statistics (Version A honesty), reorg → reseal consistency, and invalid-mint rejection. All simulated; no broadcast, no real keys.
