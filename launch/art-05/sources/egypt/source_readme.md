# Egypt v1 — Alabaster & Pyramid Fields

Open `egypt-v1.html` directly in Edge/Chrome. Complete embedded 3D runtime, model, maps and actual-source poster; no server or internet required. Drag/touch to rotate, Open/Close, Reset. Cosmetic only: no custody or chain state changes.

## Delivery
- HTML: **2,693,785 bytes**, strictly below 5,000,000.
- GLB: **1,467,052 bytes**.
- `egypt.blend`: editable packed Blender source; `mechanism.blend`: inherited trimmed mechanism.
- `maps/`, `maps.py`, `author.py`: procedural materials and geometry, not scans.
- `poster.png`/`.jpg`: actual Blender source render. Desktop/mobile PNGs: actual offline browser captures.
- `inventory.json`, `delivery-check.json`, source ZIP: exact-byte identities and archive readback.

## Verified
Reopened source: 24 moving and 39 static meshes, 81 motion samples, zero unintended surface intersections. Latch releases 80 degrees before lid opens 105 degrees; ornaments travel with the lid. Explicit mating bearings alone are excluded. Ten hinge attachment intersections and hollow floor ray at z=0.265 pass. Sampling is not continuous collision certification.

Source/export bidirectional nearest-world-vertex error: 1.712013073529306e-7, below 1e-5. Actual GLTFLoader: 63 meshes, 14,942 triangles, four materials, zero nonfinite vertices or degenerate triangles. Three lid-parented pyramids and plateau verified; decoded color/roughness variation passes.

Fresh offline file:// Edge desktop and 390x844 touch-emulated mobile: open/close, drag/touch rotation, interrupted reset, reduced motion, no overflow, zero HTTP requests and JS errors. Full-open maximum absolute projected NDC 0.892365. Real corrupt-GLB parser fallback and no-JS poster pass. RTX 4060 host; no physical-phone performance claim.

Real failure preserved in `extended-initial-output.txt`: initial test read red rather than green for glTF packed roughness and reported zero range. Correct channel gives range 48 without relaxing the >10 gate. Optional Codex attempt failed authentication (`lane-output.txt`); no Codex edits accepted. Recovery reran build and all source/parity/theme/browser/extended gates successfully.

## Visual limits and interpretation
Research-backed brief predates modeling; three simplified uninscribed pyramids represent one Egyptian landscape/material thread, not all Egypt or an accurate archaeological model. Actual mobile inspection shows all three pyramids, ivory/honey stone and brass fittings without clipping. Stone is opaque satin, not physically translucent alabaster. Veins are procedural; stepped corner/seam details and long inherited clasp are stylized. Minor edge aliasing and flat lighting remain. No photoreal-equivalence or human art approval claimed. Per-asset human review was explicitly waived.

## Reproduce
Python with Pillow/numpy/Playwright, installed Edge, Blender 5.2.1, Node with package.json pinned dependencies. Shared installed compiler in `../iceland-pilot/node_modules` is build-time only; standalone source users install dependencies here.

1. `python maps.py`
2. `blender -b --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python verify_browser.py` and `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites source/export/poster; preserve manual edits separately. Three.js license included. No blockchain operations, minting, keys, deployment, VPS changes or modifications to shared art/previews. Branch backup only; integration is a separate card.
