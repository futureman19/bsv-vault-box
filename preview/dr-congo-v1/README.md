# DR Congo v1 — Raffia & River

Open **dr-congo-v1.html** directly in Edge/Chrome. The complete model, maps, Three.js runtime and actual Blender-rendered poster are embedded. Drag/touch to rotate, open/close the lid, reset; reduced motion snaps to the requested pose. This is a cosmetic inner collectible, not an outer custody container or transaction.

## Delivered
- Standalone HTML: **2,960,420 bytes**, strictly below 5,000,000.
- GLB: **1,620,404 bytes**.
- `dr-congo.blend`: packed editable Blender source; `mechanism.blend`: inherited trimmed family articulation source.
- `maps/`: original procedural 512×512 raffia-inspired color, roughness and normal maps.
- `poster.png` / `poster.jpg`: actual source render, not AI artwork. Desktop/mobile PNGs are actual offline browser captures.
- `dr-congo-v1-source.zip`: reproducible source, assets, evidence and inventory. `delivery-check.json` verifies archive inventory and every payload byte on readback.
- `design-brief.md`: research and measurable contract written before modeling.

## Design and limits
Kuba raffia textile traditions documented by the Met inform the ochre/dark geometric panels; UNESCO's description of Salonga and the central Congo basin informs the forest-and-river lid. This is an original stylized synthesis, not a reproduction of a named textile, sacred/royal motif, geographic river map, or an assertion that one tradition represents all Congolese communities. No research photographs or textile pixels were copied. Full citations and attribution limits are in the brief.

The broad chest has brass fittings, dark satin framing, a hollow liner and low forest relief. Weave is a generated portable surface pattern, not individually interlaced physical fibers. Canopies are rounded abstract foliage, not botanical trees; the river is a continuous flat enamel-like inlay, not transparent moving water. Hardware is simplified. Back/interior details are design extrapolations. No photoreal equivalence, manual sculpture, real harvested materials or user visual approval is claimed.

Two bounded presentation corrections: lower and separate the canopy banks to reveal the river, then raise the default browser camera to make the water readable on mobile. Final mobile visual inspection confirms the winding strip and full box fit. At low user-selected viewing angles foliage can still occlude the river. The source poster uses a lower independent studio camera and lighting, not a pixel-identical browser camera.

## Actual verification
- Real GLTFLoader: **18,916 triangles, 154 meshes**, zero nonfinite vertices or degenerate triangles. Final source and GLB have three packed portable maps. Loader reads variation from the proper glTF channels: color red range 170, roughness GREEN range 41, normal red range 12.
- Independently reopened saved source: exact inherited lid/latch local pivots; 91 lid ornaments; 130 connected river vertices; 63 downward centerline rays hit exposed water. Width 3.72000003, depth 2.38000011; measured relief 0.24523635 above lid.
- **81 opening samples, all 107 moving and 47 static meshes, zero unintended surface intersections.** Latch-vs-lid also tested; only explicitly named mating bearing contacts excluded. Ten overlapping attachment pairs verify hinge/body/lid seating. Hollow floor ray z=0.2650000155.
- Staged motion: latch releases 80° before lid opens 105°; source pivots unchanged. Source/export nearest-vertex error both ways **1.712013073529306e-7**, below 1e-5 tolerance. This is sampled surface collision and nearest-vertex parity, not continuous collision proof, manufacturing certification or exact topology/material-render equivalence.
- Offline `file://` Edge: desktop 1440×1080, mobile 390×844 touch emulation. Actual mouse/touch drag, native open/close, reset during motion, reduced motion, full-open silhouette projection, no horizontal overflow, no external HTTP requests or JS errors. Corrupt bytes reached GLTFLoader and showed poster/disabled controls; no-JS poster separately tested.
- Mobile is desktop RTX 4060 browser emulation, not physical-phone performance. No FPS guarantee.
- Five deliberately altered observed-feature records are rejected by the theme predicate; three invalid geometry records rejected by the motion test. These are post-implementation negative controls, not test-first claims or modified-model collision controls.
- `source-check.json`, `theme-source-check.json`, `hinge-attachment-check.json`, `parity-check.json`, `browser-check.json`, `theme-check.json`, raw output text, `inventory.json`, and `delivery-check.json` contain evidence.

## Real failures and fixes
`initial/theme-output.txt` preserves a real failed assertion: the first test incorrectly measured roughness from red, yielding range 0. Standard glTF roughness is green; the corrected test reads green and measures 41, retaining the strict variation requirement. `initial/theme-observed.json` preserves the failed measurement. Early poster/desktop captures preserve the too-high/river-obscuring canopy.

The first maps run also failed on NumPy int8 + 128 overflow; normal-map intermediate arithmetic was changed to int16 before conversion to uint8. No fabricated successful output replaced this failure. The optional Codex CLI lane failed HTTP 401/token refresh and made no asset changes; all implementation and verification were performed directly by Hermes. A transient Git Bash fork retry recovered on the final build run.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; Node.js with Three.js/esbuild dependencies from package.json; installed Edge. No blockchain node is involved. From the repository root:

```text
python preview/dr-congo-v1/maps.py
blender --background --factory-startup --python-exit-code 1 --python preview/dr-congo-v1/author.py
python preview/dr-congo-v1/build.py
node preview/dr-congo-v1/tests.mjs
blender --background --factory-startup --python-exit-code 1 --python preview/dr-congo-v1/verify_source.py
blender --background --factory-startup --python-exit-code 1 --python preview/dr-congo-v1/verify_parity.py
python preview/dr-congo-v1/verify_browser.py
python preview/dr-congo-v1/verify_theme.py
python preview/dr-congo-v1/package_delivery.py
```

Use the installed Blender executable path where `blender` is not on PATH. Authoring and checks resolve paths from their own directory; regenerated outputs overwrite manual source edits. Build uses local node_modules or sibling iceland-pilot/node_modules; for an extracted source archive run npm install in its directory. Dependencies are build-only, never runtime downloads. The included generated author.py is standalone with the included trimmed mechanism; no Japan source directory is needed for authoring. Three.js MIT license included.

## Provenance, storage and scope
Mechanism, runtime and harness adapted from Japan Cedar v1 on local base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. Japan's cedar tree, finger joints, granite feet and textures were not retained. No prior acceptance evidence was reused. All additions are confined to this folder; shared kit and other previews remain unchanged. Branch backup only, no merge or public deployment.

Not minted, signed, uploaded, hosted or stored on-chain. Hashes establish bytes, not authenticity, ownership or permanent availability. Off-chain storage/pinning and issuance remain unimplemented. Collection direction: 201 equally one-of-one designs, no launch accessories. No wallet, secrets, blockchain queries, broadcasts or VPS access occurred. Per-asset review was waived by the task; completion is technical/art-delivery acceptance, not an unrecorded human approval.
