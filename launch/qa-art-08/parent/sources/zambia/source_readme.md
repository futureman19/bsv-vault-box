# Zambia v1 — Zambezi / Basalt Gorge

Open **zambia-v1.html** directly in Edge/Chrome. The complete model, runtime, maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid and Reset view. No server or network is required. This is cosmetic inner-collectible art, not an on-chain seal operation.

## Delivered
- HTML **3,254,642 bytes**, strictly below 5,000,000; GLB **1,898,704 bytes**.
- `zambia.blend`: editable packed Blender source; `mechanism.blend`: inherited, trimmed mechanism input copied from the Japan pilot. `author.py` and `maps.py` reproduce the model and compact generated basalt maps.
- `poster.png`/`poster.jpg`: real Blender source render. Desktop/mobile closed/open, rear-open, fallback and no-JS screenshots are actual offline browser captures, not promotional illustrations.
- `zambia-v1-source.zip`: source/assets/scripts/evidence. `inventory.json`: exact bytes and SHA-256. `delivery-check.json`: required-file and ZIP readback verification. No node_modules or .blend1 backups.

## Design and limits
The brief was written before modeling from UNESCO's description of the Zambezi, basalt gorges and mist at Mosi-oa-Tunya / Victoria Falls. This is a shared Zambia/Zimbabwe landscape, not a claim of exclusive Zambian ownership. See `design-brief.md` for source and coordinate contract. No source photographs or third-party textures were copied.

Original procedural basalt body, raised gorge banks, connected blue-green river and ivory waterfall, olive accents and family brass fittings. The river is one connected 117-vertex surface with a 0.413934-unit drop. The lower channel is recessed **between raised banks**, not carved through the lid. The gorge is a stylized relief, not a scale reconstruction, realistic hydrodynamics or a physical geological specimen. Basalt bands are visibly procedural and can read as carved/painted stone; waterfall is a rigid sculptural curtain, greenery simplified pebble-like forms. No photoreal equivalence claimed.

One bounded visual correction added solid upper/lower river beds after the first source render made the front water sheet look unsupported; `initial/unsupported-water-edge.jpg` preserves that candidate. Final desktop/mobile and rear-open screenshots were visually inspected: whole model/controls fit, terrain/water read clearly, no obvious floating parts. This is autonomous v1 acceptance under the batch review waiver, not a claim of human art approval.

## Verified on final bytes
- Actual Three GLTFLoader: **17,264 triangles, 96 meshes, 6 materials**, zero nonfinite vertices and degenerate triangles; actual decoded basalt color range 52/255 at 512x512.
- Saved source independently reopened: **56 moving + 39 static meshes**, **81 sampled poses**, zero unintended intersections. All new terrain/river/foam/accent meshes included; explicit inherited mating hinge leaf/barrel and latch knuckle/bridge/pin contacts only are exempted. Ten attachment pairs and a hollow-floor ray at z=0.2650000155 pass. This is sampled surface evidence, not continuous or manufacturing certification.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7** (<1e-5); three packed procedural images. Mechanism pivot locations exactly retained; 80-degree latch release precedes 105-degree lid opening. Geometry test asserts 3.72x2.38 lid, 0.09 seam, all 40 source ornament meshes in the declared lid envelope, connected water geometry and material zones.
- Offline file:// Edge: desktop 1440x1080 and touch-emulated mobile 390x844; native buttons, mouse/touch rotation, open/close, interrupted reset and reduced motion pass. No external HTTP requests, runtime errors or overflow. Full-open maximum absolute NDC 0.892365. Real corrupted GLB invokes parser-error poster fallback; no-JS poster also passes.
- Theme test actually detaches the loaded water group from the lid and confirms rejection, then restores it. Unit tests reject invalid assets and check choreography endpoints.
- Tests ran on Windows Edge/NVIDIA RTX 4060. Mobile emulation is **not physical-phone performance**, and no FPS or long-session certification is asserted.

## Real failures retained and corrected
`initial/reduced-motion-reset-failure.txt`: a fixed 60ms post-reset observation failed. Harness now waits for the actual zero-progress state with a bounded 2s timeout rather than assuming a wall-clock frame cadence; viewer behavior was not weakened.
`initial/multi-material-group-failure.txt` and observed JSON: the first theme harness incorrectly expected the two-material river to load as a directly named mesh. Actual GLTFLoader creates a named group with material primitive children. The test now checks those real children and their semantic group's lid ancestry; source test independently checks the original single connected mesh. The actual detach negative control still fails as intended.
An optional Codex implementation lane exited on authentication failure before editing. All implementation and final checks were executed directly by Hermes; no credential store was accessed or changed.

## Reproduce
Python with numpy/Pillow/playwright, installed Edge, Blender 5.2.1, Node/esbuild/Three.js are build/test dependencies only. `build.py` resolves this folder's node_modules or sibling `iceland-pilot/node_modules`; install package.json dependencies in this folder for standalone source extraction. Node here means JavaScript tooling, not a blockchain node. Source authoring uses only included mechanism.blend/maps, no original artwork path.

From repository root:
```
python preview/zambia-v1/maps.py
blender --background --factory-startup --python-exit-code 1 --python preview/zambia-v1/author.py
python preview/zambia-v1/build.py
node --test preview/zambia-v1/tests.mjs
blender --background --factory-startup --python-exit-code 1 --python preview/zambia-v1/verify_source.py
blender --background --factory-startup --python-exit-code 1 --python preview/zambia-v1/verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python preview/zambia-v1/verify_geometry.py
python preview/zambia-v1/verify_browser.py
python preview/zambia-v1/verify_theme.py
python preview/zambia-v1/package_delivery.py
```
On this host Blender is `C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe`. Regeneration overwrites source/model/render; save manual variants separately. Refresh inventory after rebuilding. Package envelopes exclude themselves to avoid circular hashes.

## Lineage and scope
Mechanics/viewer/testing adapted from Japan and Iceland pilots at local base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; shared art/vault-kit untouched. Three.js MIT license included. Additive only under preview/zambia-v1. Branch backup only, no merge, public deployment, mint, blockchain queries, keys, funds, VPS or production-system changes. Collection direction remains 201 equally one-of-one designs; no accessories added.
