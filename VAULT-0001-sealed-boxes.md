# VAULT-0001: Sealed Vault Boxes on BSV
**Status:** DRAFT (unproven — see §11 Graduation)
**Version:** 0.1.0 · **Date:** 2026-10-26
**Depends on:** 1Sat Ordinals envelope conventions (BRC-160 alignment), post-Genesis BSV Script (OP_PUSH_TX covenant capability)
**Companion files (same directory, same commit):** `vault_ref.py` (reference implementation + tests), `vault_vectors.json` (golden vectors)

---

## 1. Abstract

A Vault Box is a BSV UTXO with a consensus-enforced two-state lifecycle — **SEALED → OPENED** — that is transferable in either state, cannot be re-sealed, and carries an immutable content commitment from creation. This document specifies the wire format, state machine, covenant rules, and the public seal-check algorithm. It defines the *wrapper* (verifiable, break-once, on-chain). The *opacity* layer (contents hidden from the owner until opening via threshold key release) is a separate extension, VAULT-0002, hooked in via §8 — the state machine here is designed so VAULT-0002 attaches without format changes.

## 2. Definitions

- **box_id** — 32-byte identifier: `sha256d(genesis_outpoint)` where genesis_outpoint is the txid‖vout of the transaction output that created the box. Stable across all transfers.
- **content_ref** — 32-byte commitment to the box's content descriptor, fixed at creation and immutable forever. In MODE-OPEN this commits to plaintext metadata; in MODE-SECRET it commits to the ciphertext (VAULT-0002).
- **state** — one byte: `0x00` SEALED, `0x01` OPENED.
- **owner_pkh** — 20-byte HASH160 of the current owner's public key.
- **lineage** — the unique chain of vault UTXOs from genesis outpoint to current UTXO.
- **release record** — (MODE-SECRET only) an on-chain attestation that key material for a box has been released. Format defined in VAULT-0002; the seal-check algorithm in §7 already consumes it.

## 3. Design invariants

1. A vault UTXO can be spent only by a transaction that recreates exactly one vault output for the same box_id with an allowed transition (§5). The covenant enforces this in consensus; clients enforce it again off-chain (§6).
2. box_id and content_ref are immutable across the entire lineage.
3. state is monotone: SEALED may become OPENED; OPENED may never become SEALED.
4. Every spend requires a signature from the current owner_pkh.
5. Seal status is computable from public chain data alone (§7), with no trusted party and no issuer involvement.

## 4. Wire format

### 4.1 Locking script layout

```
<vault covenant prefix>  OP_CODESEPARATOR  <ord envelope>
```

**Vault covenant prefix** (authoritative state — consensus-enforced):

```
push(state)            ; 1 byte
push(box_id)           ; 32 bytes
push(content_ref)      ; 32 bytes
push(owner_pkh)        ; 20 bytes
<COVENANT_BODY>        ; constant compiled covenant code (Appendix A)
```

The constant COVENANT_BODY bytes for this spec version are the canonical script body; a decoder verifies a vault UTXO by checking the bytes after the four data pushes equal the canonical body exactly (ref impl: `CANONICAL_BODY`). This defeats lookalike scripts carrying vault-shaped data without vault rules. **Draft note:** the reference implementation uses a placeholder body constant; it is replaced by the compiled sCrypt artifact at graduation (§11).

**Ord envelope** (metadata mirror — 1Sat-aligned, BRC-160):

```
OP_FALSE OP_IF "ord" OP_1 "application/vnd.vault+json" OP_0 <json> OP_ENDIF
```

The JSON metadata MUST contain `box_id`, `content_ref`, `state`, `owner_pkh` mirroring the covenant pushes, and MAY carry display fields (`name`, `image`, `collection`). On any mismatch, **covenant pushes are authoritative** and indexers MUST flag the output TAMPERED. The envelope exists so generic 1Sat indexers can discover vault boxes; the covenant prefix is what gives the fields meaning.

### 4.2 Spends

The unlocking script supplies: `<sig> <pubkey> <tx preimage material per COVENANT_BODY>`. Standard SIGHASH_ALL. (MODE-SECRET opening adds a release-request flag push; see §8.)

## 5. State machine

| From | To | Name | Consensus rules (covenant-enforced) |
|---|---|---|---|
| SEALED | SEALED | transfer | owner sig valid; exactly one vault output; box_id, content_ref, state unchanged; owner_pkh updated |
| SEALED | OPENED | open | owner sig valid; exactly one vault output; state := OPENED; box_id, content_ref unchanged; owner_pkh may update (self-open or open-to-recipient) |
| OPENED | OPENED | transfer | owner sig valid; exactly one vault output; state unchanged |
| * | * | anything else | **invalid**: no reseal, no content substitution, no box_id change, no fan-out of vault outputs, no state outside {0,1} |

Destruction is deliberately impossible within the covenant: a vault UTXO cannot be spent to a non-vault output. (Burn addresses, if ever desired, would be a separate spec; a broken-wrapped box is indistinguishable from a sealed one otherwise.)

## 6. Client-side transition validation (indexers, marketplaces)

Every implementation MUST re-validate each lineage transition off-chain: decode both spent and created vault outputs (§4), check the §5 table, check the canonical COVENANT_BODY, and check the ord-envelope mirror consistency. A single invalid transition marks the box TAMPERED permanently. This is the "protocol/client validation" layer: consensus rules stop invalid spends from confirming at all; client validation is defense in depth for thin-indexer users and catches covenant-template forgeries.

## 7. Seal-check algorithm (the public verifiability core)

Input: box_id, a chain-data source (§9 tiers), confirmation threshold K (RECOMMENDED: K ≥ 6 for high-value boxes; K ≥ 3 minimum).

```
SEAL-STATUS(box_id):
  1. Trace the lineage from genesis outpoint to the current vault UTXO,
     validating every transition per §6.
     - lineage broken or unresolvable           → UNKNOWN (indexer gap; do not trust)
     - any transition invalid                   → TAMPERED
  2. If current UTXO is spent by an opening transition with ≥ K conf:
     → OPENED-VERIFIED
  3. If current UTXO is unspent, state = SEALED:
     - (MODE-SECRET) if any release record for box_id exists on-chain
       → UNSEALED-DISCREPANCY                   (key released without a confirmed opening — e.g. deep reorg or leak; box MUST NOT trade as sealed)
     - otherwise → SEALED-VERIFIED
```

Properties: fully public-data; no issuer; "unspent" is necessary but **not** sufficient (step 3's release-record check is what separates "unopened" from "uninspected" in MODE-SECRET — see companion research report `sealed-box-report.md`, §4 items 12–14).

## 8. MODE-SECRET hook (VAULT-0002, forward compatibility)

MODE-OPEN boxes carry plaintext-referenced content; the seal is purely the state machine (valuable for bank-box/escrow semantics where the owner knows what's inside). MODE-SECRET boxes set content_ref := hash of the threshold-encrypted ciphertext and rely on VAULT-0002: a k-of-n key-keeper committee that publishes per-box key shares on-chain only after observing an opening transition with ≥ K confirmations. The opening spend in MODE-SECRET carries one extra push (release-request flag) so watchers can index release requests deterministically. VAULT-0001 implementations MUST ignore-but-preserve unknown extra pushes in the opening unlocking script, so VAULT-0002 deploys without a format fork.

## 9. Verification tiers

- **Tier 0 — trusted indexer** (1sat-server / WhatsOnChain-style APIs): fast, custodial-grade trust. Wallets may default here but MUST label it.
- **Tier 1 — SPV**: lineage txs verified by merkle proofs against block headers; header chain validated by proof-of-work. Trustless for confirmation status; the RECOMMENDED minimum for marketplaces.
- **Tier 2 — full scan**: independent node. Reference for dispute resolution.

## 10. Security considerations

- **Forged vaults:** scripts with vault-like data but non-canonical COVENANT_BODY are not vaults; §4.1 body check is mandatory.
- **Envelope/covenant mismatch:** treated as TAMPERED, not as a soft error.
- **Reorgs:** opening (and in MODE-SECRET, key release) is only meaningful ≥ K conf; see research report §4 item 12 for the residual silent-leak risk and its mitigations in MODE-SECRET.
- **Low-entropy content:** in MODE-OPEN, content_ref commitments over guessable content are enumerable; MODE-OPEN users should treat content as public-by-default. MODE-SECRET exists precisely for hidden content.

## 11. Graduation (Draft → Stable)

Per the spec-development pipeline, this spec remains **Draft** until ALL of:
1. ~~COVENANT_BODY placeholder replaced by a compiled sCrypt artifact~~ **DONE — mainnet, not just regtest (2026-10-26):** covenant compiled with scrypt-ts 1.20.0 (4,560-byte script) and exercised live on BSV mainnet: Box A deploy `fe2c763f0a4fa1c01ef2af8f4c0628d89d6e1389d995b0a5e202e06baafae95d` → sealed transfer `f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39` (remains SEALED, unspent); Box B deploy `9a3007e5ace7a1c1dafe23017e4c0a6ad1b04dbc4919cc57f8464a9f03e70303` → open `2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f` (state byte 00→01 in the script trailer). Lineage and covenant bytes verified against public chain data. Funding: Dogfood vault policy-gated send (tx `039afde2…804e3`). All 8 script-VM graduation tests also pass. Deployment script: `vault/scripts/mainnet-cycle.ts`. Deployment note: boxId/contentRef were set as commitment props; spec §2's outpoint-derived box_id binding is the reference for v0.2.
2. Golden vectors (`vault_vectors.json`) pass under a second, independent implementation (e.g. a TypeScript decoder built from this document alone). Partially de-risked: the Python reference implementation and the sCrypt covenant now agree on the state machine semantics, but byte-level envelope parity is not yet claimed.
3. Seal-check demonstrated end-to-end against a Tier-1 SPV data source.
Validated so far: wire format, state-machine semantics, seal-check logic (`vault_ref.py`, executed) + covenant script execution (`vault/tests/vault.test.ts`, 8/8). Pending: on-network deployment, second-implementation byte parity, SPV wiring.

## Appendix A — Reference covenant (compiled artifact, graduation-tested)

The normative implementation is `vault/src/contracts/vault.ts` (compiles to `vault/artifacts/vault.json`; property is named `boxState` because `state` is a reserved sCrypt keyword). Core logic:

```ts
export class Vault extends SmartContract {
  @prop(true) boxState: bigint         // 0n = SEALED, 1n = OPENED
  @prop() boxId: Sha256                // immutable
  @prop() contentRef: Sha256           // immutable
  @prop(true) owner: PubKey

  @method()
  public transfer(sig: Sig, nextOwner: PubKey) {
    assert(this.checkSig(sig, this.owner), 'owner signature required')
    assert(this.boxState == 0n || this.boxState == 1n, 'invalid boxState byte')
    this.owner = nextOwner                       // boxState/contentRef untouched -> preserved
    const amount: bigint = this.ctx.utxo.value
    const outputs: ByteString = this.buildStateOutput(amount) + this.buildChangeOutput()
    assert(this.ctx.hashOutputs == hash256(outputs), 'hashOutputs mismatch')
  }

  @method()
  public open(sig: Sig) {
    assert(this.checkSig(sig, this.owner), 'owner signature required')
    assert(this.boxState == 0n, 'only a sealed box can be opened')
    this.boxState = 1n                           // irreversible: no method clears it
    const amount: bigint = this.ctx.utxo.value
    const outputs: ByteString = this.buildStateOutput(amount) + this.buildChangeOutput()
    assert(this.ctx.hashOutputs == hash256(outputs), 'hashOutputs mismatch')
  }
}
```

Semantics normative in §5; implementation normative in the artifact. On-chain deployment still pending per §11.
