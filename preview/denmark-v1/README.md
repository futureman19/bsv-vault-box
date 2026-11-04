# Denmark v1 — Møn Chalk & Baltic

Open **denmark-v1.html** directly in Edge/Chrome. Full model, runtime, textures and actual-source poster are embedded. Drag/touch to rotate, Open/Close, Reset. Cosmetic inner-collectible motion only; no seal, custody, wallet or chain action.

## Delivered
- HTML **2,039,658 bytes**; GLB **949,460 bytes**. Strict whole-HTML cap: <5,000,000.
- `denmark.blend`: packed editable procedural Blender source; `denmark.glb`: portable model.
- Three original procedural maps, 512×256; actual Cycles `poster.png` and embedded JPEG. No copied research photographs or AI promotional replacements.
- `mechanism.blend` retains the existing Japan pilot's trimmed collection mechanism. Shared base kit and other previews unchanged.
- Source ZIP, inventory with SHA-256 and exact sizes, delivery readback, browser screenshots, checks and raw logs.

## Verified
Independent saved-source reopening: 44 moving and 35 static meshes, **81 sampled poses**, zero unintended surface intersections; latch-vs-lid included. Only original named concentric bearing contacts excluded. Ten attachment overlaps connect the hinge components. Hollow interior floor ray z=0.2650000155. Original pivot matrices match exactly.

Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7** (<1e-5). Actual GLTFLoader: **10,412 triangles, 82 meshes, 5 materials**, no degenerate or nonfinite geometry. Three cliff sections, 24 flint shoreline stones and water travel with the lid; detached-ornament negative control is rejected. Motion unit test rejects three invalid asset inputs.

Offline file:// Edge: 1440×1080 desktop and 390×844 touch-emulated mobile, native open/close, drag, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open maximum absolute projected NDC ~0.8924. Genuine corrupt-GLB parser failure activates poster fallback; no-JS poster also checked. GPU is desktop RTX 4060: **not a physical-phone test**.

## Visual verdict and limitations
White chalk escarpment, green plateau crown, turquoise Baltic inset and dark flint feet/shore make a coherent Denmark-inspired landscape miniature. Source and actual mobile screenshot were visually inspected. This is deliberately stylized: cliffs are faceted/repetitive, plateau is a green abstraction rather than individual beech trees, water has a straight rectangular boundary and no waves, and the source poster has visible sampling noise. The dark seam is prominent; tiny mobile disclaimer/hardware details are less legible. Not photorealism, geographic reconstruction, continuous collision proof or mechanical engineering certification.

## Preserved failures and fixes
1. `build-initial-failure.txt`: requested shared dependency path was empty. Installed the declared build dependencies locally in this new preview only; no dependency upgrades or shared checkout edits. node_modules is excluded from delivery/git.
2. `extended-initial-failure.txt`: runtime theme test initially searched only meshes, but GLTFLoader splits the two-material cliff into children under named groups. Fixed the oracle to inspect group names and lid ancestry; retained the three-cliff requirement and map-range threshold. No art/threshold relaxation.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/playwright; installed Edge; Node.js with `npm ci` in this directory. Runtime needs only a WebGL browser, not these build dependencies.
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with `verify_source.py`, `verify_theme.py`, `verify_parity.py` using the same flags.
5. `node test_motion.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py` (refresh hashes after any changed output).

`author.py` is standalone with included mechanism. `prepare.py` is the historical assembly helper and requires the sibling Japan source; it is not needed to reproduce. Regeneration overwrites outputs; preserve hand-edited source separately. Three.js MIT license included. Research attribution and frozen pre-model contract in design-brief.md. One-of-one collection direction is 201 designs, not proof of minting/storage. No deployment, chain access, public site modification or merge performed; branch backup only. Final collection integration is a separate card.
