# Czechia v1 — Bohemian Cut Glass

Open `czechia-v1.html` directly in Edge/Chrome. Complete offline 3D viewer: **2,092,763 bytes**; GLB **1,002,740 bytes**. Drag/touch rotate, open/close, reset and reduced-motion support. No server or network runtime dependency.

## Design and honest visual verdict
A research-backed, invented cut-glass-inspired cobalt box with a central faceted rosette and eight satellites. See the pre-model `design-brief.md` for sources and dimensions. Procedurally authored Blender geometry/maps, not hand-cut Czech glass, scans, a historic-pattern replica or photographic reconstruction. Materials intentionally use opaque polished enamel and pale faceted ornaments: they read somewhat like frosted stones rather than transparent crystal. This is a stylized craft tribute, not optical glass simulation or user-approved photorealism. Actual mobile-closed and desktop-open screenshots were visually inspected: silhouette intact; details small on mobile; outer lid ornaments naturally hidden from the front when open. No AI poster substitution.

## Executed acceptance
- Source independently reopened: 25 moving / 39 static meshes, 81 sampled poses, zero unintended surface intersections. Named inherited hinge/latch bearings alone exempted. Hollow floor ray z=0.26500001549720764; ten hinge attachment pairs intersect as designed. Sampled surface checks, not continuous mechanical/manufacturing certification.
- Source/export nearest-vertex error in both directions **1.712013073529306e-7**, below 1e-5; three packed authored maps.
- Actual GLTFLoader: **14,500 triangles**, no degenerate/nonfinite geometry. Nine ornaments parented to moving lid; 72 polygon facets each in source, bounded placement. Decoded color/roughness map variation checked (roughness green channel).
- Real offline file:// Edge: desktop 1440×1080 and touch-emulated mobile 390×844, native controls, rotation, open/close, reset mid-motion, reduced motion, full-open viewport fit, no HTTP(S) requests/errors/overflow. Actual corrupt GLB parser input exercises fallback. No-JS poster verified separately. Mobile emulation is not physical-phone performance testing.
- Motion unit tests: 2 pass / 0 fail. Deliberately detached ornament negative control rejected and restored in-memory: post-implementation regression evidence, not test-first TDD. Corrupt GLB and invalid-geometry unit controls also exercise failure paths.
- `delivery-check.json` and `inventory.json`: exact byte/hash inventory and ZIP readback. ZIP excludes dependencies, backups and itself.

No art gate failed in this run. Initial setup copy attempted to read nonexistent Japan `tests.mjs`; corrected to the actual Iceland test file before executing checks. Shared dependency path lacked the actual compiler, so unchanged pinned packages were installed within this new folder only. No sibling preview was repaired or modified.

## Files and reproducibility
`czechia.blend` editable packed source; `czechia.glb` export; `mechanism.blend` inherited trimmed mechanism from Japan v1; `maps/`; actual `poster.png`/JPEG; browser captures; scripts; raw `*-output.txt`; machine-readable checks. Three.js 0.180.0 MIT license included; esbuild 0.25.11 build-only.

From this folder: `npm ci --ignore-scripts --no-audit --no-fund`; `python maps.py`; run Blender 5.2.1 `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`. Run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`. Python requires numpy/Pillow/Playwright and installed Edge. `setup_author.py` documents the original adaptation from sibling Japan source; not needed to rebuild delivered `author.py`. Regeneration overwrites source/export; save manual edits separately and refresh evidence/inventory afterward.

Local art asset only. Cosmetic opening is not a seal or transaction. No blockchain node, keys, minting, transfers, VPS, website deployment or merge. Branch backup only; final collection integration is separate. Off-chain storage remains a proposal, with no availability promise. Launch collection: 201 equally one-of-one designs.
