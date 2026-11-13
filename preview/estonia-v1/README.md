# Estonia v1 — Limestone & Bog

Open **estonia-v1.html** directly in Edge/Chrome. Everything needed at runtime is embedded: 3D geometry, portable maps, Three.js and the actual Blender-rendered poster. Drag/touch to rotate, Open/Close lid and Reset view. No server or internet needed. Cosmetic animation only; no mint, wallet, seal operation, deployment or blockchain access.

## Delivery
- HTML: **2,104,643 bytes**, strictly below 5,000,000.
- GLB: **972,956 bytes**; 13,008 triangles, 120 runtime meshes, 7 materials.
- `estonia.blend`: packed editable source; `mechanism.blend`: inherited trimmed family mechanism.
- `maps/`: three generated 256px limestone maps, not scans.
- `poster.png` / `poster.jpg`: actual source render, not promotional AI imagery.
- Desktop/mobile closed/open captures and fallback/no-JS captures: actual offline browser evidence.
- `inventory.json`, source ZIP, and `delivery-check.json`: exact bytes, SHA-256 and ZIP readback. Local Git attributes preserve these bytes through Windows Git checkout.

## Theme and visual limits
Pale limestone, three raised organic peat/moss rings around inset blue-green water, and an eighteen-plank front boardwalk. The pre-model brief cites Estonia's limestone and Viru Bog boardwalk as material/landscape inspiration. This is an invented landscape composition, not a geographic reconstruction, traditional craft object, or assertion that the bog grows directly on exposed limestone.

Actual source/mobile visual inspection found all three pools and the boardwalk readable and the whole box framed. The rims resemble shallow bowls rather than natural excavations; moss is stylized lumpy edging rather than fibrous vegetation. Water has a dark material base but reflects pale teal under studio lighting. The boardwalk is low-contrast and has no realistic wood grain. Limestone grain is subtle and may look like a generic pale surface at mobile size. These are disclosed stylization limits, **not photorealistic equivalence**. Open-view hardware silhouettes show dark hinge gaps; saved-source tests prove the inherited attachment pairs intersect but do not establish manufactured mechanical fit. No per-asset human approval is claimed; the card explicitly waives that review until collection integration.

## Verified
- Independent saved-source reopen, original lid pivot (0,1.32,1.668), three pools, 18 planks, all 63 ornament meshes owned by lid, pool-center rays reaching water, upward rim faces and ornament height 1.973–2.158.
- Source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed portable image maps; runtime decoded color/roughness/normal ranges 32/44/14 (roughness sampled from green).
- **81 sampled poses**, all 79 moving and 38 static source meshes, zero unintended surface intersections; latch against lid included. Only named original mating bearing contacts excluded. Ten hinge attachment pairs and interior floor ray z=.265 pass. This is sampled surface checking, not continuous collision/manufacturing certification or co-moving ornament intersection testing.
- Real GLTFLoader: zero nonfinite vertices and zero degenerate triangles.
- Edge offline `file://`: desktop 1440×1080, mobile 390×844 touch emulation; rotation, native controls, open/close, interrupted reset, reduced-motion snapping, no overflow, no HTTP requests or JS errors. Full-open vertex projection maximum absolute NDC .9091 or less. GPU reported RTX 4060: **not physical-phone performance**.
- Actual corrupted GLB parser rejection presents poster with disabled controls; no-JS poster also verified.
- Motion tests: two tests passed, zero failed; asset validator includes invalid-input rejection.
- `negative-detached-output.txt`: deliberate post-model negative control detached one water object in memory, exited 1 with `AssertionError: Detached ornament rejected`. No invalid source was saved. This demonstrates a capable-of-failing gate, not a previously observed art defect or test-first history.

## Recovery / tooling notes
The retried worker found no Estonia artifacts and created this folder from the prewritten brief. Shared `preview/iceland-pilot/node_modules` existed without the esbuild entrypoint; pinned build dependencies were installed **only here**, not into another preview. The inherited HTML template contained literal truncated CSS; the local adaptation repaired that fragment before first build. No failed asset acceptance occurred during this run; the intentional negative control is preserved separately. Research web search returned citations/excerpts; the direct extraction backend was unavailable. No source photographs or article text became textures.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node with the included pinned package-lock. These are author/test dependencies, not viewer requirements.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender as above on `verify_theme.py`, `verify_parity.py`, `verify_source.py`.
6. `node --test --test-reporter=tap tests.mjs`
7. `python verify_browser.py`; `python verify_extended.py`
8. Optional negative control: Blender `--python verify_theme.py -- --negative` must exit 1.
9. `python package_delivery.py` validates evidence, writes inventory and ZIP, and verifies archive readback.

`setup.py` documents initial adaptation from the sibling Japan pilot and requires that sibling; it is not needed after extraction. All other author/build/check files resolve relative to this folder. Build uses local dependencies first, with inherited sibling fallback. Regeneration overwrites authored outputs; preserve manual edits separately and regenerate evidence/hashes. Source ZIP excludes dependencies, backups and itself.

Three.js 0.180.0 MIT license included. Geometry/maps are script-authored, not hand-sculpted. Family mechanism, viewer and collision-test lineage: Japan Cedar & Moss on base commit ff5d78f; shared vault kit unchanged. Local art only; branch backup is authorized, merging/integration is separate.
