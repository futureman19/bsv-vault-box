# VAULT-0001 consensus differential

## Result (executed 2026-10-27)

**Zero disagreements for the three canonical regtest transactions against the live Lean evaluator and SV-node v1.2.3.** All three script verdicts were valid under both the block and relay flag words: six agreeing transaction/column cells, zero undecided runs, zero unknown descriptions, zero flag-word drifts, and zero witnesses. This is bounded positive-path conformance evidence, **not a proof that the covenant cannot be bypassed**.

The committed [corpus](consensus-evidence/vault.jsonl) contains exact signed transaction bytes and every prevout's script, amount, outpoint and actual creation height. [Lean results](consensus-evidence/spec.jsonl), [node cells](consensus-evidence/cells.jsonl), [driver output](consensus-evidence/node.log), and [witness manifest](consensus-evidence/node/sv-node/manifest.json) are real execution output. The witness JSONL is intentionally empty.

## Environment and pins

- Windows host; execution in `wsl -d Ubuntu-24.04`, Linux x86_64, kernel `6.6.87.2-microsoft-standard-WSL2`; approximately 15 GiB RAM and 4 GiB swap reported.
- Deliverable base: bsv-vault-box `d0b807c`, branch `codex/consensus-differential`. Only `REVIEWS/` changes.
- External clone: `/home/futureman19/consensus-t_a71c39fc/bsv-script-lean`, commit `387dab351273e9018cffb595ef40521f39e4b8d3`; clean source tree after execution. No vendoring or submodule.
- Lean `leanprover/lean4:v4.34.0`; Mathlib `5ed2965256430c3649e86755f9576b54eca72435`; Rust `1.95.0` (installed via elan/rustup without modifying shell startup files).
- Reference executable `/home/futureman19/bitcoin-sv-1.2.3/bin/bitcoind`: `Bitcoin SV version v1.2.3`; RPC subversion `/Bitcoin SV:1.2.3/`, version `101020300`. The formal project's reference source pin is `6504a3aff65ba97c0f6c80962b033e35ecbfed4b`. This run verified the binary/RPC version, not a reproducible binary-to-source build attestation.

## Base verification

Executed in the external clone:

```sh
git clone https://github.com/Calhooon/bsv-script-lean
cd bsv-script-lean
git checkout --detach 387dab351273e9018cffb595ef40521f39e4b8d3
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
VERIFY_LIGHT=1 make verify
```

Initial attempt stopped at `lake: not found`; after installing elan and the pinned Lean toolchain, libraries/evaluator compiled and self-test passed, then smoke stopped at `cargo: not found`. Installed the pinned Rust toolchain and reran the exact light gate successfully (exit 0). An intervening shell-wrapped attempt had a malformed exit-status wrapper; it is not used as evidence. The final run used Python `subprocess.run` with an explicit environment and captured the make return code.

[Full successful output](consensus-evidence/verify-light.log):

- Lean libraries and evaluator build passed (evaluator build: 2054 jobs).
- CLI 13/13 rows; fixed vectors 28/28, each twice.
- Self-test: flow 1094/1094 and seed 10000/10000 agree with their recorded comparison verdicts; `bsvs --self-test: GREEN`.
- Live bsv-rs 0.7.0 smoke: 10000/10000 agree with **recorded bsv-rs** verdicts; zero panic/nondeterminism. These are upstream seed tests, not additional VAULT tests.
- Final line: `verify: LIGHT, not GREEN (steps 1, 3 and 4 passed; step 2 SKIPPED BY NAME, VERIFY_LIGHT=1)`.
- Kernel witness and axiom check explicitly skipped by light mode; not passes.

## Canonical shapes

IDs come from `vault/evidence/regtest-cycle.txt`, linked as one lifecycle (box 0). The exporter independently recalculates each txid from raw bytes.

| Shape | Transaction ID | Mined height | Inputs | Bytes | Lean / node |
|---|---|---:|---:|---:|---|
| Deploy | `75736f4ef1b20c3b77c53bc47ac001e70d7b71123cb458962164b983b28b86e4` | 170 | 1 | 4856 | valid / valid |
| Sealed transfer | `bf1823bf3529b18e025b2ffdcfcfc0aeb0d92aa44f2c711d0bf415de5d59f847` | 176 | 2 | 9880 | valid / valid |
| Open | `33c369ac3970c1f7321edccbe3581b37a27cc694fb5c0661f1cba85ca4ad7659` | 177 | 2 | 9878 | valid / valid |

Deploy spends P2PKH funding and creates the sealed covenant; it does not execute the newly created covenant. Transfer spends the covenant at input zero plus P2PKH fees, creates its sealed successor with a different owner, and exercises owner signature and successor-output binding. Open spends that successor plus fee funds and creates the opened state, exercising the opening branch and output binding. No transaction was synthesized, re-signed or broadcast during this task.

### Recovering the original data

The running 18443 node had tip 158, while these transactions were mined at 170–177 on the separate stopped 18445 chain documented in `vault/REGTEST.md`. Therefore the running node could not supply this recorded lifecycle. It was left unchanged.

The retained chain was found at `C:/Users/futur/sealed-box-research/.worktrees/t_abde32f1/bsv-vault-box/vault/.regtest-node/regtest`. Only `blocks`, `chainstate`, `frozentxos`, and `merkle` were copied into a task-owned WSL `replay-node/regtest`. **No wallet, credentials or mempool were copied.** The copy was started wallet-disabled, peer-disabled, txindex-enabled, Genesis height 1, on RPC 18445. [collect.py](consensus-evidence/collect.py) uses an explicit read-only RPC allowlist to export the corpus. It is an optional local recovery helper; readers can replay the committed corpus without this chain or exporter.

## Differential configuration and exact reproduction

Run the following in WSL, after the light gate above and with the reference node binary installed. Set `EVIDENCE` to the absolute location of this report's sibling directory:

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd "$HOME/consensus-t_a71c39fc/bsv-script-lean"
(cd harness && cargo build --release --locked --bin run_svnode --bin run_diff)
export EVIDENCE=/mnt/c/Users/futur/sealed-box-research/.worktrees/t_a71c39fc/REVIEWS/consensus-evidence
python3 "$EVIDENCE/run.py"
```

[run.py](consensus-evidence/run.py) records the exact argument arrays and invokes these core commands from the external clone:

```sh
eval/bsvs corpus "$EVIDENCE/vault.jsonl" --out "$EVIDENCE/spec.jsonl" \
  --config sv-regtest --genesis-height 1 --chronicle-height 15000
harness/target/release/run_svnode \
  --corpus "$EVIDENCE/vault.jsonl" --spec "$EVIDENCE/spec.jsonl" \
  --spec-config sv-regtest --genesis-height 1 --chronicle-height 15000 \
  --rpc http://127.0.0.1:18563 \
  --cookie "$HOME/consensus-t_a71c39fc/oracle-node/regtest/.cookie" \
  --witnesses "$EVIDENCE/node" --cells "$EVIDENCE/cells.jsonl"
```

The helper starts a new wallet-disabled, peer-disabled oracle node from the upstream `harness/oracle/bitcoin.conf`, changing only Genesis to 1 and Chronicle to 15000, with its own data directory and ports. Its policy limits are zeroed to consensus maxima, as required by the upstream driver (the `verifyscript` RPC itself always uses the policy path). The driver validates settings, probes era bits, obtains live Lean flag words, and checks every applied node flag word. Observed block word `0xD402B`; relay word `0xD47FF`.

**Corpus format caveat:** `params.era` is `pre-genesis` because the Rust corpus validator computes that descriptive label using hard-coded *mainnet* height thresholds. Actual execution is post-Genesis/pre-Chronicle: explicit `sv-regtest(genesis=1,chronicle=15000)` and the derived/probed words establish the real era. Heights and transaction bytes were not altered to accommodate the validator. An initial missing-era/then post-genesis-label export was refused before comparison; the final export satisfies this format requirement. An initial oracle call also returned startup `-28 Verifying blocks`; the helper now waits for readiness.

### What was compared

- **Live Lean vs live SV-node v1.2.3:** all three transactions, both flag-word columns. Six cells all valid and agreeing; no timeouts, no skipped cells, no divergence witnesses.
- Lean transaction gates were separately valid for all three in both columns. The node driver here compares **script verdicts**, not the node's full transaction admission/block path.
- Relay-word column used the **same consensus-limit oracle instance**, not a separate default-policy node. Thus it demonstrates relay-flag agreement, not like-for-like default mempool-limit agreement or fresh mempool admission. Historical mining is separately recorded in the source lifecycle.
- bsv-rs ran only the upstream base smoke. VAULT-specific bsv-rs, go-sdk, @bsv/sdk, GoBDK and Teranode comparisons were **not run**: the bounded reference comparison targets the consensus implementation, and additional adapters are not needed to establish the reported two-implementation result. No claims about their acceptance of these VAULT transactions.

## Witnesses and interpretation

The upstream manifest's `generated: 2026-09-23` is its hard-coded fallback when `SOURCE_DATE` is unset (`run_svnode.rs`), **not this run's date**. It is retained verbatim. Its `maxscriptnumlengthpolicy: 4` reflects the empty oracle chain's pre-Genesis tip; the driver's explicit-height probes and per-input words determine the tested post-Genesis execution, not that tip-level readback.

**Witness count: 0.** The empty `node/sv-node/consensus-evidence.jsonl` and manifest record the clean result. This is not inferred merely from `GREEN`: upstream GREEN can include explained divergences; here both the divergent-run count and witness count are explicitly zero.

This supports acceptance parity for these exact valid deployment, transfer and opening bytes under the pinned formal definition and reference node's script semantics. It does not prove owner authorization for all possible inputs, immutable-field enforcement against adversarial mutation, absence of alternate spend paths, compiler correctness, a universal sealed-state invariant, full node correctness, mainnet activation parity at other heights, or miner policy acceptance. No adversarial corpus or covenant-specific Lean theorem was added. The Lean project itself explicitly says it **does not prove the node correct**. No full kernel-witness/axiom gate was run.

No mainnet requests or broadcasts, wallet signing, covenant changes, or protected-file edits occurred. Both task-owned nodes were stopped after verification. The pre-existing 18443 node remained running and unchanged.

**Recommended next action:** review and merge this report as bounded positive-path evidence. A separately scoped negative/mutation corpus would be the next useful security test, not an expansion of the claims made here.
