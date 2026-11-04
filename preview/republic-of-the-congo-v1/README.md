# Republic of the Congo v1 — Odzala Bai / Forest & Wetland

Open `republic-of-the-congo-v1.html` directly in Edge/Chrome. All runtime assets are embedded: **2,769,789 bytes HTML**, **1,529,464 bytes GLB**. Drag/touch to rotate; Open/Close and Reset; reduced motion supported. Cosmetic articulation only, not a custody/seal operation. No minting, chain queries, hosting or deployment performed.

## Design and files
Research-backed contract: `design-brief.md` (Republic of the Congo, not DRC). Dark umber grain, brass fittings and low forest-clearing miniature: seven stylized trees, 21 canopy crowns, irregular ochre bank and reflective green water. This is an invented landscape interpretation, not traditional craftsmanship, a geographic model or an assertion of timber provenance. Sources are cited in the brief; no photographic textures are embedded.

`congo.blend` is editable packed Blender source; `congo.glb` is exported geometry/maps. `mechanism.blend` is the trimmed inherited family mechanism. `maps/`, `maps.py`, `author.py`, viewer/build/test scripts allow regeneration. `poster.png/jpg` are actual source renders. Desktop/mobile PNGs are actual offline browser screenshots, not promotional illustrations. `inventory.json` records exact payload bytes/SHA-256; `delivery-check.json` verifies the source ZIP by reading it back.

## Verified
- Build succeeds under the strict 5,000,000-byte HTML limit.
- Actual GLTFLoader: 18,184 triangles, 185 meshes, 12 materials; no nonfinite vertices or degenerate triangles.
- Reopened source: hollow interior floor z=0.2650000155; ten intersecting hinge attachment pairs. **81 poses, 146 moving meshes versus 39 static meshes**, plus latch-versus-lid checks; zero unintended sampled intersections. Only explicitly named mating bearings exempted.
- Source/export maximum nearest-vertex error in both directions: **1.712013073529306e-7**, below 1e-5.
- Contract dimensions, original pivot positions, seam <=0.10 and all 130 ornament meshes attached to lid; relief <=0.65. Stage order remains 80-degree latch release before 105-degree lid opening.
- Desktop 1440x1080 and mobile 390x844 touch emulation over offline file://: rotation, native buttons, open/close, interrupted reset, reduced motion, no overflow, no external requests/errors. Full-open projection max absolute NDC 0.892365. Actual corrupted GLB reaches loader and shows poster fallback; no-JavaScript poster tested separately.
- Theme checks count trees and exposed clearing/water objects, verify parentage and decoded color-map variation. Missing-canopy negative control is rejected. Motion tests include invalid-asset negative controls.

## Real failure and correction
The independent contract gate failed on canopy relief above the frozen 0.65 limit. `initial/relief-limit-failure.txt` preserves it. Two tallest groups were reduced (.55 to .51 and .52 to .50); one intermediate measurement was 0.651793. No acceptance threshold was loosened. Source, export, actual poster and all runtime checks were regenerated afterward. The earlier light-wood render is retained as a rejected palette checkpoint. An optional Codex lane failed authentication before making changes; Hermes authored/recovered and independently tested the delivery.

## Visual limits
Actual-source and final mobile images show a readable box with trees around visible water. Trees are simplified toy-like broadleaf clusters, not a botanical reconstruction or dense rainforest. Mobile water can read as a green clearing; the source render shows reflections more clearly. The stylized pond is ecological inspiration, not proof of a specific wetland type. Hardware is inherited family design; grain remains procedural. No photoreal equivalence, physical-phone performance, continuous collision proof or human art approval is claimed. Per-asset review was waived for collection production.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/Playwright; installed Edge; Node.js with package.json's pinned Three/esbuild versions. Build uses local node_modules or sibling iceland-pilot/node_modules; dependencies are build-time only, excluded from delivery. From this folder:

1. `python maps.py`
2. `blender --background --factory-startup -t 4 --python-exit-code 1 --python author.py`
3. `python build.py`; `node --test tests.mjs`
4. Run Blender with the same flags for `verify_contract.py`, `verify_source.py`, `verify_parity.py`.
5. `python verify_browser.py`; `python verify_theme.py`
6. `python package_delivery.py`

Authoring overwrites generated source/render. `bootstrap.py` is historical mechanism extraction and needs sibling Japan source; the included mechanism avoids that dependency for normal regeneration. Three.js MIT license is included. All changes are confined to this new preview folder. Branch backup only; final collection integration is separate.
