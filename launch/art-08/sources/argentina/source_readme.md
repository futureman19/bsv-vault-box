# Argentina v1 — Quebrada Chromatic Ridge

Open `argentina-v1.html` directly in Edge/Chrome: the real 3D collectible, runtime, procedural maps and actual source-render poster are embedded. Drag/touch to rotate, Open/Close lid, Reset; reduced-motion preference supported. **HTML 2,906,138 bytes; GLB 1,608,988 bytes.** Local art only: not minted, hosted, signed or stored on-chain. No blockchain services, keys, production directories or shared base kit changed.

## Design and visual result
The research-backed `design-brief.md` was written before authoring. This is a regional Jujuy/Quebrada interpretation: coloured mineral stone body and a real multi-peak folded-strata lid relief, satin brass hardware, dark mineral seam and irregular stone feet. It is procedurally Blender-authored, not hand sculpted, scanned or accurately reconstructed terrain. No source photographs or traditional/sacred designs are copied.

Actual source poster, desktop/mobile closed views and open view were visually inspected. The ridge is visible at mobile size, full open silhouette fits, interior reads hollow and no obvious floating pieces were seen. **Visual limits:** pale pastel mineral palette; rounded peaks and repeated jagged colour bands can read decorative rather than eroded geology; broad body bands differ from the finer terrain bands. Mountain-to-lid boundary is an applied relief, not a recovered geological continuity. Large inherited clasp, dark seam and pebble feet retain the family style. Render is deliberately stylized, not photorealistic or reference-equivalent. Source poster has some sampling grain (24 samples, no denoising).

## Verified evidence
- `source-check.json`: independent saved-source reopen; 81 poses, all 17 moving and 39 static meshes, zero unintended sampled surface intersections. Latch versus lid included. Only named concentric bearing contacts excluded. Hollow floor ray z=0.2650000155; ten hinge attachment pairs in `hinge-attachment-check.json`. Sampled surface intersections are not continuous/mechanical certification or volumetric containment proof.
- `parity-check.json`: evaluated saved-source versus separately imported export, both directed nearest-vertex errors 1.712013073529306e-7, below 1e-5. Three packed procedural maps.
- `theme-check.json`: exact baseline pivot matrices; ridge owned by lid; ridge bounds z=1.9780000448–2.6380648613, six mineral materials. Detaching ridge intentionally causes ownership assertion failure, then restoration passes. This negative control is post-implementation regression evidence, not test-first TDD.
- `motion-log.txt`: two inherited fail-capable motion/asset-contract tests pass; endpoints/clamping and staged 80-degree latch then 105-degree lid.
- `browser-check.json`: actual Three GLTFLoader, 16,766 triangles, 61 runtime meshes, ten materials; zero degenerate or nonfinite geometry. Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: native controls, drag/touch rotation, open/close, interrupted Reset, reduced motion, no overflow, zero external HTTP requests or unexpected errors. Open projection max absolute NDC 0.892365. Actual corrupt GLB parser fallback tested.
- `extended-check.json`: no-JS poster, poster pixel presence, viewer country-copy regression, actual loaded lid ancestry, decoded base colour ranges 141/102 and roughness GREEN-channel range 63; maps 512 or 256 px.
- `inventory.json` / `delivery-check.json`: exact bytes and SHA-256, explicit required files, source ZIP readback hashes. Self-referential envelopes/logs excluded from inventory. Local `.gitattributes` preserves exact bytes on Windows.

Browser uses desktop RTX 4060; mobile emulation is not physical-phone or performance evidence. Passing geometry/tests is separate from visual realism.

## Genuine failures and fixes
`initial/author-failed.txt` preserves Blender failure: fractional power of a tiny negative sine at a boundary yielded complex coordinates. Clamped the nonnegative ridge envelope before exponentiation; no acceptance threshold relaxed. Simplified coplanar underside tessellation to four corners before export. Initial preparation also found tests lived in Iceland rather than Japan, and the specified sibling dependency directory was empty; copied the existing motion tests and installed pinned local build dependencies instead. Bash's Node shim required the native Node executable for motion testing. These are tooling corrections, not fabricated successful runs.

## Files / reproduction
Editable `argentina.blend`, standalone `argentina.glb`, embedded HTML, actual `poster.png`/JPEG, screenshots, `maps/`, generator and independent gates are included in `argentina-v1-source.zip`. `mechanism.blend` is the inherited trimmed Japan mechanism; Three runtime is MIT (`THREE-LICENSE.txt`). No AI promotional image is used.

Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, Node and installed Edge. From this folder:

1. `npm ci --no-audit --no-fund` (local dependencies; not required by delivered HTML).
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python verify_acceptance.py`; `python package_delivery.py`.

Regeneration overwrites output; preserve manual edits separately. Build prefers local dependencies and only falls back to sibling Iceland dependencies. No other sibling files are needed by authoring or verification. Dependencies/cache/Blender backups are excluded. Delivery is this folder and its ZIP, not an external hosted copy. Branch backup only; integration and collection-wide review belong to the existing final integration card.
