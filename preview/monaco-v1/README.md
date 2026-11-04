# Monaco v1 — The Rock & Riviera

Open **monaco-v1.html** directly in Edge/Chrome. All 3D runtime, GLB, maps and actual-source poster are embedded. Drag/touch to rotate; Open/Close lid; Reset view. Reduced-motion preference snaps to endpoints. No server or internet connection required.

## Delivered
- `monaco-v1.html`: **2,447,623 bytes**, strictly below 5,000,000.
- `monaco.glb`: **1,260,984 bytes**.
- `monaco.blend`: packed editable Blender source; `mechanism.blend`: inherited trimmed mechanism input.
- `maps/`: original procedural 256px stone color, roughness and normal maps; no photographed textures.
- `poster.png` and `poster.jpg`: actual source render, not AI artwork. Desktop/mobile closed/open, rear-open and fallback screenshots are actual offline browser captures.
- `monaco-v1-source.zip`: source, model, HTML, poster, maps, scripts, license and evidence; `inventory.json` contains exact byte counts/SHA-256. `delivery-check.json` records ZIP readback and totals, outside the archive to avoid self-reference.

## What passed
- Saved source independently reopened: **60 moving meshes, 51 static meshes, 81 poses**, no unintended surface intersections. Latch vs lid also sampled; only explicit mating hinge leaf/barrel and latch knuckle/bridge/pin bearings exempt. Ten attachment pairs connect hinge mounts to body and moving leaves to lid. Hollow floor ray z=0.2650000155. Sampled surface checks are not continuous mechanical certification.
- Original hinge/latch transforms compared independently with mechanism.blend. Latch releases 80° in first quarter; lid then opens 105°. All 44 landscape/building/garden meshes are lid-owned. Seven pitched roofs, six green garden clusters; max ornament z=2.7300000191.
- Source/export nearest-vertex discrepancy **1.712013073529306e-7**, below 1e-5; all three maps packed in saved source.
- Actual Three GLTFLoader: **17,332 triangles, 111 meshes, 8 materials**, zero nonfinite vertices or degenerate triangles. Decoded map ranges: color 31, roughness GREEN channel 47, normal red channel 9.
- Real offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, rotation, interrupted Reset, reduced motion, no horizontal overflow, no external HTTP requests or console/page errors. Full-open maximum absolute projected coordinate 0.892365, below clipping threshold 1. Reduced-motion rendered-frame samples restricted to endpoints.
- Actual corrupted GLB input reaches parser and yields poster fallback with disabled controls; no-JS poster also checked. Expected parser error recorded separately, not counted as successful runtime error.
- Negative controls: detached ornament rejected, then restored; three invalid geometry summaries rejected. Source poster nonblank/alpha coverage and procedural palette tested. Strict payload and exact archive-entry/readback checks.

## Visual result and limits
Sourced brief-led fictional miniature: pale stone, red/ivory geometric panels, satin brass and a blue enamel sea around a rocky old-town terrace. Stylized Mediterranean village, **not a precise Monaco landmark or photorealistic reconstruction**. Fine building details are intentionally sparse; rounded garden clusters, faceted rock, flat sea and modest source-render noise remain. Browser lighting makes blue water lighter cyan. The dark seam may suggest slight openness; it is an intentionally modeled reveal. Cosmetic deviation from the initial brief: no side hanging ring was added; retained family clasp/corner fittings carry the hardware language. Rear/interior are authored extrapolations.

Source render and actual mobile closed/desktop open captures were visually inspected: unclipped silhouettes and broadly readable palette/miniature; no obvious major floating parts. Browser emulation on an RTX 4060 is **not physical-phone performance**. See `assessment.md` for the real failed optional lane, missing dependency build failure/fix and visual qualifications. No visual-equivalence, manufacturing, FPS or cross-device certification is implied.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/playwright, installed Edge, Node.js with the pinned package-lock dependencies. From this directory:

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `node tests.mjs` then `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `test_theme.py`.
6. `python verify_browser.py` and `python verify_extended.py`
7. `python package_delivery.py`

All runtime assets are offline; npm is build-time only. `setup.py` is historical local adaptation tooling referencing the sibling Japan pilot and is not needed to reproduce the delivered source. Regeneration overwrites outputs; preserve manual edits separately. Build prefers local dependencies, with optional sibling Iceland fallback. The provided sibling dependency directory was empty, so this delivery installed unchanged pinned versions locally. Folder-local `.gitattributes` preserves exact hashed bytes in Git.

## Provenance / scope
Research sources and pre-model dimensions/palette are in `design-brief.md`. Textural/architectural motifs are independently authored interpretations, not scans, traditional craft replicas or licensed third-party images. Mechanics/viewer/tests derive from the repository Japan/Iceland pilots; Three.js 0.180.0 MIT license included.

Art-only branch backup. Not minted, signed, deployed, on-chain or custody-tested. No keys, nodes, broadcasts, VPS, production docs or vault code accessed/changed. This is one inner collectible of the planned 201 equal-scarcity one-of-ones; opening its lid is cosmetic only. Collection-wide integration and review are separate downstream work.
