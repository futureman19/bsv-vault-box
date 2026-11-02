# Morocco / Atlas & Tile — actual interactive 3D pilot

Open **morocco-atlas-v1.html** directly in a WebGL-capable browser. It embeds the real GLB, Three.js runtime and actual rendered-poster fallback. No network, wallet or server is needed. Cosmetic staged latch release/lid opening only; not minted, hosted or deployed.

## Delivered
- `morocco-atlas-v1.html`: **2,962,532 bytes**, below both 4.5 MB target and strict 5,000,000-byte limit.
- `morocco.glb`: **1,629,864 bytes**; actual portable textured geometry.
- `morocco.blend`: editable named parts and packed maps.
- `poster.png`, `poster.jpg`: actual model renders, not AI promotional illustrations.
- `reference-comparison.jpg`: primary concept vs actual model at equal measured warm-object width with uniform scaling, no warping; perspective/lighting differ.
- Desktop/mobile closed/open screenshots, rear-open, fallback and no-JS captures; top-down physical-coordinate diagnostic.
- Reproducible author/maps/viewer/test scripts, input hashes, complete evidence and source ZIP.

## Verified
Real GLTFLoader: 17,652 triangles, 325 meshes, 8 materials, zero nonfinite vertices/degenerate triangles. There are 270 individual ceramic prisms, a real eroded rear-centre ridge, four compact generated maps (maximum dimension 512), correct lid ancestry, and no tree/moss/glacier/river geometry.

Saved source independently reopened: hollow-floor ray, ten body/hinge/leaf attachment pairs, **81 full-motion samples** including all new terrain/hardware; zero disallowed overlaps. Only the original narrowly named mating bearing contacts are excluded from collision rejection. Bearing contact and ridge-to-rear-tile-bed attachment also persist in all 81 samples. This is sampled intersection/contact evidence, not continuous CAD or manufacturing proof. The rear lid clearance can appear visually floating from the front-open view, but the mesh contact chain is independently tested.

Source/export bidirectional world-vertex parity tolerance 1e-5. Independently reopened re-export has exact JSON, positions, normals, indices and embedded images; a few UV float32 roundtrips differ by at most 5.96e-8, below 1e-6. It is not byte-identical; both hashes are recorded.

Offline Edge `file://`: desktop 1440×1080 and mobile-emulated 390×844; native pointer/touch rotation and button taps, open/close, reset mid-motion, reduced motion, genuine corrupt-GLB fallback, no-JS poster. Zero unexpected external requests, uncaught errors or horizontal overflow. Full-open projected silhouette max absolute NDC≈.951. Tested on desktop RTX 4060, not a physical phone; no FPS/performance promise.

## Bounded review / remaining visual limits
The broad proportions and rear-centre placement follow the primary. One landmark correction rounds/narrows the initially rectangular mountain base. The model is intentionally a lightweight authored study: stone banding is too regular compared with the concept; wood and metal are cleaner, tile motifs differ and fine ceramic finish is less legible on mobile; the ridge is simpler than the multi-peak concept. The family latch is longer than the concept clasp; the ring is on the adjacent left side rather than the primary front face. Its lid top can look lighter under studio highlights. These differences are disclosed, not claimed exact or photoreal.

Initial open framing failed at NDC 1.0016; camera zoom-out on opening was corrected and final desktop/mobile tests pass. Initial roughness-map test sampled red incorrectly; corrected to glTF's green channel without altering the asset. Original failed evidence is retained under `initial/`. No more polishing or other boxes started; next step is user visual review.

## Reproduce locally
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, Edge and Node. Run `npm install` here for pinned Three 0.180.0 and esbuild 0.25.11; build.py can alternatively reuse the repository's installed `../iceland-pilot/node_modules`. Those dependencies are compile-time only and excluded from the ZIP. Included mechanism.blend is the self-contained trimmed mechanism source; no prior Japan model is required to author.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py` and `python test_theme.py`
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_reexport.py`, `render_review.py` using the same flags.
5. `python verify_browser.py`, `python verify_extended.py`, `python compare.py`.
6. `python package_delivery.py` only in this checkout/profile: it verifies original inputs and writes the declared local delivery folder.

`setup.py` is historical acquisition/provenance, not a reproduction prerequisite: it references the prior repository and original concept path. Regeneration overwrites manual source edits. `design-brief.md` contains physical dimensions and concise Met/Britannica references; this study does not assert a single identity for all Morocco. No source imagery is represented as a survey or scan.
