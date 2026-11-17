# Liberia v1 — Sapo Rainforest & River

Open `liberia-v1.html` directly in Edge/Chrome. Entire runtime, real GLB, maps and source-rendered poster are embedded: **3,905,725 bytes HTML**, **2,377,424 bytes GLB**. Drag/touch rotate, zoom, Open/Close, Reset; reduced motion supported. Cosmetic collectible only, no custody operation. Not minted, hosted or deployed.

## Design and visual limits
Research-backed landscape inspiration in `design-brief.md`, written before modeling. Dark warm timber, green inset/seam, winding teal river, three broadleaf miniatures and satin brass. Source-authored Blender geometry and procedural maps, not scans, hand sculpture or protected timber. This is deliberately stylized: sparse flattened crowns and a shallow ribbon stream suggest a miniature landscape rather than dense rainforest. Liberia/Sapo specificity depends on the accompanying title; no botanical/geographic reconstruction or photoreal equivalence is claimed. Hardware/interior extrapolate the collection family. Closed desktop and open mobile screenshots were visually inspected; no clipping/major layout defect observed. Full-open front view hides lid-top scenery naturally.

## Verified
- Independent saved-source reopening: hollow floor z=0.2650000155; 10 attachment intersections; 81 motion samples, all 75 moving vs 99 static meshes plus latch-vs-lid. Zero unintended surface intersections; narrow original mating bearing exclusions only. Sampling is not continuous engineering certification.
- Same original pivot mechanics: latch releases 80 degrees before lid opens 105 degrees. Two motion/asset-contract unit tests pass, including rejected missing/empty/nonfinite assets.
- Independent GLB import/source vertex parity max error 1.712013073529306e-7 (<1e-5). Four packed maps.
- Real browser GLTFLoader: 29,834 triangles, 174 meshes, 12 materials; zero nonfinite/degenerate triangles. Delivery checker independently decodes all embedded maps and requires variation.
- File:// offline Edge, 1440x1080 desktop and 390x844 touch-emulated mobile: native open/close, drag, interrupted reset, reduced motion, no overflow, no HTTP requests/errors. Open silhouette max absolute NDC 0.892365. Actual corrupt GLB parser rejection displays poster; separate no-JS fallback check. RTX 4060 D3D11; not physical-phone/FPS testing.
- Theme checks require 3 trunks, 15 crown clusters, 47 lid ornaments, continuous 132-vertex river, size/height and parentage.
- Exact file sizes and SHA-256 readback inventory: `inventory.json`; `delivery-check.json` excludes itself/inventory from recursive hashing.

## Real failures and corrections
Optional Codex lane failed HTTP 401 token refresh before implementation; no lane patch accepted, no credentials accessed. Hermes authored directly. First motion invocation failed because Japan had no tests.mjs; copied the original Iceland tests and both passed. First default-backend browser run failed its zero-errors assertion (original error detail was not captured); next run timed out. Added diagnostic failure recording and explicitly selected D3D11 hardware rendering; full rerun passed without relaxing assertions. No geometry collision or parity failures occurred. These are harness/runtime corrections, not a claimed visual red-to-green result.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/Playwright; installed Edge; Node with Three/esbuild from `package.json`. Build falls back to sibling `iceland-pilot/node_modules` (worktree symlink); standalone source build requires installing dependencies locally. No runtime network dependencies.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`; `node --test tests.mjs`
4. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python verify_browser.py`; `python verify_delivery.py`.

Regeneration overwrites authored outputs; preserve manual variants separately. `setup.py` records initial adaptation from Japan and requires that sibling; it is NOT needed to rebuild this self-contained author source. Source mechanism/viewer/test lineage: local base ff5d78f1e0d486af5c882c184fc08049996ebdc8, Japan/Iceland pilots. Three runtime license included. No third-party photographs embedded. No other previews, shared kit, production code, chain or VPS modified. Branch backup only; integration remains separate.
