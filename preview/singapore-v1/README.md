# Singapore v1 — Orchid & Celadon

Open **singapore-v1.html** directly in Edge/Chrome. Entire offline 3D viewer, model, maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion honored. Cosmetic inner collectible only: no chain, wallet, seal or custody state changes. Not minted, deployed or hosted.

## Delivery
- Standalone HTML: **2,224,118 bytes** (<5,000,000).
- Standalone GLB: **1,086,740 bytes**.
- `singapore.blend`: packed editable Blender source; `mechanism.blend`: included inherited family mechanics.
- `maps/`: generated 256px celadon color, roughness and normal maps; not scans.
- `poster.png` / `poster.jpg`: actual source render, no AI illustration.
- Desktop/mobile closed/open screenshots, corrupt-input and no-JS fallback captures; JSON checks, exact inventory and reproducible source ZIP.

## Design and provenance
`design-brief.md` was written before modeling and cites NParks for Singapore’s national orchid and differentiated flower anatomy. Three shallow enamel flower appliqués have pink upper petals, ivory lower sepals, purple lips and amber throats; stems and leaves travel with the lid. Celadon ceramic panels, jade-colored seam/feet and brass are invented complementary design choices, not asserted traditional Singapore craft. No third-party photographs or textures are embedded. Reused Japan pilot mechanics/viewer/test lineage from base commit ff5d78f; original pivot matrices independently compared to the included trimmed mechanism. Three.js MIT license included. This is script-authored art, not artisan work or botanical reconstruction.

## Executed verification
- Build succeeded: `HTML_BYTES 2224118 GLB_BYTES 1086740`.
- Actual offline Edge GLTFLoader: 89 meshes, 20,178 triangles, 9 materials; zero nonfinite vertices or degenerate triangles.
- Independent saved-source reopen: 50 moving and 39 static meshes, **81 motion samples**, zero unintended surface intersections, hollow floor ray z=0.26500001549720764. Hinge mount/leaf attachment pairs checked. Only named family mating bearings exempted. This is sampled surface-intersection evidence, not continuous or mechanical certification.
- Source/export nearest-vertex parity max error **1.712013073529306e-7**, below 1e-5; three packed maps.
- Theme: 15 lobes across three flowers; differentiated materials; original pivot matrices; all floral ornaments under lid; bounded relief height. Deliberately detaching one lobe in memory causes the real assertion `Detached ornament rejected` (theme-negative.txt). This is a postimplementation negative control, not a discovered asset defect or test-first claim. File on disk is never modified by the negative control.
- Motion module: 81 staged samples, endpoint/clamp and invalid-asset rejection checks.
- Desktop 1440×1080 and mobile 390×844 touch emulation under offline `file://`: native open/close, rotation, interrupted Reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open maximum absolute projected coordinate 0.93754 (<1).
- Real corrupted GLB reaches the parser and activates the poster; JavaScript-disabled poster verified separately. Portable map channels decoded (roughness GREEN), nonzero ranges; poster nonblack pixels checked.
- Delivery inventory records exact bytes/SHA-256 and ZIP readback. Local `.gitattributes` preserves exact bytes through Git.

## Honest visual limits
Source and actual mobile closed/open renders were inspected. Whole silhouette fits, celadon/pink/ivory/brass palette reads clearly and no grossly broken or detached component is visible. The orchid is stylized, not botanically exact; at mobile scale it can read as generic blossoms. Broad smooth lobes, simplified leaves and repetitive arrangement remain deliberate v1 simplifications. The dark recessed seam and stepped rim can make the closed lid look slightly lifted. Clasp backing/corner joints are conspicuous; hardware is chunky. Source poster has visible sampling noise (24 samples, no denoising). Hinge attachment is numerically verified but not visually resolvable at tiny mobile size. No photoreal-equivalence, physical-phone FPS, manufacturing fitness or human art approval is claimed. Per-asset human review was explicitly waived for this collection batch.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with pinned package.json/lockfile. Shared prescribed pilot dependency folder was empty (compiler absent); pinned dependencies were installed only in this new folder. No other preview or shared kit changed. node_modules is not delivered. Authoring/build overwrites generated outputs; preserve manual edits separately.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`. Expected-failing negative: add `-- --negative` to the theme invocation.
5. `node test_motion.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py` (local ZIP/inventory; no external publishing).

Next: integrate the backed-up art branch through the separate final collection card; do not merge or deploy this pilot independently.
