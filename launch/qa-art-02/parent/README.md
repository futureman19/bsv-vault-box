# ART-02 — bounded review of 25 unchanged candidates

All exact assigned IDs reviewed. Result: **18 review-candidate passes, 7 needs-decision, 0 polished, 0 omitted**. Pass is not final art approval. No existing art, production docs, dependencies, wallet, chain or sale state changed.

## Evidence and provenance

`review-results.json` is the per-ID handoff, including immutable refs, HTML/GLB/blend/archive hashes and sizes, image paths, visual findings, actual executed checks and remaining gates. Parent ledger pinned to `6db6388d04fee0da8e0324a640d5880a5813a39c`; its exact bytes are retained in `parent-ledger.json`. `sources/` contains byte-verified committed promotional WebP and source design briefs/READMEs, not newly generated art. `smoke/` contains 100 fresh full viewport captures; `boards/` contains 25 corresponding comparison boards (proportional display, cropped desktop UI, not calibrated material/lighting comparisons).

Five read-only delegated visual inspections examined the five panels for every design (delegation `deleg_51280029`). `visual-findings.json` faithfully condenses their findings by hardware, terrain, texture and marketing gap. Parent separately reinspected Atlantic and São Tomé comparison boards; substantive appearance mismatches confirmed, renderer malfunction not established. The pre-created **QA-ART-02 t_5c96269b** owns the next independent verification. These delegated observations do not replace that gate or user approval.

## Executed bounded checks

- 25 committed HTML payloads byte/hash checked against parent; all **2,017,782–4,490,498 bytes**, strictly below 5,000,000.
- Selected standalone GLB and editable blend blob hashes verified. GLB size header verified and its exact base64 bytes found embedded in each HTML.
- 25 existing source ZIPs read back: safe unique paths, CRC, and exact required HTML/GLB/blend hashes. Full archive inventory validation remains explicitly historical parent evidence; this pass rechecked required payloads, not every archive member's inventory hash.
- 50 fresh offline Edge cases: desktop 1440×1080 and mobile/touch emulation 390×844 per ID. Real drag/touch rotation, Open/Close, interrupted Reset, reduced-motion endpoints, no external HTTP requests/page errors and no horizontal overflow passed.
- 25 fresh JavaScript-disabled mobile poster checks and 25 actual-loader finite-position/nonempty mesh checks passed.
- Common Albania motion-contract tests rerun against each design's exact `motion.mjs`: 25 modules passed. These test staged latch-before-lid poses/clamps and invalid-asset rejection; **not fresh mesh-collision sampling**.
- Original source/hinge/collision reports remain historical. No source authoring/export occurred, no full Blender reopen/parity/collision rerun, no fresh corrupt-GLB fallback test. Physical phone performance and independent security certification are not established.

`diagnostics.txt` preserves the absent-test-file harness assumption and redundant read-only packaging diagnostic timeout. No art gates were weakened. `motion-summary.txt` uses an inherited “original motion suites” console label; authoritative scope is the shared-test provenance in `motion-results.json`.

## Needs decision — no substantial redesign performed

| ID | Unresolved visible fidelity |
|---|---|
| atlantic-ocean | Repetitive zigzag ocean surface and flatter/lower ridge than promotion. |
| brazil | Repetitive round crowns, flat tan terrain and reduced forest-bank realism. |
| dominican-republic | Pale irregular island base/stone relief less pronounced. |
| germany | Village terrain reads as a flat regular platform. |
| haiti | Botanical steel ornament flatter; metal bluer/more mottled. |
| sao-tome-and-principe | Coarse dominant checker-like material across exterior/interior versus quieter promotional finish. |
| uzbekistan | Turquoise ornament relief not clearly readable enough to substantiate the presentation claim. |

These are fidelity/acceptance decisions, not demonstrated broken controls or detached geometry. Changing these major material/terrain treatments to match enhanced illustrations could become substantial artistic redesign; user approval is reserved. Therefore zero speculative corrections were made and all immutable originals are retained. The other 18 also have explicitly recorded material/lighting simplifications, not claimed photoreal equivalence.

## Reproduce

From repository worktree, with Python Playwright/Pillow and Edge installed:

1. `python launch/art-02/prepare.py`
2. `python launch/art-02/smoke_viewers.py --ids <the exact IDs in review-results.json>`
3. `python launch/art-02/boards.py`
4. `python launch/art-02/motion_checks.py`
5. `python launch/art-02/extended_checks.py`
6. `python launch/art-02/finalize.py`

Existing delivered viewers use recorded machine-local paths; scripts require the immutable Git objects and original review output directory. Source ZIPs remain at their exact committed paths and are not duplicated into this evidence package. This is review evidence, not a new model delivery or hosted preview. The small report ZIP contains reports and comparison boards; complete capture evidence is on the feature branch.

Next: QA-ART-02 independently verifies all 25 and preserves the seven decision holds; request the user's fidelity direction before substantial redesign. Nothing here authorizes launch, storage spending, minting or deployment.
