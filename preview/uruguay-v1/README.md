# Uruguay / Quebrada & Grassland — autonomous v1

Open **uruguay-v1.html** in Edge/Chrome. Everything needed at runtime is embedded: the actual model, maps, Three.js runtime and actual-source fallback poster. Drag/touch to rotate, open/close the lid, or reset. This is an art preview, not a custody operation, minted asset, hosted page or human-approved artwork.

## Delivery
- HTML: **2,266,525 bytes**, strictly below 5,000,000.
- GLB: **1,116,544 bytes**.
- `uruguay.blend`: named editable Blender source, packed maps; `mechanism.blend`: inherited mechanical baseline.
- `maps/`: three deterministic procedural 256px maps. Not scans or copied photography.
- `poster.png`/`poster.jpg`: render of the actual saved source, not AI promotional art.
- Desktop/mobile closed/open, rear-open, fallback/no-JS PNGs: real offline browser captures.
- `inventory.json`, source ZIP and `delivery-check.json`: exact-byte identities and archive readback. ZIP includes standalone GLB, source, viewer, maps, scripts and evidence; dependency installs and backup files excluded.

## What passed
Actual Three GLTFLoader: **17,116 triangles, 78 runtime meshes, 8 materials**, zero nonfinite vertices and zero degenerate triangles. Color maps vary by 60 and 59 byte values; roughness varies by 60 in glTF's green channel.

Saved-source reopening: hollow floor ray z=0.2650000155; ten actual intersecting attachment pairs connecting hinge mounts/body and leaves/lid. **81 motion samples, 37 moving and 39 static meshes, no unintended intersections**. All terrain and vegetation included. Only moving hinge leaf/fixed barrel and latch knuckle/bridge/pin bearing contacts excluded. Full per-pose data in `motion-samples.json`; sampled surface tests are not continuous collision/manufacturing certification.

Inherited lid/latch pivot matrices match exactly. Staged latch releases 80° before lid opens 105°. Twenty-one landscape source meshes belong to the lid: two multi-material banks, one continuous stream and eighteen scrub forms. Thirty-one vertical channel-center rays reach unobstructed water. Terrain reaches z=2.3397565 and its outside edges meet the lid. Negative control genuinely detaches an ornament and rejects its ownership; invalid runtime-asset controls reject missing pivots, zero triangles and NaN bounds.

Independent saved-source/export bidirectional nearest-vertex error **1.712013073529306e-7**, under 1e-5. Three images remain packed. This is vertex geometry parity, not a claim that Blender and browser lighting are identical.

Offline file:// Edge, desktop 1440x1080 and 390x844 touch emulation: native open/close, mouse/touch rotation, interrupted reset, reduced-motion snapping, full-open framing (maximum absolute NDC 0.912804), no overflow, no external HTTP requests and no unhandled runtime errors. Invalid embedded GLB reaches the actual parser and produces a disabled-controls poster fallback. No-JS poster also passed. RTX 4060 desktop GPU; **no physical-phone performance claim**.

## Actual failures and fixes
- Initial terrain outside edges stopped at z2.00 above lid top 1.978. The independent attachment assertion failed; edges now descend to 1.974. The failed output is preserved in `initial/terrain-attachment-failure.txt`.
- Runtime theme test initially counted only named meshes and missed the two bank groups: GLTFLoader splits multi-material meshes into children. The preserved failing probe has 19 named meshes. Corrected oracle checks named group ancestry before mesh-only texture checks; all 21 landscape nodes now pass. No model or count threshold was weakened.
- The task-prescribed shared node_modules path was empty, causing MODULE_NOT_FOUND. Installed pinned Three/esbuild locally in this new directory; no runtime network dependency. `npm ci` is the portable rebuild route.
- Optional Codex input lane failed HTTP 401 before editing. Hermes authored, reviewed and ran all successful checks directly; no Codex patch accepted. No credential store was modified.

## Visual verdict and limits
Actual desktop and mobile images show readable rolling green banks around a winding blue-green stream, within the complete keepsake-box silhouette. The relief reads as a **shallow stream valley rather than a dramatic deep gorge**; it is not a scale topographic model. Uruguay identity depends on the researched written context, not an exclusive landform. Body texture can look dappled/concrete-like or woven, rather than natural stone. Scrub is simplified, water flat/opaque, terrain boundary visibly decorative, feet faceted, and the green seam prominent. Full-open front view hides most top scenery behind the upright lid; rear-open capture shows its continued attachment. Hinges pass physical contact tests but are visually small and can look separated in mobile front view. No photoreal equivalence, ecological precision, mechanical engineering or final human art approval claimed.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node.js and pinned npm dependencies. Commands from this directory:

```text
npm ci --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme_source.py
node tests.mjs
python verify_browser.py
python verify_theme.py
python package_delivery.py
```

Normal authoring is self-contained via included mechanism.blend; no other pilot needed. The optional build dependency fallback looks in sibling Iceland only if local node_modules is missing. Regeneration overwrites source/art/render; preserve manual edits separately. Refresh README measurements and inventory after changes. Three.js MIT license included. Geometry/mechanism/viewer lineage: Japan pilot on base ff5d78f, itself derived from Iceland. Researched facts and artistic deviations are in the prewritten `design-brief.md`.

## Scope
All delivery changes are additive under `preview/uruguay-v1/`. Shared art kit and older previews remain unchanged. Branch backup only; no integration merge, production deployment, blockchain node, keys, mint, transaction, VPS access or external messaging. The separate collection integration card owns merging and final full-set review.
