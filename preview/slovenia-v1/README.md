# Slovenia v1 — Soča & Alpine Limestone

Open **slovenia-v1.html** directly in Edge/Chrome. All runtime assets are embedded; no server, network or wallet required. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion preference snaps poses. This is a cosmetic inner collectible, not an outer custody container.

## Delivery
- Standalone HTML: **2,489,728 bytes** (strictly under 5,000,000).
- Standalone GLB: **1,298,260 bytes**.
- `slovenia.blend`: editable, packed Blender source; `mechanism.blend` is the trimmed inherited articulation source.
- `maps/`: independently generated limestone color/roughness and green bank map; no photographs or scans.
- `poster.png` / `poster.jpg`: actual saved-source model render, not an AI illustration. Browser PNGs show actual offline runtime.
- `inventory.json`, `delivery-check.json` and source ZIP: exact SHA-256/byte inventory and archive readback evidence.

## Verified
Actual GLTFLoader: 16,652 triangles, 76 meshes, five materials; zero nonfinite vertices or degenerate triangles. Decoded texture variation includes glTF roughness green channel. Saved Blender source reopened independently; source/export nearest-vertex error in both directions 1.712013073529306e-7 units, below 1e-5. Three packed maps retained.

81 staged motion samples check all 37 moving and 39 static meshes, plus latch against lid. No unintended surface intersections; only explicitly named mating bearing surfaces exempt. Ten hinge attachment pairs checked. Hollow interior floor ray at z=0.265. Original lid/latch world pivots compared against included mechanism source. Landscape meshes all belong to lid; a deliberately detached ornament is rejected by the ancestry gate. Continuous river mesh connectivity and 47 exposed vertical channel rays verified. This is sampled surface clearance, not continuous mathematical or engineering certification.

Offline file:// desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, drag/touch rotation, interrupted reset, reduced motion, unclipped open pose, no horizontal overflow, no external HTTP(S) requests, no runtime errors. Genuine corrupt GLB reaches the loader error path and shows poster/disabled controls; no-JS poster also tested. GPU is desktop RTX 4060; no physical-phone FPS or performance claim.

## Visual outcome and limits
A brief-driven, stylized pale-stone box with warm brass, dark jade reveal and sinuous green inlay beneath low jagged alpine banks. It is not an exact model of the Soča valley, traditional Slovenian craft, or photoreal limestone. The surface can read as lightly marbled polished stone. Banks are angular/pleated, vegetation accents are repetitive small cushions, and water is an opaque polished mineral inlay rather than simulated transparent water. Source poster is intentionally low-sample and has visible grain. Front open view hides much of the lid landscape; `desktop-open-rear.png` shows its continued attachment.

One bounded presentation correction raised the viewer camera to expose more of the river at mobile size; initial low-angle screenshot is retained. Initial missing esbuild failure is preserved in `initial/missing-build-dependencies.txt`: the main checkout node_modules directory was empty, so scoped dependencies were installed in this new folder. No geometry failures were suppressed. Human per-asset review was expressly waived for this batch; technical PASS is not a claim of human visual approval.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright and installed Edge; Node with pinned package lock. `npm ci --prefix preview/slovenia-v1 --no-audit --no-fund` restores local build dependencies. No node_modules or backup files in source ZIP.

From repository root:
1. `python preview/slovenia-v1/maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python preview/slovenia-v1/author.py`
3. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node --test preview/slovenia-v1/tests.mjs`
5. `python preview/slovenia-v1/build.py`
6. Run Python on `verify_browser.py`, `verify_extended.py`, `package_delivery.py` in this folder.

The author is self-contained with included mechanism and maps. `setup_author.py` records one-time scaffolding lineage and requires sibling Japan source; it is NOT needed for rebuild. Regeneration overwrites source/render/export. Recompute inventory after regeneration. Three.js runtime MIT license included. Research URLs in design brief inform material/landscape only; no third-party imagery embedded.

## Scope
Only new `preview/slovenia-v1/` content; no shared kit, existing preview, production site, vault, mint, keys, nodes, chain queries, VPS, funds or broadcasts. Branch backup only, no merge or hosting. Collection direction: 201 equally one-of-one boxes; no issuance or storage availability guarantee. Final integration belongs to its separate dependent card.
