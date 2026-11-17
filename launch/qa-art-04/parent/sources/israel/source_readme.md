# Israel v1 / Negev Erosion

Open **israel-v1.html** directly in Edge/Chrome. Drag or touch to rotate; Open/Close lid and Reset view are functional. Everything needed at runtime is embedded. No server, wallet, internet connection or blockchain operation is involved.

## Delivered
- Standalone offline HTML: **2,904,746 bytes**, strictly below 5,000,000.
- Exported `israel.glb`: **1,650,920 bytes**.
- `israel.blend`: editable, packed Blender source; `mechanism.blend`: included trimmed mechanical baseline from the Japan pilot.
- Three independently generated 512x512 limestone maps and reproducible author/build/check scripts.
- `poster.png` and `poster.jpg`: actual source render, not AI promotional artwork.
- Desktop/mobile closed/open captures, rear-open and real corrupted-input/no-JS fallback captures.
- `inventory.json`, `delivery-check.json`, acceptance JSONs, raw logs and source ZIP.

## Theme and visual verdict
Research-backed Negev erosion interpretation: pale limestone body, ochre mineral beds, irregular elongated basin on the lid, satin brass hardware and umber seam. Sources and the measurable pre-model contract are in `design-brief.md`. All artwork/maps are procedurally authored; no source photographs, scans or sacred symbols are used. It is not a survey of Makhtesh Ramon or a statement that one landscape represents all of Israel.

Actual source and browser images were inspected. The object is coherent and the sculpted depression is readable in the source render. Deliberate limits: coarse faceted relief, regular procedural sediment bands, low-detail stone feet and clean hardware. The basin reads as a raised landscape attached to the lid, not a cavity cut through the lid itself; depth is less conspicuous at mobile scale. At full opening the basin faces away from the front camera; rear-open capture shows it. The front-open hinge clearance can look suspended despite the tested attachment bridges and bearing alignment. No photorealism, historical craftsmanship or reference-image equivalence is claimed.

## Verified evidence
- `source-check.json`: independently reopened saved source, genuine hollow interior floor ray z=0.2650000155; **81 motion samples**, **17 moving meshes and 39 static meshes**, zero unintended surface intersections. All new terrain is included. Latch-vs-lid is checked separately. Only named mating hinge leaf/barrel and latch knuckle/bridge/pin bearings are exempt. Ten hinge attachment pairs overlap in `hinge-attachment-check.json`. Sampled surface checks are not continuous collision or manufacturing certification.
- `contract-check.json`: original mechanism pivots preserved exactly; lid 3.72 x 2.38 x .30; basin center floor z=2.02, maximum rim z=2.458031, relief 0.438031; all three source images packed; exact base/normal PNG identity in GLB. Exported roughness is packed in the standard ORM green channel.
- `parity-check.json`: both directions of source/export nearest-vertex comparison pass within 1e-5; maximum error **1.712013073529306e-7** units. This proves evaluated world geometry, not byte-identical Blender re-export or every shader parameter.
- `browser-check.json`: real Three GLTFLoader, **14,426 triangles**, **58 meshes**, **6 materials**, zero nonfinite vertices or degenerate triangles. Edge offline file:// desktop 1440x1080 and 390x844 touch emulation: native controls, rotation/touch drag, open/close, interrupted reset, reduced motion, no overflow, no external HTTP requests or runtime errors. Full-open maximum projected NDC **0.892365**, inside viewport.
- `theme-check.json`: three loaded material primitives under the terrain parent, lid ancestry, relief/aspect/seating, actual decoded color/roughness/normal variation (ranges 42/37/17), no cedar/tree objects, no-JS poster. Temporarily detaching the real loaded terrain is correctly rejected by the parent gate, then restored.
- Actual corrupted GLB bytes reach GLTFLoader; parser error is caught, poster appears and controls disable. This expected negative-control error is not counted as a successful-render runtime error.
- `tests.mjs`: staged 80-degree latch then 105-degree lid, clamped endpoints, finite poses, invalid-asset rejection.
- `delivery-check.json`: strict bytes, required file set, exact SHA-256 inventory, ZIP readback, and offline extracted delivery HTML load/controls.

Browser tests use Edge on NVIDIA RTX 4060. Mobile is viewport/touch **emulation**, not physical-phone performance. No FPS, worldwide browser support, geometry watertightness or cryptographic custody claim.

## Real failures and fixes
1. `initial/reduced-motion-failure.txt`: inherited viewer updated reduced-motion pose only in requestAnimationFrame; a 70ms assertion failed during the initial run. Open and Reset now update the actual pose and public state immediately. The unchanged browser test passes after rebuilding. This is an interaction fix, not a waived timing gate.
2. `initial/multi-material-ancestry-failure.txt`: initial theme harness expected Terrain to be a mesh. GLTFLoader correctly splits the multi-material mesh into primitive children under a Terrain group. The harness now follows actual ancestry and reads roughness from glTF's green channel. Geometry/size/collision gates were not relaxed.

## Rebuild
Dependencies: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js with Three 0.180.0 and esbuild 0.25.11. Run from this folder:

```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
node --test tests.mjs
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_contract.py
python verify_browser.py
python verify_theme.py
python package_delivery.py
```

`build.py` finds local node_modules or the sibling iceland-pilot installation. The worktree uses the explicitly authorized link to that existing toolchain. Source archives exclude dependencies. Install package.json dependencies locally for standalone rebuilding. `setup.py` documents initial reuse from the sibling Japan pilot and is **not required for rebuilding** the included complete `author.py`; it needs that sibling and preserves the patched viewer. Regeneration overwrites source/export/poster outputs, so preserve manual edits separately. The unchanged Three runtime license is included. Inventory excludes its own file, delivery-check and ZIP to avoid circular hashes; ZIP contains inventory and all inventoried payloads.

## Scope
One local inner collectible art asset in the planned 201 one-of-one collection. Cosmetic opening is not an on-chain seal break. No minting, keys, nodes, chain queries, public deployment or changes to shared art/other previews. Branch backup only; no merge. Per-asset human review was explicitly waived for this production batch, which does not imply human visual approval.

Recommended next step: include this branch in the separate final collection integration card.
