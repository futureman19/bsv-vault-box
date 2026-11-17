# Vietnam v1 — Emerald Karst

Open **vietnam-v1.html** directly in Edge/Chrome. All model, textures, runtime and the actual Blender-rendered poster are embedded. Drag/touch to rotate, Open/Close lid and Reset. Cosmetic inner-collectible motion only; nothing minted, signed, hosted or sent to a blockchain.

## Delivery
- HTML: **2,268,101 bytes** (strictly below 5,000,000).
- GLB: **1,120,896 bytes**.
- `vietnam.blend`: packed editable source; `mechanism.blend`: included inherited mechanical scaffold.
- `maps/`: generated 256px limestone color/roughness maps; no scans or research imagery.
- `poster.png`/`poster.jpg`: actual final source render. Desktop/mobile PNGs: actual offline browser captures.
- Source ZIP, inventory and delivery-check contain exact bytes/hashes and readback evidence.

## Design and visual limits
Research-backed Ha Long Bay–Cat Ba inspiration, not a map or a claim to represent every Vietnamese tradition. Five limestone stacks with simplified green crowns stand in an emerald inset on a pale limestone chest with brass fittings. Entire landscape travels with the lid. See the prewritten design brief for sources and dimensions.

Actual screenshot inspection confirmed all five islands readable at mobile size, fully framed; open view shows the hollow interior and entire latch/lid. This is deliberately stylized: angular stacks, polygonal vegetation rather than trees, opaque flat teal water rather than realistic waves, and softly mottled body shading. The inherited clasp is chunky, and dark reveal/stepped corner trims remain visible. No photorealism, geographic fidelity, artisan authorship or previous human art approval claimed. The user waived per-asset review for this batch.

## Verified
- Saved-source independently reopened: 22 moving and 39 static meshes, **81 poses**, zero unintended moving/static or latch/lid surface intersections. Explicit bearing contacts only excluded. Ten hinge attachment overlaps and hollow-floor ray at z=0.265 verified. Sampled surface intersections are not continuous solid-collision/manufacturing certification.
- Source/export bidirectional vertex error **1.712013073529306e-7**, below 1e-5. Three packed source maps. Actual loader checks finite vertices and zero degenerate triangles.
- Five separate island footprints, crown faces, lid ancestry, contained footprints and .30–.68 height range; original pivot matrices unchanged. Detaching an island in memory is rejected by the real ownership assertion, then restored without saving.
- Actual offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native controls, drag/touch rotation, open/close, interrupted reset, reduced motion, full-open projection, zero external requests/JS errors/overflow. Actual corrupt GLB reaches parser failure and displays poster. No-JS poster also verified. Emulation on desktop GPU is not physical-phone performance.
- Runtime decoded color ranges 69 and 59, roughness green-channel range 14; no blank-map proxy. Poster nonempty-pixel gate, visible/accessibility country-copy gate.
- Motion unit tests: 2 passed, 0 failed; includes invalid-asset rejection.

## Real failure and correction
Initial height test was too permissive (.71) and accepted an irregular summit reaching .70377354 above water, outside the frozen .68 brief. Tightening the oracle to the original brief produced the actual failure in `initial/height-failure.txt`. The tall island nominal height was reduced from .68 to .65 (rather than relaxing the brief). Source/render/GLB and all browser, parity, collision and theme checks were regenerated and passed. Initial measured geometry is retained in `initial/height-before-correction.json`; it is not final acceptance evidence.

## Reproduction / provenance
Blender 5.2.1; Python with numpy/Pillow/Playwright and installed Edge; Node with exact package-lock dependencies. Shared pilot node_modules was inspected and lacked esbuild, so pinned build dependencies were installed **only in this folder**; no other preview modified. No dependency download occurs at viewer runtime.

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender likewise on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python build.py`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

All commands from this directory. Authoring overwrites generated files; preserve manual edits separately. Rebuild inventories after any regeneration. Mechanical scaffold, viewer and checks adapted from repository Japan/Iceland pilots at baseline ff5d78f; Three 0.180.0 is MIT (included license), esbuild 0.25.11 build-only. Source scripts use folder-relative paths; build fallback may discover sibling dependencies but local npm ci removes that dependency. Archive excludes node_modules and Blender backups. No changes outside this new preview folder, no deployment or merge.
