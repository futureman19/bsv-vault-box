# Cabo Verde v1 — Fogo / Atlantic Caldera

Open **cabo-verde-v1.html** directly in Edge/Chrome: self-contained, offline, no server. Drag/touch to rotate; Open/Close lid; Reset view. Reduced-motion preference snaps. Cosmetic motion only: no chain operation, custody action, mint, hosting or deployment.

The original brief was written before authoring from UNESCO's Fogo biosphere and tentative-list descriptions (research-notes.md). Dark warm stone, an Atlantic-blue reveal, brass fittings and a sculptural open horseshoe caldera with a genuinely recessed crater. Original procedural Blender geometry/maps, not scans, hand sculpture or third-party imagery. Poster is rendered from the actual saved source.

## Verified
- Build output: HTML **3,504,236 bytes**, GLB **2,022,488 bytes**, strictly below the 5,000,000-byte HTML limit. All runtime assets embedded.
- Saved source reopened: 33 moving and 38 static meshes; 81 poses, no unintended surface intersections. Every terrain element included. Only documented mating bearings excluded; ten hinge attachment pairs verified. This is sampled surface clearance, not a continuous collision or manufacturing certificate.
- Exact inherited pivots; 80-degree latch release precedes 105-degree lid rotation. Hollow interior floor ray at 0.265 units.
- Source/export nearest-vertex max error 1.712013073529306e-7 units (<1e-5). Actual GLTFLoader: 75 material-split meshes, 17,808 triangles, 7 materials; zero nonfinite vertices or degenerate triangles.
- Theme gate checks crater depression (0.333778 units), east ridge opening, west ridge, upward terrain normals, dimensions, <=0.10 seam, maps and parentage. Flattened-crater negative control is rejected; this is postimplementation regression evidence, not TDD.
- Offline file:// desktop (1440×1080) and touch-emulated mobile (390×844): native controls, drag/touch rotation, full opening, interrupted reset, reduced motion, no overflow, no external requests or JS errors. Full-open projected maximum about 0.8924 NDC. Corrupt bytes reach real GLTFLoader and show the poster; no-JS poster also checked. RTX4060/Direct3D11, not physical-phone performance.
- delivery-check.json records exact hashes/bytes and ZIP inventory/readback; inventory.json hashes all included files except packaging envelopes to avoid circularity.

## Honest visual limits
Stylized miniature relief, not photorealism, surveyed Fogo topography or a representation of all Cabo Verde culture. Mottled stone can still resemble granite/concrete; the terrain is faceted and its rust/ash patches visibly procedural. The east opening is clearer from above than the default front-left camera; the tiny cultivated patches are symbolic and not individually readable on mobile. Hardware is family-derived ornamental construction, not certified load-bearing engineering. The long clasp is retained for tested motion. No human per-asset art approval is claimed (waived for this batch).

## Failures and corrections
The initial theme test rejected ridge depth exceeding the predeclared 1.65-unit footprint; the ridge was narrowed, not the limit relaxed (initial/theme-failure.txt). Initial poster retained. One Cycles denoiser run hit real OOM; disabled denoising and bounded rendering to four threads, then rendered successfully (initial/denoiser-memory-failure.txt). A 180-second browser run timed out under shared-host contention; bounded fresh tests selected D3D11 and passed. Exported multi-material meshes have an intermediate group: corrected runtime ancestry traversal rather than incorrectly requiring direct mesh parentage (initial/ancestry-harness-failure.txt). Roughness variation is checked in glTF's green channel, not the constant red channel. A final source audit corrected ridge winding and added an upward-normal assertion. No checks were waived.

## Files and reproduction
Editable cabo-verde.blend, portable cabo-verde.glb, frozen mechanism.blend, generated maps, actual poster, desktop/mobile closed/open/fallback and terrain screenshots, scripts and JSON evidence are included. The offline viewer itself needs no dependencies. Build dependencies: Blender 5.2.1, Python with numpy/Pillow/playwright, Node.js, Three 0.180/esbuild from package.json, Edge. Scripts resolve relative to this folder; build.py uses local node_modules or sibling iceland-pilot/node_modules. The source ZIP does not include dependencies. Install package.json dependencies locally for standalone rebuilding.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites generated art; preserve manual source edits separately. Mechanics/viewer/test lineage is repository Japan/Iceland at base ff5d78f; original folders and shared art kit remain unchanged. Three.js MIT license included. No blockchain software, keys, chain queries, VPS or production directories were touched. Branch backup only; no merge.
