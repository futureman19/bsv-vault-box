# Dominica v1 — Rainforest & Boiling Lake

Open `dominica-v1.html` directly in Edge/Chrome. Complete embedded 3D model, textures, runtime and actual-source poster: **2,616,769 bytes**, below 5,000,000. Standalone `dominica.glb`: **1,391,576 bytes**. Drag/touch rotate, open/close staged lid, reset, reduced-motion support. No server/network, wallet or chain required.

## Art and honest visual result
Dark volcanic-stone keepsake chest with brass fittings and forest-green reveal. Five sculpted green ridges and 105 canopy clusters surround a pale grey-blue basin on the lid. The sourced pre-model contract is `design-brief.md`. This is an invented landscape inspired by Dominica’s Morne Trois Pitons National Park, not Dominican Republic, not a geographic survey or traditional craft replica. All geometry/maps are procedural Blender authorship, not photogrammetry, purchased models or hand sculpture. No research imagery is copied.

Actual source and mobile/rear-open browser renders were visually inspected. Lake, foliage and stone body are visible without normal-view clipping; hardware appears seated. The canopy is simplified rounded clusters; ridges remain toy-like/conical, the body can read as concrete, and the lake is opaque ceramic-like rather than boiling water. No steam/fluid simulation or photoreal-equivalence claim. Initial plain-hill version is retained in `initial/before-canopy.png`; a single canopy correction improved rainforest readability. Source poster has bounded 24-sample noise; it is a real render, not AI promotion. Per-asset human review is waived for this collection batch; this is not a claim of individual human visual approval.

## Independently exercised gates
- `python verify_all.py`: BUILD, MOTION, SOURCE, PARITY, THEME_SOURCE, BROWSER, EXTENDED **PASS**; checks assert actual outputs and terminate nonzero on failure.
- Real Three GLTFLoader: **19,988 triangles, 167 meshes, 6 materials**, zero nonfinite vertices and degenerate triangles. Three 256px maps decoded: stone color range 47, actual roughness green-channel range 91, canopy color range 61.
- Reopened `.blend`: 128 moving / 39 static meshes; **81 poses**, zero unintended sampled surface intersections. Every lid ornament and canopy included. Original bearing-only exclusions are explicitly recorded; hollow floor ray z 0.265; 10 intersecting hinge attachment pairs. This is sampled surface evidence, not continuous collision/manufacturing certification.
- Source/export bidirectional nearest-vertex max error **1.712013073529306e-7**, below 1e-5; three images packed in source. Original lid/latch pivot matrices independently compared with included trimmed mechanism. Latch releases 80° before lid opens 105°.
- Lake bounds and 9 unobstructed downward aperture rays, 5 ridges, 105 canopy clusters, all terrain owned by lid. Deliberately detached lake is rejected; source reloaded afterward. This is postimplementation negative regression coverage, not a TDD claim.
- Actual offline `file://` Edge desktop 1440×1080 and touch-emulated 390×844: native open/close, mouse/touch rotation, interrupted reset, reduced motion, no overflow, external HTTP requests or JS errors. Full-open max absolute projected NDC ~0.8924. Real corrupt embedded GLB triggers loader failure/poster; no-JS poster separately tested. Mobile emulation on RTX 4060 is not physical-phone performance evidence.
- `package_delivery.py`: exact byte/SHA-256 inventory and ZIP-entry/hash readback, including explicit required source/GLB/HTML/evidence set. Packaging envelopes excluded from recursive inventory by design. Folder-local `.gitattributes` preserves bytes through Git checkout; indexed blob comparison performed before commit.

## Files and reproduction
`dominica.blend` is editable packed source, `mechanism.blend` the included inherited articulation seed; `author.py` generates final geometry and source poster. Maps are in `maps/`; `maps.py` regenerates them. `viewer.js`, `template.html`, `motion.mjs`, bundled runtime and pinned `package.json`/lockfile reproduce the offline viewer. `desktop-*.png`, `mobile-*.png`, source poster, JSON checks and raw outputs are execution evidence. `dominica-source.zip` is the source/evidence bundle, excluding node_modules, backups and caches.

From this folder, with Python + Pillow/numpy/playwright, installed Edge, Blender 5.2.1 and Node:
1. `npm ci --no-audit --no-fund` (exact Three 0.180.0 / esbuild 0.25.11).
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` (set `BLENDER` if not at documented Windows default).
5. `python package_delivery.py`

Regeneration overwrites outputs; preserve manual edits separately. The authoring script needs no sibling source; build prefers local node_modules and falls back to sibling Iceland tooling. Required initial shared toolchain was empty, so exact dependencies were installed locally only; failed build and optional Codex auth failure are disclosed in `initial/findings.md`. No Codex implementation was accepted. Three.js MIT license included. Mechanism/viewer/test lineage is Japan/Iceland from base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8; shared kit and earlier previews untouched.

## Scope
Local inner collectible art only; branch backup is not hosting. No minting, tokens, signed authenticity, on-chain storage, custody verification, deployment, keys, chain queries or node startup. Proposed launch collection remains 201 equally one-of-one designs. No blockchain code, shared kit, other previews or production files changed. Integration belongs to the separate collection card.
