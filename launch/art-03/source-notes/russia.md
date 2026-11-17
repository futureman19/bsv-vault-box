# Russia v1 — Baikal Blue Ice

Open `russia-v1.html` directly in Edge/Chrome. Self-contained offline interactive model: **HTML 2,645,132 bytes; GLB 1,394,992 bytes**. Drag/touch rotation, Open/Close, Reset and reduced motion. No minting, hosting, chain access or custody action.

## Design and limits
Research-backed written brief was saved before modeling. Navy fractured-mineral body, blue seam, brass family fittings and seven low polygonal ice plates. All geometry/maps are procedurally authored, not scans or handmade traditional craft. This is an abstract Baikal winter-inspired collectible, not a geographic replica or a representation of all Russia.
Actual source poster and mobile browser images were visually inspected. Complete silhouette fits; blue-and-brass identity is readable. Ice is deliberately opaque/faceted, cracks graphic, some side mapping stretches, and fine details are small on mobile. Poster has visible sampling grain (24 samples, denoising disabled). Seven plates exist; overlap in projection hides some from the front. No photorealism, optical ice simulation, reference equivalence or human approval claimed.

## Verified
- Saved source reopened: 23 moving and 39 static meshes, **81 poses**, zero unintended surface intersections. Includes all seven lid slabs and latch-versus-lid checks. Only named original mating bearings exempt. Ten hinge attachment pairs checked, hollow floor ray z=0.2650000155. Sampled surface tests, not continuous collision or manufacturing certification.
- Original mechanism pivot world matrices match exactly. 80-degree latch release precedes 105-degree lid swing. Detached-slab negative control correctly fails ownership assertion.
- Source/export nearest-vertex maximum error **1.712013073529306e-7**, within 1e-5. Three packed generated maps.
- Actual GLTFLoader: **13,992 triangles, 62 meshes, 5 materials**, zero nonfinite/degenerate geometry. Decoded color ranges 115 and 49; actual green-channel roughness range 41.
- Offline file:// Edge desktop 1440x1080 and touch-emulated mobile 390x844: native controls, drag/touch rotation, close, interrupted reset, reduced motion, no overflow/errors/external requests. Full-open projection maximum 0.892365. Corrupt embedded GLB hits real parser and displays poster; no-JS poster works. RTX 4060 desktop GPU, not physical-phone performance.
- Source poster decoded/nonblack. Exact inventory and ZIP readback in delivery-check.json. Folder-local attributes preserve bytes in Git.

## Rebuild
From repository root: `npm install --prefix preview/russia-v1 --no-audit --no-fund`, `python preview/russia-v1/maps.py`; run Blender 5.2.1 with `--background --factory-startup --python-exit-code 1 --python preview/russia-v1/author.py`; then `python preview/russia-v1/verify_all.py`. Python needs Pillow and Playwright; installed Edge required. Node dependencies are build-only, never runtime downloads. Generator overwrites source/export/poster; preserve manual work separately.

Mechanism, viewer and base validation adapted from Japan pilot on repository baseline ff5d78f; original shared kit unchanged. `mechanism.blend` is included. Three MIT license included. Source archive excludes installed dependencies/backups and packaging envelopes.

## Failures and controls
Optional Codex lane failed authentication before edits; no Codex changes accepted and no credentials changed. Direct Hermes implementation completed instead. First build failed because inherited node_modules lacked esbuild; installed folder-local pinned dependencies and rebuilt successfully, without changing the HTML limit. No art/collision failure occurred. Tests reject detached lid ornament, corrupt GLB, invalid asset bounds/missing lid and incorrect motion endpoints. These are actual negative controls, not a fabricated red-to-green art history.
