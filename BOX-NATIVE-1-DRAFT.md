# BOX-NATIVE-1 — native wrapper experiment

**Status: Draft / research-only / requested custody product NOT completed.**

## 1. Verdict and scope

The existing VAULT-0001 covenant commits to `contentRef`; it does not lock referenced NFT UTXOs. This experiment adds an executable native token with a one-use wrapper, not a generic custody vault. There is no demonstrated external asset deposit, independent asset release, sibling-UTXO authentication, multi-item inventory, or 1Sat support. A single token changing phases is **not** fulfillment of the requested container product. Do not deploy or fund this artifact.

The supported experimental format is BOX-NATIVE-1 only: one genesis-anchored native token whose wrapper and ownership state occupy the **same UTXO**. Its NFT identity is the trusted genesis transaction outpoint, never the reusable 32-byte asset label alone. The label is immutable descriptive data. Cloning a label or script does not clone a valid anchored identity, but consensus does not prevent people creating unrelated lookalike genesis outputs.

## 2. Actual implementation

`vault/src/contracts/nativeVault.ts` compiles through pinned scrypt-ts 1.4.5, scrypt-cli 0.2.3, scryptlib 2.2.6 and native sCrypt compiler 1.20.0. The checked-in `vault/artifacts/nativeVault.json` contains executable Bitcoin Script. `vault/src/native-custody.js` builds real serialized BSV transactions and unlocking scripts; attack tests re-sign malicious outputs and regenerate preimages before running the Script VM.

The public method is `move(sig, action, recipient, txPreimage, prevouts)` at the compiled ABI. The sCrypt source supplies the last two arguments automatically; the low-level fixture supplies them explicitly. Owner signatures use ALL|FORKID. The covenant's preimage verification binds outputs, input outpoints and input value. Supplied prevouts must match the transaction and contain exactly one outpoint (36 bytes).

State: `phase` (integer 0–4), compressed `owner` public key; immutable `asset` label (32 bytes under the client acceptance grammar). Script and serialized state are decoded using the compiled artifact and round-trip checked; unrelated scripts fail closed.

| Action | Source | Destination | Authority |
|---|---|---|---|
| pack (0) | FREE (0) | PACKED (1) | current owner |
| remove (1) | PACKED (1) | FREE (0) | current owner |
| seal (2) | PACKED (1) | SEALED (2) | current owner |
| transfer (3) | any valid phase | same phase, new owner | current owner |
| open (4) | SEALED (2) | OPENED (3) | current owner |
| withdraw (5) | OPENED (3) | WITHDRAWN (4) | current owner |

Every valid spend creates exactly one continuation with the **entire** input value and same asset label/code. There are no change outputs, other inputs, or payment outputs. No method restores a withdrawn wrapper. The withdrawn native token can transfer but cannot repack. “Withdraw” here is a phase transition, **not** extraction of a pre-existing independent NFT or an unlocked P2PKH ordinal. This restriction is visible in the lab.

## 3. Fees and ordering

All prototype transactions have **zero fee** and preserve positive principal. An initial fixed-fee design had an unreplenishable reserve and was removed after a RED principal-conservation test. Zero fees eliminate that local exhaustion bug but do not establish miner acceptance or production usability. Authenticated fee sponsorship/change and replenishment remain required design work. Never fund the prototype to try to work around this restriction.

Single input at index 0, single output at index 0. There are no ordinal identity claims, inscriptions, sat-offset tracking, or arbitrary funding inputs. No 1Sat token may be imported. The initial source is a synthetic non-chain UTXO; descendant scripts execute for real in the local interpreter. No block has been mined, no node acceptance has been demonstrated, and nothing is broadcast.

## 4. Enforcement versus validation

**Executed Script rules:** current owner signature, irreversible phase transitions, exact output script/value, immutable native asset label/code, one input only, no duplicate or omitted continuation, no unauthorized change output or value diversion. A malicious sibling proof cannot pass hashPrevouts verification. There is no accepted sibling-asset proof system.

**Client/local validation:** a trusted genesis anchor, correct parent outpoints, full serialized history replay through the VM, same native identity, strict supported script decoding, and local in-memory spent-output tracking. The inventory API reports a singleton only for phases 1–3; this is native-token wrapper membership, not proof of external custody.

**Not proven:** chain inclusion, authoritative current unspent status, absence of a competing chain spend, external NFT authenticity/custody, multi-item conservation, production fee policy, independent implementation consensus parity. `verifyHistory.valid` means anchored local-history validity, not “safe to pay.” `LocalLedger` is not a blockchain oracle.

## 5. Reproduce safely

From `vault/`:

```
npm ci --ignore-scripts
npx ts-patch install
npx scrypt-cli compile -i 'src/contracts/**/*.ts'
npx tsc
npm run test:native
npm run vectors:native
npm run lab:native
```

The explicit ts-patch step matters: ignoring installation scripts otherwise lets the CLI misleadingly report **0 passing / 0 failing** without compiling a contract. Require actual artifacts and a nonempty executed VM suite.

Lab: http://127.0.0.1:4318. It signs only public disposable fixture identities. It has no wallet connection, custom key input, address deposit flow, RPC, external fetch or broadcast capability. The page is under `vault/lab/`, not the deployed `docs/` tree. Browser gate from repository root: `python test/native-lab-browser.py`.

## 6. Remaining requested-product gates

1. Design real deposit and withdrawal of independent asset UTXOs, with a bounded authenticated sibling/ancestor proof or another concrete consensus construction. Prove no counterfeit box can authorize a held asset. Current code intentionally does not claim this.
2. Define a supported NFT grammar and authenticity model; 1Sat requires actual inscription/satoshi ordering proofs, not a label or content hash.
3. Implement multi-item inventory conservation and atomic add/remove/seal/transfer/open/withdraw for that model; prove omitted/duplicate/substituted assets fail in each affected input script.
4. Design fees/change without principal depletion or fee diversion. Exercise full transactions including funding inputs.
5. Independent review, independent VM/node execution, chain-aware unspent verification/reorg handling, wallet integration, recovery, and realistic size/fee limits. The pinned installation reported 20 npm audit findings (1 low, 9 moderate, 9 high, 1 critical); these dependencies were not upgraded in this research slice.
6. Only after these gates, replace the production site's emphasis with a real vault-management product. Existing claw and approved Blender assets remain untouched.

**Closure: BLOCKED on an implemented and independently verified external-asset custody construction.** This commit is a functioning local research artifact and explicit handoff, not completion or deployment clearance. No automatic deployment or funded testing.
