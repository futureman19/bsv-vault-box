# Mali v1 — Bandiagara Ochre

Open **mali-v1.html** directly in Edge/Chrome. The real 3D model, runtime, maps and source-rendered poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion is supported. No network or server needed.

- HTML: **2,457,564 bytes**, strictly below 5,000,000.
- GLB: **1,249,588 bytes**; 16,126 triangles, 54 meshes, four materials.
- Editable packed `mali.blend`, standalone `mali.glb`, original procedural `maps/`, actual Blender `poster.png`/JPEG, desktop/mobile closed/open/rear/fallback captures.
- `mali-v1-source.zip` contains the explicit required artifact set, scripts, source, trimmed inherited mechanism, evidence and inventory. No node_modules or backups.

## Design and provenance
The prewritten `design-brief.md` is the primary reference, not an invented approved illustration. UNESCO's [Cliff of Bandiagara](https://whc.unesco.org/en/list/516/) describes sandstone plateau, escarpment and plains, and erosion-created caves/rock shelters. Its indexed description was rechecked during this run. The sculptural interpretation has three unequal terraced shoulders and two recessed gullies on a rear-half lid relief. No third-party photographs are embedded. No sacred motifs or traditional-artisan authorship are claimed. Hardware is inherited BoxSV family geometry, not Malian historical metalwork.

Ochre map mean RGB is 169.79 / 111.75 / 60.68; all three authored maps are 256 square. Physical-axis UV projection avoids wood-like grain stretching. Terrain width is 2.80, depth 1.015, highest point z=2.74669 over a lid top at 1.978. Three shoulder heights are 2.63207 / 2.74669 / 2.56630; gullies 2.30506 / 2.25076. One closed terrain mesh seats into the lid and belongs to Lid_Hinge.

## Actual acceptance
- `source-check.json`: saved source independently reopened; 17 moving and 37 static meshes; **81 motion poses**, zero unintended surface intersections. Every moving mesh, including terrain, tested against static meshes; releasing latch tested against lid. Only named mating hinge leaf/barrel and latch knuckle/bridge/pin contacts exempt. Ten hinge attachment pairs intersect as intended; floor ray at z=0.265 proves a recessed hollow interior.
- `theme-source-check.json`: measured bounds, unequal shoulders, recessed gullies, inherited pivot matrix parity. Deliberately detached terrain is rejected by the ancestry assertion.
- `parity-check.json`: bidirectional nearest-world-vertex distance **1.712013073529306e-7**, below 1e-5; three packed source images. This is geometry parity, not byte-identical source re-export.
- `motion-output.txt`: 81 staged poses, 80° latch release before 105° lid opening; three invalid-asset controls rejected.
- `browser-check.json`: actual GLTFLoader reports no nonfinite vertices or degenerate triangles. Offline file:// desktop 1440×1080 and touch-emulated mobile 390×844 tested rotation, native buttons, opening/closing, interrupted reset and reduced motion, no overflow, no external HTTP requests, no uncaught/errors on valid loading. Open projected silhouette maximum absolute NDC 0.89237. Genuine corrupt GLB input reaches parser and shows poster fallback.
- `extended-check.json`: runtime terrain ancestry, decoded color variation and roughness **green-channel** variation, country/accessibility copy, source poster pixels, no-JS poster fallback. Final mobile closed/open screenshots inspected: all three shoulders readable; raised lid/latch and hollow body fit without obvious disconnections.
- `delivery-check.json` / `inventory.json`: exact SHA-256 and byte inventory; explicit required file membership and archive readback. Archive and envelope excluded from recursive inventory.

## Failures and bounded fixes
The recovered prior optional Codex run failed authentication (401); no Codex patch was accepted. `lane-output.txt` is retained; credentials were not accessed or altered. Hermes authored and independently exercised this delivery.

A premature build tried to read the poster before rendering completed (`initial/build-before-poster.txt`). The first browser gate then failed waiting for model readiness (`initial/browser-first.txt`). Inspection found collapsed terrain skirt faces where the original perimeter top equalled its bottom. The perimeter top was raised 0.025, retaining its embedded lower skirt; no validation thresholds were relaxed. The final actual loader reports zero degenerate triangles. `initial/first-poster.png` is the initial actual source render. A subsequent brief audit added the missing family side ring and mount; the complete source/export/render/browser suite was rerun. Earlier pre-ring logs are explicitly historical under `initial/`.

The shared pilot compiler path was absent; the prescribed shared dependency tree was not populated. Pinned Three/esbuild dependencies were installed **only in this new folder**, with lockfile; node_modules is ignored. All final viewer runtime assets remain embedded.

## Visual limitations
Stylized procedural geology, not photorealism, a surveyed Bandiagara section, or a depiction of every Malian culture. Terraces are broad and regular; mineral pores are subtle and bronze is close in value to the body at mobile scale. The source render retains some 24-sample Cycles noise. Rear corner hardware is partially occluded by the relief. The dark seam is deliberately prominent. No physical-phone performance, continuous mechanical collision certification or manufacturing suitability is claimed. Mobile tests ran on desktop Edge / RTX 4060.

## Reproduce
Python with numpy, Pillow and Playwright; installed Edge; Blender 5.2.1; Node.js with the pinned package-lock.

1. `npm ci --ignore-scripts --no-audit --no-fund` inside this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_checks.py` (set BLENDER_EXE to override the documented Windows default; motion test uses the installed Windows node.exe path).
5. `python package_delivery.py`

Authoring replaces generated artifacts; preserve manual edits separately. Scripts use folder-relative source assets. The viewer and trimmed mechanism derive from the Japan pilot; no shared kit or previous preview is modified. Three.js license is included. This is local collectible art only: not minted, hosted, signed, chain-admitted or deployed; no wallets, keys, blockchain nodes, transactions or production website changes. Branch backup only; collection integration is a separate card.
