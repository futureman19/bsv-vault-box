# Independent adversarial review — VAULT sealed-box stack

Reviewer: grok (did not author this code). Scope: master @ `072eb69`. Method: read specs + implementations, run the stated gates, then try to break them with extra inputs. No broadcasts, no spends, no keys.

**Gates run (all pass):** `python -B v3_ref.py` 15/15; `node.exe test/vault3.test.js`; `node.exe --test test/checker.test.js` 15/15; `python -B test/python-parity.py` (50 cases); `node.exe --test test/checker-ui.test.js`. Regtest was **not** re-executed (needs a local BSV node); claims below use `vault/scripts/regtest-cycle.js` + the two committed evidence logs. `vault/artifacts/vault.json` is **gitignored and absent** from this worktree; covenant review is `vault.ts` + `vault.test.ts` + live mainnet scripts (read-only).

Live (GET only, 2026-10-26):

| Box | txid | trailer state | WoC unspent | conf |
|---|---|---|---|---|
| A | `f3590347…dd39` | `6a0001` **00** … `2500000000` | yes, 1 sat @ vout 0 | 19 |
| B | `2aaa4efa…e67f` | `6a0001` **01** … `2500000000` | yes, 1 sat @ vout 0 | 19 |

Both locking scripts start with `ARTIFACT_PREFIX` `0176018801a901ac2097dfd76851bf465e8f7155`.

---

## Verdict

I would **not** treat this system's `SEALED-VERIFIED` headline, or a pack printed by a random client, as sufficient to pay for a mystery box. The **covenant state machine** (SEALED→OPENED, no reseal, no `contentRef` swap, no theft of the 1-sat output without the owner key) looks sound on the evidence I have. The **draw library**, given a valid manifest and a pinned `D=1` seed, is deterministic and I could not grind a single box as a non-miner. Trust fails at the seams: advertised odds vs rejection sampling, mint **format split** between the official demo and the public checker, sealed boxes never binding `content_ref` to a manifest in the checker, issuer-chosen `boxId`, and an unpinned compiled artifact.

---

## Findings (severity-ranked)

### H1 — HIGH — Official mint format is invisible to the public checker

**Where:** `vault/scripts/regtest-cycle.js:75-80` (1Sat `OP_FALSE OP_IF "ord"` envelope) vs `docs/vaultcheck.js:178-205` (`taggedJson` only accepts scripts matching `/^(006a|6a)/`, i.e. `OP_FALSE OP_RETURN` / `OP_RETURN`).

**Attack / failure:** Operator follows REGTEST.md, mints a correct pack as an ordinal inscription. Buyer pastes that mint txid into https://futureman19.github.io/bsv-vault-box/. Checker never sees `VAULT3-MINT`, sets `claimed = null`, verdict **`INVALID-MINT`**. Conversely, a seller can pass the public checker with an OP_RETURN mint the demo never produces, while the “canonical” inscription sits beside it.

**PoC (executed):**

```
ord envelope prefix:     0063036f7264…     → checker: "Expected exactly one VAULT3-MINT payload"
OP_RETURN VAULT3-MINT:   006a0b5641554c54… → checker: parsed JSON OK
```

`CHECKER.md:50` admits “not ordinal envelopes”. That is a protocol split, not a footnote: the only executed lifecycle uses the format the public verifier cannot read.

---

### H2 — HIGH — `allow_pack_duplicates: false` inverts later-slot odds vs committed “rarity = weight/total_weight”

**Where:** `VAULT-0003-draw-at-open.md:40` (“rarity = weight / total_weight”) and `:68-71` (rejection sampling); `draw.js:23-32`.

**Math:** Slot 0 is drawn from π_i = w_i / W. A rejected redraw is π conditioned on “id not already taken.” For a 2-design pack that is sampling **without replacement**: slot 1 is the complement of slot 0. If the catalog is skewed, slot 1’s distribution is the **inverse** of the advertised table.

**PoC (50,000 packs, `draw.js`):**

Manifest: `pack_size=2`, `allow_pack_duplicates=false`, weights `{common:99, rare:1}` (advertised rare = 1%).

| slot | P(common) | P(rare) |
|---|---|---|
| 0 | 0.98942 | 0.01058 |
| 1 | 0.01058 | **0.98942** |

Same table with `allow_pack_duplicates=true` (30,000 packs): slot 1 rare = 0.011 (matches the table).

This is not a grind. It is a buyer-odds bug if any UI/spec sentence treats weights as per-slot probabilities. A 2-card “99% common” no-dup pack is a **99% rare second card**.

On the 1,000-design Genesis catalog (9 main slots, 8,000 packs) the effect is small: commons 0.98976 vs advertised 0.98999; mean retries/pack 0.039. Large catalogs hide the lie; **the algorithm still allows the 2-card bomb**, and `validateManifest` will accept it.

SHA-256 modulo bias for W=90,910: relative error ~ 2^−239. Irrelevant. Weight-walk at `index == cumulative` correctly assigns the **next** id (`draw.js:26`, `index < cumulative` ≡ spec “cumulative > draw_index”). Checked on weights `[2,3,5]`: indices `0,1 → 0`; `2 → 1`.

---

### M1 — MEDIUM — `OPENED-VERIFIED` does not mean the output is still unspent

**Where:** `docs/vaultcheck.js:304-308`.

```js
if (isUnspent && v.state.boxState === 0)
    verdict = conf >= K ? 'SEALED-VERIFIED' : 'SEALED-PENDING'
else if (v.state.boxState === 1)
    verdict = conf >= K ? 'OPENED-VERIFIED' : 'OPENED-PENDING'  // no unspent test
else verdict = 'SPENT-UNRESOLVED'
```

**Attack:** Seller shows the opening tx. Checker returns `OPENED-VERIFIED` (and will even recompute a pack). The opened covenant UTXO was already transferred to someone else. Buyer pays for an outpoint they cannot spend.

**PoC (executed against `docs/vaultcheck.js` in the checker test VM):** unspent list empty → `SPENT_SEALED = SPENT-UNRESOLVED` (good), `SPENT_OPENED = OPENED-VERIFIED` with `unspent: false`. The stock checker fixtures already return `OPENED-VERIFIED` with `unspent: false` for the opening tx (mock unspent list points at the sealed outpoint).

Spent **sealed** outputs are handled. Spent **opened** outputs are not.

---

### M2 — MEDIUM — Sealed boxes never check the manifest / `content_ref` weld

**Where:** `docs/vaultcheck.js:309` (`checkPack` only if `boxState === 1`).

**Attack:** Buyer is told “this sealed mystery box is welded to odds table T.” They paste holding txid **and** `manifestTxid` into the public checker. Result: `SEALED-VERIFIED` with **no** `packStatus`, **no** commitment comparison. A seller can pair any sealed vault with any published manifest in the UI; the weld is not verified until after open.

**PoC:** `checkBox(sealed, 3, {manifestTxid})` → `verdict=SEALED-VERIFIED`, output keys `vout,state,unspent,conf,verdict` only.

`content_ref` is a hash, not a locator (`CHECKER.md:17-22`) — fine. Ignoring a locator the user **did** supply is the bug.

---

### M3 — MEDIUM — `boxId` is issuer-chosen; duplicate IDs share packs

**Where:** `VAULT-0001-sealed-boxes.md:15` (normative `sha256d(genesis_outpoint)`); `vault/src/contracts/vault.ts:24-27` (constructor takes any `Sha256`); `vault/scripts/mainnet-cycle.ts:121-126` (`mkRef('VAULT-0001 live box A id')`); `vault/scripts/regtest-cycle.js:144-150` (hash of a **funding** outpoint, not the covenant’s own outpoint). `REGTEST.md:92` already flags this.

**Attack:** Issuer deploys N boxes with the same `boxId`. Any that open in the same draw block receive the **identical** pack (`draw.js:11` seed domain is `boxId` + block hash, not outpoint). Marketplace identity (“the genesis box”) is not unique. Not theft of the UTXO; it is identity / fairness.

Live Box A/B are **not** outpoint-bound. v0.1 is what is on mainnet.

---

### M4 — MEDIUM — Compiled covenant is not in git; compiler is `scrypt-ts: "latest"`

**Where:** `vault/.gitignore:4` (`artifacts/`); `vault/package.json:35` (`"scrypt-ts": "latest"`). Task asked to review `vault/artifacts/vault.json` — **file does not exist in the repo**.

**Impact:** A reviewer cannot pin bytecode to `vault.ts`. `npm ci` today need not equal scrypt-ts 1.20.0, which is what `ARTIFACT_PREFIX` / `ARTIFACT_CODETAIL` (`docs/vaultcheck.js:21-24`) fingerprint. New compiles can silently fall off the public checker; old mainnet boxes cannot be reproduced from source + lockfile alone (`package-lock.json` may pin a moment in time, the declared range does not).

I did not recompile. Live scripts match the published prefix/trailer. That is not a source↔artifact proof.

---

### M5 — MEDIUM — Spec §6 preimage ≠ implemented preimage

**Where:** spec `:68` `SHA256("VAULT3-DRAW" || box_id || seed || slot || retry)`; `draw.js:11` / `v3_ref.py:52` `VAULT3-DRAW|{boxId}|{seed}|{slot}|{retry}` as UTF-8 with **decimal** slot/retry.

A second implementation written from the spec (raw concatenation, big-endian slot, 32-byte hashes) will not replay this library’s packs. JS additionally rejects `|` in `boxId`/`seed` (`draw.js:6`); Python `v3_ref.py` does not — so the “reference PoC” is not a validator.

Library-internal JS↔Python parity holds (50 cases). Spec-level interoperability does not.

---

### M6 — MEDIUM — Unbounded rejection loop in the Node library

**Where:** `draw.js:23-32` (`while(true)`); `docs/vaultcheck.js:144` (budget 100,000, fail-closed).

**PoC:** weights `{100000, 1}`, `pack_size=2`, no dups. First seed that drew the heavy item needed **48,142** retries (geometric mean ~100,001). `Number.MAX_SAFE_INTEGER` weights are legal (`manifest.js:49`). Node `drawPack` will spin; the browser checker throws and refuses a pack. Same protocol, two availability behaviors. A griefing issuer (or a copy-paste catalog) DoSes indexers that call `draw.js` with no cap.

---

### L1 — LOW — Draw delay `D` is not on-chain

`draw.js:4,36-44` default `D=1`; checker hardcodes `height + 1` (`docs/vaultcheck.js:244`). Spec allows `D=0`. Executed: 20-design pack, open height 100, `D=0` pack `[12,14,9,6,16]` vs `D=1` `[6,6,2,9,14]`. Anyone using the library’s `delay` argument disagrees with the public checker. No opener-controlled **value** besides *when* they broadcast; with `D=1` they cannot see the seed first. Miner grind is still priced in hashpower (`D=0` ≈ remine one block; `D=1` ≈ two consecutive).

---

### L2 — LOW — Covenant fingerprint is prefix + tail, not the body

Documented in `CHECKER.md:48`. `findVaultOutputs` (`docs/vaultcheck.js:64-66`) does not require the full 4,560-byte artifact. I did **not** produce a working anyone-can-spend lookalike that still matches prefix+tail+trailer; treat as residual, not a demonstrated steal.

---

### L3 — LOW — Spec/implementation drift on the wrapper (not a spend bug)

- Spec `owner_pkh` (20 bytes); contract `owner: PubKey` (33-byte compressed). Live trailer matches the contract.
- Spec §5 open-to-recipient in one tx; `open()` (`vault.ts:53-61`) cannot change owner.
- Spec §4.1 ord envelope on the vault UTXO; deployed script has none (`REGTEST.md:26`).
- Checker hex regexes are lowercase-only (`parseStateTrailer` `[0-9a-f]`). WoC today returns lowercase; an uppercase source would yield `UNRECOGNIZED-STATE` / `NOT-A-VAULT`.

---

### L4 — LOW — Checker is Tier-0 WoC, K=3, TOCTOU

Unspent is a point-in-time WoC read (`docs/vaultcheck.js:293-298`). Spec §7 wants K≥6 for high-value and lineage tracing. `index.html:31` says the proof is “the chain itself” and that the operator is untrusted; the JS still trusts WoC and the GitHub Pages copy of `vaultcheck.js`. Classic buy-between-check-and-payment race remains.

---

## Area reports (explicit “no findings” where clean)

### 1. Draw function (`VAULT-0003` §6, `draw.js`, `v3_ref.py`)

| Check | Result |
|---|---|
| Opener-controlled inputs at open | **No finding.** Seed is box id (fixed at mint) + draw-block hash. No extra nonce. |
| D=0 vs D=1 timing | See L1. Not an opener grind for D=1. |
| Rejection termination | Terminates iff each table has ≥ bound unique ids (`manifest.js:70`). Pathological **time** is M6. |
| Rejection vs committed rarity | **H2** — not uniform-independent; small skewed no-dup tables invert later slots. Large Genesis table ≈ advertised. |
| Weight-walk `idx == cumulative` | **No finding.** Next item. Last index `W-1` hits the last row. |
| SHA-256 domain collisions | **No finding** in JS (`|` rejected; 5-field encoding injective). Spec text without delimiters **is** collidable (M5). |
| Canonicalization | **No finding** in `manifest.js`: key order is code-point sort; floats / zero / negative / duplicate ids / wrong totals throw; extra JSON whitespace cannot survive `canonicalSerialize`. Python PoC is looser (not a production parser). |

Could not predict a D=1 pack. Could not bias a single box at open time without mining.

### 2. Covenant (`vault/src/contracts/vault.ts`; artifact missing)

Read `vault.ts`, `vault/tests/vault.test.ts` (8 script-VM cases: theft, content swap, reseal, double-open, sealed+opened transfer), live ALL\|FORKID spends.

| Check | Result |
|---|---|
| Forge successor | **No finding.** `hashOutputs` binds `buildStateOutput(amount)+buildChangeOutput()`. |
| Skip states | **No finding.** `open` requires `boxState == 0n` and writes `1n` only. |
| Reseal | **No finding.** `transfer` does not mutate `boxState`; tampered next instance → `hashOutputs mismatch` (test L155-167). |
| Swap `content_ref` | **No finding.** `@prop()` immutable; forged next instance rejected (test L72-90). |
| Steal output | **No finding** without owner `checkSig`. Amount is `ctx.utxo.value` (cannot peel the 1 sat to a non-vault output). Extra outputs besides state+change fail the hash. |
| Deploy already-OPENED / garbage state | Possible at construction (no on-chain genesis constraint). Not a spend of someone else’s box. Checker would not call it SEALED. |
| Identity | **M3.** |

I would trust this UTXO not to reseal or mutate `contentRef` **if** I am looking at the real compiled body (see M4).

### 3. Public checker (`docs/vaultcheck.js`)

| Check | Result |
|---|---|
| Hide opened/spent as sealed | **No finding** for sealed: spent sealed → `SPENT-UNRESOLVED`. Genesis compiler trailer is not parsed as SEALED. |
| Hide spent opened | **M1.** |
| Fake odds on a sealed box | **M2.** |
| Trailer edges | End-anchored; extra suffix → `UNRECOGNIZED-STATE`. Compressed 02/03 only. |
| Artifact-prefix collision | Residual L2; no working fake. |
| Unspent races | L4. |
| Mint parse | **H1.** |
| Opening height vs later transfer | Tests cover this; `findOpening` walks back to SEALED parent. **No finding.** |
| Draw-block previous-hash | Fail-closed on mismatch. **No finding.** |

### 4. Regtest demo vs `REGTEST.md`

The two evidence files (`vault/evidence/regtest-cycle.txt`, `regtest-cycle-repeat.txt`) show the five listed checks: pending at D=1, two child-process replays equal, forged inscription mined and client-rejected, unique main slots, legendary slot 9. Script structure matches those asserts.

**Gaps (not faked; not proven either):**

- Replay is the **same** `draw.js` in a child process (`regtest-cycle.js:176-177`), not a second algorithm. `REGTEST.md:10` is honest.
- Invalid mint is **client** `verifyMint`, not consensus. Honest at `:11`.
- Demo never calls `docs/vaultcheck.js`. Combined with H1, the lifecycle does **not** prove the public checker would accept its own mints.
- No miner-resistance, reorg, SPV, or mainnet VAULT-0003 run. Honest at `:90`.
- Box identity is not spec §2 (`REGTEST.md:92`).
- I did not re-run the node. I am not claiming the logs are authentic beyond “they are in git and consistent with the script.”

---

## What I would need before trusting a paid sealed box

1. Pin `D=1` in the manifest/covenant (or refuse D=0).
2. Pin mint encoding: either teach `taggedJson` the ord envelope, or mint OP_RETURN like the manifest. One wire format.
3. Checker: verify `manifestTxid` for **SEALED** boxes; require `unspent` for OPENED if the UTXO is what is being sold.
4. Commit `vault.json` (or a SHA-256 of the locking body) and pin `scrypt-ts` to 1.20.0, not `latest`.
5. Bind `boxId` to the genesis outpoint (spec v0.2) or treat today’s ids as non-unique labels.
6. If `allow_pack_duplicates` is false, publish **per-slot** probabilities (or forbid tiny skewed tables), not `weight/total_weight` as “the rarity.”
7. Do not use this checker as SPV. Label WoC.

Until then: the live 1-sat toys (Box A sealed, Box B opened) match the v0.1 wrapper. They are not a mystery-pack product.
