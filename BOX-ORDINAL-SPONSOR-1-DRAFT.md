# BOX-ORDINAL-SPONSOR-1 — Draft: bounded parent commitment and fee sponsorship

## Status and scope

Local compiled-Script implementation of both requested targets, not a production-ready vault. Extends `BOX-ORDINAL-PAIR-1-DRAFT.md`; existing ordinal admission and anchored history requirements remain mandatory. No public UI, network, signing service, broadcast or real-money integration is added. Contract bytecode/ABI changes: this is a new construction, not an upgrade of already deployed UTXOs.

## 1. Parent commitment without recursive witnesses

For the actual parent transaction bytes `T`, supply exactly `h = SHA256(T)` (32 bytes). Each covenant checks `SHA256(h) == ctx.utxo.outpoint.txid`, using raw digest order, not displayed reversed txid order. Its preimage is authenticated by the existing sCrypt machinery and its own actual UTXO script. The complete ordered prevout vector is authenticated against hashPrevouts.

The prior implementation checked `SHA256(SHA256(T))` and did **not parse T**. Supplying its inner digest preserves that hash-only condition while removing embedded historical unlocking scripts. No midstate opcode, sibling introspection, trusted server, SNARK, oracle or digest of omitted *required script fields* is introduced. This is NOT a general proof of a sibling's locking script or amount. An alternative that simply claims sibling scripts from this digest would be unsound; it is neither used nor claimed.

Sibling-code authenticity still follows induction: the admitted EMPTY box forces two identical PACKED scripts, and every real paired covenant forces both exact next scripts. Subsequent inputs must name outputs 0/1 of the same actual parent. Immutable origin and owner/phase states survive each transition. The local UTXO boundary executes actual spent scripts, not witness-selected substitutes. Admission/replay is essential: a copied-label counterfeit can have a valid standalone spend but is not the anchored ordinal (regression retained).

Both covenant witnesses contain a 32-byte parent digest, regardless of transfer count. sCrypt preimages contain fixed-size current code/state, not recursive parent transactions. Full raw ancestry remains necessary for current client verification and naturally grows linearly; the fixture stores it explicitly. No claim of constant-size history or general maximum transaction size is made: voluntarily padded unlocking scripts can enlarge transactions. The bounded claim concerns required proof data and canonical builder output.

## 2. Input/output and authorization rules

Two supported modes:

* Legacy offline mode: exactly two inputs and exactly two one-sat outputs, zero fee; sponsor parameters must be empty/zero.
* Sponsored mode: exactly three inputs. Input 0 is the original ordinal, input 1 its paired control (EMPTY box during deposit), input 2 the authenticated funding outpoint. No additional inputs.

Outputs 0/1 are exactly one sat each. Before withdrawal they are identical next-state contracts; after withdrawal both are P2PKH to the current owner. The ordinal remains the first input sat and first output sat. Funding is last, never before either principal.

Both owner and sponsor covenant signatures MUST end in `0x41` (SIGHASH_ALL|FORKID); NONE and ANYONECANPAY are rejected even when cryptographically valid. The sponsor explicitly authorizes the exact custody transition in each covenant witness. The actual funding input additionally executes its own P2PKH signature. A covenant authorization is not a substitute for that input's signature.

Let `V` be the authenticated funding output amount and `C` declared change:

* `0 < V <= 2100000000000000` sat.
* `0 <= C < V`.
* `1 <= V - C <= 10000` sat, enforced in Script.
* If `C > 0`, output 2 is exactly `C` sat to canonical P2PKH HASH160(sponsor public key).
* If `C == 0`, there is no output 2.
* No other outputs or destinations; all output bytes are committed by hashOutputs.

The two principal inputs/outputs are one sat each for the admitted genuine chain, so the actual transaction fee is exactly `V-C`. Sponsor amount, script and outpoint are proven, not caller-trusted. The deposit's foreign one-sat base case remains an admission/actual-chain property, as before. Fees above the cap require a new protocol decision; the builder must not silently increase it. Tests use 500 sat per custody transition, with 100000-sat funding and 99500-sat change; acceptance at 1 and 10000 sat and no-change funding is tested too. These are test amounts, not a miner fee quote.

## 3. Bounded authenticated funding-parent grammar

A funding parent MUST be a canonical non-SegWit serialized transaction with one input, one output at index 0, and the following exact decomposition:

```
prefix = version[4] || 01 || previousOutpoint[36]
       || scriptSigLength[1] || scriptSig[N] || sequence[4] || 01
output = amount[8 LE] || 19 || 76a914 || HASH160(sponsor)[20] || 88ac
parent = prefix || output || locktime[4]
```

Script checks:

* Prefix length is `47 + N`, in `[47,155]` bytes.
* Byte 4 is `01` (one input).
* Byte 41 is the single-byte length `N <= 108`; extended CompactSize encodings are excluded.
* Byte `46+N` is `01` (one output), and is the final prefix byte.
* Locktime length is exactly four bytes.
* Reconstructed `HASH256(parent) || 00000000` equals authenticated third prevout.
* Output is reconstructed using the sponsor key and amount, not supplied unchecked.

Thus all transaction boundaries are fixed/validated: no unparsed arbitrary prefix can hide extra outputs or reinterpret a purported suffix. The full authenticated parent is at most 193 bytes. Its scriptSig bytes are included, not ignored. Consensus still validates the funding transaction's input and chain existence; the covenant proves the consumed output's exact script/value/outpoint, not the funding transaction's confirmation.

Restriction/trade-off: arbitrary wallet UTXOs, multi-input funding transactions, multiple outputs, or scriptSigs longer than 108 bytes are not accepted. A sponsor can prepare a one-input/one-output P2PKH consolidation transaction first. This extra preparation has its own fee and confirmation/ancestor policy; it is not free or hidden in the measured custody fee. The local fixture prepares a genuinely signed funding parent (500-sat preparation fee) from a distinct assumed synthetic P2PKH root and verifies that preparation in the VM. Synthetic root ancestry is NOT validated as a real chain.

Change from a custody transaction cannot directly sponsor the next transition: that parent has multiple inputs/outputs. Spend it into a qualifying P2PKH preparation parent first. No recursive witness growth is reintroduced: only that bounded preparation parent's raw input signature is included. The prototype does not automate a production sponsor UTXO pool.

## 4. Executed evidence

Commands from `vault/`:

```
npx scrypt-cli compile -i 'src/contracts/ordinalPair.ts'
npx tsc --noEmit
npx mocha --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/native-custody.test.js
npm run vectors:ordinal
npm run vectors:ordinal-sponsored
```

Compiler: 1 passing, 0 failing. Typecheck: exit 0. VM tests: 90 passing (25 original external, 38 sponsored/bounded, 27 native). Original external test file unchanged. Vector checks reproduce exact raw bytes and artifact hash; deliberate regeneration uses the corresponding script with `--write`.

The deterministic sponsored vector executes deposit, seal, **12 alternating Alice/Bob ownership transfers**, open, withdraw. Every funding preparation and custody spend is VM-verified; complete anchored custody history replays. Old-owner open attempts are rejected after each alternating transfer in tests.

| Measured serialized transaction | Bytes |
|---|---:|
| Deposit | 11727 |
| Seal | 15856 |
| Each of 12 ownership transfers | 15853–15856 |
| Open after transfer 12 | 15853 |
| Withdraw after transfer 12 | 8810 |

Per-covenant unlocking scripts in this vector: 4231–4233 bytes, including current sCrypt preimage, all authorizations and proofs. Each parent commitment: exactly 32 bytes. Full funding parents: retained in vectors, bounded by 193 bytes. Current continuation locking script: 3545 bytes. Total custody history: 242495 bytes; separate funding-parent history: 3061 bytes. Root assumptions, raw funding parents, raw custody transactions and identity are retained in the fixture; no data is hidden in a server.

Baseline at `68be07458a025220b6a543400c7db789dfa0bd56` was 11990 / 36150 / 84469 / 181115 / 368774 bytes for deposit/seal/transfer/open/withdraw. The new proof no longer copies the entire preceding transaction twice. Stored history still grows with the number of transitions.

Evidence: `evidence/ordinal-sponsored-bounded/`; golden bytes: `vault/fixtures/ordinal-sponsored-vectors.json` and updated legacy zero-fee vectors. Security regressions include authenticated funding value/code/outpoint, prefix count/length ambiguity, wrong sponsor and owner signatures/sighash, missing funding signature, fee cap/zero/negative fee, change omission/diversion/duplication, extra/reordered inputs, principal diversion, old-owner attacks, counterfeit companion code and counterfeit standalone history.

## 5. Remaining production gates

Still Draft: no independent implementation or full-node/miner execution, no miner fee/policy acceptance, no mainnet inclusion, no SPV/indexer or wallet compatibility proof, no security audit, no production funding preparation/replenishment service, no broad inscription grammar support, no upgrade/migration path for old bytecode. Existing real-value/public launch gates remain disabled. Local assumed UTXOs are not funded assets. Owner controls opening; sealed does not mean secret contents. Normal double-spend/finality rules still apply.
