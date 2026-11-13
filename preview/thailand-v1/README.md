# Thailand v1 — Celadon & Carved Waves

Open `thailand-v1.html` directly in Edge/Chrome. Complete offline 3D viewer: **2,258,199 bytes**; embedded standalone `thailand.glb`: **1,123,908 bytes**. Drag/touch rotation, zoom, staged Open/Close and Reset. No runtime network dependencies.

## Design and honest visual result
Research-backed blue-green celadon shell with three curved pale ceramic wave ribbons and restrained brass. Smithsonian and Tokyo National Museum sources in the pre-model design brief informed material/craft choices, not copied imagery. This is a contemporary stylized interpretation, not an antique reproduction or a uniquely Thai motif claim. Celadon traditions span multiple countries.

Actual mobile and open desktop renders were inspected. The cool glaze/brass palette and wide chest are coherent. The waves are shallow raised tubes rather than historical engraved decoration; body mottling can read like stone, feet and hardware are visibly simplified, and the dark seam is conspicuous. The retained long released clasp projects above the open lid. Front-open views show the underside, naturally hiding the exterior wave relief. No photoreal equivalence, human art approval, artisan authorship, physical-phone performance or manufacturing suitability is asserted.

## Verified evidence
- `source-check.json`: independent saved-source reopening, hollow floor ray z0.265, **81 sampled poses**, **21 moving and 39 static meshes**, zero unintended intersections. Includes all new waves/frame; only explicitly named mating bearings exempt. Ten physical attachment pairs checked. Sampled surface collision checks, not continuous analytical collision proof.
- `parity-check.json`: source and actual GLB reimport vertices agree within 1e-5 world units; packed images confirmed.
- `theme-check.json`: exact inherited pivot matrices, three lid-parented waves, bounded geometry and seating; deliberate detached-wave negative control rejected.
- `browser-check.json`: actual GLTFLoader finite/nondegenerate geometry; desktop 1440×1080 and 390×844 mobile touch emulation over offline file://; native rotation/open/close/reset during motion, reduced motion, full-open projected fit, zero HTTP requests, zero errors and no overflow. Real corrupt GLB parser fallback tested.
- `extended-check.json`: source palette ranges, actual decoded runtime maps (roughness green channel), accessible Thailand copy, nonempty source render and no-JS poster.
- `motion-output.txt`: 2 tests pass, 0 fail, staged 80° latch then 105° lid endpoints and rejection tests.
- `inventory.json` / `delivery-check.json`: exact byte counts and SHA-256 for every payload, required-artifact ZIP inventory and byte-for-byte readback. `.gitattributes` preserves payload bytes through Git.

## Real failure and bounded correction
`theme-initial-failure.txt` preserves an actual failure against initial wavy-height tubes: lower extent 1.958135 was outside the stricter seating band. The initial tube also rose off the surface along portions of its length. Rebuilt all ribbons at constant center z2.022, radius .045; underside now z1.977, embedded .001 into the lid top1.978. This tiny hidden seating overlap is the deliberate deviation from the brief's nominal 1.98 lower bound; exposed relief stays above the lid. Same failing assertion now passes; no collision exemptions were added. All source/export/browser checks were rerun after correction.

## Reproduce
Blender 5.2.1, Python (numpy/Pillow/Playwright), installed Edge, Node with exact dependencies in package-lock.json. The shared Iceland node_modules existed without an esbuild entrypoint, so pinned dependencies were installed only in this new directory, not into another preview. node_modules excluded from delivery.

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

`mechanism.blend` and inherited viewer/test lineage are copied from the Japan pilot at base ff5d78f. All authored scripts resolve local assets relative to this folder. Regeneration overwrites model/source/render; preserve manual edits separately. Maps and geometry are procedural, not scans. Poster is a real source render, not AI promotional imagery. Three.js MIT license included. Editable packed source, maps, scripts, evidence and source ZIP are included; build dependencies/backups are not.

Art-only branch backup. No blockchain node, keys, wallet, mint, broadcast, production site, Hetzner, merge or public deployment. Cosmetic opening is not opening an on-chain seal. Next step: collection integration card, after the full set is ready.
