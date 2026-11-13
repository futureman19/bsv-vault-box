# Bulgaria v1 — Rose Valley

Open **bulgaria-v1.html** directly in Edge/Chrome. Complete offline 3D viewer: **4,054,038 bytes**; standalone **bulgaria.glb: 2,455,884 bytes**. Drag/touch rotate, Open/Close, Reset, reduced motion. No runtime network dependencies, minting, hosting or blockchain activity.

## Art and provenance
The prewritten design brief cites Bulgaria's tourism authority and National Geographic on Kazanlak's rose-growing/oil tradition. Three pink floral rosettes sit on a green carrier over dusty wine timber and satin brass. This is script-authored stylized relief, not botanical reconstruction, traditional Bulgarian furniture, scanned material or human hand-carving. Generated grain/stone maps retain inherited cedar filenames for reproducibility, but use the new wine palette. No research photographs are embedded.

Mechanism/interior and viewer lineage: Japan Cedar v1 from repository base ff5d78f; geometry authored afresh around its included trimmed mechanism.blend. Shared art/vault-kit and all other previews remain unchanged. Three 0.180.0 MIT license included; local pinned build dependencies are excluded. The supplied sibling toolchain lacked esbuild, so dependencies were installed only in this directory.

## Verified evidence
- `source-check.json`: independently reopened source; 81 sampled poses, all 83 moving / 99 static meshes, zero unintended surface intersections. Latch-versus-lid included. Only explicit mating bearings exempt; ten connected hinge attachment pairs and hollow floor ray z=0.2650000155. Sampled surface tests, not continuous mechanical certification.
- `parity-check.json`: saved source versus GLB imported through Blender, bidirectional maximum world-vertex difference 1.712013073529306e-7, below 1e-5.
- `theme-check.json`: three centers, 36 petals, twelve leaves, lid ownership and bounded height. Deliberately detached center correctly failed with `ornament detached from lid`; restored without saving the mutation. This is a post-implementation negative control, not a claimed TDD failure/fix.
- `motion-output.txt`: two Node tests pass, including invalid/missing/empty asset negative cases and staged 80-degree/105-degree endpoints.
- `browser-check.json`: actual GLTFLoader finite and nondegenerate geometry; desktop 1440×1080 and mobile 390×844 touch emulation over offline file://. Native controls, drag, interrupted reset, reduced motion, open silhouette projection, no overflow, no external requests/errors. Actual corrupted embedded GLB reaches parser and displays fallback. No-JS poster checked.
- `material-check.json`: actual loader-decoded color and green-channel roughness variation; compact maps, country copy and canvas aria-label.
- `delivery-check.json` / `inventory.json`: exact bytes/SHA-256, explicit required artifacts and ZIP entries read back. Delivery checker can fail on absent files, collision records, overbudget HTML or byte changes.

## Visual verdict and limits
Actual source poster and mobile browser screenshot inspected. All three roses and complete closed silhouette are visible; primary controls are readable. Wine timber reads lighter/dustier pink under source lighting; lid can look like painted lacquer. Rounded petals are intentionally simplified rather than rose spirals; green carrier makes leaves less distinct. Stone feet and family joinery/hardware are stylized extrapolations. The green reveal is decorative, not a real seal. Source render retains mild sampling noise (24 samples, denoising disabled). No photorealistic equivalence, user art approval, physical-phone performance or production/custody claim.

## Rebuild
Python with Pillow/numpy/Playwright; Blender 5.2.1; installed Edge; Node and package-lock dependencies (`npm ci` here). Build/test dependencies only; delivered HTML needs no installation.
1. `python maps.py`
2. `blender -b --factory-startup --python-exit-code 1 --python author.py`
3. Same Blender command for `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
4. `node --test --test-reporter=tap tests.mjs`
5. `python build.py`, `python verify_browser.py`, `python verify_materials.py`
6. `python package_delivery.py`

`adapt.py` records the one-time adaptation from the Japan scripts, **do not rerun it** on already-adapted sources. Regeneration overwrites generated assets; preserve manual source edits separately. `poster.png` is rendered from the exported source, not AI promotional art. Source archive excludes node_modules, backups and caches. Folder-scoped Git attributes preserve inventoried bytes on Windows.

Autonomous v1 art delivery under the user's no-per-asset-review directive. Branch backup only; collection integration is a separate card.
