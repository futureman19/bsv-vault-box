# Croatia v1 — Plitvice Tufa

Open `croatia-v1.html` directly in Edge/Chrome: all model, maps, runtime and actual-source poster bytes are embedded. Drag/touch rotate, Open/Close lid and Reset. This is cosmetic collectible art, not a transaction, hosted release or mint.

## Delivery
- HTML: **2,436,522 bytes**, strictly below 5,000,000.
- GLB: **1,227,844 bytes**; 14,136 triangles, 78 meshes, seven runtime materials, zero degenerate triangles or nonfinite vertices through the real GLTFLoader.
- `croatia.blend`: editable Blender-authored source; `mechanism.blend`: included inherited family mechanism from Japan pilot. `maps/`: three generated PNG maps; no scans or copied research imagery.
- `poster.png`/`poster.jpg`: actual source render. Browser desktop/mobile closed/open and fallback captures are genuine offline file:// evidence.
- `inventory.json`, source ZIP and `delivery-check.json`: exact bytes/SHA-256 and archive readback. Local `.gitattributes` preserves bytes across Git checkout.

## Verified
Saved source independently reopened. Hollow interior floor ray Z=0.2650000155. Ten hinge attachment pairs. 81 sampled poses include all 39 moving meshes against 39 static meshes, plus latch-vs-lid checks; zero unintended surface intersections. Explicit bearing contacts alone excluded. This is discrete sampled surface evidence, not continuous swept-volume proof or engineering certification.

Lid and latch preserve the supplied mechanism and staged 80-degree latch / 105-degree lid choreography; two motion tests pass, including invalid-asset rejection. Geometry/source-export maximum nearest-vertex distance 1.712013073529306e-7 (<1e-5).

Theme checks: three distinct turquoise water levels, two cascades, 23 lid-owned ornaments, maximum ornament Z=2.51507, four exposed cascade face-center rays, varying packed color/roughness maps. A deliberately detached lake is rejected. Actual decoded roughness uses glTF GREEN channel; ranges 57/255 (tufa color and roughness), 36/255 (feet).

Desktop 1440×1080 and mobile 390×844 touch emulation over offline file://: native open/close, rotation, reset interrupted movement, reduced motion, no overflow, no external HTTP requests or JS errors. Full-open vertex projection max absolute NDC 0.90901. Corrupted embedded GLB reaches the actual loader and shows poster fallback; no-JS poster also tested. GPU is desktop RTX 4060; no physical-phone/FPS claim.

## Real failure and bounded correction
`initial/theme-output.txt` preserves the first source gate failure: cascade 0 face center was occluded by Lake / 1. Initial straight sloping strips were replaced with stepped lip-and-drop ribbons; the same strict ray-hit-identity gate now passes all four face centers. `initial/poster.png` retains the earlier source render. This was a real geometry failure, not a relaxed gate. Detached-lake negative control is a separate post-implementation regression experiment, not test-first history.

## Visual verdict / limits
Cream chest, three ascending turquoise basins and brass read clearly on mobile. The lakes remain stylized bowl-like terraces, not an accurate Plitvice topographic model. Cascades are exposed geometrically but still subtle at mobile scale. Opaque glossy turquoise inlays are not fluid simulation, transparent water or photorealism. Stone porosity is understated; green bank accents are simple lobes, not botanical foliage. Visible source-render noise remains because denoising was disabled. The narrow green seam can read as an open gap. Full-open front view naturally hides the decorated lid exterior; parentage/source checks establish that it travels with the lid. Hardware/interior are family design extrapolations, not Croatian historical craftsmanship.

Research links and the pre-model visual contract are in `design-brief.md`. No third-party photographs embedded. Three.js MIT license included. Collection scope: 201 one-of-one designs with equal edition scarcity; no accessories issued, on-chain storage, custody verification or public deployment implied.

## Reproduce
Blender 5.2.1, Python with Pillow/numpy/Playwright, Edge, Node build tooling. The supplied shared dependency folder was inspected and lacked esbuild; pinned dependencies were installed only in this new preview folder. No shared preview files changed. Build dependencies are not runtime downloads and are excluded from delivery.

1. `npm ci --ignore-scripts --no-audit --no-fund` inside this folder.
2. `python maps.py`
3. `blender -b -t 4 --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender likewise with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs`
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`

`setup.py` records initial adaptation lineage and needs the sibling Japan/Iceland pilots; do not rerun it during ordinary reproduction because it resets viewer scripts. The included helpers/mechanism make normal authoring self-contained. Regeneration overwrites source and changes hashes; rerun inventory after rebuilding. No Codex lane used: direct bounded authoring was safer than delegating art validation.
