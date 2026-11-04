# Liechtenstein v1 — Three Sisters Limestone

Open `liechtenstein-v1.html` directly in Edge/Chrome. Entire runtime, GLB, maps and source-rendered poster are embedded: **HTML 2,520,882 bytes; GLB 1,327,900 bytes**. This is a local cosmetic collectible, not minted, hosted or connected to blockchain custody.

## Design and visual verdict
The sourced, pre-model `design-brief.md` interprets Liechtenstein's Three Sisters and northern Rätikon limestone as a wide pale stone box with three distinct rocky summits on a muted alpine-green base. The three peaks are countable in the actual mobile view. No supplied approved illustration exists; this is a written-brief-led original interpretation, not a surveyed mountain replica or traditional craft artifact. All source/maps are procedural, not scans or hand sculpture.

Actual source poster, mobile closed and full-open captures were visually inspected. The complete silhouette fits; no obvious major detached component or broken text was found. The pale stone can read as marble/ceramic rather than specifically limestone, peaks are deliberately angular, and the rectangular green terrain carrier is stylized. Source poster retains visible sampling noise (24 samples, denoising disabled). Small hardware is simplified, and the round medallion is decorative—not a functional lock. At full opening the terrain is naturally behind the lid. No photoreal-equivalence, physical-phone performance, manufactured hardware or continuous collision claim.

## Verification actually run
- `source-check.json`: independently reopened saved Blender source; **81 poses, 20 moving and 39 static meshes**, zero unintended sampled surface intersections. Includes all three peaks and terrain. Only inherited named mating bearing pairs excluded; all 10 hinge attachment pairs intersect as intended. Hollow floor ray z=0.2650000155.
- `parity-check.json`: saved-source/imported-GLB nearest-vertex error **1.712013073529306e-7**, threshold 1e-5; all three maps packed. Geometry correspondence, not byte-identical re-export.
- `theme-check.json`: three distinct peak meshes, grounded height bounds, direct lid ancestry and independently compared original mechanism pivot matrices.
- `extended-check.json`: actual GLTFLoader ancestry and decoded color/roughness variation. Roughness is tested in GREEN. All maps 512×256; ranges 52/85/69. Country text and accessible canvas label checked; no-JavaScript poster works.
- `browser-check.json`: offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844, native controls, pointer/touch rotation, open/close, interrupted reset, reduced-motion endpoints, no horizontal overflow, no external HTTP requests or runtime errors. **14,196 triangles, 59 meshes, 5 materials**, zero nonfinite vertices/degenerate triangles. Full-open maximum absolute projected coordinate **0.912737307912 < 1**. Actual corrupt GLB reaches the parser and triggers poster fallback. RTX 4060 desktop GPU; mobile is emulation only.
- `motion-output.txt`: two tests pass, zero fail, including rejected invalid asset inputs and staged **80° latch then 105° lid** endpoints.
- `theme-negative.txt`: deliberate unsaved removal of peak-one's parent fails with `AssertionError: Peak detached from lid`, exit 1. Normal saved source then passes unchanged. This is a post-implementation negative control, not a discovered production defect or test-first claim. No real art failure/fix occurred in this run.
- `delivery-check.json` and `inventory.json`: explicit required artifact set, exact bytes/SHA-256 and ZIP entry-by-entry readback. Inventory excludes itself and packaging envelopes to avoid circular hashes. Folder-local `* -text` preserves exact Git bytes.

## Files / provenance
`liechtenstein.blend` is editable source; `liechtenstein.glb` portable model. `mechanism.blend` is the included trimmed Japan family mechanism, reused without changing pivots. Shared kit and sibling previews remain untouched. `poster.png`/`poster.jpg` are rendered from the authored source, not AI promotional replacements. Desktop/mobile captures are real offline browser output. `maps/` contains generated textures. `liechtenstein-v1-source.zip` includes source, model, viewer, maps and evidence, not dependencies or backups.

Lineage: Japan pilot mechanism/helpers and viewer from repository base ff5d78f; Iceland motion tests. Some inherited internal helper/object names refer to cedar/granite; actual body/lid material is mapped limestone, and no tree/finger-joint geometry is retained. `setup.py` records the one-time scoped adaptation and requires the sibling Japan pilot; normal regeneration uses only included source files. Three.js 0.180.0 MIT license included; esbuild 0.25.11 build-only. Shared pilot node_modules was empty (compiler absent), so unchanged pinned dependencies were installed only in this new directory, not into a shared checkout.

## Reproduce
Python with numpy/Pillow/Playwright, Blender 5.2.1, Node and installed Edge are build/test dependencies only. From this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender as above with `verify_source.py`, `verify_parity.py`, `verify_theme.py`. Add `-- --negative` to theme test for expected exit 1.
6. `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
7. `python package_delivery.py`.
Regeneration overwrites generated files, so retain manual variants separately and regenerate byte inventories after any change. No wallet, keys, chain node, mint, deployment, production site or external messaging was used. Push is branch backup only; collection integration is a separate card.
