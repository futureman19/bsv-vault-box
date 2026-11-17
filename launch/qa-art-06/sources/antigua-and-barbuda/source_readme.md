# Antigua and Barbuda v1 — Limestone & Pink Shore

Open `antigua-and-barbuda-v1.html` directly in a modern WebGL browser. Fully embedded 3D model/runtime/poster; rotate, zoom, Open/Close lid and Reset. Cosmetic collectible preview only; not minted, hosted, signed or chain-verified.

## Delivered and verified
- HTML **1,861,981 bytes**, GLB **793,632 bytes**. Strict HTML ceiling: 5,000,000 bytes.
- Packed editable `antigua-and-barbuda.blend`, included trimmed `mechanism.blend`, procedural maps and reproducible scripts. Source poster is an actual Cycles render, not generated marketing art.
- Saved-source reopening: 81 sampled poses, all 21 moving and 35 static meshes, zero unintended surface intersections. Latch-vs-lid included; only explicit inherited mating bearings exempt. Ten hinge attachment overlaps and hollow floor ray at z=0.265 pass. Sampled surface evidence, not continuous clearance/manufacturing certification.
- Source/export bidirectional nearest-vertex maximum error 1.712013073529306e-7 (<1e-5). Three packed source images. Original mechanism pivot matrices independently compared.
- Five coastal ornament meshes belong to the lid; a real deliberately detached ornament is rejected by the same assertion. Five rays through the arch aperture miss the crown, a higher crown ray hits. Stylized negative space, not a surveyed landmark.
- Actual Three GLTFLoader geometry, material map decoding, native desktop and 390x844 touch-emulated mobile file:// Open/Close, drag, interrupted Reset, reduced motion, no overflow, no external HTTP requests or unexpected JS errors pass. Corrupted embedded GLB reaches parser and displays poster; no-JS poster passes. See browser/extended JSONs for actual metrics. Emulation is not phone hardware testing or an FPS claim.
- Motion tests assert 81 staged poses, 80-degree latch followed by 105-degree lid endpoint and reject three malformed-asset controls.
- SHA-256 inventory/archive readback and staged Git byte parity are separate final delivery gates.

## Visual verdict and limits
Actual source and browser captures were inspected. Pale stone body, turquoise inset, pink crescent shore and genuinely open arch are readable and fully framed, including mobile. The miniature is deliberately abstract: the pink shoreline reads as a smooth ribbon rather than individual shell grains; the thick clean arch can read as a sculpture/handle rather than eroded natural rock, and limestone is broadly plaster/stone-like. Water is glossy opaque material, not simulated or transparent ocean. No exact geography, photorealism, original artwork equivalence or human art approval is claimed. The lid's landscape is hidden from the front in the open pose; rear-open capture documents it. Supporting mobile text is small. Render is 24 samples without denoising and retains fine grain.

## Real failure and fix
Initial build failed `MODULE_NOT_FOUND` for `preview/iceland-pilot/node_modules/esbuild/bin/esbuild`: the required shared dependency link resolved to an empty directory. Source/parity/theme tests had passed before that build. Installed pinned dependencies locally in this new folder, removed the temporary link, and rebuilt successfully without loosening any acceptance gate. `initial-build-failure.md` records the observed error. No art/collision failure occurred. Detached-ornament and malformed geometry tests are deliberate negative controls, not claimed test-first failures.

## Reproduce
Dependencies: Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node build runtime. `npm ci --no-audit --no-fund` in this folder (three 0.180.0 and esbuild 0.25.11). Node is only a local JS compiler/test runtime; no blockchain node was run.
1. `python maps.py`
2. Blender `--background --factory-startup --python-exit-code 1 --python author.py`
3. Same Blender flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`
4. `python build.py`; `node tests.mjs`
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites generated source/model/poster. Build prefers local dependencies, otherwise sibling Iceland dependencies. Offline HTML has no source-build dependencies. Scripts resolve locally. Package excludes node_modules, caches, backup files and packaging envelopes. `.gitattributes` preserves exact bytes across Windows Git checkouts.

Research links and pre-model contract: `design-brief.md`. No website imagery/textures copied; maps/geometry are script-authored, not scans or hand sculpture. Family mechanism, viewer and baseline verification adapted from Japan Cedar v1 at base ff5d78f1e0d486af5c882c184fc08049996ebdc8. Three runtime MIT notice included. Shared vault kit and all existing previews remain unchanged. Local branch backup only, no production deployment, wallet, keys, chain queries, broadcasts or merge.
