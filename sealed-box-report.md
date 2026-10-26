# Sealed-Box NFT Feasibility Report
**Question:** Can BSV support a genuinely sealed, transferable, fixed-content NFT box — hidden from its owner until a publicly verifiable on-chain opening, with no issuer server and no trusted parties?
**Date:** 2026-10-26 · **Status:** research deliverable, prototype executed, no funds spent, no real keys used

---

## 1. Threat model and definitions

**Parties:** issuer (creates inventory and boxes), current owner, previous owners, buyers verifying seals, miners, any external infrastructure operators.

**Adversary classes considered:**
- **Malicious issuer** — knows the creation-time data; may try to peek at assignments or cherry-pick rare NFTs for boxes they control.
- **Malicious current owner** — will run any offline computation on data they possess or can read; controls a sandboxed wallet.
- **Malicious previous owner** — retains everything they ever knew; tries to inspect after selling "sealed."
- **Miner / hashpower adversary** — can reorg shallow blocks and mine private forks.
- **Unavailable infrastructure** — any party that can simply disappear.

**Definitions.** For a box *b* with seal outpoint *U(b)* (the current UTXO carrying the box ordinal):

- **SEALED(b)** ⟺ (i) *U(b)* is unspent on the canonical chain; (ii) no covenant-valid opening transaction for *b* appears on the canonical chain with ≥ K confirmations; (iii) no key-release record for *b* has been published by the key-holding mechanism. All three conditions must be checkable from public data alone.
- **OPENED(b)** ⟺ a covenant-valid opening spend of *U(b)* is confirmed ≥ K deep **and** the content key for *b* has been released.
- **The seal property** (the product requirement): *learning the plaintext of b's contents is feasible **iff** OPENED(b) is publicly verifiable* — for everyone, including the owner, previous owners, and the issuer.

"Unredeemed" (UTXO unspent) is **not** "uninspected" throughout: an unspent seal output says nothing about who has read the plaintext unless the key-management design ties the two together. That tie is the entire problem.

---

## 2. Feasibility verdict

| Option | Verdict |
|---|---|
| Original constraints, pure BSV, no external party, no trusted hardware | **No suitable construction found.** A structural argument (below) shows why; this is not a universal impossibility proof. |
| Witness encryption to a chain event | **Theoretically plausible, not deployable in 2026**, and even theory doesn't solve the private-fork problem. |
| Threshold key-release committee (relaxation R1) | **Feasible today with existing tools.** Smallest sufficient relaxation. Recommended if the seal property is non-negotiable. |
| TEE network (relaxation R2) | Deployed (Lit Protocol "Naga" mainnet), but adds hardware trust and BSV is not natively supported. |
| Product change: draw-at-open from committed inventory (fallback R5) | Fully deployable, trust-minimized — but is a different product (explicitly out of scope for the main answer; see §12). |

**Bottom line:** the plastic-wrapper property — *learning == public event* — cannot come from BSV script, commitments, signatures, timelocks, or ZK proofs alone. It requires entropy that does not exist until the opening event, which today only an external release mechanism (committee, TEE, beacon) can supply at practical cost.

---

## 3. The structural argument (why the pure construction fails)

Let π be any candidate protocol under the original constraints. Secrecy requires the plaintext to depend on entropy E that the owner does not have. Opening is owner-initiated and non-interactive (no issuer server, no external operators). Therefore the opening procedure must be computable from **owner-held data ∪ public chain data** alone. Anything computable from that set is computable in a private sandbox **without broadcasting anything** (executed as T2–T4 in the prototype: each variant decrypted locally with zero blocks mined).

Contrapositive: a genuine seal requires the decryption key to depend on data that **does not exist before the public opening event**. Only three sources of such future-bound entropy are known:

1. **Future canonical-chain data** (block hashes, confirmed transactions). Encrypting to an *unknown* future value requires witness encryption (WE) to a chain-membership statement. For arbitrary event predicates this is provably as hard as general WE over the blockchain (Campanelli et al., "Encryption to the Future," prove far-future EtF ⟹ WE for NP — ePrint 2021/1423). No general WE candidate is concretely efficient in 2026 (§10). And critically: **WE soundness gives nothing against an attacker who can *produce* the witness privately** — a hashpower adversary mines a private fork containing the opening tx, decrypts off-chain, discards the fork, and sells the box as sealed. No standard WE security notion covers this; the literature treats it only as an honest-majority assumption (Liu–Jager–Kakvi–Warinschi, Des. Codes Crypto. 2018, DOI 10.1007/s10623-018-0461-x). DecryptChain (ePrint 2026/1195) names the general disease: premature decryption failures are **silent** — no public transcript exists.
2. **An external party's release action** — a threshold committee or oracle releasing key material upon observing the confirmed opening. This is relaxation R1 (§6). Deployable today; it is a threshold-trust design, not trustless.
3. **Trusted hardware** — TEE-held keys released on verified chain state (relaxation R2). Deployed but adds vendor/federation trust.

nLockTime, VDF time-lock puzzles, and drand-style timelock supply future-bound entropy **gated on time, not on an owner-chosen opening event** — and time-lock puzzles are privately solvable, so they leak without any public record. They fail requirement 4 (no mandatory reveal date) and the seal property simultaneously.

**Conclusion:** under the fixed requirements, one requirement must change: either admit an external key-release mechanism (R1/R2), or drop "contents fixed and hidden until owner-chosen opening" (fallback, §12).

---

## 4. Autopsy of the known failed shortcuts (all 14, explicitly)

1. **Public ciphertext + owner-held key** — permits private inspection. *Executed:* T2 decrypted with zero on-chain footprint.
2. **Key from opening signature** — signatures are computable offline; so is any key derived from one. *Executed:* T3.
3. **Signed tx ≠ broadcast/confirmed** — correct; and covenant checks can only run *inside* a confirmed spend, so they cannot gate what the signer learns while constructing it.
4. **Transfer cannot erase retained keys/plaintext** — correct; hence no design may ever let any owner touch key material (R1 satisfies this: owners never hold shares — executed T5.4).
5. **Re-encryption doesn't revoke copied data** — correct; only helps if plaintext was never exposed.
6. **nLockTime = eligibility, not encryption** — confirmed (on BSV additionally, CLTV/CSV remain NOPs post-Genesis, so no in-script timelock exists at all; eligibility-only).
7. **Time-lock puzzles solve privately and don't bind to ownership** — confirmed; plus they impose a mandatory reveal-by-time.
8. **Commitment proves consistency, not confidentiality** — *executed:* T1 recovered a box's content by enumerating 1000 candidate preimages in **1.2 ms**. Salting defeats enumeration (T1b) but salt custody = key custody: whoever holds the salt enumerates instantly. Commitments transfer the problem; they don't solve it.
9. **Public deposits/outpoints reveal membership** — mitigated by encrypting assignments (threshold ElGamal) rather than committing hashes; ciphertexts over a public inventory are non-enumerable without the key.
10. **The assigner may know and cherry-pick** — solved by a verifiable re-encryption mix-net over threshold-encrypted assignments: no single party (issuer included) learns the permutation unless *all* mixers collude (§6, creation step).
11. **ZK proofs alone don't make public execution confidential** — confirmed; proofs in this design attest shuffle/opening correctness, never secrecy.
12. **Reorg can erase an opening record after leakage** — *executed:* T5.6. Mitigations: committee releases only after K confirmations (K ≫ typical reorg depth), releases are published on-chain **and** as signed off-chain attestations clients retain, and seal verification treats "key released but no opening record" as BAD (box unmarketable as sealed). Residual risk, stated honestly: a deep reorg erasing *both* records before any client snapshots them yields silent leakage. This is a confirmation-depth economic assumption, not a cryptographic fix.
13. **"Encrypt to a future block hash" mechanics** — shown in §3.1: it is WE to a chain statement; the future blocks' unpredictable bits act as the key (LJKW18). Impractical and private-fork-vulnerable.
14. **Unspent seal output ≠ secrecy** — confirmed; seal status must be a 3-part public check (§1).

---

## 5. Required distinctions — which construction achieves what

| Property | Hash commitment | Owner-key ciphertext | Timelock (drand) | **R1 committee** | WE-to-event |
|---|---|---|---|---|---|
| Contents cannot be substituted | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hidden from public | ❌ (enumerable) | ✅ | ✅ | ✅ | ✅ |
| Hidden from owner until opening | ❌ | ❌ | ✅ (but forced by time) | ✅ | ✅ (in theory) |
| Previous owners retain no inspection capability | ❌ | ❌ | ✅ | ✅ (never held keys) | ✅ |
| Buyers can verify opening occurred | ✅ | ❌ | ✅ | ✅ | ✅ |
| No-opening-record ⟹ not inspected | ❌ | ❌ | ❌ (after time T) | ⚠️ (up to k-of-n collusion — silent) | ❌ (private fork) |
| Issuer need not know assignments | ❌ | ❌ | ❌ | ✅ (mix-net) | ✅ |
| Deployable today, no external trust | — | — | ✅ but wrong primitive | ❌ (committee = relaxation) | ❌ |

No row satisfies all properties under the original constraints. R1 satisfies all except "no external trust," where it substitutes an explicit, accountable k-of-n assumption.

---

## 6. Strongest candidate construction (relaxation R1: threshold key-release committee)

**One-sentence shape:** threshold-IBE (tlock-style) where the "identity" is not a drand round but the box's opening identifier; a k-of-n committee publishes key shares only after observing a confirmed, covenant-valid opening spend on BSV. Everything else — inventory, ciphertexts, boxes, opening records, release records — lives on-chain. Academically this is signature/identity-based witness encryption over a committee (McFly, ePrint 2022/433, reports concretely efficient timings: ~10–15 s enc/dec at 500-node committee on BLS12-381); deployed siblings are drand/tlock (time-only) and Fairblock/Lit (condition-triggered, other chains).

### Creation & assignment
1. Issuer commits the full 1,000-NFT inventory on-chain (Merkle root in a setup tx). No silent expansion later: box count and inventory are pinned in the same tx.
2. Each NFT assignment is ElGamal/IBE-encrypted to the committee's joint public key (joint key produced by a Pedersen/GJKR DKG — no trusted dealer, so the issuer never touches shares).
3. An m-hop **verifiable re-encryption mix-net** (m = 3–5 independent parties, one may be the issuer) shuffles the encrypted assignments; each hop posts a shuffle proof. Practical tooling exists: ZKShuffle (Circom+Groth16; 52 items ≈ 87k R1CS constraints, ~4.5 s browser proving; ~1.7M constraints / tens of seconds for 1,000 items), Geometry's Rust Bayer–Groth prover (~50 ms for 52 cards), or Verificatum VMN (production voting deployments: Estonia IVXV, Swiss Post). Bayer–Groth: DOI 10.1007/978-3-642-29011-4_17 (note: no ePrint version exists).
4. Result: box *i* → ciphertext of NFT π(i) published on-chain (1Sat ord envelope or OP_FALSE OP_RETURN — BSV has no push-size limit). **No single party knows π unless all mixers collude; the issuer cannot cherry-pick.**

### Sealing
Each box is a 1Sat ordinal (BRC-159/160) whose locking script is an sCrypt/OP_PUSH_TX **covenant** enforcing: any spend of the seal UTXO must reproduce the box in exactly one of two forms — (a) a new sealed-box output (transfer), or (b) an "OPENED" output carrying the box id (opening). The covenant cannot create secrecy (the committee does that) but it makes the opened/sealed state machine consensus-enforced and client-verifiable. BSV can do this: OP_PUSH_TX pushes the BIP143 preimage; the script verifies it in-script and constrains every output (post-Genesis opcode restoration; sCrypt stateful contracts productize it).

### Minting (claw machine)
Buyer pays 1 BSV; the mint tx transfers a seal UTXO to the buyer's key. The animation is pure interface. Box index assignment at sale can be FIFO or drawn from public tx entropy — irrelevant to security, since the content mapping is encrypted.

### Sealed transfer
Ordinary covenant-preserving spend to the new owner. No key material ever exists in any owner's hands at any point — so nothing can be retained, copied, or leaked by sellers. This is what makes "previous owners cannot inspect" actually hold (T5.4).

### Opening
1. Owner broadcasts the opening tx (covenant forces the OPENED output; owner's signature proves ownership of the current seal UTXO).
2. Each committee operator runs a BSV watcher; upon ≥ K confirmations of the covenant-valid open, it publishes its IBE key-share / partial decryption for identity `open:<box_id>` — on-chain (small OP_RETURN tx) plus a signed attestation clients can keep.
3. Any k shares reconstruct the key; anyone (owner, marketplaces, indexers) decrypts the box ciphertext. The NFT revealed is the one assigned at creation — provably, via the mix-net proofs and the on-chain ciphertext.
4. The OPENED ordinal remains transferable (requirement 7).

### Seal verification (any buyer, public data only)
SEALED(b) ⟺ seal UTXO unspent ∧ no confirmed OPENED record ∧ no release record. Indexers (1sat-server, WhatsOnChain) expose all three.

### The required per-approach questions, answered for R1
- **Who knows each secret?** Content keys: no one individually — k-of-n shares. Permutation: no one individually (mix-net). Owner keys: owners (spending only, never content).
- **What exists before opening?** Public: inventory commitment, encrypted assignments, shuffle proofs, box ciphertexts, seal UTXOs. Nothing that decrypts anything.
- **What becomes available only after opening?** k key shares, published by committee members after K-conf observation of the opening spend.
- **Why can't it be computed privately?** Shares live only with operators; the joint key is never reconstructed except threshold-decryption of released identities. Private computation yields nothing below k colluding operators.
- **Who supplies it; what if they disappear?** Operators. If active operators drop below k before a proactive handoff (CHURP-style refresh, ePrint 2019/017), unopened boxes are bricked forever — drand's own docs concede this failure mode. Mitigations: larger n, proactive refresh, shares escrowed/re-shared to successor committees, multi-network redundancy. **None eliminate the dependency. This is the price of the seal.**
- **Transfers without exposure?** Ownership = UTXO; content keys never transfer because owners never hold them.
- **Prior owner / issuer peeking?** Prior owner: nothing retained; their crafted open spends a dead outpoint (invalid). Issuer: never sees shares (DKG) or permutation (mix-net); can only peek via ≥ k collusion with operators.
- **Public opening vs private fork?** Committee requires K confirmations and publishes attributable release records; a private fork doesn't reach watchers as canonical. Residual silent-collusion risk (≥ k operators decrypt everything privately, any time) is the honest trust assumption — no deployed design escapes it.

---

## 7. Secrets lifecycle (R1)

- **Content key per box** — born as threshold shares (DKG); never whole anywhere; released as shares on confirmed opening; post-opening public. Holder: committee.
- **Assignment permutation π** — born inside the mix-net; never known to any single party; effectively public after all boxes open. Holder: distributed across mixers.
- **Owner signing keys** — standard wallet keys; authorize transfer/opening only; never gate decryption.
- **Committee long-term keypair** — joint public key on-chain at setup; private key exists only as shares; must be proactively refreshed (CHURP) across operator churn; loss of quorum = permanent seal.
- **Salts** — unnecessary: ElGamal/IBE ciphertexts are non-enumerable; no hash commitments guard low-entropy data.

---

## 8. Adversarial analysis

- **Malicious issuer:** cannot expand or swap inventory (setup commitment); cannot learn assignments (mix-net, unless all mixers collude); cannot learn contents (no shares); cannot be required later (no issuer-held secret; disappearance-safe). Worst case: issuer *runs one mixer* — still learns nothing alone.
- **Malicious owner:** sandbox computation yields ciphertext only; opening is the sole key-release trigger; cannot open-and-reseal (covenant state machine + spent outpoint).
- **Malicious previous owner:** retains nothing useful (T5.4 executed); forging an open on an old outpoint is invalid.
- **≥ k colluding operators:** silently decrypt everything, any time — the core residual trust. Mitigated by large n, diverse operators, on-chain attributable release records, optional staking/slashing. **Not eliminable in R1.**
- **Miners:** censorship delays openings (liveness, chain-wide property); reorgs handled by K-conf + attestations (T5.6); a miner cannot trigger release (watchers need confirmations, not mempool).
- **Infrastructure disappearance:** issuer can vanish at launch with zero impact. Committee disappearance below quorum bricks unopened boxes — the stated consequence of R1.

---

## 9. Exact BSV implementation boundaries

- **Consensus/script-enforced:** box ownership; the sealed→opened state machine (OP_PUSH_TX covenant via sCrypt; enforces OPENED output on opening spends); transfer rules; the impossibility of re-sealing.
- **Protocol/client-validated (independently implementable):** seal status (3-part public check); mix-net proofs; share-release records; ordinal tracing of the current seal outpoint. All from public chain data — requirement 9 holds for everything except key custody.
- **Off-chain computation:** shuffle proving (seconds–minutes, once, at creation); committee watching and partial decryption; client decryption after release.
- **External trust (explicit):** k-of-n committee honesty (secrecy) and persistence (liveness of future opening). Nothing else.
- **Not available on BSV and not needed:** native block-header/height opcodes (in-script SPV via supplied headers + PoW check exists if ever needed); CLTV/CSV (NOPs post-Genesis — irrelevant since no timelock is used).
- **Cost:** trivial by BSV standards — one setup tx, ~1 KB/box ciphertext data, one covenant spend per transfer/open, one small release-record tx per opening.

---

## 10. Prior art and honest novelty assessment

- **WE:** Garg–Gentry–Sahai–Waters 2013 (ePrint 2013/258) — theoretical; general WE remains non-deployable in 2026 (best lattice candidates rest on non-falsifiable assumptions, e.g. ePrint 2022/1140). The one efficient implemented WE is extractable WE for KZG commitments (ePrint 2024/264; code: github.com/rot256/research-we-kzg) — algebraic relations only, not chain events.
- **Encrypt-to-chain/time:** LJKW18 "How to Build Time-Lock Encryption" (DOI 10.1007/s10623-018-0461-x); Campanelli et al. EtF (ePrint 2021/1423, proves event-encryption is WE-hard); McFly signature-based WE (ePrint 2022/433 — the academic form of R1); Cassiopeia "on-chain WE via committee" (ePrint 2023/635 — R1 exactly, with accountability); DecryptChain (ePrint 2026/1195 — documents silent premature-decryption failures).
- **Deployed threshold release:** drand/tlock (ePrint 2023/189; docs.drand.love — time-gated only; League shutdown = ciphertexts die); Lit Protocol Naga mainnet (TEE-sealed federated operators, on-chain access-control conditions, EVM/Solana native — BSV only via a trusted HTTP bridge in a Lit Action); Fairblock FairyRing (threshold IBE with condition triggers for integrated chains).
- **Sealed packs in production:** NBA Top Shot (contents fixed pre-sale via on-chain hash, reveal **centralized** by Dapper); Metaplex Candy Machine / nft-packs (contents decided/drawn at mint or open); Gods Unchained chests (drawn at open); Parallel (Chainlink VRF at reveal). **No deployed system anywhere achieves provably-fixed-pre-sale AND hidden-from-owner trustlessly.** A BSV design with committed ciphertexts + covenant-enforced opening + committee release would be a genuinely novel construction — not a repack of an existing product.
- **ZKCP/adaptors:** Maxwell 2011/2016 (bitcoincore.org ZKCP announcement) and adaptor signatures (ePrint 2020/476) give "publish ⟹ reveal" only when the *publisher already holds the secret* — the direction asymmetry is structural (executed: T4). They cannot power a box the owner opens alone.
- **Verifiable shuffles:** Bayer–Groth (DOI 10.1007/978-3-642-29011-4_17); production: Verificatum (Estonia IVXV, Swiss Post, vVote, Helios/Belenios), ZKShuffle (Manta/zkHoldem), Geometry mental-poker toolkit. Shuffling 1,000 committed NFTs on-chain-verifiably costs seconds of proving and modest verification fees — solved problem.

---

## 11. Decisive prototype — executed, actual results

`sealed_box_prototype.py` (stdlib Python, real secp256k1 arithmetic with throwaway toy keys, fully simulated chain; nothing broadcast, nothing real). Full output in `prototype_results.json`. Results:

- **T1** enumeration of unsalted commitment: content recovered with 1,000 hashes in **1.2 ms** → commitments don't hide.
- **T1b** salted commitment hides from non-holders → salt custody = key custody.
- **T2** owner-held key: decrypted locally, **0 blocks mined** → private inspection trivial.
- **T3** key = H(opening signature): decrypted offline, no broadcast → signatures aren't opening events.
- **T4** adaptor release: owner completed adaptor **offline**, decrypted without publishing → publish-to-reveal cannot bind the signer.
- **T5 (R1 lifecycle, simulated chain):** committed inventory + simplified shuffle + 3-of-5 Shamir shares; mint → SEALED-VERIFIED; transfer → SEALED-VERIFIED; previous-owner open → **defended**; honest open → shares released only after 3 conf → correct pre-assigned NFT recovered; reorg-after-release → **detected** as inconsistent seal; committee at 2-of-5 online → opening impossible (the R1 consequence, demonstrated).

What the prototype deliberately does NOT do: real DKG/mix-net proofs (simplified, labeled), real BSV regtest txs. **Next prototype step:** sCrypt covenant for the seal state machine on regtest + a 3-process local committee watching regtest — establishes the BSV-specific mechanics end-to-end before any mainnet consideration.

---

## 12. Smallest necessary relaxations, ranked, with user-facing consequences

1. **R1 — k-of-n key-release committee (recommended).** Consequence to state to users: *"Sealed boxes are guaranteed by N independent key-keepers; as long as at least k of them exist and are honest, sealed means sealed — forever. If fewer than k survive, unopened boxes can never be opened."* Everything else is on-chain, open-standard, issuer-independent.
2. **R2 — TEE network (Lit-style).** Faster to integrate but adds Intel/AMD trust, a federated operator set, and (for BSV) a trusted data bridge. Strictly worse trust surface than R1 done natively.
3. **R3 — wait for practical WE.** Not a plan: no deployable scheme, and private-fork publication-binding is unsolved even theoretically.

**Clearly separated fallback (product change, NOT the requested product):** commit the inventory on-chain at creation; draw each box's NFT at opening from verifiable public randomness (future block hash via in-script SPV, or committee/beacon). Every existing "provably fair" pack does this. It satisfies transferability, seal verification, issuer-unpredictability, and server-independence completely — but the box contains *a draw from the committed set*, not a specific NFT assigned before sale. If the marketing truth "the NFT was in your box since creation" is load-bearing, this fallback is not available.

---

## 13. Recommendation

Build **R1** if the seal property is worth a standing committee; it is the only identified design that keeps every fixed requirement — fixed pre-sale contents, owner-hidden, open-when-you-want, opened-state collectible, publicly verifiable seal, issuer-free long-term operation (issuer can vanish; the committee cannot). Frame the committee as public infrastructure (a "seal league," drand-style federation of independent operators) rather than company infrastructure, so the standard survives the company.

---

## Sources (primary, as retrieved)

- eprint.iacr.org/2013/258 · 2013/860 · 2020/476 · 2021/1423 · 2022/433 · 2022/1140 · 2023/189 · 2023/635 · 2024/264 · 2019/017 · 2026/1195 · 2017/566
- DOI 10.1007/s10623-018-0461-x (LJKW time-lock encryption) · DOI 10.1007/978-3-642-29011-4_17 (Bayer–Groth shuffle; no ePrint version)
- docs.drand.love/docs/timelock-encryption · github.com/drand/tlock · github.com/rot256/research-we-kzg
- developer.litprotocol.com (Naga mainnet, node-ops, Lit Actions) · docs.fairblock.network
- hub.bsvblockchain.org/bitcoin-protocol-documentation/specification/upgrade-history · xiaohuiliu.medium.com/op-push-tx-3d3d279174c1 · docs.scrypt.io · docs.1satordinals.com · bsv.brc.dev/tokens/0160 · wiki.bitcoinsv.io/index.php/NSequence
- developers.dapperlabs.com/Packs/Events/Minted · github.com/metaplex-foundation/metaplex-program-library (nft-packs) · portal.godsunchained.com/blog (chests) · parallelalpha.medium.com (Chainlink VRF)
- github.com/verificatum/verificatum-vmn · github.com/Manta-Network/zKShuffle · zkholdem.xyz ZKShuffle paper · nmohnblatt.me/mental-poker-1 · maci.pse.dev
- bitcoincore.org/en/2016/02/26/zero-knowledge-contingent-payments-announcement · en.bitcoin.it/wiki/Zero_Knowledge_Contingent_Payment
- eprint.iacr.org/2025/819 (DKG SoK) · github.com/microsoft/electionguard
