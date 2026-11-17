# Seychelles / Granite & Lagoon — v1

Open **seychelles-v1.html** directly in Edge/Chrome. It embeds the complete interactive model, runtime, maps and actual Blender-rendered poster. Drag/touch to rotate; Open/Close lid and Reset view work offline and honor reduced motion.

- HTML: **2,457,005 bytes** (<5,000,000).
- GLB: **1,271,080 bytes**.
- Editable packed source: `seychelles.blend`; reusable inherited mechanism: `mechanism.blend`.
- Procedural maps: 256×256 granite base color, roughness and normal. These are original generated maps, not scans or copied research imagery.
- `poster.png` and `poster.jpg` come from the actual authored source. Desktop/mobile screenshots show the actual final offline viewer, not promotional artwork.

## Design and visual limits
A wide pink-grey granite keepsake with brass fittings, a dark teal seam, three rounded vertically fluted boulders, and an opaque turquoise lagoon enamel in a pale sand-colored shore. It is an intentionally **stylized landscape collectible**, not a geographical scale reconstruction, photorealism or a physically manufacturable granite chest. The shallow lagoon and sand are decorative surface inlays, not simulated transparent water or individual sand grains. Weathering is restrained; material highlights are lighter than the authoring palette. Rear/interior hardware is family extrapolation.

`design-brief.md` was written before authoring. Its approximate initial height estimate is superseded by the explicit inherited-mechanism exception: body skin Z .10–1.56, seam centered 1.618 with .108 height, slab centered 1.828 with .30 height, slab 3.72×2.38. Boulders reach Z 2.69 (below the +.85-above-lid ceiling). Preserving the original pivot geometry took precedence over the rough height estimate. This is not a cedar/wood or basalt reskin.

Final image inspection: mobile title/object/buttons fit; three rocks and contained lagoon remain readable. Open desktop image shows the hollow cavity and attached-looking hinges without obvious clipping. Open-front view naturally hides the exterior lid landscape; `desktop-open-rear.png` supplies the opposite view. Small secondary UI text and simplified enamel-water appearance remain deliberate v1 limits.

## Verified acceptance
- Independently reopened saved source: original `Lid_Hinge` and `Latch_Pivot` positions retained, all five terrain meshes lid-parented, three boulders, narrow seam and lagoon boundary containment.
- **81 sampled poses**, **21 moving / 39 static meshes**, **zero unintended surface intersections**. Every moving part checked against static body; releasing latch checked against lid meshes. Only explicit hinge leaf/barrel and latch knuckle/bridge/pin bearings exempt. Ten attachment pairs overlap; downward interior ray hits floor at Z .265. Sampled surface intersections are not continuous collision or manufacturing certification.
- Independent source/export world vertex nearest-neighbor error **1.712013073529306e-7**, below 1e-5 tolerance. This is geometry parity, not byte-identical re-export or shader identity.
- Actual Three GLTFLoader: **60 meshes / 19,532 triangles / 5 materials**, no nonfinite vertices or degenerate triangles. Runtime base/normal/roughness image variation ranges 162/69/85; no nonfinite UVs.
- Offline **file://** desktop 1440×1080 and mobile 390×844 touch emulation: native rotate/open/close, reset during motion, reduced motion; no external HTTP requests, JS errors or horizontal overflow. Open silhouette fits viewport (max absolute projected NDC about .8924). Real corrupted GLB reaches parser and triggers poster fallback; no-JS poster also passes. Emulation used desktop NVIDIA RTX 4060, not a physical phone or performance benchmark.
- `tests.mjs` verifies staged 80-degree latch then 105-degree lid and rejecting missing pivots/empty geometry/NaN bounds.
- `delivery-check.json` plus `inventory.json`: exact bytes/SHA-256, required-file set, embedded GLB/poster identity and ZIP entry readback. Inventory excludes itself, delivery report and ZIP to avoid recursive hashes.

## Genuine failure and bounded correction
Initial visual review found the lagoon protruding beyond the sand boundary. A source-geometry containment assertion then **failed with nine outside vertices** (indices 47–55), preserved in `initial/lagoon-containment-failure.json`; `initial/poster-before-shore-fix.png` is the original render. Shrinking/recentering/lowering the lagoon fixed the same assertion without loosening it. In the same one bounded correction, dominant-axis UV projection fixed side-face texture stretching. All final gates were rerun.

Optional Codex implementation lane failed 401 token refresh before making edits; Hermes authored and verified directly, without touching credentials. An initial shell `node` shim returned `stdin is not a tty`; native Node/Python subprocess execution fixed invocation. One Edge navigation closed transiently before loading; unchanged browser tests passed on rerun. These tool failures are not presented as asset passes.

## Reproduce
Dependencies: Blender 5.2.1; Python with numpy, Pillow and Playwright; installed Edge; Node.js with Three 0.180.0 and esbuild 0.25.11. `build.py` resolves local node_modules or sibling `iceland-pilot/node_modules`; standalone source extraction requires `npm install` here. No runtime external dependencies.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python verify_all.py` (set `BLENDER` if not installed at the documented Windows default).
4. `python package_delivery.py`

Regeneration overwrites source and renders; preserve manual edits separately. `verify_all.py` reopens source, checks parity/theme/collisions, tests motion, builds HTML and runs both browser suites. Source archive includes scripts, maps, .blend, standalone GLB, viewer, poster and evidence; no dependencies, credential files or .blend1 backups. Repack after any source/evidence change.

## Provenance and scope
Landscape source: https://worlds50beaches.com/anse-source-dargent/ — successfully retrieved text describes large coastal granite boulders and shallow clear waters; only factual inspiration used. Geometry/maps are procedurally authored, not hand sculpture or photogrammetry. Reused mechanism/viewer/testing pattern from repository Japan pilot at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8, with family lineage to Iceland. Three.js MIT license included.

Only `preview/seychelles-v1/` is added. Shared kit and existing previews unchanged. Branch backup only; no merge, website deployment, blockchain node, keys, broadcasts, minting or chain queries. Cosmetic opening does not open an on-chain seal. Collection direction remains 201 equally one-of-one designs; per-asset human approval was waived for this batch, not claimed as obtained.
