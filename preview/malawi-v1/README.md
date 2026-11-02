# Malawi v1 — Lake of Stars

Open `malawi-v1.html` directly in Edge/Chrome. All runtime JavaScript, model, textures and the actual Blender-rendered poster are embedded. Drag or touch to rotate, Open/Close lid, Reset view. Local cosmetic art only: not minted, hosted, signed, on-chain or a custody action.

## Deliverables
- Standalone HTML: **2,544,716 bytes**, strictly below 5,000,000.
- `malawi.glb`: **1,378,228 bytes**; 18,496 triangles, 79 meshes, six materials measured by actual GLTFLoader.
- `malawi.blend`: editable packed Blender source; `mechanism.blend`: inherited family articulation/interior/hardware baseline.
- `maps/`: three procedurally generated 256×256 granite color/normal/roughness maps, not scans.
- `poster.png` / `poster.jpg`: actual saved-source render; desktop/mobile closed/open, rear-open, corrupt-model and no-JS captures.
- `design-brief.md`: research sources and measurable contract written before modeling.
- `malawi-source.zip`: source, standalone model/viewer, maps, scripts, screenshots, logs and evidence. Exact hashes in `inventory.json`; ZIP readback in `delivery-check.json`. Inventory excludes its own recursive envelopes and caches/backups.

## Verified scope
Family pivots retained: latch releases 80° before lid opens 105°. Independently reopened saved source: 81 poses, all 40 moving meshes against 39 static meshes, plus latch against lid; zero unintended surface intersections. Explicit hinge/latch mating bearings alone excluded. Ten hinge attachment pairs intersect as expected; hollow floor ray reaches z=0.2650000155. Every shore, lake and fish ornament is a direct lid child. This is sampled surface-intersection evidence, not a continuous or manufacturing guarantee.

Independent source/export world-vertex parity maximum distance **1.712013073529306e-7** (<1e-5). Three packed source maps. Actual GLTFLoader: zero nonfinite vertices or degenerate triangles. Four boulders, three fish bodies and tails, one lake inset and one sandy shoreline verified; no inherited tree, foliage or moss. Texture variation checks decode real images and use glTF's green channel for roughness. A deliberately missing-boulder validation input is rejected; motion tests reject invalid asset records; corrupted real GLB reaches parser failure and displays poster.

Offline `file://` Edge: 1440×1080 desktop and 390×844 touch-emulated mobile; native buttons, pointer/touch drag, open/close, interrupted reset and reduced motion. No external HTTP requests, unhandled runtime errors or horizontal overflow. Fully open default projection remains inside viewport (max absolute NDC approximately 0.892365). Real corrupt-GLB and no-JavaScript poster fallbacks tested. Mobile emulation uses the desktop RTX 4060, not physical-phone performance.

## Visual result and limitations
A deliberately stylized pale granite keepsake chest, turquoise enamel lake plaque, irregular sandy rear shore, four rounded rocks and three gold/blue cichlid-inspired ornaments. It is not a surveyed Lake Malawi scene, a species illustration, traditional Malawian craft replica, photorealistic reconstruction or user-approved reference match. The title and research contextualize the lake motif; fish anatomy alone does not uniquely identify Malawi.

Actual mobile screenshot review found the complete box comfortably framed, controls legible and theme coherent. Granite remains pale/softly mottled rather than highly geological; rocks are simplified, fish small and visibly ornamental, water an enamel inset rather than simulated water. Source studio and browser lighting differ. Rear/interior and brass fittings are family-design extrapolations.

One visual correction replaced inherited collapsed/stretched side UVs with dominant-face, equal-scale planar mapping; `initial/uv-stretch-poster.png` retains the earlier appearance. A genuine roughness acceptance failure read red instead of glTF's green channel; `initial/roughness-channel-failure.txt` retains it. Corrected test keeps the nonzero variation gate. A Cycles allocation failure is preserved in `initial/render-memory-failure.txt`; rendering was reduced to 900×800, 16 samples and two threads, then completed successfully. Optional Codex implementation failed authentication and supplied no edits; Hermes authored and verified directly. No credential stores were inspected or modified.

## Reproduction
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, Node with Three/esbuild from package manifest. Build resolves local `node_modules` or sibling `iceland-pilot/node_modules`; offline viewer needs neither. Windows default paths in `run_checks.py` may be overridden with `BLENDER` and `NODE_EXE`. To use a standalone extracted archive, install its package dependencies locally. Run from this directory:

```text
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python run_checks.py
python package_delivery.py
```

Authoring overwrites model/poster; save manual edits separately. `run_checks.py` rebuilds the HTML and runs motion/source/parity/browser/theme checks with fatal failures and logs. Packaging verifies explicit required files and every ZIP entry hash on readback. There is no separate delivery-folder copy or hosted preview claim.

Mechanics/viewer/check lineage: Japan Cedar v1 and Iceland pilot at base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`. Three.js MIT license included. Research photographs/textures are not embedded. Changes restricted to `preview/malawi-v1/`; shared kit and other previews untouched. Collection context: 201 equally one-of-one boxes (195 countries, five oceans, Moon); this card supplies Malawi only. No blockchain access, deployment, integration or merge.
