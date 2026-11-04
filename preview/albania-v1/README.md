# Albania v1 / Stone City

Open **albania-v1.html** directly in Edge/Chrome. Drag or touch-rotate, Open/Close lid, Reset view. All runtime assets are embedded; no server or internet is required. The poster is rendered from the delivered Blender source, not promotional AI art.

## Delivery
- Standalone HTML: **2,130,065 bytes**, strictly below 5,000,000.
- Standalone GLB: **1,011,784 bytes**.
- `albania.blend`: packed editable source; `mechanism.blend`: inherited trimmed mechanical baseline.
- Three generated 256x256 maps in `maps/`, reproducible author/maps/build scripts, actual-source poster and desktop/mobile closed/open/rear/fallback captures.
- `inventory.json`: exact SHA-256 and bytes for the delivered payload. `delivery-check.json`: archive readback, gate summary and exact principal sizes. `albania-v1-source.zip`: source/payload/evidence, no dependencies or backups.

## Theme and visual limits
The sourced brief precedes model creation. Gjirokastra's stone-built houses and grey roof coverings inform a limestone chest with three invented, lid-borne houses. This is **stylized architectural miniaturization**, not a replica of a named house, a geographic city model, craft-authentic stonework or a representation of all Albania.

Actual source and mobile screenshot inspection found three readable houses, seated on the lid, a complete chest silhouette and no obvious detached geometry. The masonry is regular/procedural and can read as tile; pale house walls can read as plaster. Roof courses are broad simplified layers rather than individually laid stone tiles. The source poster retains some sampling noise (24 samples, denoising disabled). Three isolated houses do not reproduce a dense hillside city. No photoreal/reference-equivalence claim. No per-asset human visual approval is claimed; the user waived that gate for this batch.

## Acceptance actually run
- Actual Three GLTFLoader: **78 meshes, 13,332 triangles, six materials**, zero nonfinite vertices and zero degenerate triangles.
- Independent saved-source reopening: **81 sampled poses**, all **43 moving and 35 static meshes**, zero unintended sampled surface collisions. All 27 house meshes travel with the lid; nine roof meshes have upward top normals. House roots meet z1.978. Ten attachment pairs prove rear hinge seating. Only named mating hinge/latch bearings excluded.
- Original articulation: 80-degree latch release first, then 105-degree lid opening; hollow floor ray z0.265. This is sampled surface testing, not continuous collision/containment or mechanical-engineering certification. Co-moving roof tiers deliberately overlap to form a layered roof.
- Saved-source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed maps preserved. Runtime decoded color ranges 53/38 and green-channel roughness range 57.
- Real offline **file:// Edge**, desktop 1440x1080 and **390x844 touch emulation**: native click/tap open/close, pointer/touch rotation, interrupted Reset, reduced motion, no overflow, no external requests or JS errors. Full-open projected geometry max absolute NDC <0.912. Actual corrupt GLB parser failure shows poster; no-JS poster also verified. These run on desktop RTX4060, not physical-phone performance tests.
- Two motion/invalid-asset tests pass. Deliberately detached house negative control fails with `AssertionError: Detached architecture` (exit 1) against the same theme validator; saved source remains unchanged. Corrupt GLB and invalid-asset negatives also exercise actual failure paths. No model-generation/acceptance failure required a geometry fix in this run; the inherited truncated mobile CSS was repaired before the initial build, not presented as a test-first failure.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright, Node, installed Edge. The supplied shared pilot dependency directory lacked esbuild, so pinned `three@0.180.0` and `esbuild@0.25.11` were installed **only in this folder**, not in a sibling preview. Build-time dependencies are excluded; runtime is fully embedded.

From this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run the same Blender command for `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

`setup.py` documents the one-time scaffold and depends on the repository's Japan and Iceland folders. It is **not needed to rebuild** the delivered source; `author.py` is already composed and uses the included mechanism. `geometry.py` is its assembly fragment, not a standalone executable. Rebuilding overwrites generated assets and requires refreshing README size figures and inventory. Three.js MIT license included. No research images/text copied into maps.

Additive art-only branch backup. Not hosted, deployed, minted, signed or stored on-chain. No wallet, blockchain node, keys, chain queries, custody implementation or shared base-kit changes. Collection direction: 201 equally one-of-one designs; accessories deferred. Next step: separate full-collection integration/review card.
