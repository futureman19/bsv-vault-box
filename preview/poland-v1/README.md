# Poland / Cobalt & Cream — v1

Open **poland-v1.html** directly in Edge/Chrome. Entire offline viewer: **2,383,576 bytes**; GLB: **1,182,436 bytes**. All runtime code, maps, mesh and actual-source poster are embedded. Drag/touch rotate, Open/Close lid, Reset and reduced motion are supported.

## Design and scope
Research-backed Bolesławiec-inspired cream/cobalt ceramic with original procedural eye motifs and an eight-petal raised lid rosette. The frozen design brief predates modeling. This is digitally authored geometry, not handmade Polish pottery, a workshop pattern reproduction, a scan or photorealism. No authentic makers' marks. Regional inspiration is not a claim to represent all Poland.

Local inner-collectible artwork only: no mint, signing, wallet, blockchain node, chain call, deployment or custody verification. Cosmetic opening has no transaction meaning. Collection direction is 201 equally one-of-one designs.

## Verified on final candidate
- Actual Three GLTFLoader: 65 meshes, 16,920 triangles, four materials, no nonfinite vertices or degenerate triangles.
- Independent saved-source reopening: 26 moving and 39 static meshes, **81 motion samples with zero unintended surface intersections**, ten explicit hinge attachment pairs and hollow floor ray z=0.2650000155. All new ornaments are directly lid-parented. Only named mating bearings exempt; this is sampled surface evidence, not continuous collision/manufacturing certification.
- Source/export maximum nearest-vertex error **1.712013073529306e-7** units (<1e-5). Two packed source maps; loader decodes color range 211 and roughness-green range 26.
- Original mechanism pivot matrices exactly preserved; staged latch release 80 degrees then lid 105 degrees. Eight petals, five front motif rows, seam 0.070 units and 3.72-wide front verified. Actual body skin height is 1.46; total closed lid/foot envelope is about 2.2 units, preserving the family mechanism rather than a literal 1.9-high skin (brief's approximate body-height target).
- Offline file:// Edge: desktop 1440x1080 and 390x844 mobile/touch emulation; native open/close, rotation, interrupted reset and reduced motion; no HTTP requests, console/runtime errors or horizontal overflow. Full-open projection max absolute NDC 0.892365. Real corrupt-GLB parser input shows fallback, and no-JS poster works. RTX 4060 host, **not physical-phone performance**.
- Negative controls reject detached petal ancestry, missing lid, empty/nonfinite geometry; raw corrupt input exercises real parser rejection. SHA-256 inventory and ZIP contents verified on readback. Folder-local Git attributes preserve exact bytes.

## Visual verdict and limitations
Actual closed mobile and open desktop screenshots were inspected. Cream/cobalt repeat, blue flower and brass fittings read clearly; no model clipping. Surface pattern remains regular/digital and glaze is stylized. Hardware is simplified; rear leaves and released latch connections are visually understated from the open hero angle despite passing geometric attachment checks. Lid ornament naturally faces away in the front open view. No external concept-equivalence or photoreal claim. The narrow cobalt seam is decorative, not a physical watertight seal.

## Failures and fixes
Optional Codex lane exited with authentication 401 before any implementation; Hermes authored and checked the asset directly. `codex-output.txt` preserves that failure (no credential files accessed). First build failed because the expected shared node_modules directory was empty; `initial/build-failed.txt` preserves it. Installed the same pinned Three 0.180.0 / esbuild 0.25.11 dependencies locally, no upgrades, then build and all gates passed. No collision or geometry failure occurred. Negative controls are postimplementation regression tests, not a claim of test-first development.

## Files and reproduction
`poland.blend`, `poland.glb`, generated `maps/`, `author.py`, `maps.py`; `mechanism.blend` copied from repository Japan pilot and inherited mechanical/viewer/test helpers. `poster.png` and JPEG are actual Cycles renders (900x800, 32 samples, two threads, no denoising); screenshots are actual browser captures. Three MIT license included. Research URLs in brief, no third-party photos embedded.

Build requirements: Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node and pinned npm dependencies. Run from this directory:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_checks.py` (Blender path configurable via BLENDER)
5. `python package_delivery.py`

Authoring overwrites generated files; keep manual edits separately. `setup.py` records initial scaffold creation and is **not** a rebuild step: it requires the sibling Japan pilot and would overwrite later viewer/template fixes. Normal author/build/check scripts are folder-local except fallback toolchain lookup. Dependencies and .blend1 backups are excluded from source ZIP. Inventory excludes itself, delivery-check and ZIP to avoid circular hashes; delivery-check identifies the archive separately. Branch backup only; integration is handled by the collection integration card.
