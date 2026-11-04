# Ethiopia v1 — Simien Escarpment

Open **ethiopia-v1.html** directly in Edge/Chrome. The actual 3D asset, runtime, maps and source-rendered poster are embedded; no server or network is required. Drag/touch rotation, Open/Close lid and Reset view work offline. Reduced-motion is honored. This is a cosmetic inner collectible, not a custody seal or transaction.

## Delivery
- HTML: **2,179,859 bytes** (<5,000,000).
- GLB: **1,031,440 bytes**.
- `ethiopia.blend`: editable script-authored Blender source with packed maps.
- `mechanism.blend`: inherited trimmed family articulation, liner and hardware.
- `maps/`, `maps.py`, `author.py`: generated stone color/roughness and reproducible geometry.
- `poster.png` / `poster.jpg`: actual source render, not AI promotion.
- Desktop/mobile closed/open/rear and fallback screenshots: actual offline browser captures.
- `inventory.json`, `delivery-check.json`, source ZIP: exact byte identities and archive readback.

## Verified
Saved-source reopening: **19 moving and 35 static meshes**, all tested in **81 opening poses**, plus latch-versus-lid checks. Zero unintended surface intersections. Only explicitly named mating bearing contacts exempted. Ten hinge attachment pairs intersect as intended; hollow floor ray z=0.2650000155. Sampling is not continuous collision proof or manufacturing certification.

Independent source-to-imported-GLB world-vertex nearest-neighbor error **1.712013073529306e-7** in both directions (<1e-5). Three packed procedural images. Original hinge/latch world matrices preserved. Three lid-owned escarpments have roots at z=1.978, stay within the brief's footprint/heights, and two valley rays reach the lid. Deliberately detached terrain is rejected by the ownership test; motion tests reject missing lids, empty geometry and nonfinite bounds. These negative controls are post-implementation regression checks, not a claim of TDD.

Actual Three.js GLTFLoader: **10,638 triangles / 57 runtime meshes / 6 materials**, zero nonfinite vertices and zero degenerate triangles. Multi-material escarpments split into runtime primitives. Color ranges 90 and 31; green-channel roughness range 81. Maximum map size 512×256. Poster is decoded and checked nonblank.

Offline `file://` Edge: desktop 1440×1080 and 390×844 mobile touch emulation pass native controls, mouse/touch rotation, interrupted reset, reduced motion, full-open framing (max absolute projected NDC 0.892365), no external requests, no JS errors or horizontal overflow. Actual corrupt GLB bytes trigger the parser's caught error/poster and disabled controls; no-JS poster works. RTX 4060 desktop GPU; not physical-phone performance testing.

## Visual outcome and limits
Final mobile screenshot shows three grounded, distinguishable plateau masses, coherent stone/olive/brass palette and readable controls; full-open image shows hollow interior and complete attached-lid silhouette. Lid terrain naturally disappears behind the opened lid from the front; rear screenshot exposes it. This is an invented stylized Simien-inspired miniature, not geographic reconstruction, photoreal equivalence, scanned stone, hand sculpture or a traditional Ethiopian craft object. Separate plateau forms read as decorative landform specimens rather than continuous mountains. Faceted tops, simplified cliffs, pale stone, modest procedural veining and slightly noisy source shadows remain visible.

One bounded visual correction reduced the initial wood-like horizontal banding and added multidirectional mineral variation. `initial/initial-banded-poster.png` preserves the rejected material reading. No numerical geometry/browser gate failed in the final verification sequence; no fabricated failure-and-fix is claimed. Research search/extraction endpoints failed; the actual UNESCO page was successfully read in the browser. Shared pilot node_modules was empty, so the exact inherited pinned dependencies were installed only in this new asset folder.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node and pinned package dependencies. `npm ci --ignore-scripts --no-audit --no-fund` in this folder. No runtime downloads.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`
6. `python verify_browser.py`; `python verify_extended.py`; `python verify_materials.py`
7. `python package_delivery.py`

`prepare_author.py` records the one-time helper derivation from sibling Japan; it is not needed to regenerate this self-contained source package. `author.py` uses included mechanism.blend only. Source/export regeneration overwrites outputs; preserve manual edits separately. Build falls back to sibling pilot dependencies only if a local install is absent. Three.js 0.180.0 MIT license included; esbuild 0.25.11 is build tooling. Folder-local Git attributes preserve exact hashed bytes.

## Scope and provenance
The sourced pre-model brief is the primary design reference. UNESCO text informed landscape selection only; no third-party photos/maps/logos embedded. The Japan/Iceland family mechanism/viewer/test lineage is reused, not their vegetation or geographic theme. Additive `preview/ethiopia-v1/` only. No production site, shared kit, wallet, keys, blockchain node, mint, broadcast, chain query, VPS or deployment touched. Branch backup only; integration remains a separate task. Collection direction: 201 equally one-of-one designs, not an issuance claim.
