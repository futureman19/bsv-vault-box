# BOX-FOUR-ORDINAL-1 — offline fixed-bundle proof (Draft)

## Result and boundary

New compiled `FourOrdinal` contract; existing single-ordinal source/artifacts and website are unchanged. Exactly four independent assumed existing one-sat inscriptions enter custody, plus one separately created control sat. Order is **collectible Box, certificate record, object one, object two, control**. Pack → seal → transfer Alice to Bob → open → withdraw executes serialized/reparsed transactions in the scryptlib BSV Script VM, not a UI permission simulation.

This is **zero-fee, synthetic-root, local VM evidence only**. No nodes started, funding, network calls, broadcast, push or deployment. No chain existence/unspentness, miner policy, independent implementation, wallet/indexer compatibility, broad NFT admission, JPEG/image artwork, reseal or production claim. The records are tiny text fixtures, not finished art. Public disposable scalars Alice=1, Bob=2, fixture issuer=3 (attacker=9): NEVER fund these keys. Public issuer keys do not provide real-world authenticity; they test the verification mechanism.

## Enforced construction

Immutable `origins` contains four ordered outpoints, each txid in wire byte order plus uint32LE output index: 144 bytes. Mutable state is phase and owner. Initial control is one sat at output zero of a separate transaction.

Pack spends the four external P2PKH-plus-envelope assets at inputs 0..3 and EMPTY control at input 4. Control requires the exact immutable origins followed by its own outpoint; it commits all five identical PACKED covenant outputs, each one sat. Each external input independently executes its P2PKH signature. Admission of supported one-sat originals is an explicit **client/actual-UTXO base-case requirement**, not Script introspection of those sibling values/envelopes.

All later inputs must be outputs 0..4 of one authenticated parent, in exactly that order. Every covenant independently checks its own UTXO index is in 0..4, its amount is one sat, the 180-byte ordered prevout vector, SHA256 of the supplied 32-byte inner parent digest, SIGHASH_ALL|FORKID current-owner signature, transition and exact entire output serialization. The parent digest does not prove arbitrary sibling script bytes: sibling authenticity follows admission and inductive exact-output commitments. Every continuation preserves all five one-sat outputs and the immutable origins. Transfer changes every owner; open irreversibly ends the seal; withdrawal only from opened sends five one-sat P2PKH outputs to the current owner.

All five input sequences/preimages stabilize before **any** input is signed. Output attacks are mutated before fresh signatures. No sponsorship or extra input/change exists in this construction. Five input satoshis return as five output satoshis: principal never pays fees. This zero-fee result is not a deployable miner fee strategy.

Identical continuation scripts do not make the assets interchangeable: ordinal interpretation follows each input sat at index 0..3 to its corresponding one-sat output. Do not infer origin merely from labels/current scripts. A copied parent can have a valid standalone spend; anchored history rejects it. Duplicate inputs, existence, spentness/conflicts belong to the ledger boundary; the helper ledger is not a full node or chain oracle.

## Certificate bytes, circularity and policy

Each original uses the existing narrow grammar:

`P2PKH(owner) || OP_FALSE OP_IF "ord" OP_1 "text/plain" OP_FALSE direct-push[1..75 bytes] OP_ENDIF`.

No arbitrary PUSHDATA, image content or alternate inscription forms are admitted. The collectible and two objects contain literal UTF-8 text. The certificate inscription contains **exactly 64 ASCII lowercase hexadecimal characters**: SHA256 of the canonical detached envelope below. The full issuer statement/signature is **not** in its transaction.

Canonical means JavaScript `JSON.stringify` with exactly the construction's field order and no whitespace:

- Statement: `{protocol:"BOX4-CERT-1",collectible:<original collectible txid_0>,objects:[<original object-one txid_0>,<original object-two txid_0>]}`.
- Issuer signature: secp256k1 ECDSA over SHA256(UTF-8 statement), DER serialized to lowercase hex; compressed public key as hex.
- Detached envelope: `{statement:<statement string>,issuer:<public key>,signature:<DER hex>}`.
- Outer manifest: `{protocol:"BOX4-MANIFEST-1",items:[{role,origin},...]}` with the four roles in fixed order, **including the certificate origin**.

The certificate names the other three originals; it deliberately does not name itself or the outer manifest, avoiding circular txid references. The outer immutable origins and manifest include its resulting origin. Detached envelope and manifest are saved in the verification bundle; they need availability separate from chain storage. The manifest is checked canonically against all four actual origins, not treated as an independently issuer-signed document.

`verifyHistory(f, entries, policy)` and `replayVectors(v, policy)` require an **explicit externally chosen** `{issuer: compressedPublicKeyHex}`. The fixture policy is exported as `TRUSTED_POLICY` (scalar-3 public key). A bundle's `policy` field is descriptive, never adopted as trust; the CLI passes the code-owned fixture policy. An attacker may put any claimed trusted issuer inside their bundle; a valid unknown-key certificate and VM-valid packing still fail against the caller's anchored policy. If a caller deliberately replaces its own policy with an attacker key, it has changed who it trusts—no verifier can repair that policy decision. Script does not check issuer provenance. The test also rejects a well-formed wrong-key signature claiming the trusted key.

## Reproduce (from `vault/`, existing local dependencies)

```sh
node node_modules/scrypt-cli/src/bin/index.js compile -i src/contracts/fourOrdinal.ts
node node_modules/typescript/bin/tsc --noEmit
node node_modules/mocha/bin/mocha.js --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/four-ordinal.test.js
node scripts/four-ordinal-vectors.js
# Only after deliberate source/artifact review:
node scripts/four-ordinal-vectors.js --write
```

On this Windows/Git-Bash host, the Node shim may report `stdin is not a tty`. The exercised alternative is `python -c "import subprocess,shutil; subprocess.run([shutil.which('node'), 'scripts/four-ordinal-vectors.js'],check=True)"`, replacing the Node arguments with the commands above. No npm pretest/clean was run; those can overwrite existing artifacts. The compiler gate explicitly reported **1 passing, 0 failing**; typecheck exited 0.

Raw deterministic fixtures: `vault/fixtures/four-ordinal-vectors.json`. They contain four original transactions, separate initial control, detached signed envelope, canonical manifest, all five raw lifecycle transactions, txids, sizes and normalized compiled-artifact SHA256. The CLI regenerates in memory, compares exact stored bytes, then replays the saved bundle with explicit trusted policy. It does not recover trust from the evidence itself.

| Transition | Serialized bytes |
|---|---:|
| Pack | 19241 |
| Seal | 32801 |
| Transfer | 32804 |
| Open | 32802 |
| Withdraw | 17869 |

## Test evidence and issues

`evidence/four-ordinal-vm/` retains actual compiler, RED, GREEN and replay stdout/stderr. Tests were written before the implementation. Initial RED was the admission behavior (empty implementation returned zero instead of four assets), not a missing-module error. The first whole-suite run then caught a real export bug: scryptlib mutates its loaded artifact object to contain BigInts. Hashing freshly parsed artifact file JSON fixes that without changing existing artifacts. Additional replay tests ran RED against accepted false origin metadata and unsupported format, then GREEN after explicit rejection checks. This does not claim a separate preimplementation RED execution for every individual adversarial rule.

Combined requested gate: **95 passing = existing 25 pair + existing 38 sponsored + 32 new**. Separately, all **27 native-custody regressions** passed and both original vector check commands exited 0 without rewriting their fixtures. The new tests cover real lifecycle and ordinal positions, exact inputs/outputs, duplicate/missing/reordered/substituted assets, immutable commitment, owner changes and old-owner rejection, sealed withdrawal, amount/code/destination changes, all five covenant VM checks, out-of-range parent index, forged certificates, unknown issuer policy, copied-label ancestry, deterministic export and replay validation. Standalone validity is explicitly not treated as chain provenance. `verifyHistory` permits valid prefixes (including initial admission); `valid:true` alone does not assert a completed lifecycle or current live UTXO.
