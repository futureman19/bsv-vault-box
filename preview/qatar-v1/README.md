# Qatar v1 — Khor Al Adaid / Dune & Tidal Blue

Open **qatar-v1.html** directly in Edge/Chrome. Actual embedded GLB, runtime, procedural maps and source-rendered poster; no server/network needed. Drag/touch rotates, Open/Close demonstrates the staged latch/lid, Reset restores the view. Cosmetic inner collectible only: no custody, seal, wallet or transaction action.

## Delivered
- HTML **2,360,912 bytes** (strictly below 5,000,000); GLB **1,196,608 bytes**.
- `qatar.blend`: editable, packed Blender source; `mechanism.blend`: inherited trimmed Japan/Iceland mechanism, not copied country artwork.
- `author.py`, `maps.py`, maps/, viewer/template/build and verification scripts reproduce the pilot. `poster.png`/jpg are actual source renders, never promotional substitutes.
- Three curved pale dunes and turquoise tidal inlay on a limestone-inspired box with champagne brass fittings. Written sourced brief predates modeling. No third-party imagery or source photographs used as textures.

## Verified evidence
- `source-check.json`: independently reopened source, 20 moving / 39 static meshes, **81 poses**, zero unintended intersections, hollow floor ray z=0.2650000155. All terrain is included. Only explicit original hinge/latch mating bearings exempt. Ten hinge attachment overlaps pass.
- `parity-check.json`: source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5; three packed maps. This is evaluated geometry parity, not binary re-export equality.
- `theme-check.json`: three bounded dune reliefs with upward top normals, lid ancestry, 64-face continuous tidal ribbon and original pivots. Deliberately detached inlay is rejected by the same contract (negative control, not an initial art defect).
- `browser-check.json`: actual GLTFLoader **18,828 triangles / 59 meshes / 4 materials**, zero degenerates/nonfinite vertices. Desktop 1440x1080 and 390x844 mobile touch emulation over offline file:// pass native rotation, open/close, interrupted Reset, reduced motion, zero external requests/errors/overflow. Full-open maximum NDC 0.937538 fits. Real corrupt-GLB parser rejection invokes poster fallback.
- `extended-check.json`: three actual decoded 256px color/roughness/normal maps vary; roughness measured in GREEN. No-JS poster passes. Country-visible and accessibility copy checked.
- `tests.mjs`: 81 motion samples, endpoint/clamp and invalid-geometry negative controls.
- `delivery-check.json` and `inventory.json`: exact byte/SHA256 inventory and ZIP readback, with explicit required-artifact checks. Folder-local Git attributes preserve bytes.

## Real failure and correction
`initial-build-output.txt` retains the missing esbuild failure: the prescribed shared node_modules location was empty. Installed the unchanged pinned manifest locally inside this folder, not another preview. Build then succeeded. Dependencies are not delivered.
The initial mobile view made the turquoise inlay too slight (`initial-mobile-low-angle.png`); a bounded higher-camera correction exposed the inlay and all three reliefs, followed by fresh browser acceptance. No geometry gate was relaxed.

## Honest visual limits
Stylized decorative relief, not a surveyed coastline, scanned limestone, authentic craft object or photoreal image. Smooth dunes have somewhat slab-like ends; pale-on-pale separation is subtle on mobile and the visible blue area remains narrow. The teal seam is decorative. The generated pores are fine and subdued, not proven geological realism. Actual renders show sampling grain. The source and final mobile screenshots were visually inspected; no claim of user aesthetic approval. Mobile emulation used desktop RTX 4060, not physical-phone performance. Sampled collisions are not continuous mechanical certification.

## Reproduce
Python with numpy/Pillow/Playwright; Blender 5.2.1; installed Edge; Node with pinned package.json dependencies (`npm ci --ignore-scripts --no-audit --no-fund` here).
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.
`setup_author.py` records the original helper extraction from sibling Japan; it is not required for regeneration because author.py and mechanism.blend are included. Scripts overwrite generated outputs; preserve manual edits first. Three MIT license included. No production directories modified, no deployment, chain operation, keys, minting or VPS access. Branch backup only; final collection integration is separate.
