# United States flag v3 — single continuous canton

Review candidate, not minted or deployed. Scope: flag placement only; v2 and approved marketing remain unchanged.

## Correction
V2 projected a complete flag independently onto each body face and allowed repeating texture sampling at lid edges. V3 allocates a single perimeter strip, starting at the rear-right seam: rear -> left -> front -> right. Exactly one navy interval (2.01–7.91 of 12.4 perimeter units) wraps the physical left end, reaching x=-0.15 on front and rear. It occupies only the upper 3/7 of the body. The remaining body is horizontal red/ivory stripes. The full-depth left lid field aligns at x=-0.15; this is the existing separately moving lid, not a duplicated body canton. All texture samplers clamp to edge. Rear treatment is an extrapolation of the visible approved reference.

One initial pass plus one local clamp-to-edge correction removed the lid-edge opposite-side color bleed. `prior/first-pass.png` is retained. No geometry, dimensions, pivots, hardware, motion, viewer controls or fireworks redesign.

## Evidence
- `canton-check.json`: independently reopened source, barycentric actual-UV sampling at 496 perimeter positions x 40 heights, zero missing samples. V2 negative control: 5 disconnected navy runs; v3: 1. No lower navy samples in v3. White stars are holes within one navy footprint, not separate cantons.
- `export-identity-check.json`: all GLB nodes exact v2; 165 non-UV accessor buffer views byte-identical. 50 UV views changed. Exported basecolor pixels exactly match authored maps.
- All 57 collectible object raw geometries, polygons, world transforms and parents exactly match v2. Mechanism source, motion module, viewer source/bundle, fireworks source and motion tests remain byte-identical.
- `source-check.json`: 81 sampled opening/latch poses, no nonbearing collisions, hollow-floor ray. Original narrowly named bearing exemptions unchanged. `hinge-attachment-check.json` verifies mounting intersections.
- `parity-check.json`: independently reopened .blend and GLB geometry within 1e-5; three packed maps.
- `browser-check.json`: offline file desktop and emulated touch/mobile, rotation, open/close, interrupted reset, reduced motion, framing, no external requests/errors/overflow, real corrupt-GLB poster fallback.
- `extended-check.json`: decoded maps, separately owned 216-particle fireworks, animation versus reduced-motion frozen arrays, full burst phase bounds at both endpoint poses and desktop/mobile, no-JS poster.
- Four `view-*.png` actual loaded-model views, plus desktop/mobile closed/open, source poster and approved-marketing/v2/v3 comparison.

The first UV test incorrectly raycast only the nominal side wall at butt-joint ends, missing front/rear walls that actually close those corners. `canton-failure-corner-oracle.txt` preserves that genuine test failure. The corrected oracle raycasts all four walls, uses nearest actual hit, retains the same one-connected-run gate and has zero missed points. No artwork or threshold was changed to pass it.

## Visual outcome and limits
The separated/repeating body canton defect is visibly corrected: one upper-left navy field wraps the corner and aligns with the closed lid. Opening naturally separates the lid's moving field from the body. This is not an exact marketing match: stars remain smaller/denser, the body canton deeper, finish more angular/brighter, and lightweight viewer fireworks much simpler than illustrated smoke/bloom. Existing geometry/hardware was intentionally preserved. Mobile is desktop-browser touch emulation, not physical-device performance. Sampled collision checks are not continuous proof. User visual approval remains pending.

## Files and reproducibility
Open `united-states-flag-v3.html` directly offline. GLB is `united-states.glb`; editable packed source is `united-states.blend`; actual-model poster is `poster.png` / `poster.jpg`. Full HTML must stay strictly below 5,000,000 bytes.

Run `python maps.py`, Blender 5.2.1 background `author.py`, `python build.py`. Build reuses the frozen shipped viewer bundle. Run Blender `verify_source.py`, `verify_mechanism.py`, `verify_parity.py`, `verify_canton.py`; Python `verify_export_identity.py`, `verify_browser.py`, `verify_extended.py`, `capture_views.py`; Node `--test --test-reporter=tap tests.mjs`. Python tests require Pillow, NumPy, Playwright with Edge. Reference/identity checks additionally require sibling committed `preview/united-states-flag-v2` and capture comparison's explicit approved marketing path. Those historical assets are not duplicated into the source archive; the author/build itself is self-contained apart from installed tools.

`inventory.json` records SHA-256/bytes for archive payload files. Source ZIP excludes node_modules, backups, pycache, its own archive, and post-package verification envelopes. `delivery-check.json` verifies archive bytes, required artifacts, copied output and delivered offline HTML. Folder-local Git attributes preserve exact bytes. Art branch only; no site/docs/master changes.
