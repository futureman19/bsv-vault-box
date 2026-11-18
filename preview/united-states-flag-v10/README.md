# USA V10 — seam-star repair candidate, not final approval

Open `united-states-flag-v10.html` offline. This is cosmetic inner-collectible art, not custody, a mint or a sale.

## Actual change

Retained the 0.30-unit thick lid, hinge/latch pivots, red feet, #B50018 red / #021F41 navy pigments, gold hardware, original-size top stars and immediate viewer-only fireworks. Four left and five front edge stars now use one registered stencil across the moving lid skirt and the **fixed navy body rim**. The seam stars were relocated vertically; they do **not** also extend onto the distant horizontal lid top. No bridge mesh ties the lid shut. Existing top stars remain independent original-size glyphs.

First UV-only attempt looked fragmented across stepped trim (preserved under `pass-0/`). One bounded profile correction aligns the side/front rim with the lid skirt and reduces bevel width to .008 while retaining lid thickness. Current desktop image reads as four/five matched stars; the .006 closure gap and highlights still interrupt the shapes. Fixed rim continuation is proven, not continuation down the main striped body wall. This is a concrete repair proposal, not permission to reinterpret an owner preference as approved.

## Fresh evidence

- `seam-check.json`: rays through actual exported triangle UVs find all nine equal-scale stars on both moving lid and fixed rim; 0.30 lid measured.
- `palette-check.json`: decoded GLB maps equal authored pixels; exact requested solid pigment bytes, identity texture factors, four red feet, unchanged gold.
- `source-check.json`: independently reopened source, 81 sampled poses with no unapproved collisions; hollow floor ray. `hinge-attachment-check.json`: ten named contact intersections. Sampling is not continuous physical simulation.
- `parity-check.json`: fresh saved-source/export vertex comparison with 1e-5 tolerance.
- `browser-check.json`, `extended-check.json`: actual offline Edge desktop/mobile emulation, native touch and mouse, rotation, open/close, interrupted reset, reduced motion, corrupt GLB and no-JS fallback; zero page errors/external requests, no overflow and full-open framing. Not physical-phone evidence.
- `fireworks-pixels-check.json`: 52 rendered phase checks including time zero against effects-hidden controls. Fireworks are presentation only, not GLB contents. Browser hero is the embedded fallback; the Blender source-only render is separate.
- `reference-comparison.jpg`: newly captured V9/V10 at the same camera, lighting and frozen effects. `historical-v9/` is clearly historical, not current evidence. `pass-0/` is the retained first attempt.

## Reproduce

Pinned local dependencies: `npm ci`. Run `python maps.py`, then Blender 5.2.1 `--background --factory-startup --python-exit-code 1 --python author_v9.py` (retained filename, now V10 author). Run `python build.py`; validate with `verify_source.py`, `verify_parity.py`, `verify_seam.py` in Blender and `verify_palette.py`, `verify_browser.py`, `verify_extended.py` in Python. `capture_fireworks.py` creates the actual-browser poster, then rebuild and rerun browser acceptance. `node --test --test-reporter=tap tests.mjs` tests choreography. Build uses the documented local Node path; adapt it elsewhere.

Source archives and full exact-byte delivery counts are in `launch/collection-repairs/`. Earlier art stays untouched. Technical passes do not prove photorealism, reference equivalence, rights or final user approval. Keep all collection/release/owner gates.
