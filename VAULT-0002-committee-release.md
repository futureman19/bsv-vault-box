# VAULT-0002: Committee Key-Release (Hidden Contents for Sealed Boxes)
**Status:** DRAFT (unproven — see §10 Graduation)
**Version:** 0.1.0 · **Date:** 2026-10-26
**Depends on:** VAULT-0001 (sealed vault boxes) · **Companion:** `v2_ref.py` (reference PoC, executed), `v2_vectors.json` (golden vectors)

---

## 1. Abstract

VAULT-0002 makes a VAULT-0001 box *opaque*: its contents are fixed at creation, encrypted on-chain, and undecryptable by everyone — owner, seller, issuer, public — until the box is opened on-chain. Opening is the sole trigger: a threshold committee of independent key-keepers observes the confirmed opening spend and publishes key shares; k shares decrypt the box. No issuer server, no trusted browser, no mandatory reveal date. Previous owners retain nothing, because no owner ever holds key material.

The research establishing why a committee (or equivalent) is *necessary* — no pure-BSV construction can bind learning to a public event — is `sealed-box-report.md`. This document names the relaxation precisely and engineers it to be as small, accountable, and open as possible.

## 2. Trust model — read this first

Two user-facing facts, stated before any mechanics:

1. **Secrecy assumes an honest threshold.** If k or more key-keepers collude, they can decrypt any box silently, at any time, leaving no trace. Nothing on any chain prevents this in 2026; the design makes collusion *attributable* (every release share is operator-signed) and *detectable* (any release without a confirmed opening is public proof of misbehavior).
2. **Liveness assumes a quorum survives.** If fewer than k operators remain before a successful key handoff, unopened boxes stay sealed forever. Proactive refresh (§8) mitigates churn; it cannot resurrect a dead quorum.

Everything else — box ownership, the sealed/opened state machine, content immutability, seal verification — is pure VAULT-0001 consensus + public data, no committee trust.

## 3. Roles

- **Issuer** — creates the NFT inventory, encrypts assignments, runs at most one mix hop. Disappearable after launch.
- **Committee operators** (n of them, threshold k) — hold DKG shares of the joint key; watch BSV; release per-box key shares per §6. v0: a fixed, publicly named federation (a "seal league," drand-style). Staking/slashing: future work.
- **Owners** — hold only their spending keys. Never key material.
- **Verifiers** — anyone with chain access: buyers, marketplaces, indexers.

## 4. Setup (once, at creation)

1. Committee runs a GJKR/Pedersen DKG over BLS12-381 → joint public key `PK`, per-operator verification keys `VK_i`. All published in the **setup transaction** with the inventory commitment and box count, so committee membership and the inventory are pinned to the same anchor.
2. Issuer encrypts each box's content with Boneh–Franklin IBE (tlock construction) under `PK`, identity `I_b = "VAULT2:" || box_id`. The same BLS machinery that powers drand timelock — except the identity is a *box opening*, not a clock round. Ciphertexts go on-chain (1Sat envelope or OP_RETURN; BSV has no practical size limit).
3. Assignments are hidden from the issuer itself by a verifiable re-encryption mix-net over the encrypted inventory (ZKShuffle-class proofs). No single party learns box→NFT unless all mixers collude.
4. Each box is created as a VAULT-0001 covenant UTXO whose `content_ref` commits to its ciphertext.

## 5. Why IBE-by-opening (and not simpler things)

- Per-box symmetric keys held by owners → offline peeking (executed failure in the prototype).
- Keys derived from signatures → offline-computable (executed).
- drand timelock → release gated by a clock, not by the owner's choice; sealed boxes become quietly inspectable after the time passes.
- The IBE identity being the *box id* means the committee's release policy (§6) is the only path to the key, and the key for one box reveals nothing about any other.

## 6. Release policy (the predicate every operator independently enforces)

Operator `i` releases share for box `b` **iff all hold**:

1. A transaction spending the *current* seal UTXO of `b` is confirmed ≥ K deep (K = 6 recommended). The spend must be covenant-valid: canonical VAULT-0001 artifact fingerprint, state flip SEALED→OPENED, box_id preserved.
2. The opening transaction itself is the release request — no extra round-trip, no flag byte required, no VAULT-0001 format change. (The §8 hook from VAULT-0001 remains as an optional explicit-request push for indexer convenience.)
3. Operator has not previously released for `b` (idempotence).

Operator then posts a **release record** on-chain:

```
OP_FALSE OP_RETURN "VAULT2-REL" <box_id:32> <operator_idx:1> <ibe_key_share:48> <operator_sig>
```

- `ibe_key_share` = `H(I_b)^{sk_i}` (BLS share of the identity key); publicly verifiable against `VK_i` — anyone can check a share is genuine without aggregating.
- `operator_sig` = operator's attribution signature over the record. A release record for a box with no confirmed opening is *self-proving misbehavior*.
- Anyone (owner, marketplace, indexer) aggregates k valid shares → IBE private key for `I_b` → decrypts. Decryption is public-after-opening by design: an opened box's contents are public knowledge, matching physical packs.

Cost per opening: k small OP_RETURN transactions (~100 bytes each), paid by operators or sponsored by the opener's fee. Trivially cheap on BSV.

## 7. Extended seal check

VAULT-0001 §7 gains one clause. `SEALED(b)` ⟺
1. current seal UTXO unspent, state SEALED (consensus-checked, covenant fingerprint verified), AND
2. no confirmed opening record for `b`, AND
3. **no k aggregatable valid release shares for `I_b` exist on-chain** (release-record scan by protocol tag).

A box failing clause 3 while its UTXO sits unspent is `UNSEALED-DISCREPANCY` — leaked or reorged — and MUST NOT trade as sealed. This is the distinction between "unopened" and "uninspected," enforced from public data.

## 8. Churn and longevity

- **Epochs with proactive refresh (CHURP-style):** each epoch the committee re-shares the joint key to the current operator set and publishes new verification commitments; old shares become useless. Compromise of < k operators per epoch heals.
- **Hard rule:** every refresh requires a live quorum. Operators exiting below k before handoff = permanent seal for all unopened boxes. v0 mitigation: n ≥ 7, k = ⌈n/2⌉ + 1…2/3, operators with public identities and independent infrastructure, documented succession contacts.
- **Sunset path:** if the federation ever votes to dissolve honestly, it SHOULD bulk-release all remaining keys to a final on-chain record set (opening every box publicly) rather than let them brick — a policy choice for the league, not this spec.

## 9. Adversarial analysis

| Adversary | Capability | Result |
|---|---|---|
| Owner | sandbox any computation | learns nothing pre-open: ciphertext + committee key only |
| Previous owner | retained data | nothing retained; opening attempt spends a dead outpoint (invalid) |
| Issuer | creation-time data | no key shares (DKG), no permutation (mix-net); can't cherry-pick |
| ≤ k−1 colluding operators | their shares | below threshold: nothing. Their early/leaked releases are attributable |
| ≥ k colluding operators | silent decryption of any box | **breaks secrecy silently — the stated trust assumption**; detected only if they post releases |
| Miner | reorg ≤ K deep | releases gated on K conf; reorg past release → UNSEALED-DISCREPANCY, box unmarketable as sealed |
| Miner with private fork | forked "opening" | committee watches canonical chain; private forks don't reach watchers |
| Operator goes dark | liveness | k-of-n absorbs < n−k+1 losses; below k: §8 sunset rule |
| Indexer lying about releases | forged view | Tier-1 verifiers re-check shares against on-chain VK_i themselves |

## 10. Graduation (Draft → Stable)

1. Reference PoC executed: `v2_ref.py` — Feldman-verifiable per-box shares standing in for BLS-IBE (models release gating, aggregation, public share verification, discrepancy detection). **DONE** (see test output).
2. Production swap: replace the stand-in with tlock-style threshold BLS (drand libraries, forked) and real DKG; 3-operator local committee against BSV regtest with VAULT-0001 covenant openings.
3. Golden vectors pass under a second implementation.
4. A public testnet "seal league" of ≥ 3 independent operators runs one full box lifecycle.

## Appendix A — Reference PoC scope note

`v2_ref.py` uses per-box Feldman-verifiable Shamir shares over secp256k1 (stdlib-only, real curve math): dealer posts commitments, shares are publicly verifiable, k shares reconstruct only that box's key. It faithfully models the *protocol semantics* — release gating on confirmed openings, share verification, aggregation, discrepancy detection, attribution — while the production cryptographic wrapper (threshold BLS-IBE) is a drop-in per §10.2. Everything in the PoC is simulated; no real keys, no broadcast.
