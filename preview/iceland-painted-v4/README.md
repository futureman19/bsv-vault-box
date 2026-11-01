# Iceland / Basalt — painted v4 EXPERIMENT

Open **iceland-painted-v4.html** directly in a browser. Everything required for the interactive viewer is embedded; no server or network is needed. This is one bounded material experiment, not final production or promotional artwork.

## Result
- Complete standalone HTML: **2,951,066 bytes**, below the literal 5,000,000-byte cap.
- GLB: **1,645,332 bytes**; unchanged 9,632 triangles, 217 runtime primitives, nine materials.
- Original mesh binary prefix, indices, vertex positions/normals, node transforms/pivots, shiny lid material and glacial vein are preserved. No displacement, accessories, chain operations or deployments.
- Original v3 viewer.js, compiled viewer and motion.mjs are byte-identical: same staged latch/lid behavior, reset, pointer/native touch, reduced-motion and fallback.

## What was painted
Synthesized procedural bitmap brushes, NOT photogrammetry, scans or exact transfer of the AI concept. Thirty-six individually assigned stone tiles occupy a shared 1024-square atlas, with irregular slab values, short mineral fractures/chips, and restrained olive/pale growth confined to lateral column-join masks. A separate shared tile puts subtle brown tarnish and contact-edge wear on brass fittings. Base color and ORM are JPEG; the modest tangent normal is lossless PNG. No screenshot hardware or baked directional lighting was projected onto the model. No additional browser material overrides exist.

`texture-atlas-preview.jpg` shows the atlas and authoring masks. Red marks eligible lateral sheltered bands, green actual growth, blue painted fractures. Shelter is a geometry-relative column-edge heuristic, not an occlusion bake: some side facets can still read as exposed. The compact square tiles have unequal physical texel density on tall columns. Shortened fractures reduce directional stretching but do not make the UVs distortion-free. Hardware uses shared local edge-wear mapping, not individually painted rivet rings.

One visual correction was made after inspecting matched-camera captures: reduce grain and green speckling, consolidate growth, shorten fractures, and strengthen slab-to-slab values. `initial-review/` preserves earlier comparison images. No further polish loop was performed.

## Evidence and limitations
- `comparison-closed.jpg`, `comparison-open.jpg`, `comparison-closeup.jpg`: actual offline Edge screenshots, approved v3 LEFT and painted v4 RIGHT, same camera and lighting. Closeup intentionally crops the full silhouette.
- `poster.png` / `poster.jpg`: actual Blender render of the exported candidate imported into the original studio, not AI artwork.
- `paint-check.json`: original binary geometry/pivot/runtime and input hash preservation, finite atlas UVs, 14,330 growth-mask pixels, zero growth-mask pixels outside authoring shelter, decoded color variation and complete HTML budget.
- `decoded-map-check.json`, `pbr-check.json`: actual browser-decoded 1024-square maps, pixel variation, every textured primitive UV range, preserved glossy lid and bounds.
- `browser-check.json`: offline file desktop and emulated mobile; zero external requests/errors; rotation/native touch, open/close, interrupted reset, reduced motion, no overflow, open silhouette framing and actual corrupt-GLB fallback. Desktop GPU emulation is NOT physical-phone testing.
- `source-check.json`: reopened source, 81 sampled motion positions with no prohibited intersections, hollow-floor ray. Intentional bearing contacts excluded; not a continuous mechanical proof.
- `editable-check.json`: reopened editable source, world triangle-corner preservation within 0.00002 model units (maximum rounded mismatch 0.00001 from floating-point round-trip in two latch barrels), exact UV corner match to GLB at five decimals and exact packed texture bytes. GLB geometry itself is binary unchanged.
- `paint-red.txt`: test-first missing candidate failure. The initial paint also failed the color-variation threshold (16.6845 versus required 18); final value is 20.6028. The initial exact rounded editable check exposed the stated floating-point issue; it was replaced by the explicit bounded tolerance above, not a geometry edit.

Visual review finds a meaningful normal-distance improvement from flat gray facets to weathered stone, with sparse localized growth. Confidence is high that the change is visible; moderate that it specifically reads as basalt rather than generic weathered stone/concrete. This is NOT promo parity or photorealism. The unchanged regular ribs, simple fittings and slab silhouette remain the main realism limit. Pale surfaces, a few notch-like fractures and green trails remain stylized. Brass wear is deliberately subtle at normal distance; the lid remains pristine as requested.

## Editable source and reproduction
`iceland.blend` contains the exact portable candidate imported back into the original studio, with packed glTF materials/UVs and editable evaluated meshes. Original construction modifiers are retained only in the untouched `original/iceland.blend`, not on the evaluated candidate. `original/author.py` and the original GLB are included. Regeneration overwrites this experiment's generated outputs.

Requires Python with Pillow/NumPy, Blender 5.2.1, and Playwright with installed Edge for browser tests:

```
python paint.py
blender --background --factory-startup --python-exit-code 1 --python editable.py
python build.py
python verify_browser.py
python verify_decoded.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
node --test tests.mjs
```

Repository comparison gates (`test_paint.py`, `verify_pbr.py`, `verify_editable.py`) additionally use the preserved sibling `iceland-lightweight-v3` and absolute original-input paths recorded in `preserved-inputs.json`. They are intended to rerun in the original repository; the source archive is independently sufficient to regenerate candidate art/viewer, not to reconstruct every historical baseline screenshot directory. `viewer.bundle.js` is the unchanged prebuilt v3 runtime; original JS and Three license are included.

`package_delivery.py` creates the source ZIP from this directory, excludes caches/backups and the archive itself, verifies safe unique archive paths and every archived file hash, and reads back every delivery copy. Hash inventory proves byte integrity, not third-party authenticity. Prior source/concept/promotional bytes remain untouched. No pushes or production changes.
