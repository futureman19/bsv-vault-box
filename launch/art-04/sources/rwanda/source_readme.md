# Rwanda v1 — Imigongo / Ochre Relief

Open **rwanda-v1.html** directly in a desktop browser. All model, runtime, maps and actual-source poster bytes are embedded. No server or connection is needed. Drag/touch rotates; Open/Close lid and Reset view work, including reduced motion. Cosmetic movement only; no custody state changes.

## Delivery
- HTML: **1,832,459 bytes**, strictly below 5,000,000.
- GLB: **811,176 bytes**; 11,060 triangles, 88 meshes, 6 materials through the actual Three GLTFLoader.
- `rwanda.blend`: editable packed Blender source; `mechanism.blend`: reusable trimmed family mechanism.
- `author.py`, `maps.py`, maps/, viewer/build/verification scripts, actual source `poster.png`/`poster.jpg`, desktop/mobile closed/open screenshots and fallbacks.
- `inventory.json`: exact SHA-256 and byte counts. `rwanda-v1-source.zip`: explicit required artifacts plus scripts/evidence, independently read back by `package_delivery.py`. Inventory and package/check envelopes exclude themselves to avoid recursive hashing.

## Design and provenance
The research-backed written `design-brief.md` preceded the model. New relief is independently composed from nested diamonds, inspired by Rwanda's imigongo raised geometric craft and earth/kaolin/charcoal palette. Research pages are references, not copied pixels. No claim of authentic artisan production, cultural completeness, traditional symbolism, hand sculpture, scans or photorealism. Nine lid relief rings and 28 front/left-side relief rings are real closed meshes. Rear/right surfaces are deliberately simpler earth panels; the unseen construction is extrapolated.

The shell uses terracotta-colored generated pigment maps and a dark wood interior, four wooden feet and restrained brass hardware. Source/browser lighting lifts the intended earth red toward coral. The narrow dark seam is visually conspicuous and can read slightly ajar even in the closed pose; it is a stylized reveal, not a watertight seal or manufacturing proof. Fine horizontal procedural surface grain can read as wood rather than plaster. These are retained v1 visual limits, not claims of reference equivalence. Source poster and mobile open screenshot were visually inspected: complete framing, readable primary controls, hollow interior; fine details show mild aliasing.

## Verified, with limits
- Independent saved-source reopen: hollow floor ray z=0.2650000155, ten hinge attachment pairs, retained pivot at (0,1.32,1.668), lid dimensions 3.72 × 2.38 × 0.30.
- 81 sampled staged opening poses: **25 moving / 63 static meshes, zero unintended surface intersections**, including every ornament. Latch rotates 80 degrees before lid rotates 105 degrees. Only existing named mating bearing contacts exempt. This is sampled BVH surface evidence, not continuous collision/manufacturing certification or a general solid-volume containment test.
- Source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5; three packed procedural maps retained. Loader reports zero degenerate triangles/nonfinite vertices.
- Desktop 1440×1080 and touch-emulated 390×844 Edge under offline file://: rotation, native open/close controls, interrupted reset, reduced motion, no overflow, zero external HTTP requests/errors. Full-open maximum projected coordinate ~0.8924, within viewport. Actual corrupt embedded GLB reaches parser and shows disabled-control poster fallback. No-JS poster independently tested.
- Theme/contract assertions verify named relief count, actual lid ancestry, map variation/size, palette material presence, ornament height and dimensions. A real runtime negative control removes a lid ornament; the identical theme assertion rejects it. Negative control is post-implementation regression evidence, not TDD.
- Initial visual review found inherited Japan/Yakushima page copy. Corrected copy and added an assertion before final rebuild/browser recapture. No geometry/collision gate failed; none was relaxed.
- Mobile emulation ran on the desktop RTX 4060, not a physical phone. No FPS or device performance claims.

## Reproduce
Build/test dependencies: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with Three 0.180.0/esbuild 0.25.11 (see package.json). Build resolves local node_modules, otherwise sibling iceland-pilot/node_modules. Standalone extraction needs dependency installation; delivered HTML needs none. No dependency folders are archived. Three MIT license is included.

From this folder:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_contract.py`.
5. `python verify_browser.py`; `python verify_theme.py`
6. `python package_delivery.py`

Authoring overwrites generated source/export/poster; preserve manual edits separately. Checks and inventory must be regenerated after changes. Mechanism/viewer/check lineage is Japan cedar v1 and Iceland, from local base ff5d78f1e0d486af5c882c184fc08049996ebdc8; original pilots and shared vault kit unchanged. Optional Codex implementation attempt failed authentication before edits; Hermes authored and verified directly. No credential files were accessed or changed.

Local art only: not minted, hosted, chain-admitted, signed, sold or deployed. The collection remains 201 equally one-of-one designs. Branch backup only; integration is separate. Per-asset human review waived for this batch.
