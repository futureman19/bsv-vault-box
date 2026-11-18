# VAULT-0001 — Sealed Vault Boxes on BSV

> **Custody status:** the deployed VAULT-0001 contract enforces a seal and immutable content commitment, not custody of the referenced NFT UTXOs. The new [BOX-NATIVE-1 local research lab](BOX-NATIVE-1-DRAFT.md) executes a singleton native-token wrapper in Script, but is **not the requested external-NFT vault** and must not be funded or deployed. External deposit/release, multi-item conservation, fee sponsorship, and chain-aware verification remain unimplemented.

**A digital safe-deposit box with a break-once, publicly verifiable seal — enforced by BSV consensus, not by any company.**

A vault box is a UTXO carrying a covenant (state machine) with exactly three legal moves:

- **transfer sealed** — ownership changes, box stays sealed
- **open** — one-way, irreversible, publicly visible
- **transfer opened** — opened boxes stay collectible

The VAULT-0001 covenant prevents resealing and changes to its committed hash. It does not hold the referenced NFT UTXOs and cannot prevent their removal or substitution. The public checker uses WhatsOnChain transaction and unspent responses; it is not independent full-node/SPV verification.

## Live on mainnet (2026-10-26)

| Box | Recorded tx | State | Verify |
|---|---|---|---|
| Box A | `f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39` | **SEALED** (recorded at that transaction) | [WoC](https://whatsonchain.com/tx/f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39) |
| Box B | `2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f` | **OPENED** | [WoC](https://whatsonchain.com/tx/2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f) |

Box A lineage: deploy `fe2c763f…e95d` → sealed transfer `f3590347…dd39`. Box B lineage: deploy `9a3007e5…0303` → open `2aaa4efa…e67f`. The seal flip is a single on-chain state byte (`00`→`01`) in the covenant trailer, enforced by the compiled contract in `vault/artifacts/vault.json`.

## Live site — boxsv.com

- **https://boxsv.com** — landing: the vault claw machine (demo play + wallet connect; no mint, checkout or paid prize; future activation needs separate approval)
- **https://boxsv.com/check.html** — the zero-dependency seal checker: paste a box's current holding txid, get a verdict from public data (old github.io URL redirects)

## Repo map

- `VAULT-0001-sealed-boxes.md` — the standard (Draft): wire format, state machine, seal-check algorithm, graduation criteria
- `VAULT-0002-committee-release.md` — committee key-release layer (Draft; shelved — requires trusting k-of-n keepers, rejected on no-third-party grounds; remains the only path for *fixed-before-sale hidden* contents)
- `VAULT-0003-draw-at-open.md` — **historical research draft, not approved launch mechanics:** deterministic draw-at-open experiments using box_id + a future block hash. Reproducible sampling does not establish fair production randomness, buyer ordering or resistance to manipulation.
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

Historical mainnet VAULT-0001 records demonstrate a break-once seal commitment, not launch-NFT custody. Later narrow serialized custody fixtures and the separate continuous local Iceland integration are research evidence, not production wallet/payment integration or miner acceptance. The public reusable-Box experience is a simulation; covenant reuse remains unsupported.

The planned collection is **201 one-of-ones: 195 countries, five oceans and one Moon**. Each launch package is planned to contain one independent collectible Box NFT with a detached signed authenticity record, not an accessory or certificate NFT. Collection records remain unsigned candidates; a separate Iceland fixture exercises signed provenance. Art approvals, rights, storage and release remain gated.

Paid randomized allocation is a product preference, not an active or proven fair sale. Price, reserves, entropy, buyer ordering, odds, reveal and legal rules remain unset. Neither the historical VAULT-0003 draft nor public deterministic fixtures establish production fairness. No checkout or mint is active.
