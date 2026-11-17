# Belarus v1 / Golden Straw

Open **belarus-v1.html** directly in Edge/Chrome. The entire actual 3D model, runtime, generated maps and real-source poster are embedded. Drag/touch to rotate; Open/Close lid; Reset view. No server or network required. This is a cosmetic inner collectible study, not a functional custody container, minted NFT or on-chain asset.

## Delivered
- Standalone HTML **4,490,498 bytes**, strictly below 5,000,000.
- `belarus.glb` **2,721,256 bytes**; `belarus.blend` packed editable source.
- `mechanism.blend` is the trimmed family articulation/liner/hardware input copied from the Japan pilot, not its country ornament.
- `maps/`, author/build/check scripts, dependency pins and Three.js MIT license.
- `poster.png` and compact `poster.jpg`: actual Blender source render, not AI promotional artwork.
- Offline desktop/mobile closed/open screenshots, rear-open view, corrupt-loader fallback and no-JS poster captures.
- `inventory.json`, source ZIP and `delivery-check.json`: measured byte counts, SHA-256 and archive readback. Dependencies/backups excluded.

## Design and limitations
The prewritten sourced brief celebrates Belarusian cereal-straw craft with a golden body and an original geometrically interlaced mat. UNESCO sources describe straw boxes and living craft transmission; this is neither a traditional-pattern replica nor artisan-authored work. No third-party photos are embedded.

The raised lid mat has **21 warp and 13 weft ribbons**, real alternating over/under relief, dark timber backing and warm brass perimeter. It travels with the lid. The body is a generated flat woven-color treatment over rigid skins: in the source render it can read as small brick/slat cladding rather than fine straw fibres. The mat is clearer at mobile size. Wood, fittings and feet are stylized; perimeter binding joints are visible. The real Cycles poster retains some sampling noise. No photorealism, exact reference equivalence, cultural endorsement or manufacturing claim is made. The source render and actual mobile capture were visually inspected; no gross resting-state clipping or floating parts was observed.

## Verified evidence
- Saved source reopened; original lid/latch pivot matrices compared with the included mechanism; hollow floor ray z=0.2650000155. Ten hinge attachment overlap pairs verified.
- **81 motion samples**, all **67 moving and 99 static meshes**, zero unintended moving/static or latch/lid surface intersections. Only explicit mating hinge/latch bearings excluded. This is sampled surface evidence, not continuous collision proof. Co-moving decorative contacts are not engineering tolerances.
- Source/GLB nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5 in both directions. Three packed source maps. Material/texture semantics checked in real loader; this is geometric parity, not byte-identical re-export.
- Actual Three GLTFLoader: **44,848 triangles, 166 meshes, 6 materials**, zero nonfinite vertices and degenerate triangles. Decoded color ranges 63/25, roughness green-channel range 40; map dimensions at most 512 square.
- Edge offline `file://`, desktop 1440×1080 and 390×844 mobile touch emulation: native controls, pointer/touch rotation, open/close, interrupted reset, reduced motion, no HTTP requests, no JS errors or horizontal overflow. Full-open maximum projected absolute NDC <0.893. RTX 4060 desktop GPU: not a physical-phone performance test.
- Genuine corrupted GLB reached GLTFLoader, triggered caught parse error and displayed poster with disabled Open. Separate no-JS poster test passed.
- Negative control deliberately detached one warp ribbon in memory: `AssertionError: Detached ribbon rejected`, exit 1. No bad source saved. Motion tests also reject missing lid, empty/nonfinite geometry. These are regression negatives, not a claim all art was test-first.
- Initial build genuinely failed because shared pilot node_modules had no esbuild. Preserved `build-initial-failure.txt`; fixed with unchanged pinned dependencies installed only in this new directory. No other preview toolchain was populated. All final acceptance gates passed.

## Reproduction
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node with pinned package.json. Run from this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. `node --test --test-reporter=tap tests.mjs`
6. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
7. `python verify_browser.py` and `python verify_extended.py`.
8. `python package_delivery.py`.

`setup.py` records initial adaptation lineage and is NOT a regeneration step; it reads sibling Japan/Iceland inputs and overwrites initial scripts. Ordinary authoring uses only the included mechanism and maps. Regeneration overwrites source/export/render; preserve manual edits separately and refresh all evidence/inventories. Map filenames retain lineage names, but contain the generated straw/timber maps, not the old Japan textures. Build uses local dependencies, falling back to sibling pilot only if local node_modules is absent. Archive excludes installed dependencies.

All changes are additive under this folder. No wallet, chain, mint, secret, production site, VPS or external-message actions. Branch backup only; integration belongs to the final collection card. Per-asset human review was explicitly waived for collection production; this is not claimed as individual visual approval.
