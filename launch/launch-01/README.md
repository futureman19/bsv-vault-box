# LAUNCH-01 — frozen candidate and acceptance ledger

This is a **201-design inventory snapshot**, not final artistic acceptance, launch approval, minting, storage purchase or security certification. Inner collectibles are separate from outer enforced BoxSV custody. All 201 designs have edition supply one: 195 country-inspired designs, five oceans, Moon. No accessories or extra certificate NFTs are included.

## Consume this handoff

Use `launch-candidates.json` and each entry's immutable `selection.commit`, not the moving branch tip. Retrieve blobs with `git show <commit>:<path>` using binary-safe output. Each viewer, model/source, archive and promotional image has an actual byte count and SHA-256. `selection.fetched_tip` records reachability at reconciliation time. `inputs/` preserves roster and gallery metadata; `source-notes/` preserves readable source README guidance, including inherited limitations (and any truncated original prose). Original source README hashes identify original Git bytes; readable snapshots may have normalized newlines.

`approval.status` separates candidates from `needs-user-review`; `user_final_approved=false` means final launch approval is not evidenced here, not a claim that no previous component was ever approved. Morocco's source README identifies approved v5; its included baseline blend/GLB is preserved by immutable hash. V6 is partial. USA selects **v9, commit `1e6b1712959013285769a152b1d50bbf119f7729`**, not the older collection-review v1. V9 remains unapproved: stars wrap the restored thick lid but do not continue fully onto the fixed body. Exact requested pigments and four-left/five-front wrapping requirements remain explicit in its record and README.

`model_sources[].role` distinguishes selected-model payloads from historical baseline files. Do not mistake USA baseline-v8.glb for the embedded current model. `marketing` identifies **published promotional illustrations**, not actual-model screenshots or definitive primary artistic references. Existing promotional review acceptance never approves the 3D model. Provenance metadata is retained, not independently certified copyright clearance.

`qa/*.json` contains parsed historical reports with immutable source paths/hashes. These are not freshly rerun full acceptance. `missing_gates` is intentionally nonempty for every entry; no candidate is launch-ready.

## Results actually measured

- Exact roster reconciliation: **201 unique IDs; 195 Country / 5 Ocean / 1 Moon**; also matches the fetched gallery roster.
- All **201 delivered viewers match selected committed HTML**. All are below 5,000,000 bytes. Largest: **4,937,632 bytes**. Aggregate standalone viewers: **592,749,853 bytes**.
- All **201 source archives located**, opened, CRC-tested and checked for safe unique paths and required current viewer/model/source payloads. Full embedded inventories checked where supported: **196**. Five remain explicitly unchecked: Iceland, Morocco, Namibia, New Zealand, Paraguay. This is not a complete rebuilding test.
- **Three byte mismatches remain**: Iceland, Morocco and Rwanda archived HTML differs from selected Git/delivered HTML by line endings only. Normalized equality is diagnostic, **not** a waiver of exact-byte identity. Model/source payloads match. No old files or archives were rewritten.
- All **201 published promotional images** decode and match their gallery image size/hash records at the frozen marketing commit. Provider-original and optimized image hashes are different layers; only `image` metadata is the expected optimized blob hash.
- GLB headers, declared size, JSON chunks and embedding are inspected. These structural checks do **not** prove source/export parity, finite full geometry, attachment, clearance, PBR correctness or animation quality.
- Representative actual delivered viewers: Afghanistan, Arctic Ocean, Iceland, Japan, Morocco, Moon and USA v9. **14/14 fresh Edge offline cases** passed across desktop 1440×1080 and touch-emulated mobile 390×844: ready state, drag rotation, native buttons, open/close, interrupted reset, reduced-motion endpoints, no horizontal overflow, no external requests or page exceptions. These are pilot-interface smoke tests, not full fallback/81-pose/source acceptance and not physical-phone performance.
- **11 ledger regression tests passed**, including missing/duplicate IDs, tampered viewer digest, false approval, budget boundary, erased archive/release holds, falsely promoted historical QA, current local byte checks and exact representative smoke coverage/hash binding.

## Visual interpretation

`representative-comparison.jpg` and `smoke/<id>/{desktop,mobile}-{closed,open}.png` are actual captures. The board compares published promo with viewer screenshots without distorting aspect ratios; it is **not equal-object-width calibrated comparison**. All sampled models visibly load. Promo/model material and detail differences remain: Iceland is much darker, Morocco is warmer/pinker with weaker motif fidelity, USA fireworks are sparser and its known seam continuation remains unresolved. The other themes remain recognizable but are simplified relative to promotional illustration. This sampling is not acceptance of the remaining designs.

An independent read-only reviewer inspected actual ledger files, reread the three mismatching archives, reran the initial eight tests and inspected the comparison. It identified insufficient semantic guards in the verifier. Those guards were strengthened; the final eleven tests pass. See `independent-review.md`. This review is of ledger integrity, not approval of all artwork.

## Repeatable bounded commands

Run from the repository root in an isolated worktree with Git, Python, Pillow, Playwright and installed Edge:

```sh
python launch/launch-01/verify_ledger.py
python launch/launch-01/smoke_viewers.py
python launch/launch-01/make_comparison.py
```

`smoke_viewers.py --ids afghanistan arctic-ocean` permits a smaller exploratory sample, but the frozen ledger regression expects the complete seven-design/14-case sample. The harness reads unchanged delivered viewers using paths stored in the ledger and writes only this card folder. On another machine, supply equivalent local files and update paths in a **new** ledger copy, preserving hashes. It does not rebuild art or execute any node/wallet tooling.

`python launch/launch-01/build_ledger.py` repeats full read-only reconciliation against available local delivery paths and **current fetched refs**, writing a new snapshot in this folder. Preserve this frozen handoff first; do not use it to silently replace approved art. Fetching and regenerating later may change the recorded marketing commit. Budget roughly several minutes; the first 180-second run timed out after a partial report, retained as `reconciliation-output.txt`. Complete runs used a 600-second timeout.

`initial-ledger.json` preserves the initial archive oracle: basename matching wrongly treated nested historical baseline files as duplicate current payloads for Morocco/USA. The corrected probe prefers exact root paths, retains required payload equality and supports both inventory mapping and `files`-list schemas. The three real newline-only differences remain flagged. No model was modified to satisfy a test.

## Storage and downstream work

HTML already embeds GLB/runtime/fallback; **do not add HTML and GLB as mandatory runtime transfer bytes**. Standalone GLB, packed source and ZIP sizes are separately recorded. Local ZIP paths are not public storage guarantees; Git-backed archives and local-only archives are explicitly distinguished. No permanent storage policy, costs, hosting availability, on-chain inscription or recovery SLA is approved.

Pre-created ART review cards own per-design visual/full acceptance and any bounded polish. ART-04 owns Rwanda's byte discrepancy; ART-05 Iceland; ART-06 Morocco. ASSETS packaging should resolve exact-byte recovery decisions without silently changing source art. Every assigned ID must remain explicit. USA unresolved artistic choice requires user review rather than a falsely approved freeze. Release/mainnet/sale gates remain held.

No production docs, existing previews, other worktrees or old deliveries were changed. Only `launch/launch-01/` is authored on `feature/launch-01-ledger`.
