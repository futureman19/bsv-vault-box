# Colombia / Coffee Cordillera — v1

Open `colombia-v1.html` directly in Edge/Chrome. All runtime assets are embedded; no server or internet is required. Drag/touch to rotate, Open/Close lid, Reset; reduced motion is supported.

## Delivery
- HTML: **2,895,139 bytes**, below 5,000,000.
- GLB: **1,568,520 bytes**.
- `colombia.blend`: packed editable source; `mechanism.blend`: reused trimmed family mechanism.
- Procedural maps, author/build/check scripts, real source-render `poster.png` and JPEG, desktop/mobile closed/open screenshots, fallback captures, evidence JSONs and raw logs.
- `inventory.json`: exact SHA-256/byte inventory; `colombia-v1-source.zip`: source and evidence excluding dependencies, caches and backups. `delivery-check.json` verifies archive readback.

## Verified
Independent saved-source reopen: **77 moving / 39 static meshes**, **81 poses**, zero unintended sampled surface intersections; named mating bearings only are exempted. Ten physical hinge attachment overlaps pass. Hollow floor ray z=0.265. Unchanged original lid/latch world pivot matrices; staged 80-degree latch release then 105-degree lid opening. This is sampled surface testing, not continuous collision proof or engineering certification.

Source/export nearest-vertex error in both directions: **1.712013073529306e-7**, below 1e-5. Actual GLTFLoader: **22,540 triangles, 116 meshes, 9 materials**, no nonfinite vertices or degenerate triangles. Three packed maps; decoded roughness variation measured in glTF green channel. Lid ancestry includes hills, 56 shrubs and four farmhouse parts. Deliberately detaching one shrub makes the same theme oracle fail; this is a post-implementation negative control, not test-first history.

Actual Edge offline `file://`: desktop 1440×1080 and 390×844 mobile touch emulation pass native open/close, drag, interrupted reset, reduced motion, full-open framing (max absolute NDC 0.892365), no overflow, no external HTTP requests or JS errors. Real corrupted GLB reaches parser failure and displays poster; no-JS poster also tested. RTX 4060 desktop GPU, not physical-phone performance.

## Visual assessment and limits
Actual mobile and open screenshots were inspected. Honey bamboo and ivory/terracotta farmhouse are readable; the miniature shows rolling cultivated hills. Coffee shrubs are stylized green clusters and rely on the title/context for species identity. Bamboo pattern is regular and can read as ribbed wood; dark green seam and brass hardware are conspicuous. No photorealism, authentic craft reconstruction, exact geographic model or all-Colombia representation is claimed. The three blended hills are low miniature relief, not a dramatic mountain skyline. Terrain travels with the lid and is hidden behind it from the front at full opening. Open silhouette is framed, cavity visible, rear hinges visually attached; numerical checks supply separate geometry evidence.

## Reproduce
Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node with the pinned package dependencies. Run in this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund` (or use installed sibling pilot dependencies).
2. `python maps.py`
3. Blender `--background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`; `node --test tests.mjs`
5. Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.
`setup.py` documents one-time Japan lineage adaptation and requires that sibling; it is not needed for rebuild. All actual authoring inputs are included. Regeneration overwrites source/output. Source-render uses 24 Cycles samples without denoising; minor sampling noise remains.

## Failure and fix
First build failed with MODULE_NOT_FOUND for sibling `iceland-pilot/node_modules/esbuild/bin/esbuild`. The main-checkout dependency directory was empty, so the specified dependency link could not provide the compiler. Installing the existing pinned package dependencies locally in this new directory fixed the build; no validator or payload cap was weakened. See `dependency-output.txt`, `build-output.txt`. No geometry/collision/browser failures occurred in this run. Research URL extraction was unsupported, so research used indexed UNESCO search results instead.

## Scope and rights
Brief frozen before modeling. Procedurally authored geometry/maps, not scans or hand sculpture. UNESCO links inform regional context only; no third-party photographs embedded. Family mechanism/viewer/test lineage is Japan cedar v1 at base ff5d78f; Three MIT license included. No edits to other previews or shared kit, no blockchain access, minting, hosting, deployment or on-chain-storage claim. Cosmetic lid motion is not custody release. The user waived individual review until the 201-item collection exists; final integration is a separate card.
