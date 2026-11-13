# United States v1 / Canyon & Copper

Open `united-states-v1.html` directly in Edge/Chrome: complete offline interactive collectible, **2,906,540 bytes**. `united-states.glb`: **1,559,352 bytes**. This is local art, not minted, hosted, signed or on-chain; no blockchain, wallet, keys or VPS accessed. The collection direction is 201 equally one-of-one designs, not a claim that this art delivers custody.

## Design and files
Research-backed brief was written before modeling. Grand Canyon sedimentary cliffs, contrasting pale caprock and a winding blue-green river inspire this invented miniature; not a scale map, geological reconstruction or representative of all American cultures. Hardware is a copper-colored family extrapolation. No borrowed photographs or cultural symbols. Generated portable maps and script-authored Blender geometry, not scans or hand sculpture.

`united-states.blend` is editable packed source; `mechanism.blend` is the inherited trimmed mechanical baseline. `author.py`, `maps.py`, `build.py` reproduce the model and viewer. `poster.png`/`.jpg` are actual source renders, not AI illustrations. Desktop/mobile closed/open and rear-open images are actual offline Edge captures. JSON checks and output text contain execution evidence. Source ZIP and SHA-256 inventory accompany this folder.

## Verified technical gates
- GLTFLoader: 16,040 triangles, 62 meshes, 5 materials; zero degenerate triangles and nonfinite vertices.
- Independent saved-source reopen, same baseline pivots, hollow interior ray at z=0.2650000155. Ten overlapping hinge attachment pairs.
- 81 opening samples include all 23 moving and 39 static meshes, including both banks and river; zero unintended surface intersections. Only named mating leaf/barrel and latch/pin contacts exempt. 80-degree latch release then 105-degree lid opening. Sampled surface evidence, not continuous clearance/manufacturing certification.
- Source/export bidirectional nearest-vertex error 1.712013073529306e-7 (<1e-5).
- Six canyon terraces, three levels on each bank; relief 0.272 and 0.512 above lid. River mesh is one connected 196-vertex component; length 2.96, width 0.17. 41/41 downward and source-hero rays reach its centerline. Detaching river from lid is a deliberate failing negative control, then restored in memory (source not mutated).
- Actual decoded color and roughness-map variation (roughness GREEN channel), max 512px maps, actual runtime lid ancestry.
- Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: drag/touch orbit, native open/close, reset during motion, reduced-motion endpoints, no overflow, no external requests or errors. Full-open max absolute NDC 0.91952. Corrupt bytes reach real GLTFLoader and activate poster fallback; JavaScript-disabled poster also tested.
- Mobile emulation ran on desktop RTX 4060: no physical-phone or FPS claim.

## Visual verdict and actual correction
Stylized canyon collectible, not photorealistic. Initial actual render concealed the river behind equal-height banks (`initial/poster-river-obscured.png`). Lowering the foreground bank to three 0.09-unit courses and setting it farther back exposed the river; final source-camera rays all pass, mobile screenshot shows its turquoise course. Rear bank remains taller. Angular cliff ends and regular banding remain intentional simplifications; body strata can read as wood grain. Water is an opaque inlay, not simulated flow. Source render has some sampling noise. In the front-open view the extended latch and shadowed hinge clearance can look detached; source overlap tests and rear view establish connected geometry but mechanical visual readability is limited. No human art approval is claimed; per-asset review is waived by the batch directive.

## Failures / fixes and tooling
Optional Codex lane exited 401 before implementation; no Codex changes accepted. Hermes authored and ran all checks directly. The required dependency junction pointed to an empty node_modules directory, so the first build failed `MODULE_NOT_FOUND` for esbuild. Installing the existing pinned Three 0.180.0 / esbuild 0.25.11 dependencies locally in this preview fixed the real build failure; no version upgrades or sibling writes. Raw Codex output retained. Reduced-motion tests wait for observed state instead of assuming 60ms contains a rendered frame, with a separate frame-by-frame endpoints-only assertion.

## Reproduce
From this directory: `npm ci --no-audit --no-fund`, `python maps.py`; then Blender 5.2.1 `--background --factory-startup --python-exit-code 1 --python author.py`. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`. Run `python build.py`, `python verify_browser.py`, `python verify_extended.py`, `python capture_rear.py`, `python package_delivery.py`. Python requires Pillow, numpy, Playwright; browser scripts require installed Edge. No dependencies in runtime HTML. Local node_modules is excluded from Git/archive; package-lock pins dependencies. Regeneration overwrites source/model/poster. Refresh inventory after any changes.

Mechanical/viewer lineage: Japan pilot at base commit ff5d78f, with baseline copied unchanged. Three.js MIT license included. Source/archive build depends on tools, not remote runtime assets. Inventory excludes itself, ZIP, delivery-check and Git readback result to avoid circular hashes; ZIP includes inventory and required GLB/source/HTML. This branch is additive-only; integration is a separate task.
