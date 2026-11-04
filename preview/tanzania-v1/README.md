# Tanzania v1 — Kilimanjaro & Ochre

Open `tanzania-v1.html` directly in Edge/Chrome. All runtime assets are embedded: **HTML 2,150,649 bytes**, **GLB 1,042,676 bytes**. Rotate by drag/touch, open/close the lid, reset, or use reduced motion. Local cosmetic collectible only: not minted, hosted, chain-admitted or a custody implementation.

## Design and files
Research-backed written `design-brief.md` preceded authoring. UNESCO's Kilimanjaro description informs a broad volcanic miniature, pale snowy rim, olive foothills and ochre earth palette. Terrain is invented and stylized, not a geographical model or current glacier map. No reference photographs, AI promotional images or cultural motifs were copied.

`tanzania.blend` is the named editable Blender source; `tanzania.glb` contains portable mesh/maps. `mechanism.blend` is the inherited trimmed Japan mechanism. `maps/` holds three generated 256px maps. `poster.png`/`poster.jpg` are actual source renders; desktop/mobile captures are actual offline browser output. Scripts, checks and raw outputs accompany a ZIP with readback-verified SHA-256 inventory. Three.js is MIT; license included.

## Verified
- Actual GLTFLoader: 58 meshes, 14,746 triangles, 7 materials; zero nonfinite vertices and zero degenerate triangles.
- Independently reopened source: 17 moving and 39 static meshes; **81 poses**, zero unintended sampled surface intersections. Latch-versus-lid also sampled; only explicit mating bearing contacts excluded. Ten hinge attachment pairs overlap as intended. Hollow floor ray z=0.2650000155.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5. Packed source maps preserved. Inherited lid/latch world pivots compared independently with the reopened baseline.
- Terrain bounds/crater/ancestry tested; actual crater depth 0.2219998837. All three exported terrain material primitives remain descendants of the moving lid. Decoded map ranges 58/58/47; roughness sampled from glTF's green channel.
- Offline file:// desktop 1440×1080 and mobile 390×844 touch emulation: native open/close, drag, reset during motion, reduced-motion endpoints, no overflow, zero external requests and errors. Full-open maximum absolute projected coordinate 0.91565 (inside frame). Corrupt embedded bytes reach the actual parser and trigger poster fallback; no-JS poster separately verified.
- Motion unit tests: 2 passed, 0 failed; include missing-lid/nonfinite/empty-geometry rejection. A deliberate detached-terrain source negative control fails. These are actual rejection tests, not declared booleans.

## Real failure and fix
The initial terrain width was 2.7528221607, above the frozen 2.75 maximum. `initial/terrain-width-failure.txt` retains the assertion failure and the initial source poster is preserved. The generator's X scale was reduced from 1.34 to 1.33 without weakening the bound; final width is 2.7322787046. Source, export, render and all checks were regenerated. `initial/detached-terrain-negative.txt` records a separate intentional ancestry rejection, not an art defect.

The shared pilot dependency folder lacked the actual compiler. The unchanged pinned package dependencies were installed inside this new preview only; no sibling toolchain was populated. The copied template contained a literal truncated mobile CSS fragment; it was replaced with complete responsive rules before the first build. No previously run failed browser test is claimed for that source repair.

## Honest visual limits
Actual source and browser screenshots were inspected. The result reads as a stylized snow-capped volcanic box with coherent hardware, a hollow interior and no obvious floating ornament. The smooth radial mountain is simplified and the secondary shoulder understated, not a faithful three-peak map. The real recessed crater is more visible in the elevated source poster than at normal mobile scale, where the white summit can read as a cap. Ochre mottling can read as wood/marble rather than unmistakable volcanic stone. The dark seam is intentionally conspicuous; gold hardware is simplified and the family clasp is long. The open front view hides the exterior terrain behind the lid as expected. Source render retains low-sample noise (denoising disabled).

Technical acceptance is not photoreal equivalence, physical fabrication certification, continuous collision proof, physical-phone performance or human art approval. User waived per-asset review for collection completion. No deployment or blockchain actions occurred.

## Reproduction
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js and pinned package dependencies are build/test tools only. `npm ci --ignore-scripts --no-audit --no-fund` in this directory restores build dependencies. Then:

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender likewise for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `python build.py`; `node --test --test-reporter=tap tests.mjs`
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites generated source/export/poster and changes byte identities. Archive excludes node_modules, caches and Blender backups. Folder-local Git attributes preserve exact delivered bytes. The mechanism source is included, so authoring does not require another preview; build can use local dependencies. No source rebuild promises byte-identical Cycles renders.

Next: integrate this backed-up branch through the separate final collection card; do not merge or publish from this asset card.
