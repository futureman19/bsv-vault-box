# India v1 — Marble & Parchin Kari

Open **india-v1.html** directly in Edge/Chrome. Entire runtime/model/maps/source-render poster are embedded: **2,322,509 bytes HTML**, **1,166,140 bytes GLB**. No network or server needed. Drag/touch rotate, Open/Close lid and Reset. Cosmetic movement only; not a custody action.

## Design and provenance
Agra's marble-inlay tradition is the regional inspiration; sources and the pre-model measurable contract are in design-brief.md. Original procedural floral layout, not a reproduction of a historical motif, artisan work, scanned marble, or a model of the Taj Mahal. Ivory body with carnelian-colored central flower, four lapis-colored flowers and jade-colored vines. There are no sacred inscriptions. This is not a claim to encompass all Indian traditions.

Named editable source: india.blend; standalone export: india.glb; generated portable maps in maps/. poster.png and poster.jpg are actual source renders. Desktop/mobile screenshots are actual offline Edge captures. mechanism.blend retains the Japan pilot's trimmed family mechanism; author.py reuses it, not Japan's cedar/tree design. The shared vault kit and other previews were not modified. Three 0.180.0 MIT license included; esbuild 0.25.11 is build-time only.

## Verified
- Actual GLTFLoader: 106 meshes, 24,748 triangles, 6 materials, zero degenerate triangles or nonfinite vertices.
- Saved-source independently reopened: 65 moving and 41 static meshes sampled over 81 poses, no unintended intersections. Latch-versus-lid also tested; only named original mating bearings excluded. Ten hinge attachment overlap pairs pass; hollow interior floor ray z 0.2650000155. This is sampled surface testing, not continuous collision/manufacturing certification.
- Original hinge/latch world matrices independently compared with reopened mechanism.blend. Staged 80-degree latch release, then 105-degree lid opening preserved. Two motion/invalid-asset tests pass.
- Saved-source/export nearest-vertex maximum error 2.4575624024691933e-7, below 1e-5. Two packed procedural images verified; loaded 256px color range 48 and roughness-green range 39.
- 49 lid-owned ornament meshes: 32 petals, 5 hearts, 8 leaves, 4 stems. Surface bounds z 1.9750000238–2.0169999599. Deliberately detached ornament is rejected by the same ancestry assertion: real negative control, not a fabricated failure history. No organic correction failure occurred.
- Offline file:// Edge 1440×1080 desktop and 390×844 touch-emulated mobile: native buttons, drag/touch rotation, open/close, interrupted reset, reduced motion, no overflow, zero external HTTP requests and zero errors. Full-open maximum absolute projected NDC 0.8923646517. Real corrupted GLB reaches parser and displays poster/disabled controls; no-JS poster also passes. RTX 4060 desktop GPU; not physical-phone performance.
- Exact bytes and SHA-256 for the delivery inventory; ZIP entries/hash readback and Git staged-blob validation. Explicit required artifact subset checked. No model signing, NFT issuance, chain storage, deployment, hosted preview or blockchain tests.

## Honest visual verdict
Actual source/mobile/open captures were inspected. Floral colors are legible at mobile size, the complete silhouette fits, and the hollow box and rear hinges read coherently. This remains a stylized v1: marble veins are regular and wavy rather than photorealistic, flowers are raised intarsia-inspired geometry rather than flush artisan inlay, hardware is simplified, and the dark green reveal makes the closed lid look slightly elevated. The source render retains sampling grain. Fine petals require zoom. At full opening the ornament naturally faces away from the default front camera. No exact-reference or photoreal-equivalence claim. Individual human approval was waived; collection integration is the next stage.

## Reproduce
Requirements: Blender 5.2.1; Python + numpy/Pillow/Playwright and installed Edge; Node/npm for pinned build-only dependencies. The prescribed shared pilot node_modules did not contain esbuild, so exact pinned dependencies were installed only in this folder. No dependency directory is included in Git/ZIP.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender the same way for verify_source.py, verify_parity.py, verify_theme.py.
5. `node --test tests.mjs`; `python build.py`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Run scripts from any working directory; they resolve included files relative to their own directory. Reauthoring overwrites source/export/poster: preserve manual edits separately. The ZIP and inventory avoid self-referential hashes; delivery-check.json records the archive hash outside the archive. Folder-local Git attributes preserve exact payload bytes on Windows. No public-site, mint, vault, key, node or server operations occurred.
