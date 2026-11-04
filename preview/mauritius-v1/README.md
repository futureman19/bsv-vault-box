# Mauritius v1 — Chamarel Chromatic Earth

Open `mauritius-v1.html` directly in Edge/Chrome: the model, runtime, maps and actual Blender-rendered poster are embedded. Drag/touch rotation, Open/Close and Reset work offline. HTML **2,499,960 bytes**; GLB **1,341,616 bytes**. This is cosmetic collectible art, not minted, hosted, signed or a custody transaction.

## Design and provenance
The pre-model `design-brief.md` cites Chamarel Geopark's volcanic-earth account. Seven original mineral-colored rolling ribbons are real lid-parented geometry over warm earth walls, dark basalt feet and inherited brass mechanism. Maps are procedural, not scans or copied photographs. `mauritius.blend` is the editable source; `mechanism.blend` is the included trimmed family mechanism. `poster.png`/`.jpg` are actual source renders; desktop/mobile PNGs are actual browser captures. Three.js is MIT; license included.

## Verified
- Independently reopened saved source: 23 moving / 39 static meshes, 81 staged poses, zero unintended sampled surface intersections; latch-versus-lid included. Only named mating hinge/barrel and latch/pin contacts excluded. Ten hinge attachment pairs intersect; hollow floor ray Z 0.2650000155.
- Source/export nearest-vertex error in both directions: 1.712013073529306e-7 (<1e-5). Packed source images retained.
- Actual GLTFLoader: 62 meshes, 21,020 triangles, 11 materials, no nonfinite vertices or degenerate triangles.
- Desktop 1440x1080 and touch-emulated mobile 390x844, offline `file://`: drag/touch rotation, native open/close, interrupted reset, reduced motion, no external HTTP requests, runtime errors or horizontal overflow. Full-open silhouette maximum absolute NDC 0.892365 (<1). Actual corrupt embedded GLB triggers poster fallback; no-JS poster also passes.
- Seven distinct palette regions, variable relief heights and lid ancestry; decoded maps vary and are <=512 pixels. Missing-ribbon negative control is rejected. Motion test covers 81 poses, 80-degree latch release before 105-degree lid opening; invalid-geometry controls rejected.
- `inventory.json` records exact SHA-256/bytes. `delivery-check.json` records archive readback. Folder-local Git attributes preserve exact bytes.

## Honest limitations
Stylized landscape, not a survey, geological simulation, photoreal reconstruction or artisan-made object. At default mobile view some pastel ribbons blend/occlude and all seven cannot be confidently counted visually; the seven separate regions are independently checked. Earth walls are smooth/procedural and can read as clay. The dark seam and long family clasp are deliberate family geometry. Rear/interior are invented. Collision tests sample surface intersections, not continuous mechanical certification. Mobile emulation is not physical-phone performance. No per-asset human art approval is claimed (waived for this batch).

## Reproduce
Python with Pillow/numpy/Playwright; Blender 5.2.1; Node with pinned `package.json` dependencies; installed Edge for browser checks. Build uses local node_modules or sibling iceland-pilot/node_modules; dependencies are build-only and excluded from delivery. `npm install` inside this folder restores local tooling if needed.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py` and `verify_parity.py`.
5. `node tests.mjs`; `python verify_browser.py`; `python verify_theme.py`
6. `python package_delivery.py`

Run commands from this directory. Authoring overwrites source/export/poster; keep manual changes separately. `assemble_author.py` is historical one-time bootstrap (requires sibling Japan), not needed for reproduction. The retained initial Codex lane failed authentication and contributed no accepted changes; Hermes authored and verified the asset directly. Recovery reran the build/source/parity/browser/theme gates successfully; no art-gate failure was observed in that recovery. Negative controls are deliberate regression tests, not a fabricated failure-and-fix story.

Only this new preview directory is delivered. No production, vault, mint, keys, chain services or deployment touched. Branch backup only; collection integration is separate.
