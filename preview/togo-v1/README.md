# Togo v1 — Koutammakou Earth Towers

Open **togo-v1.html** directly in Edge/Chrome. Fully embedded 3D, maps, runtime and actual-source poster; no server or network. Drag/touch to rotate, Open/Close lid, Reset view. Reduced motion snaps. Local collectible art only, not minted, deployed or a custody operation.

## Delivered
- Standalone HTML: **2,643,365 bytes**, strictly below 5,000,000.
- GLB: **1,411,136 bytes**; 21,452 triangles, 67 meshes, 5 materials.
- `togo.blend`: packed editable source; `mechanism.blend`: frozen inherited mechanical baseline.
- `maps/`: independently generated earth color/roughness and stone maps. No third-party image textures.
- `poster.png`/`poster.jpg`: actual source render; desktop/mobile closed/open captures and fallback captures are actual offline browser output.
- Design brief, generators, check scripts, raw outputs, inventory and source ZIP included.

## Verified
Independent saved-source reopen: all 28 moving and 39 static meshes included in **81 poses**, zero unintended surface intersections. Only named concentric hinge/latch bearings excluded. Ten hinge attachment overlap pairs pass; hollow floor ray z=0.2650000155. This is sampled surface clearance, not continuous collision or engineering certification.

Source/export maximum nearest-vertex error **1.712013073529306e-7**, within 1e-5. Packed maps present. Actual GLTFLoader: zero nonfinite vertices and zero degenerate triangles. Four towers, two caps, twelve lid-owned miniature meshes; downward court ray reaches the lid. A deliberately detached in-memory tower is rejected by the ancestry gate and restored without saving. This is a post-implementation negative control, not test-first evidence.

Offline file:// Edge desktop and 390×844 mobile touch emulation: native open/close, drag/touch rotation, reset mid-animation, reduced motion, no overflow, no external HTTP requests and no runtime errors. Actual corrupt GLB reaches the parser and produces the poster; no-JavaScript poster passes. Full-open projected maximum absolute NDC 0.912971 (<1). This is desktop RTX 4060 browser emulation, not physical-phone performance.

## Visual verdict and limits
A stylized architectural homage to the shared Togo/Benin Koutammakou landscape, not a surveyed takienta or a claim of cultural completeness. Two conical caps read clearly on mobile; the small court is present but only modestly legible. Horizontal courses evoke applied earth but can also read as wood/planks or layered fabrication. The palette appears lighter under studio illumination. The pronounced dark lid seam, clean brass, rectangular box and stone feet are family extrapolations. Source render retains fine sampling noise (denoising disabled). The raised lid conceals the miniature from the default full-open front view; it remains attached. No photorealism, artisan authorship, sacred-symbol reproduction or exact reference equivalence claimed. Technical gates pass; human aesthetic approval is not claimed, and per-asset review was explicitly waived.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node.js with pinned Three 0.180.0 and esbuild 0.25.11. Shared pilot node_modules existed without an esbuild entrypoint; dependencies were installed locally only within this new preview. Node.js is build/test tooling, not a blockchain node. Dependencies are ignored and excluded from delivery.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python build.py`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

`setup.py` records original adaptation and requires the sibling Japan pilot; do not rerun it for routine rebuilds. Final generators and frozen mechanism are self-contained. Regeneration overwrites outputs; preserve manual edits separately. Motion/viewer/mechanical lineage: Japan cedar v1 from base commit ff5d78f. Research links in design-brief.md. Three.js MIT license included. Exact-byte inventory excludes itself and packaging envelopes to avoid recursive hashes; ZIP readback verifies every entry. All changes are additive within preview/togo-v1. Branch backup only, no merge or public deployment.
