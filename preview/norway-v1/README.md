# Norway v1 — Fjord & Gneiss

Open **norway-v1.html** directly in Edge/Chrome. All runtime assets are embedded; no server, wallet, network or installation required. Drag/touch to rotate, Open/Close lid, Reset view. Reduced-motion preferences snap the articulated pose.

## Delivered
- Standalone HTML: **2,285,951 bytes**, strictly below 5,000,000.
- `norway.glb`: **1,117,300 bytes**, embedded maps and real articulated geometry.
- `norway.blend`: named, editable, packed Blender source; `mechanism.blend` is the included inherited mechanical baseline.
- `poster.png` / `poster.jpg`: real source render, not AI promotional artwork.
- Desktop/mobile closed/open, rear-open, corrupt-input fallback and no-JS screenshots.
- `design-brief.md`: research-backed pre-model contract. Geometry and maps are script-authored, not scanned or hand-sculpted.
- Source ZIP, byte/SHA-256 `inventory.json`, and verified archive `delivery-check.json`.

## Verified acceptance
- Saved source reopened independently: **81 poses**, **20 moving / 35 static meshes**, zero unintended surface intersections. Latch-versus-lid also checked. Only explicitly named mating hinge/barrel and latch/pin bearings excluded. Ten hinge/body/lid attachment pairs intersect as expected; hollow floor ray hits z=0.265.
- Same baseline pivot matrices; staged **80° latch release then 105° lid opening**. Independent motion tests cover all 81 stages and reject invalid geometry controls.
- Source/export maximum nearest-vertex distance **1.712013073529306e-7 units**, below 1e-5. Three packed procedural maps. Actual GLTFLoader: **11,090 triangles, 57 meshes, 7 materials**, zero nonfinite vertices/degenerate triangles.
- Two solid banks have peaks z=3.06047 and 3.01144, seated skirts, continuous water at z=2.012. Seventeen centerline samples plus both +/-0.1 width rays hit water; terrain and waterfall belong to the lid. Deliberately detaching the water fails the ancestry check, then restoration passes. Waterfall height/endpoints tested.
- Runtime decoded color ranges 114 and 51; actual glTF green-channel roughness range 39. Maps no larger than 512px. No external material downloads.
- Real offline `file://` Edge, desktop 1440×1080 and touch-emulated mobile 390×844: native controls, pointer/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no HTTP requests or runtime errors. Actual corrupt GLB reaches parser and shows poster with disabled controls. No-JS poster verified separately.
- Full-open projection maximum absolute NDC **0.885853**, inside viewport. Emulation ran on the desktop NVIDIA RTX 4060; no physical-phone performance/FPS claims.
- Archive explicit required-file set and every ZIP member verified by readback; SHA-256 inventory records exact bytes, preserved across Git with local `* -text` attributes.

## Real failure and correction
`initial/open-framing-failure.txt` retains an actual failed browser gate: **Open model clipped: 1.0088349968591457**. Raising the default camera to reveal the water exhausted the inherited 11-unit orbit limit. The fix increases opening reframe from 15% to 25% and permits a 14-unit orbit distance; the same strict `<1` projection assertion now passes at 0.885853. No acceptance threshold was relaxed.

The first mobile composition partly hid the fjord (`initial/mobile-closed.png`). One bounded presentation/geometry pass raised the camera and widened the center water corridor/bank spacing. The final native-size screenshot communicates two banks and a broad central channel. Source, GLB, source poster, collisions, parity and browser checks were regenerated after that geometry edit.

## Honest visual limits
This is a stylized miniature inspired by Norway's crystalline fjord walls, not a geographic model of a named fjord. Banks are faceted compact peaks rather than long valley walls. Water is opaque, flat-shaded blue-green, not fluid or optical-depth simulation; the small pale cascade is subtle. The procedural folded body bands can read as wood grain. Green/gray material regions are schematic. Brass is inherited collection language, not a claim of Norwegian artisan authorship. Rear/interior design is extrapolated. No photorealism, reference equivalence, continuous collision proof, manufacturing certification or user art approval is claimed.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, and Node with the pinned package.json toolchain. The prescribed shared `iceland-pilot/node_modules` was empty; exact Three 0.180.0 and esbuild 0.25.11 packages were installed only in this new folder. Dependencies are build-only and excluded from the ZIP/Git.

From this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly with `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
5. `node tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py` (local ZIP only).

Regeneration overwrites source/export/render; preserve manual edits separately. Recompute sizes and inventory after regenerating. `initial/` is historical evidence, not the final output. No third-party photos copied; Three.js MIT license included. Mechanical/viewer/test lineage is repository Japan v1; only Norway's new directory is changed.

## Scope / next
Local collectible art and authorized `art/norway-v1` branch backup only. Not hosted, minted, signed, uploaded to content-addressed storage or on-chain. No key, node, transaction, chain query, production-site edit, VPS access or merge. Cosmetic opening does not alter custody. Per-asset human review was waived; final collection integration is a separate dependent card.
