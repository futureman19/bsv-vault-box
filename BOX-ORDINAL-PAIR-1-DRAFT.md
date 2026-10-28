# BOX-ORDINAL-PAIR-1 — Draft, local external-custody construction

## Verdict and limits

An independently existing, synthetic 1-sat inscription is actually spent from its ordinary P2PKH owner into enforced custody. It is NOT minted as a native box token. The same first input sat remains in output zero throughout deposit → seal → transfer → open → withdrawal to buyer P2PKH. The companion control sat remains at output one. Both outputs are independently enforced compiled sCrypt covenants after deposit. No custodian/backend key, key handover, signature oracle, or off-chain owner registry exists.

This is a bounded local proof, NOT production readiness or mainnet/indexer acceptance. The updated construction supports exactly one authenticated P2PKH sponsor input after the two principal inputs, positive fees capped at 10000 sat, and optional sponsor-only change. Legacy two-input zero-fee local fixtures remain supported. Recursive raw-parent witnesses are replaced by authenticated 32-byte inner SHA256 digests. See `BOX-ORDINAL-SPONSOR-1-DRAFT.md` for the exact funding-parent grammar, bounds, security argument and remaining limitations. The previous implementation's withdrawal was 368774 bytes; that historical artifact is not the current format. There is no privacy: sealed means withdrawal prohibited, not contents hidden. An owner can open then withdraw; it cannot withdraw directly while sealed.

## Pinned source and supported admission grammar

Primary spec: https://github.com/BitcoinSchema/1sat-ordinals/blob/4f6d8d78d90acd807843cd254a9068586c793c20/README.md (saved verbatim at `vault/fixtures/1sat-primary-spec.md`). It permits locking-script-before-envelope or envelope-before-locking-script and arbitrary locking scripts on transfers, with ordinal input/output sat ordering preserved.

Fetched actual transaction hex from:
https://api.whatsonchain.com/v1/bsv/main/tx/10f4465cd18c39fbc7aa4089268e57fc719bf19c8c24f2e09156f4a89a2809d6/hex
Saved as `vault/fixtures/primary-1sat-example.hex`; parsed txid matches the spec's example. Output zero is one sat and begins `OP_DUP OP_HASH160 9cc74552f4cbc188358fedb5fa001c8768e303a4 OP_EQUALVERIFY OP_CHECKSIG OP_FALSE OP_IF 6f7264 OP_1 ...`. Its content type is `model/gltf-binary`. This is evidence for the actual P2PKH-before-envelope form, NOT a claim that our deliberately narrower text fixture decoder admits this model asset.

This prototype's explicit admitted mint grammar is only:
`76a914{20-byte-owner-hash}88ac 0063036f7264510a746578742f706c61696e00 {one-byte-length 01..4b} {exactly length payload bytes} 68`, value exactly one sat. This is canonical P2PKH plus one trailing ord envelope, MIME `text/plain`, one direct content push of 1..75 bytes. No envelope prefix, codesep, multiple inscriptions, other fields, PUSHDATA variants, arbitrary wallets, fungible tokens, or other NFT standards are claimed supported. The fixture uses published disposable scalars 1 and 2; NEVER fund them.

The saved existing inscription's ID is `54b6282c05903564447259974241c72f33fa8f6c719987abc4489a937cfc4aca_0`. Its funding ancestry is synthetic, not a claimed mainnet UTXO. All transactions are serialized and reparsed before execution. The mainnet example is read-only evidence, never spent.

## Construction and invariant

Contract immutable `origin` is the foreign inscription outpoint encoded as 32-byte little-endian transaction hash + 4-byte little-endian index. Mutable fields: phase (0 empty, 1 packed, 2 sealed, 3 opened) and compressed owner public key.

1. Create a one-sat EMPTY box with the foreign outpoint and owner. The initial box lives at output zero of its own separate transaction.
2. Deposit consumes foreign inscription input zero and EMPTY box input one. Box Script verifies `hashPrevouts` through sCrypt's preimage machinery, exact foreign outpoint, its own outpoint, current owner signature, and exact two principal output commitments plus any authorized sponsor change. Both principal outputs are one sat, identical PACKED contract scripts. The foreign inscription input separately requires its actual P2PKH signature.
3. Every subsequent spend MUST consume parent output zero and output one in that order, followed only by the optional authenticated sponsor input. Each covenant independently checks its actual preimage value is one sat, SIGHASH_ALL|FORKID owner signature, SHA256 of the 32-byte parent digest equals its actual preimage outpoint hash, paired prevouts, phase transition, and all outputs including any sponsor change. Both continuation outputs MUST be identical next-state scripts, preserving the immutable foreign anchor. Transfer is allowed only when sealed; it changes BOTH owners to the buyer. Seal is only from packed; open only from sealed.
4. Withdrawal is allowed only from opened. Both outputs become one-sat ordinary P2PKH outputs to the current owner. Output zero is the original ordinal; output one is the released companion control sat. The inscription envelope is not copied: identity follows the existing ordinal's spend ancestry, as the primary transfer spec describes.

**No Script introspection of sibling locking scripts is assumed.** Sibling state/code authenticity is an inductive invariant: the initial box covenant commits BOTH real output scripts; each subsequent real asset/control covenant commits BOTH real next scripts. Their outpoints must name the same parent at indices 0/1. Replacing either sibling, even with the same label, changes its parent hash and fails. Validating admission plus replay establishes the base case; consensus checks the actual UTXO scripts, never witness-provided replacements. The old raw-parent witness was never parsed or used to establish sibling code. Its hash-only check can therefore be factored into SHA256(innerDigest) == actual outpoint txid without losing a script/identity check. This is not a general compressed proof of arbitrary parent outputs. The separate sponsor funding parent IS reconstructed from a fully bounded, parsed transaction grammar; an unauthenticated output suffix is never accepted.

## Security and verification boundaries

- **Executed Script rules:** owner and sponsor authorization, state restrictions, paired outpoint co-spend, inner-parent-digest binding, authenticated bounded funding parent, positive capped sponsor fee, exact outputs/value preservation and sponsor-only change. Signed output mutations are applied BEFORE all preimages/signatures are rebuilt.
- **Ledger/consensus rules:** actual UTXO script lookup, input existence, duplicate-input prohibition, no overspend, and no conflicting accepted spends. Script alone does not detect prior confirmation/double spend. The local ledger models these boundaries; it is not a full node.
- **Client rules:** supported initial inscription grammar/value, initial box canonical code/phase/anchor/owner, complete ancestry beginning at that foreign UTXO, positional ordinal identity, chain inclusion/finality. The test client proves local ancestry but does not obtain SPV proofs, query an indexer, or validate the synthetic funding roots' ancestry. Sponsored funding preparation transactions are locally VM-verified from assumed roots. Production must prove the existing inscription origin and actual unspent funding ancestry.
- **Explicit counterfeit counterexample:** a newly fabricated parent with copied scripts/label can have a locally valid next spend. The test executes this successfully, then demonstrates rejection by anchored history. Therefore checking a script label or standalone current VM spend is NOT sufficient NFT authentication. Counterfeits cannot replace the true deposited asset/control pair or satisfy its owner/prevout commitments.
- **Seller-copy resistance:** after a confirmed transfer of the genuine pair, both real UTXOs require buyer signatures. Retaining Alice's old key, parent bytes, or copied scripts cannot spend either actual new output. Competing pre-transfer sales are ordinary conflicts and require normal confirmation policy.
- **Ordinal identity:** each source asset input is first and exactly one sat; each destination output is first and exactly one sat. No mixing into a larger output, padding before the ordinal, or transfer of a replacement label occurs.

VM is `scryptlib` / `@scrypt-inc/bsv` with `S.DEFAULT_FLAGS` and post-Genesis element-size limits. It is not an independent node/miner implementation. Nonstandard covenant recognition by a particular 1Sat wallet/indexer, miner policy, fee policy, SPV proofs, audit, and independent implementation parity remain unverified. Draft status is intentional.

## Reproduction and checked artifacts

From `vault/`:

```
npx scrypt-cli compile -i 'src/contracts/ordinalPair.ts'
npm run test:ordinal
npm run test:ordinal-sponsored
npm run vectors:ordinal
npm run vectors:ordinal-sponsored
npx mocha --no-config tests/ordinal-pair.test.js tests/native-custody.test.js
```

Expected compiler gate: 1 passing, 0 failing, `artifacts/ordinalPair.json`. Do not trust compiler exit status alone. Deterministic vectors include all raw transactions, txids, sizes and compiled artifact SHA-256 over compact `JSON.stringify(JSON.parse(artifact))` (line-ending independent); regenerate deliberately with `node scripts/ordinal-pair-vectors.js --write`.

Low-S preimage grinding changes each input sequence, therefore changes every SIGHASH_ALL signature's hashSequence. Builder stabilizes ALL covenant input sequences before signing ANY input; sequential grind-and-sign silently invalidates earlier input signatures.

The original 25 regressions remain intact (their raw-parent mutation API now hashes those bytes into the authenticated digest). They cover the positive lifecycle, foreign input substitution in the box VM, sealed withdrawal, seller opening/withdrawal after transfer, parent tampering, sibling outpoints/code, counterfeit same-label ancestry, omission/duplication/substitution, fee/change diversion, an unproved sponsor input, buyer-authorized withdrawal redirection, ordinal continuity, and ledger conflicts. New sponsored VM tests cover funding proofs, signatures, fee bounds, change destinations, repeated alternating transfers and fixed witness sizes. Prior native experiment remains untouched as a clearly separate regression suite. Public site/deployment artifacts are unchanged; no broadcast, push, deployment or real funds are involved.
