# Serbia v1 — Pirot / Woven Crimson

Open **serbia-v1.html** directly in Edge/Chrome. All runtime JavaScript, model, maps and actual-model poster are embedded. Drag/touch to rotate; Open/Close lid; Reset view; reduced-motion support. No server, wallet or network connection required.

## Delivery
- Standalone HTML: **2,303,237 bytes**, strictly below 5,000,000.
- `serbia.glb`: **1,140,356 bytes**.
- `serbia.blend`: editable named Blender source with packed maps. `mechanism.blend` is the copied trimmed family mechanism, not a newly authored Serbian historical object.
- `maps.py`, `maps/`, `author.py`: original procedural textile and modeled stepped relief. Not scans, hand sculpture or museum-image derivatives.
- `poster.png` / `poster.jpg`: actual source render; desktop/mobile closed/open and fallback screenshots are actual offline browser captures.
- JSON checks, raw test outputs, exact SHA-256 inventory and source ZIP document the artifact. The inventory excludes itself and packaging envelopes to avoid circular hashes.

## Research and visual interpretation
The prewritten `design-brief.md` cites Serbia's intangible cultural heritage register and the Ethnographic Museum in Belgrade on Pirot tapestry weaving, red fields/borders and stepped diamonds. This is a new stylized composition inspired by that tradition, **not an authentic/reproduced historical kilim**, nor a claim to represent all Serbian culture. No third-party image pixels are used.

Crimson geometric textile panels sit inside dark brown framing with brass fittings. Three paired ivory/indigo stepped reliefs are actual closed mesh prisms on the lid. The brown structure is walnut-inspired but has no species-specific wood-grain map. The source render reads pinker than the browser and retains visible sampling grain (24 samples, denoising disabled). In mobile view the textile identity is clear, but shallow relief depth and tiny weave are not strongly legible; patterns are intentionally cropped by frames. Broad hardware and the dark seam are inherited family styling. These limitations do not establish photorealistic quality or historical fidelity.

## Verified acceptance
- Actual GLTFLoader: **66 meshes, 14,744 triangles, 6 materials**, zero nonfinite vertices and zero degenerate triangles. All six reliefs remain lid children. Decoded 512px color/roughness/normal ranges are 216/24/24; roughness checked in GREEN channel.
- Independently reopened saved Blender source: original pivot matrices match exactly, slab dimensions 3.72 × 2.38 × .30, five textile panels, six positioned relief meshes, seam <.12, hollow floor ray z=0.2650000155. Ten explicit hinge attachment intersections pass.
- **81 motion poses**, all 23 moving and 43 static meshes, zero unintended intersections. Latch-versus-lid included. Only named concentric leaf/barrel and latch knuckle/bridge/pin bearings excluded. Sampled surface clearance is not continuous collision, solid containment or manufacturing certification.
- Source/export nearest-vertex error in both directions **1.712013073529306e-7**, below 1e-5. This is geometry parity, not byte-identical Blender re-export or render equivalence.
- Offline `file://` Edge: 1440×1080 desktop and 390×844 touch-emulated mobile, native controls, drag/touch rotation, open/close, reset during motion, reduced motion, no overflow, no external HTTP requests or JS errors. Full-open maximum absolute NDC ~0.8924. Actual corrupt GLB reaches parser and produces poster fallback; no-JS poster also passes. NVIDIA RTX 4060; **not physical-phone performance**.
- Motion tests cover staged 80-degree latch followed by 105-degree lid and reject missing/empty/nonfinite assets. Theme negative control rejects an omitted relief; this is postimplementation regression evidence, not test-first TDD. `initial/failures.md` records actual failed optional CLI auth and missing build-dependency run, plus fixes. No acceptance thresholds were relaxed.
- Visual inspection of source poster, actual mobile closed and desktop open captures found no obvious major clipping/broken geometry; the material and depth limitations above remain.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js build tooling. No blockchain node is used. From this directory:
1. `npm ci --no-audit --no-fund` (pinned Three 0.180.0 and esbuild 0.25.11).
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` (build, motion, reopened source, parity, theme, browser, extended, package).
Set BLENDER environment variable for a different Blender path. Original sibling dependency folder was empty; local pinned dependencies were installed instead. The offline HTML needs none of these build dependencies. Regeneration overwrites source/export/poster; preserve hand edits separately. Rebuilding changes artifact hashes; regenerate inventory afterward.

## Scope
Art-only additions under `preview/serbia-v1/`, branch `art/serbia-v1`. No merges or production changes. No keys, chains, minting, transactions, VPS, deployment or external messaging. Cosmetic opening is not opening an on-chain seal. Collection direction is 201 equally one-of-one designs; storage/on-chain integration and authenticity signing remain unimplemented. Per-asset human review waived for this batch; final collection integration is a separate dependent card. Three.js runtime license included.
