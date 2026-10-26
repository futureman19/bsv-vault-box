# VAULT-0003: Draw-at-Open — Trustless Mystery Layer
**Status:** DRAFT · **Version:** 0.1.0 · **Date:** 2026-10-26
**Depends on:** VAULT-0001 · **Companion:** `v3_ref.py` (reference PoC, executed), `v3_vectors.json`
**Supersedes:** VAULT-0002 (committee key-release) for products where no trusted third party is acceptable. VAULT-0002 remains the only path for *fixed-before-sale hidden contents*; VAULT-0003 is the trustless alternative that trades "fixed" for "no trust."

---

## 1. Abstract

A VAULT-0003 box is a VAULT-0001 sealed vault whose contents are **not assigned at creation**. The full inventory — every design, its rarity weight, its metadata — is committed on-chain before the first box sells. Opening draws the assignment deterministically from the box ID and the hash of a block that does not exist until the opening is already broadcast. Nobody — issuer, owner, or miner below 51% cost — can know or influence the outcome beforehand, and anyone can recompute it afterward. No committee, oracle, server, or trusted party of any kind.

This is the "Copenhagen" box: no hidden fact of the matter exists until opening collapses it. (The physical-Pokémon, fixed-contents version requires VAULT-0002's trusted keepers or future witness-encryption math.)

## 2. Draw semantics — Version A (with replacement), pack model

Each box contains a **pack of N cards** (default N = 10; the format supports any N, e.g. 100). Each card is an independent draw from the full inventory, derived from a per-slot seed (§6). Duplicates of a design can exist across boxes; each minted instance is unique by construction (identity = `(design_id, box_id, slot)`).

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
     "manifest_version": 1 }
   ```
   Weights are integers; rarity = weight / total_weight. The manifest is PUBLIC by design — buyers must be able to audit the odds (and any per-slot guarantees) before paying.
2. **Manifest root** = SHA-256 of the canonical manifest bytes. Every box's covenant `content_ref` field carries this root (repurposing VAULT-0001's field: for mystery boxes it commits the catalog, not a specific content).

Immutability follows from VAULT-0001: `content_ref` can never change, so every box is welded to the manifest it was born under.

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
        draw_index = SHA256("VAULT3-DRAW" || box_id || seed || slot || retry) mod table.total_weight
        design     = walk table weights in order until cumulative > draw_index
        if allow_pack_duplicates or design not already drawn FROM THIS TABLE: accept, break
        retry += 1                                                        // deterministic rejection sampling
```

- **Dedup scope is per-table** (prevents non-termination): main-table slots dedup among themselves; a slot with its own table (e.g. guaranteed-rare) dedups only against slots sharing that table — its card may coincide with a main-table pull, exactly like a physical pack's rare slot.
- **Manifest validity rule:** with `allow_pack_duplicates: false`, every table must contain at least as many designs as the number of slots bound to it.

- **Everything is replayable:** box_id, block hash, slot, retry are all public or derivable — any verifier recomputes the entire pack bit-for-bit.
- **D = 0** (hash of the open block itself) is acceptable for low-value boxes; the including miner could orphan-and-remine for a reroll at block-reward cost.
- **D = 1** (the *next* block) is the default: the miner who includes the opening cannot know the outcome at inclusion time, and manipulating it requires mining two consecutive blocks. The reveal finalizes one block after opening — a small, honest delay.
- The draw is **client-verified**, not script-enforced: Bitcoin Script cannot read block headers, so the covenant enforces the state machine (VAULT-0001, unchanged) and the pack contents are a deterministic public function of chain data. Every wallet, indexer, and marketplace computes the same pack; a wrong claim is objectively refutable.

## 7. Opening and pack minting

1. Owner broadcasts VAULT-0001 `open` — seal breaks on-chain, irreversible.
2. After the draw block exists, anyone computes the full pack from §6.
3. The opener mints the pack in one child transaction of the opening tx, tagged `VAULT3-MINT`, carrying `{manifest_root, box_id, designs: [d0..dN-1]}` — one inscription per card (each its own 1Sat ordinal, individually tradable) or a single pack inscription with the ordered list (cheaper; cards tradable as a unit). Validity rule (client-enforced): **the mint is valid iff the design list equals the recomputed pack, in slot order, including retry replays.** Any deviation = invalid, MUST be rejected by indexers and marketplaces.
4. Opened box, pack, and individual cards are independent collectibles; all transferable (VAULT-0001 opened-transfer for the box).

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
