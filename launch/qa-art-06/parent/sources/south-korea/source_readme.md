# South Korea v1 / Lacquer & Pearl

Open **south-korea-v1.html** directly in Edge/Chrome. Complete offline HTML **2,156,999 bytes**, GLB **1,004,244 bytes**. Rotate, open/close, reset; reduced-motion supported. Cosmetic inner-collectible preview only, not custody, minting or an on-chain seal operation.

## Design and delivered source
Research-backed Korean lacquer/pearl craft interpretation; see the pre-model `design-brief.md`. Five twelve-petal lid chrysanthemums with brass scrolling stem, twelve body/side rosettes, pearl border, dark lacquer shell and family brass fittings. Invented simplified patterns, no copied museum imagery, scans or animal materials. Script-authored Blender geometry, not hand-crafted traditional inlay.

`south-korea.blend` is editable packed source; `mechanism.blend` is the inherited trimmed Japan mechanism. `south-korea.glb` contains portable maps. `maps.py`, `helpers.py`, `author.py` reproduce the asset. Poster PNG/JPEG are actual source renders, not promotional AI art. Desktop/mobile closed/open and fallback screenshots are actual offline Edge captures.

## Verified
- Source independently reopened: hollow floor ray z 0.265; ten hinge attachment pairs; 81 motion samples covering all 31 moving and 50 static meshes, zero unintended surface intersections. Named coaxial bearing contacts alone excluded. Sampled surface tests, not continuous collision/manufacturing certification.
- Same inherited pivots and 80-degree latch release before 105-degree lid opening. Runtime motion tested at 81 progress values; missing-pivot negative control rejected.
- Source/export bidirectional vertex error 1.712013073529306e-7 (<1e-5). Three packed authored 256px maps; actual loader verifies finite, nondegenerate triangles. Actual roughness variation read from green channel.
- Theme: five lid flowers, twelve petals each, twelve body/side flowers, lid ancestry and bounded relief height. Deliberately detached ornament rejected by unchanged acceptance check; this is a post-implementation negative control, not a historical test-first failure.
- Offline file:// desktop and 390x844 touch-emulated mobile: native controls, drag/touch rotation, full-open framing, close, interrupted reset and reduced motion; no external HTTP requests, unhandled errors or horizontal overflow. Actual corrupt GLB parser input and JavaScript-disabled poster fallback tested. This is desktop GPU emulation, not phone hardware performance.
- Exact SHA-256 inventory, explicit required deliverables, ZIP member/hash readback and staged Git byte checks. Inventory excludes itself and packaging envelopes to avoid recursion.

## Honest visual limits and adjustments
Actual source/mobile images were inspected. Floral identity and front hardware read clearly; lid motifs are foreshortened at the inherited mobile camera. Finish reads satin blue-black rather than perfectly polished lacquer. Petals are raised angular appliques, not flush artisan inlay or physically accurate wavelength-dependent nacre. Source poster retains modest Cycles sampling noise. Hidden rear/interior are family extrapolations. No photoreal-equivalence claim or human art approval.

The initial source render was checked before adding the specified medallion/side ring; final source, poster, GLB and all gates were regenerated afterward. No acceptance failure occurred in that bounded correction. The supplied shared compiler directory was absent/empty, so unchanged pinned dependencies were installed only in this folder; no sibling toolchain was modified. An inherited accessibility label was corrected before final delivery.

## Reproduce
Requirements: Blender 5.2.1, Python with Pillow/numpy/Playwright and installed Edge, Node with `npm ci --ignore-scripts --no-audit --no-fund` here. Dependencies are build-only and excluded from delivery.
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender similarly on `verify_theme.py`, `verify_parity.py`, `verify_source.py`.
4. `node tests.mjs`; `python build.py`
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Scripts resolve local files; build optionally falls back to the sibling pilot toolchain if local node_modules is absent. Regeneration overwrites generated source/render outputs. Three.js MIT license included. No production/public site changes, deployment, keys, node startup, chain queries, minting or external messaging. Branch backup only; integration belongs to the final collection card. Planned collection: 201 equally one-of-one designs; storage availability and on-chain issuance remain unimplemented here.
