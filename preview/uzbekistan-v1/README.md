# Uzbekistan v1 / Rishtan Blue

Open **uzbekistan-v1.html** directly in Edge/Chrome. All model, texture, runtime and actual-source poster bytes are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion is honored. Local art only, not minted, hosted, signed, or custody verified.

## Delivery
- HTML: **2,523,153 bytes**, strictly below 5,000,000.
- GLB: **1,284,020 bytes**; 15,888 triangles, 67 meshes, 6 materials.
- `uzbekistan.blend`: editable packed Blender source; `mechanism.blend`: included inherited articulation baseline.
- `maps/`, `maps.py`, `author.py`: generated maps and reproducible geometry. `poster.png/jpg` are rendered from the actual source, not AI substitutes.
- Desktop/mobile closed/open images and fallback captures are actual offline Edge screenshots.
- `inventory.json` identifies exact payload bytes/SHA-256. The generated source ZIP is read back by `package_delivery.py`; it is a deliverable, not checked into Git.

## Verified
Saved source reopened independently: 28 moving and 39 static meshes tested across **81 poses**, no unintended surface intersections. Latch-vs-lid included; only explicit concentric bearing contacts exempt. Ten hinge attachment pairs verified. Interior floor ray z=0.2650000155. This is sampled surface evidence, not continuous mechanical certification.

Source/export bidirectional maximum world vertex error **1.712013073529306e-7**, below 1e-5. Original lid/latch pivots independently compared to the included mechanism. Eight raised petals and the entire medallion belong to the lid; ornament maximum z=2.09800005 and radius=.72000005. Four ceramic skin volumes have no overlapping corner volumes.

Actual GLTFLoader: zero degenerate triangles or nonfinite vertices. Decoded ceramic color range 213; glTF green-channel roughness range 27; clay range 32. All maps at most 512px. Desktop 1440×1080 and touch-emulated 390×844 Edge over offline file://: native controls, drag/touch rotation, opening/closing, reset during motion, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open maximum absolute NDC=.892365. Actual corrupt GLB parser input triggers poster fallback; no-JS poster tested. RTX 4060 desktop GPU; **not physical-phone performance**.

Two motion unit tests pass, including rejection cases. A deliberate post-implementation detached-petal negative control really failed with `AssertionError: Ornament detached from lid`; it changes only the in-memory test scene and never saves it. The unchanged delivered source passed. This is regression proof, not a pre-model RED run. No accidental geometry/build failure occurred during this bounded implementation.

## Visual result and limits
Research-backed Rishtan-inspired palette with an invented eight-petal motif, not a verified traditional pattern or artisan-authored pottery. Actual source and mobile captures were inspected: wide silhouette, floral skin, attached low medallion and controls are readable; no obvious viewport clipping or floating ornament. Ceramic looks satin/painted rather than photoreal glazed ware; lid flowers are pale, repeats clip at face edges, the dark seam is visually broad, hardware is simplified and the source render has some sampling grain. These are disclosed v1 stylizations, not reference equivalence. No sacred inscriptions or third-party image textures. Research links and frozen dimensions are in `design-brief.md`, written before modeling.

## Reproduce
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, Node with the exact package-lock dependencies. The main checkout's promised shared esbuild entrypoint was absent, so pinned build-only dependencies were installed **inside this directory**, without changing the shared pilot. No runtime network downloads.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. `node --test --test-reporter=tap tests.mjs`
6. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
7. `python verify_browser.py` and `python verify_extended.py`.
8. `python package_delivery.py`.

`setup.py` records the one-time adaptation and depends on the repository Japan/Iceland templates; do not rerun it over a modified asset. Normal reproduction uses the included mechanism and has no sibling dependency. Regeneration overwrites source/export/poster; manual edits belong in a separate source copy. Three.js 0.180.0 MIT license included; esbuild 0.25.11 build tooling. No chain/node/wallet/keys/broadcasts, production edits or VPS access. Branch backup only; integration is a separate card.
