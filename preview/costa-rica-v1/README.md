# Costa Rica v1 — Arenal & Rainforest

Open **costa-rica-v1.html** directly in Edge/Chrome. Complete local 3D viewer: **3,002,581 bytes**. Standalone GLB: **1,677,396 bytes**. Drag/touch to rotate, Open/Close lid, Reset; reduced-motion preference supported. No network assets, server, wallet, mint or custody operation.

## Artwork and limitations
A dark green-gray volcanic-stone keepsake chest carries an Arenal-inspired fluted cone and 24 low rainforest canopy clusters. Research-backed written brief precedes model authoring; no supplied concept illustration. All geometry/maps are procedural Blender authorship, not scans or hand sculpture. The poster is rendered from the actual source, never AI promotional art.

Actual mobile and open-rear screenshots inspected: whole silhouette fits, hardware and landscape are visible; ornament moves with lid. Stone looks soft/mottled rather than rough lava; canopy clusters are simplified rounded crowns in a fairly regular ring, not botanical trees. Cone is strongly faceted and looks fan-like from the raised-lid angle. Its small summit depression is not legible at phone size. This is a stylized landscape miniature, not geographic, photoreal or historical-craft equivalence. Inherited brass fittings are a family design invention.

## Verified evidence
- `source-check.json`: independently reopened packed source; 42 moving / 39 static meshes, **81 poses**, no unintended surface intersections. Every moving decoration included. Only named mating bearing contacts exempt. Hollow floor ray z=0.26500001549720764. Ten hinge attachment pairs checked.
- `parity-check.json`: bidirectional evaluated source/export vertex error **1.712013073529306e-7**, under 1e-5. Three packed image resources verified.
- `theme-source-check.json`: exact inherited pivot matrices, cone height and 24 canopies with lid ancestry. An intentionally detached cone is correctly rejected; mutation is never saved.
- `browser-check.json`: real GLTFLoader geometry validation; offline `file://` desktop 1440x1080 and touch-emulated mobile 390x844. Native open/close, touch/mouse rotation, reset during motion, reduced motion, full-open projected bounds, no overflow/HTTP requests/unhandled errors. Genuine corrupted GLB triggers poster fallback.
- `extended-check.json`: actual runtime map decoding including green-channel roughness variation; canopy/cone counts and ancestry, palette, poster nonempty, no-JS fallback, no inherited Japan text.
- `delivery-check.json`: explicit required artifact set, byte/SHA-256 inventory, ZIP readback. All checks are assertions capable of failing, not unchecked status flags.

Sampling is not continuous collision/mechanical certification. Emulated mobile uses a desktop GPU, not physical-phone performance. No FPS or production-readiness claim.

## Failure and fix
The first build failed: `Cannot find module ...preview/iceland-pilot/node_modules/esbuild/bin/esbuild`. The mandated junction targeted an existing but empty dependency directory. Installed the declared build dependencies **only in this new directory** with `npm install --ignore-scripts --no-audit --no-fund`; build then passed without changing the size gate. `failure-history.json` records this observed toolchain failure. No model collision or geometry gate failure occurred. The deliberately detached ornament is a separate negative-control test, not a spontaneous defect.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node build tooling (not a blockchain node). In this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `python verify_browser.py` and `python verify_extended.py`
7. `python package_delivery.py`

`mechanism.blend` is the trimmed existing Japan-family mechanical base; author.py requires no sibling geometry. `setup.py` is the one-time adaptation provenance script and references the Japan sibling; **do not rerun it for normal rebuilding**, because it overwrites scripts. Regeneration overwrites source/art/evidence, so preserve manual edits separately and regenerate the inventory afterward. Three.js MIT license included. No node_modules or Blender backups in archive. Folder-local Git attributes preserve exact payload bytes.

Only preview/costa-rica-v1 added. Branch backup is not deployment or integration. Collection direction: 201 equally one-of-one designs; art completion does not mint anything or prove custody. Per-asset human review was explicitly waived for this production batch; final collection integration is a separate task.
