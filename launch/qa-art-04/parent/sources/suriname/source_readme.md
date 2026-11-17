# Suriname v1 — Granite & Rainforest

Open **suriname-v1.html** directly in Edge/Chrome: a self-contained offline collectible study. **HTML 2,469,009 bytes; GLB 1,269,168 bytes.** Drag/touch rotate, Open/Close lid, Reset view. Reduced-motion preference honored. No network runtime dependencies.

## Design and delivered files
The sourced, pre-model `design-brief.md` selects Central Suriname's granite inselbergs, tropical forest and river landscapes. Warm-gray stone body, bare rounded dome, low green canopy and a winding blue-green inlay, with family brass hardware. Invented miniature composition, not a surveyed Voltzberg reconstruction, indigenous craft claim, or comprehensive representation of Suriname.

`suriname.blend` is editable Blender source; `suriname.glb` embeds geometry and portable maps. `mechanism.blend` is the inherited trimmed Japan mechanism. `maps.py` produces four 256px procedural maps, not scans. `author.py` generates the model and actual Cycles poster. `poster.png/jpg` and desktop/mobile closed/open screenshots show this model, never AI promotional substitutes. Source archive and exact inventory are produced by `package_delivery.py`.

## Verified
- Saved-source reopened independently: hollow floor at z=0.265, ten intersecting hinge attachment pairs, 46 moving/39 static meshes, **81 sampled poses and zero unintended intersections**. Latch-vs-lid included; only explicit inherited bearing contacts excluded. This is sampled surface collision testing, not continuous engineering certification.
- Same inherited pivots, staged 80-degree latch release followed by 105-degree lid opening. Two motion/asset-negative unit tests pass.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7** (<1e-5). Four packed maps retained.
- Actual browser GLTFLoader: **17,708 triangles, 85 meshes, 10 materials**, zero nonfinite vertices/degenerate triangles.
- All relief is lid-owned; detached-river negative control rejected. Bare dome top z=2.78251648 exceeds all 27 low canopy clusters. All 48 river face-center downward rays hit the river. Geometry and sampled top visibility are not hydrological realism.
- Actual map channel decoding: color range 91, roughness GREEN range 95, normal red range 24; 256px maps.
- Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, mouse/touch rotation, reset interrupted motion, reduced motion, zero external requests/JS errors, no horizontal overflow. Open silhouette maximum absolute projected NDC 0.892365. Corrupt GLB actually fails the loader and shows poster; no-JS poster checked. Emulation ran on RTX4060, not physical phone performance.
- Actual visual inspection: mobile closed dome smoothly rounded/bare, entire box fits, labels/controls readable; desktop open is hollow, attached and unclipped. The lid-top miniature naturally hides behind the open lid from the default front view.

## Honest limitations and preserved corrections
Stylized collectible, not photoreal reference equivalence. Stone grain is fine/cloudy rather than a geological scan; forest is low simplified canopy lobes, not botanical trees. River is an exposed ribbon/inlay, subtle on mobile, not a recessed fluid simulation. Its terminal edges are invented. Rear hardware/interior are family extrapolations. Nominal dimensions are inherited wide-body proportions (approximately 3.72×2.38); fittings extend beyond them.

`initial/jagged-dome.png` preserves the first overly rough dome; a low-frequency smooth deformation corrected its silhouette. `initial/river-endpoint-ray-failure.txt` preserves a real test failure: an exact terminal-edge ray missed due to boundary precision. The corrected oracle samples each actual face center, retaining all 48 segments and strict hit identity. No geometry was changed to conceal that probe failure. Initial build failed because the prescribed shared node_modules target was empty; local `npm install --no-audit --no-fund` restored the declared tooling. A Git Bash Node shim returned `stdin is not a tty`; native node.exe ran the tests. Optional Codex failed auth before producing edits; Hermes authored and verified everything directly. No credentials were read or modified.

## Reproduce
From this folder: install package dependencies (`npm ci --no-audit --no-fund`), Python numpy/Pillow/playwright and installed Edge; Blender 5.2.1.
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme_source.py`.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.

Use explicit native Node path on Windows if the shell shim fails. `build.py` prefers folder-local dependencies, then the sibling Iceland path. Runtime needs neither. Regeneration overwrites source/export/poster; preserve manual changes separately. ZIP excludes node_modules, backups and caches. Inventory excludes itself, delivery-check and ZIP to avoid recursive hashes; ZIP is read back and every entry verified. Folder-local Git attributes preserve exact bytes.

No mint, keys, chain queries, wallet operations, public hosting, VPS access or production edits. Cosmetic lid motion does not affect custody. The collection direction is 201 equal-scarcity one-of-one designs; this branch is one local art asset awaiting separate collection integration. Three.js MIT license included.
