# VAULT-0001 — Sealed Vault Boxes on BSV

> **Custody status:** the deployed VAULT-0001 contract enforces a seal and immutable content commitment, not custody of the referenced NFT UTXOs. The new [BOX-NATIVE-1 local research lab](BOX-NATIVE-1-DRAFT.md) executes a singleton native-token wrapper in Script, but is **not the requested external-NFT vault** and must not be funded or deployed. External deposit/release, multi-item conservation, fee sponsorship, and chain-aware verification remain unimplemented.

**A digital safe-deposit box with a break-once, publicly verifiable seal — enforced by BSV consensus, not by any company.**

A vault box is a UTXO carrying a covenant (state machine) with exactly three legal moves:

- **transfer sealed** — ownership changes, box stays sealed
- **open** — one-way, irreversible, publicly visible
- **transfer opened** — opened boxes stay collectible

Everything else — re-sealing, swapping the contents, destroying the box — is impossible by consensus rule. Anyone can verify a box's seal from public chain data alone.

## Live on mainnet (2026-10-26)

| Box | Current tx | State | Verify |
|---|---|---|---|
| Box A | `f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39` | **SEALED** (stays sealed forever) | [WoC](https://whatsonchain.com/tx/f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39) |
| Box B | `2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f` | **OPENED** | [WoC](https://whatsonchain.com/tx/2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f) |

Box A lineage: deploy `fe2c763f…e95d` → sealed transfer `f3590347…dd39`. Box B lineage: deploy `9a3007e5…0303` → open `2aaa4efa…e67f`. The seal flip is a single on-chain state byte (`00`→`01`) in the covenant trailer, enforced by the compiled contract in `vault/artifacts/vault.json`.

## Live site — boxsv.com

- **https://boxsv.com** — landing: the vault claw machine (demo play + wallet connect; real minting switches on at launch)
- **https://boxsv.com/check.html** — the zero-dependency seal checker: paste a box's current holding txid, get a verdict from public data (old github.io URL redirects)

## Repo map

- `VAULT-0001-sealed-boxes.md` — the standard (Draft): wire format, state machine, seal-check algorithm, graduation criteria
- `VAULT-0002-committee-release.md` — committee key-release layer (Draft; shelved — requires trusting k-of-n keepers, rejected on no-third-party grounds; remains the only path for *fixed-before-sale hidden* contents)
- `VAULT-0003-draw-at-open.md` — **the chosen mystery layer (Draft):** trustless draw-at-open packs. Committed on-chain inventory + odds before sale; opening draws a 10-card pack from box_id + future block hash; verifiable rejection sampling (no within-pack dupes), guaranteed-rare slots, zero trusted parties
- `v3_ref.py` + `v3_vectors.json` — VAULT-0003 reference PoC, executed (15/15): determinism + independent replay, no-pack-before-collapse, rarity distributions match weights, coupon-collector stats, reorg consistency, invalid-mint rejection
- `v2_ref.py` + `v2_vectors.json` — VAULT-0002 reference PoC, executed: Feldman-verifiable per-box shares over secp256k1 stand in for threshold BLS-IBE (15/15)
- `sealed-box-report.md` — the feasibility research behind it: why fixed-content-hidden-until-opening needs a key-release committee (VAULT-0002), full threat model, prior art
- `vault/` — the sCrypt covenant (compiled, script-VM tested 8/8, deployed to mainnet)
- `vault_ref.py` + `vault_vectors.json` — Python reference implementation + golden vectors (16/16)
- `sealed_box_prototype.py` + `prototype_results.json` — executed attack PoCs (every pure-BSV secrecy shortcut demonstrated failing)
- `docs/` — the seal checker (static, zero dependencies, `vaultcheck.js` runs in browser and Node)

## Status

**Draft.** Graduated: covenant compiled + mainnet-exercised; script-VM attack suite green; live seal checker. Pending for Stable: second-implementation byte parity on golden vectors, SPV-tier seal verification, 1Sat ord-envelope alignment for indexer discovery. **VAULT-0002 spec + executed PoC now in-repo** (Draft): committee key-release delivers hidden-until-opening contents; production graduation needs a real threshold-BLS swap + a live 3-operator testnet seal league.

## Honest scope note

The on-chain seal (break-once state machine, immutable content commitment, public verification) is fully trustless and live. The mystery layer is **VAULT-0003 draw-at-open**: provably fair packs drawn from a committed inventory at opening, no committee, no oracle, no server. The trilemma — {fixed before sale, hidden which one, no trusted party}, pick two — is documented in the report; VAULT-0002 (committee) remains on the shelf for the fixed+hidden corner if it's ever wanted.
