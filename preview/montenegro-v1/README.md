# Montenegro v1 — Durmitor & Tara

Open **montenegro-v1.html** directly in Edge/Chrome. All runtime code, geometry, maps and the actual-source poster are embedded. No server or network needed. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion snaps to endpoints.

## Deliverables
- Standalone HTML: **2,662,825 bytes**, strictly below 5,000,000.
- `montenegro.glb`: **1,394,088 bytes**; `montenegro.blend`: editable packed Blender source.
- `mechanism.blend`: included inherited articulation/hollow interior, from the repository Japan pilot. New stone shell, terrain, maps and vegetation authored for this country.
- `poster.png` / `poster.jpg`: actual Blender source render, not AI promotional imagery.
- Desktop/mobile closed/open, rear-open, corrupt-model and no-JS screenshots; reproducible scripts and JSON acceptance evidence.
- `montenegro-v1-source.zip`, `inventory.json`, `delivery-check.json`: exact SHA-256 payload inventory and ZIP readback proof. Dependencies/caches/backups excluded.

## Verified
- Actual Three GLTFLoader: **80 meshes, 16,416 triangles, five materials**, zero nonfinite vertices or degenerate triangles.
- Independently reopened saved source: hollow interior floor z=0.2650000155; ten intersecting hinge attachment pairs; unchanged lid/latch pivot matrices.
- **81 sampled opening poses**, every one of 41 moving meshes against 39 static meshes and latch meshes against lid meshes: zero unintended intersections. Only original mating hinge and latch bearings exempt. This is sampled surface intersection evidence, not continuous collision detection or manufacturing certification.
- Bidirectional source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed source maps; loaded color/roughness variation and intended palette independently checked (roughness GREEN channel).
- All **25** terrain/water/forest meshes have lid ancestry. The water mesh is topologically connected; **61** downward centreline rays hit the unobstructed river. A deliberate detached-ornament negative control fails ownership validation. Invalid geometry metadata and genuinely corrupted GLB input are rejected.
- Offline **file://** Edge desktop 1440x1080 and touch-emulated mobile 390x844: native button open/close, mouse/touch drag, interrupted reset, reduced-motion endpoints, no overflow, zero external HTTP requests and zero unexpected errors. Full-open maximum absolute projected NDC 0.915648. Real parser failure shows poster and disables controls; no-JS poster tested separately.
- Tests ran on a desktop RTX 4060; **not physical-phone performance testing**.

## Visual decision and limits
The brief is the primary art reference, researched before modeling; there was no supplied Montenegro illustration. Pale karst, green seam, brass hardware and turquoise water are recognizable as a stylized landscape collectible. It is not a geographic Tara model, traditional craft replica, scan, photoreal product or human-approved final design.

One bounded correction reduced the foreground bank and widened water to expose the river at mobile size; retained initial render and explanation are in `initial/`. This deliberately revises the brief's foreground-height/water-width targets. Final mobile inspection confirms readable river and complete framing. The water remains an opaque turquoise inlay, not simulated water; vegetation is regular and bead-like, stone shading is procedural/repeating, and terrain is visibly faceted. The river reads more as a ribbon than a deep gorge. Source render has sampling grain. These limitations are not hidden by technical PASS.

The initial front-open screenshot made hinges appear separated because the attachments are partly occluded. Rear-open inspection shows brass connection consistent with the independent ten-pair attachment proof; no definite floating assembly found. This is not a manufacturability claim. Terrain naturally hides behind the open lid in front view.

Initial build failed because the requested shared node_modules directory was empty. Pinned dependencies were installed only in this new folder, not in shared previews. No art checks or payload limits were waived. Negative controls are post-implementation acceptance tests, not a test-first claim.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/playwright; installed Edge; Node/npm. From this folder:

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Scripts resolve local paths; build may use installed sibling dependencies if local dependencies are absent. No sibling source needed for regeneration. Generation overwrites source/render/export; save manual edits separately. Generated artifacts are byte-preserved with folder-scoped Git attributes.

## Rights and safety
Original procedural geometry/maps, no third-party photos embedded; UNESCO/IUCN citations in design-brief.md are factual inspiration. Mechanism/viewer lineage: existing Japan pilot at base ff5d78f1e0d486af5c882c184fc08049996ebdc8. Three.js MIT license included. One of the planned 201 equally one-of-one designs; not minted, hosted, signed, deployed, on-chain stored, custody-tested or production certified. Cosmetic lid motion does not open any on-chain seal. No blockchain tools, keys, wallets, VPS, minting or broadcasts accessed. Only this new preview directory is committed; branch backup only, no merge. Collection integration/review is a separate dependent card.
