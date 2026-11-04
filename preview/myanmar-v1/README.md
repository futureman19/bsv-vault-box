# Myanmar v1 — Bagan Lacquer

Open **myanmar-v1.html** directly in Edge/Chrome. The complete model, runtime, maps and actual Blender-render poster are embedded. Drag/touch to rotate; Open/Close lid and Reset view. Cosmetic motion only, not a custody or blockchain operation.

- HTML: **3,040,969 bytes**, below the strict 5,000,000-byte cap.
- GLB: **1,672,672 bytes**; 18,312 triangles, 59 runtime meshes, four materials.
- Editable packed source: `myanmar.blend`; inherited trimmed mechanics in `mechanism.blend`.
- `maps/`: three generated 512x512 maps. No scans or research photographs embedded.
- `poster.png`/`.jpg`: real source render. Desktop/mobile screenshots: actual offline Edge rendering, not promotional imagery.
- `myanmar-v1-source.zip` plus `inventory.json` and `delivery-check.json`: exact-byte inventory and ZIP readback verification.

## Design and visual limits
The sourced pre-authoring brief interprets Bagan lacquer craft as a dark polished vault with vermilion diamond linework, red interior and a shallow oval ornament. The pattern is invented, not an authentic named traditional design. Incisions are evoked by mapped colour rather than actual carved grooves. No bamboo substrate, sacred icons, temple model or geographic terrain is claimed. Gold/brass fittings are the collection's mechanical language, not historical lacquerware reproduction.

Actual-source and browser visual inspection found a complete coherent box with readable black/red geometric decoration and seated fittings. The source poster has strong pale lid reflections and visible render grain (24 samples, no denoising); the browser reads warmer. The oval's fine detail is small on mobile. Pattern joins are regular/procedural and visually busy at edges. Not photorealistic, handmade, museum-equivalent or human art-approved. Per-asset human review was explicitly waived for this batch.

## Verified boundaries
- Independently reopened source: 81 sampled poses, **20 moving / 39 static meshes**, zero unintended intersections. Every new ornament is a moving lid child. Only named inherited mating-bearing contacts excluded. Hollow floor ray hits at z=0.2650000155; ten hinge attachment pairs intersect as intended. Sampling is not continuous collision proof or manufacturing certification.
- Exact pivot matrices compared independently against included original mechanism. Latch releases 80 degrees before the lid rotates 105 degrees; reverse choreography and invalid geometry rejection exercised by two Node tests.
- Independent Blender GLB import/source comparison: maximum nearest-vertex discrepancy **1.712013073529306e-7**, below 1e-5. Three packed source maps retained. Not a byte-identical re-export claim.
- Theme: four lid ornaments, four continuous skin panels, bounded ornament heights, source slab dimensions and mapped roughness. Deliberately detaching one ornament caused **EXPECTED FAIL: Detached lid ornament**; restoring it passed. This is a post-implementation negative control, not a claim of test-first failure. No actual asset failure-and-fix occurred in this run.
- Real GLTFLoader: no degenerate triangles/nonfinite vertices. Decoded colour ranges 3 and 155; roughness GREEN-channel range 25. All maps 512x512.
- Offline `file://` Edge desktop 1440x1080 and mobile 390x844 touch emulation: rotation, native open/close, interrupted reset, reduced motion, no horizontal overflow, no HTTP(S) requests or errors. Full-open max absolute projected coordinate <0.893. Actual corrupt GLB parser failure displays poster; no-JS poster also checked. Mobile emulation uses the desktop RTX 4060, not a physical-phone performance claim.

## Reproduce
Build dependencies are pinned in package.json/lock: Three 0.180.0, esbuild 0.25.11. The prescribed shared pilot node_modules existed without its compiler; used a preview-local pinned install rather than modifying another preview. Runtime remains fully offline.

Python requires Pillow/numpy/playwright; browser checks require installed Edge. Blender used 5.2.1 LTS. From this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`; `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`; `node --test --test-reporter=tap tests.mjs`
4. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`, `verify_pivots.py`.
5. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

Regeneration overwrites generated source/art/evidence; preserve manual edits separately. `assemble_author.py` and `author-parts.json` retain how the self-contained author script was assembled from the Japanese pilot's mechanics/helpers; directly running author.py is sufficient. Folder-local Git attributes preserve exact bytes. Source archive excludes node_modules, caches and .blend1 backups. Three MIT license included.

Local asset and authorized branch backup only. No deployment, chain query, wallet, keys, mint, sale, VPS or public-site modification. The 201-piece collection integration is a separate dependent card.
