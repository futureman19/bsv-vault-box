# Mozambique v1 — Bazaruto / Tidal Dunes

Open **mozambique-v1.html** directly in Edge/Chrome. Complete offline viewer: **2,726,679 bytes**; embedded model / standalone `mozambique.glb`: **1,517,484 bytes**. No network or server required. Drag/touch rotate, open/close, reset and reduced motion are supported. Cosmetic inner collectible only; not minted, hosted, signed or chain-admitted.

## Design and provenance
Research-first `design-brief.md` cites ANAC and NASA text describing Bazaruto's white dunes, turquoise shallows and current-carved channels. All geometry/maps are independently procedural, not scans or third-party image textures. Three asymmetric raised sandbanks sit on a turquoise lid with a mapped winding deep-water channel; cream wind-ripple shell, sandy feet, dark teal seam and satin brass family hardware. Not a scale model, geographic map, ethnographic craft claim or representative of every Mozambican culture.

Mechanism, viewer and check lineage: Japan cedar pilot on base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8, itself inheriting the Iceland mechanism. Included `mechanism.blend` is the trimmed baseline, not the new artwork. Shared base kit and all existing previews remain unchanged. Three.js license included. Source uses Blender 5.2.1; Node/esbuild is build tooling only (no blockchain node).

## Verified
- Actual GLTFLoader: 58 meshes, 19,036 triangles, 4 materials, zero nonfinite vertices or degenerate triangles. Four decoded 512×512 maps: color, packed roughness, normal and water color; variation verified using actual glTF channels.
- Independent saved-source reopen: hollow floor ray z=0.2650000155; ten intersecting hinge-attachment pairs. Original named pivots retained. Latch releases 80 degrees before lid rotates 105 degrees. Two executable motion/invalid-asset tests pass.
- **81 sampled poses**, all 19 moving and 39 static meshes, plus latch-vs-lid surfaces: zero unintended intersections. Only explicit inherited mating bearings excluded. Dune ornaments belong to the lid. This is surface-intersection sampling, not continuous swept-volume proof or manufacturing certification.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5; four packed source maps. This checks evaluated geometry, not byte-identical blend re-export.
- Offline file:// Edge desktop and 390×844 touch-emulated mobile: real pointer/touch rotation, open/close, reset during motion, reduced motion, corrupt actual GLB parser fallback, no-JS poster, zero external requests/errors/overflow. Full open projected vertex max absolute NDC 0.892365. Desktop RTX 4060; **not physical-phone performance testing**.
- Theme check verifies three relief heights (~0.36, 0.46, 0.22), moving parentage, decoded map variation and size. Missing-dune negative control is rejected. Delivery check reads back every inventory hash and verifies embedded GLB/poster exactly.

## Visual limits
Actual browser screenshot inspection finds a coherent cream/turquoise/brass palette and legible dune motif, but a stylized rather than photoreal object. Dunes are simple peaked reliefs; body ripples are regular and somewhat wood-like. Water is opaque mapped color, not physical fluid or bathymetry. The inherited recessed seam can make the closed lid look raised; in the front open view the hinge connection is visually ambiguous despite ten verified attachment intersections. Interior depth is subtle; rear view is included. No exact-reference-equivalence claim; there was no preexisting Mozambique marketing artwork. Poster is a real source render, not AI promotion.

## Failures and controls
`initial-failures.md` retains the shell-node and short browser-wait failures. The first texture check sampled the red channel of glTF roughness, returning zero; `initial-theme-channel-failure.json` preserves that observation. Corrected test reads the required green channel and measures range 30 without changing or weakening the material. Missing-dune, missing-lid, nonfinite geometry and actual corrupt-GLB controls demonstrate rejection. Codex lane could not authenticate (401); all implementation and verification were performed directly by Hermes.

## Reproduce
Dependencies: Python + numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, Node + package.json dependencies. `build.py` resolves local node_modules or sibling iceland-pilot/node_modules (junction in this worktree). Standalone source extraction requires dependency installation; runtime HTML does not.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. `node --test tests.mjs` (on this Windows shell use `C:/Program Files/nodejs/node.exe` directly).
5. Run Blender with the same flags on `verify_source.py` and `verify_parity.py`.
6. `python verify_browser.py` and `python verify_theme.py`.
7. `python verify_delivery.py`.

Regeneration overwrites generated model/source/render; preserve manual edits separately. SHA-256 inventory excludes itself and delivery-check to avoid circular hashes. No production edits, VPS access, keys, chain queries, minting or deployments. Branch backup only; integration belongs to the final collection card.
