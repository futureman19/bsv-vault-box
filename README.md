# VAULT-0001 — Sealed Vault Boxes on BSV

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

## Seal checker (live)

Paste a box's current holding txid, get a verdict from public data: **https://futureman19.github.io/bsv-vault-box/**

## Repo map

- `VAULT-0001-sealed-boxes.md` — the standard (Draft): wire format, state machine, seal-check algorithm, graduation criteria
- `sealed-box-report.md` — the feasibility research behind it: why fixed-content-hidden-until-opening needs a key-release committee (VAULT-0002), full threat model, prior art
- `vault/` — the sCrypt covenant (compiled, script-VM tested 8/8, deployed to mainnet)
- `vault_ref.py` + `vault_vectors.json` — Python reference implementation + golden vectors (16/16)
- `sealed_box_prototype.py` + `prototype_results.json` — executed attack PoCs (every pure-BSV secrecy shortcut demonstrated failing)
- `docs/` — the seal checker (static, zero dependencies, `vaultcheck.js` runs in browser and Node)

## Status

**Draft.** Graduated: covenant compiled + mainnet-exercised; script-VM attack suite green; live seal checker. Pending for Stable: second-implementation byte parity on golden vectors, SPV-tier seal verification, 1Sat ord-envelope alignment for indexer discovery, VAULT-0002 (committee key-release for hidden contents).

## Honest scope note

The on-chain seal (break-once state machine, immutable content commitment, public verification) is fully trustless today. Contents *hidden from the owner until opening* requires the VAULT-0002 threshold key-keeper committee — the research report proves no pure-chain construction can provide it, and names exactly that relaxation. Don't let anyone sell you "sealed" without it.
