# United Arab Emirates v1 — Desert Loom

Open `united-arab-emirates-v1.html` directly in Edge/Chrome. Embedded model, runtime and actual-source poster; drag/touch rotate, Open/Close, Reset and reduced-motion support. Art only, not minted or hosted.

## Delivered
- HTML **3,000,132 bytes**, GLB **1,663,960 bytes**.
- `uae.blend`: editable script-authored source; `uae.glb`: portable geometry/maps.
- `mechanism.blend`: included inherited trimmed mechanism from Japan pilot; unchanged original pivots.
- `maps/`: independently generated textile-inspired color/roughness and stone maps. No third-party imagery.
- Poster is an actual Cycles source render, not AI illustration. Browser screenshots are actual offline captures.
- Source ZIP and `inventory.json` bind exact payload bytes; `delivery-check.json` records archive readback.

## Verified
Saved-source reopening: 59 moving and 39 static meshes, 81 sampled poses, zero unintended surface intersections. Checks cover every moving ornament, moving/static and releasing latch/lid. Only explicit mating bearings are exempt. Ten hinge attachment pairs intersect as intended. Hollow floor ray z=0.2650000155. This is sampled surface clearance, not continuous engineering certification.

Source/export bidirectional nearest-vertex error 1.712013073529306e-7 (<1e-5). Seven invented diamonds consist of 28 raised segments, all lid-parented and bounds-checked; original pivot matrices verified independently. Actual GLTFLoader validates nonfinite/degenerate vertices; portable textile base-color range 213 and roughness GREEN-channel range 35. Motion unit tests cover staged endpoints and invalid-asset rejection.

Offline file:// Edge desktop 1440x1080 and 390x844 touch-emulated mobile: native open/close, rotation, interrupted reset, reduced motion, full-open framing, no overflow, no external HTTP requests or runtime errors. Corrupt real GLB input reaches the parser and shows the actual poster; no-JS poster also tested. Mobile emulation is not physical-phone performance.

A real accessibility regression was caught: inherited canvas label still said Cedar and Moss. `initial-accessibility-failure.txt` preserves the failure; corrected to Desert Loom, rebuilt and reran both browser suites without relaxing the assertion.

## Visual limits
Deep red/ivory/charcoal woven-inspired bands and raised diamonds are visible, with restrained brass. This is a stylized rigid textile homage, not an artisan-made Al Sadu object, historical reconstruction, textile simulation or photoreal reference match. At mobile scale individual diamonds are too small/foreshortened for reliable visual counting; geometry count is independently verified. The ornament faces away when fully open. Rough stone feet and inherited elongated clasp are collection interpretations. No single motif represents all UAE culture. UNESCO source is factual inspiration only; no source media copied.

## Reproduce
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, Node and pinned package dependencies. Shared pilot dependency folder was empty at preflight; dependencies were installed only in this new preview, not in sibling/shared folders. Dependencies are build-time only and excluded from delivery.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Same Blender command on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.

Regeneration overwrites output; source hashes then require rebuilding inventory. Three.js MIT license included. No production-site edits, blockchain nodes/keys/queries, minting, broadcasts, external messaging or deployment. Branch backup only; integration is separate.
