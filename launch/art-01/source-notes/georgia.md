# Georgia v1 — Svaneti Stone & Snow

Open `georgia-v1.html` directly in Edge/Chrome, offline. Drag/touch to rotate; Open/Close lid; Reset view. Reduced-motion preference is honored. This is an inner collectible art preview, not custody, minting, hosting, or a transaction. Research and pre-model contract are in `design-brief.md`.

## Delivered
- Standalone HTML **4,258,189 bytes**, strictly below 5,000,000; GLB **2,642,344 bytes**.
- `georgia.blend`: editable, packed Blender source. `mechanism.blend`: copied trimmed family mechanics, not a shared-kit modification.
- `maps/`: three independently procedural 256px stone color/roughness/normal maps. No source photos, scans, AI promotional replacements or downloaded texture assets.
- `poster.png`/`.jpg`: actual source render. Desktop closed/open/rear and mobile closed/open/fallback/no-JS captures are actual file:// browser output.
- Scripts, checks, raw logs, exact SHA-256/byte `inventory.json`, and `georgia-v1-source.zip` with inventory readback. `delivery-check.json` excludes itself and the archive from the payload inventory to avoid recursive hashes.

## Verified acceptance
Actual Three GLTFLoader: **36,676 triangles, 179 meshes, 7 materials**, zero nonfinite vertices and degenerate triangles. Decoded base-color, normal and roughness-channel ranges are 45, 20 and 32. All ridge/tower ancestry leads to Lid_Hinge; a detached-tower negative control was rejected. Saved source confirms front-left tower coordinates, taper-height range, named pivots and lid parentage.

Independent saved-source reopening: hollow floor ray z=0.2650000155, ten hinge-attachment contacts. **81 sampled poses, all 22 moving meshes against 155 static meshes**, plus releasing latch against lid/ornament: zero unintended intersections. Only original named mating bearing classes are excluded. This checks sampled surface intersections, not continuous collision or manufacturing certification.

Source/export nearest-vertex bidirectional maximum error **1.712013073529306e-7**, under 1e-5; all three source maps packed. Geometry parity is not byte-identical reexport certification.

Offline file:// Edge desktop 1440x1080 and 390x844 touch emulation: native open/close, mouse/touch rotation, interrupted reset, reduced motion, zero HTTP(S) requests/errors/overflow; full-open projected silhouette max absolute NDC <0.893. Actual corrupted GLB triggers parser failure and poster; no-JS poster passes. GPU reported NVIDIA RTX 4060; **not physical-phone performance evidence**. Motion tests cover 81 staged poses, -80-degree latch then -105-degree lid, and invalid geometry rejection.

## Actual failures and corrections
1. First build produced HTML **5,006,363 bytes**, GLB **3,206,368 bytes** and failed the unchanged strict cap. Reduced maps from 512 to 256; retained actual variation. See `initial-size-failure.txt`.
2. Inherited browser check assumed reset diagnostics update within 60ms; one actual run failed. Replaced that arbitrary sleep with a bounded 1500ms wait on the exact zero-progress state, retaining the same native action/assertion. See `initial-browser-timing-failure.txt`.
3. Initial theme test incorrectly expected a multi-material glTF terrain node to be a mesh and inspected roughness in red rather than glTF's green channel. Corrected hierarchy traversal/channel test, not the art or acceptance budget.
4. Optional Codex lane failed 401 before edits; no Codex output was accepted and no credentials changed. All implementation and verification were performed directly by Hermes.

## Visual scope and limitations
Actual desktop closed and mobile open screenshots were visually inspected: masonry, snowy ridge, tapered tower and brass are legible; no obvious clipping; hollow interior and connected lid visible. This is **stylized procedural collectible art**, not photorealism, exact architecture, or comprehensive Georgian representation. Warm beige dressed stone is lighter and more uniform than weathered vernacular masonry. Tower slits are shallow applied dark geometry, not excavated openings. Snow is material-assigned ridge faces, not separate drifts. Green seam is conspicuous; feet and inherited clasp remain simplified. Open front view naturally conceals the lid ornament behind its underside; rear-open capture shows it. No human per-asset approval is claimed; the task explicitly waived it until collection completion.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node/Three/esbuild from included package.json. Build resolves local node_modules or sibling `iceland-pilot/node_modules`; dependencies are not archived. Source authoring itself uses only included files. No blockchain node or network service is used.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Blender with same flags on `verify_source.py`, then `verify_parity.py`.
5. `python verify_browser.py`; `python verify_theme.py`; `node --test tests.mjs`
6. `python package_delivery.py`

Regeneration overwrites output; save manual variants separately and refresh evidence/inventory afterward. Source lineage: copied Japan mechanics/viewer/check patterns from local base ff5d78f; new art exclusively in this directory. Three.js MIT license included. No shared kit, earlier preview, vault, mint, docs, evidence, VPS, keys or blockchain was modified or accessed for operations. Branch backup only, no merge or deploy.
