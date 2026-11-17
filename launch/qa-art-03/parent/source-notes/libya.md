# Libya v1 — Acacus / Wind-carved Arch

Open **libya-v1.html** directly in Edge/Chrome. Complete offline interactive 3D: drag/touch rotation, zoom, staged Open/Close lid and Reset; reduced-motion support. **HTML 3,075,051 bytes; GLB 1,712,132 bytes.** Nothing is minted, hosted or deployed. Cosmetic opening is not an on-chain custody action.

## Design and deliverables
Research-backed brief was written before modeling; see `design-brief.md`. This is a procedural interpretation of Acacus desert landscapes, not a scale replica, stone scan, hand sculpture or comprehensive national portrait. Ochre body, pale low dune relief and an actual open arch on the lid; inherited brass hardware and hollow interior. No third-party images or rock-art symbols used.

`libya.blend` is packed editable Blender source; `libya.glb` portable geometry/maps; `mechanism.blend` is the inherited trimmed family mechanism. `author.py` and `maps.py` reproduce the asset. `poster.png`/`.jpg` are actual Blender source renders, never AI promotional images. Desktop/mobile closed/open and rear-open captures show the actual offline viewer. Runtime Three.js 0.180.0 MIT license included. Viewer/mechanism/test lineage: Japan cedar v1 and Iceland pilots in base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8; those folders were not edited.

## Checks actually run
- Saved .blend independently reopened. Hollow floor ray, ten intersecting hinge attachment pairs, unchanged rear pivot (0,1.32,1.668), latch parent and true arch aperture/crown ray checks pass. Filled-aperture geometry negative control is rejected by the same aperture predicate.
- **81 sampled poses**, all **18 moving** and **39 static** meshes, zero unintended surface intersections. Latch against moving lid included. Exempt only inherited named mating hinge-leaf/barrel and latch-knuckle/bridge/pin bearings. This is sampled surface collision evidence, not continuous clearance or mechanical-engineering certification.
- Source/export nearest world-vertex error below 1e-5; exact measured result in `parity-check.json`. Three packed procedural images. Actual GLTFLoader checks zero nonfinite/degenerate geometry, finite bounds and decoded map variation. Base-color red-channel ranges 86 and 40, both 512 square.
- Motion tests pass release-before-lift, reversal, clamped endpoints and malformed-asset rejection. Saved source theme dimensions/parentage/aperture checks pass.
- Offline file:// Edge desktop 1440×1080 and mobile 390×844 touch emulation: native open/close, drag, interrupted reset, reduced motion, no overflow, no external HTTP requests or runtime errors. Actual corrupted bytes reach GLTFLoader and produce the poster fallback; no-JS poster also passes. Full-open projected silhouette fits. Mobile emulation is not physical-phone performance.
- `inventory.json` gives exact byte counts/SHA-256 for deliverables, sources and evidence. `delivery-check.json` verifies required file set, size ceiling and inventory readback. Inventory excludes itself, its delivery envelope and temporary caches/backups to avoid recursive hashes.

## Honest visual limits and bounded correction
The silhouette and genuine arch opening read clearly on mobile. The arch remains chunky/handle-like rather than a detailed natural monument. Dunes are low relief and visually subtle. The first finish read strongly as wood; one bounded correction darkened and disrupted the bands and roughened the arch. Final surfaces still have some wood-like horizontal mottling, not photorealistic mineral texture. The narrow dark seam looks conspicuous; from the front open view the bearing area can appear slightly floating, although independent saved-source attachment intersections pass. Rear interior/hardware are family extrapolations. No human art approval or photoreal-equivalence claim.

Actual failure retained: first Cycles poster render failed with OIDN out-of-memory (`initial/render-oidn-failure.txt`). Disabling render denoising fixed it; the final real render has some sampling noise. Initial wood-like screenshot is retained. Optional Codex lane failed authentication before any implementation; Hermes authored and ran everything directly. No credentials were read or changed. Native node.exe was used for motion tests after the shell shim reported `stdin is not a tty`.

## Reproduce (from repository root)
Dependencies: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node/esbuild/Three. Build resolves local node_modules or sibling `preview/iceland-pilot/node_modules`; that ignored worktree link is development-only, not a runtime dependency. No dependency directory is shipped.

1. `python preview/libya-v1/maps.py`
2. Blender with `--background --factory-startup --python-exit-code 1 --python preview/libya-v1/author.py`
3. `python preview/libya-v1/build.py`
4. `node --test preview/libya-v1/tests.mjs` (Windows shell shim: use `C:/Program Files/nodejs/node.exe`)
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `python preview/libya-v1/verify_browser.py` and `python preview/libya-v1/verify_extended.py`.
7. `python preview/libya-v1/package_delivery.py` after updating final documentation. Keep motion output at `motion-output.txt`.

Regeneration overwrites authored files. Preserve manual edits elsewhere first. Rebuilding source/render may change hashes; regenerate inventory. Only this new preview directory is committed; branch backup is `art/libya-v1`, no merge. Launch direction remains 201 equally one-of-one designs. Off-chain storage/issuance remain proposals, not implemented by this asset.
