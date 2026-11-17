# ART-01 — bounded review, not art approval

All 26 assigned designs reviewed against parent ledger commit `6db6388d04fee0da8e0324a640d5880a5813a39c` (ledger SHA-256 `28e032084f6bddf80143fd3bfd0e5b06cbdf84dc2343937e7b9bc71734ac3c9c`). Exact immutable viewer/model/marketing refs, sizes and archive hashes are in `review-results.json` and `packaging-results.json`.

## Outcome
- 26 reviewed, none missing; 9 pass this bounded visual audit with disclosed limitations, 17 needs-decision, zero polished/changed designs.
- Pass is not user approval or launch readiness. All prior candidate/approval/release holds remain.
- 104 fresh full-resolution screenshots, 26 comparison boards. Four read-only delegated visual inspectors examined all boards; parent additionally inspected Afghanistan and confirmed Panama tree-count and Malaysia palette discrepancies. Independent downstream QA remains required.
- No demonstrated broken mechanism or runtime defect warranted regeneration. Remaining issues concern stylistic/material fidelity and promotional exaggeration; changing terrain, materials or promotional art to resolve the larger gaps requires art-direction decisions. No paid generation, existing preview mutation, production edit, mint, key or funds operation.

## Executed checks
- All 26 viewers hash-match selected committed bytes and are strictly below 5,000,000 bytes (1,933,034–4,331,574 bytes).
- All selected source BLEND/GLB bytes hash-match; GLB container and embedded-buffer checks run. Source ZIP hashes, CRCs, safe unique paths and required HTML/GLB/BLEND member presence checked afresh. This does not reopen Blender or establish full archive-inventory parity; Namibia's inherited full-inventory hold stays explicit.
- 52 offline Edge cases: desktop 1440×1080 and emulated touch mobile 390×844; ready, drag, reset, open/close, interrupted reset, reduced-motion endpoints, no horizontal overflow, no external HTTP(S) requests or page errors. All pass. This is not physical-phone performance or fine-grained reduced-motion timing proof.
- 26 motion-unit runs passed. Barbados runs its original 81-pose numerical script; Costa Rica has no original test file, so the unchanged Afghanistan motion contract assertions were applied to its exact module. Other designs use their original tests. These are not collision tests.
- New source generation/parity, full sampled collision, corrupt-GLB and no-JS fallbacks were not rerun for unchanged assets; historical evidence is not relabeled fresh.

## Harness corrections (2, no product changes)
1. Initial motion extraction failed because Barbados uses `test_motion.mjs`, not `tests.mjs`: Git exit 128, `fatal: path 'preview/barbados-v1/tests.mjs' does not exist in '1251c2891f359e1efd2454959801905d215a2c66'`. Filename discovery also found Costa Rica lacks a test file.
2. Conservative safety scan then rejected Barbados `node:fs`. Inspection showed its sole write is card-local `new URL('motion-check.json',import.meta.url)`; this exact scoped use was allowed. No node/chain executable was invoked. Both actual failures are retained here as diagnostic transcriptions, not raw captured logs.

## Review use
`review.html` is a self-contained poster/comparison report, NOT an interactive model viewer. Full-size captures are in `smoke/<id>/`; boards use scaled/cropped desktop images and are not calibrated equal-size material comparisons. No collision can be inferred from them. Unchanged interactive viewers remain at the exact `delivered_viewer.path` in the frozen ledger; their hashes were checked before opening. Models, sources and original ZIPs are not redundantly repackaged into this evidence-only report.

Run from the worktree: `python launch/art-01/prepare.py`, `python launch/art-01/smoke_viewers.py --ids <assigned IDs>`, `python launch/art-01/run_motion.py`, `python launch/art-01/make_boards.py`, `python launch/art-01/finalize.py`. Python needs Playwright/Pillow; Edge and Node are local dependencies. The frozen ledger contains machine-local delivery paths; portability is not claimed.

Next: QA-ART-01 independently inspects all 26 outcomes and preserves the 17 visual decision holds. User chooses whether the simplified candidates or closer model/marketing alignment should guide any further art work. No model is silently promoted to an approved baseline.
