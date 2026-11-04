# Germany / Erzgebirge Woodcraft — v1

Open **germany-v1.html** directly in Edge/Chrome. It is a self-contained offline 3D collectible study: drag/touch to rotate, Open/Close lid, Reset view. No server or network assets required. This is an inner collectible's cosmetic movement, not custody opening. Not minted, hosted, signed, or chain-verified.

## Delivered
- HTML **3,937,345 bytes**, below 5,000,000; GLB **2,345,748 bytes**.
- `germany.blend`: packed editable Blender source; `germany.glb`: standalone geometry/maps.
- `mechanism.blend`: inherited trimmed Japan/Iceland mechanical baseline, not a second Germany design.
- `maps/`: generated honey wood base color, endgrain and roughness. The unused granite swatch retained by the map generator is not present in the final model.
- `poster.png` / `poster.jpg`: actual source render, not AI promotional imagery.
- Desktop/mobile closed/open, rear-open, corrupt-input fallback and no-JS screenshots.
- `design-brief.md`: sourced pre-model contract; `inventory.json`, `delivery-check.json`, source ZIP and reproducible scripts.

## Actual checks
- Blender 5.2.1 independently reopens source: unchanged lid/latch pivot transforms, three tiered turned trees, two houses/two roofs, all 14 vignette meshes on the lid. Root rays hit the oval base at z=2.0400002; roots z=2.03999996. Lid slab dimensions match 3.72 × 2.38 × 0.30 within 1e-5.
- Deliberately detach one tree: ancestry assertion fails; restore its parent: passes. This is a post-implementation negative control, not a claimed test-first run.
- 81 sampled poses cover **42 moving / 99 static meshes**, plus latch-versus-lid checks: zero unintended surface intersections. Only named concentric hinge/latch bearing pairs excluded. Ten hinge attachment pairs touch; hollow floor ray hits z=0.265. Sampled surface tests are not continuous collision proof or engineering certification.
- Saved-source/export nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5, both directions. Three packed maps retained. This is geometric parity, not byte-identical re-export certification.
- Actual Three GLTFLoader: **30,156 triangles, 141 meshes, 6 materials**, zero degenerate/nonfinite vertices. Runtime theme counts, lid ancestry, decoded base-color and green-channel roughness variation pass.
- Edge offline `file://`, desktop 1440×1080 and touch-emulated 390×844 mobile: drag/touch rotation, native Open/Close, interrupted Reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open maximum absolute projected NDC **0.912738** (rounded upward), below 1. Corrupted actual GLB reaches parser and shows poster; no-JS poster separately checked. Reduced-motion rendered samples contain endpoints only.
- Motion unit tests: 2 passed, 0 failed, including invalid-asset rejection.
- Archive inventory and SHA-256 readback verified by `package_delivery.py`; exact-byte Git attributes protect delivered bytes across Windows checkout.

## Honest visual verdict
The source and actual mobile captures show a coherent pale honey-wood box with a wooden toy village and warm brass family fittings. Both houses read clearly. Three turned trees can be counted, but the rear-right tree is partly occluded by its house from the default mobile view. The seam is deliberately dark and quite pronounced, rather than a tightly closed hairline. Fine source-render sampling noise remains; brass and honey wood are close in hue, and the miniature geometry is simplified. No claim of photorealism, exact traditional craft reconstruction, artisan manufacture, real wood species identification, geographic accuracy, or physical-phone performance. Testing used an RTX 4060 desktop GPU with mobile emulation.

No supplied Germany artwork existed; the prewritten research-backed brief is the design reference. This regional inspiration does not claim to represent all Germany. No third-party photographs were embedded.

## Real failure and correction
`initial/extended-probe-failure.txt` preserves a test-harness error: naming the animation callback `probe` while assigning `window.probe=true` replaced the callback with a boolean. Renamed the callback `sampleProgress` while retaining the same endpoint-only assertion; the final extended check passes. This was a harness defect, not a model fix. The expected detached-tree failure is separately in `theme-check.json`.

## Reproduce
Build-time requirements: Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node and pinned Three 0.180.0/esbuild 0.25.11. The shared pilot node_modules directory contained no compiler; pinned dependencies were installed **inside this new directory only**. Runtime is entirely embedded. No dependency upgrades or sibling preview edits.

From this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test --test-reporter=tap tests.mjs`
7. `python verify_browser.py` and `python verify_extended.py`
8. `python package_delivery.py`

`setup.py` records the initial adaptation from the read-only Japan pilot; it requires that sibling and would overwrite adapted scripts, so it is not part of normal regeneration. All other source/build/check scripts resolve their assets within this directory. Authoring overwrites generated source/export/poster; preserve manual edits separately. Packaging excludes dependencies, backups and caches. Three.js MIT license included.

## Scope / next
Branch backup only on `art/germany-v1`; no merge/deploy, no keys, nodes, minting, funds, chain queries or VPS access. All additions are under `preview/germany-v1/`. Per-asset human review was waived; final collection integration and collective visual review are the next stage.
