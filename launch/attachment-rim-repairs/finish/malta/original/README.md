# Malta v1 — Honey Limestone & Harbour

Open `malta-v1.html` directly in Edge/Chrome: complete offline interactive collectible, no server or network assets. **HTML 1,997,011 bytes; GLB 906,108 bytes.** Source is `malta.blend`; actual source render is `poster.png`. All runtime assets are embedded. Drag/touch rotate, Open/Close, Reset and reduced motion are supported.

## Design and provenance
Research-backed brief was written before authoring. Honey-cream Globigerina-inspired ashlar walls surround a hollow liner. A blue harbour inlay carries an invented low angular bastioned peninsula, with small masonry blocks. This is not an accurate map of Valletta or reconstruction of a heritage building. The palette/geology references are linked in `design-brief.md`; no third-party photographs, scans or AI promotional substitutes are embedded. Geometry and maps are procedurally authored, not hand-sculpted.

Mechanism and viewer/test lineage: Japan Cedar pilot and Iceland pilot from base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`. The trimmed `mechanism.blend` is included. Shared kit and earlier previews are unchanged. Three.js MIT license is included.

## Verified
- Independent saved-source reopening: original lid/latch pivots, hollow interior floor at z=0.2650000155; ten hinge attachment pairs.
- 81 opening poses; 25 moving meshes and 125 static meshes, including all new ornaments; zero unintended surface intersections. Only named original mating bearing contacts excluded. Not continuous collision certification.
- Source/export nearest-world-vertex error 1.712013073529306e-7, below 1e-5. Three packed generated maps.
- Actual browser GLTFLoader: finite vertices, no degenerate triangles. All nine harbour/peninsula meshes owned by lid; real decoded base-color and green-channel roughness variation.
- Theme gates verify staggered ashlar count, concave bastion perimeter, relief height, warm palette and downward rays showing blue water on both sides. A detached-ornament negative control is rejected.
- Actual offline file:// Edge desktop and 390×844 touch-emulated mobile: drag/touch rotation, native open/close buttons, interrupted reset, 80-degree latch then 105-degree lid, reduced motion, full-open framing, no overflow, no external requests/errors. Actual corrupt GLB reaches parser and shows fallback; JavaScript-disabled poster verified.
- `inventory.json` hashes exact included bytes. `delivery-check.json` verifies source ZIP inventory and readback, explicit required deliverables and HTML budget. `.gitattributes` preserves exact bytes across Windows checkout.

## Visual verdict and limitations
Actual source render and desktop/mobile screenshots inspected. Water is readable on both sides of the peninsula even on mobile; no major clipping or broken geometry found. Pale stone is smooth and stylized rather than weathered photographic limestone. The relief reads as an abstract fortified landform, not uniquely Malta without its title. Source render has mild sampling grain (24 samples, no denoising). Open-view latch has a small apparent gap at this angle; inherited articulation is unchanged and sampled collision/hinge tests pass, but no engineering claim is made. Mobile emulation is not physical-phone performance. User waived per-asset review; technical completion is not user art approval.

## Real failures and fixes
Optional Codex lane exited 1 with expired-token HTTP 401, no changes accepted. Hermes implemented directly without touching credentials. Initial build exited 1 (`Cannot find module .../iceland-pilot/node_modules/esbuild/bin/esbuild`): the prescribed dependency directory existed but was empty. Installed the declared existing package dependencies locally in this new preview folder (`npm install --prefix preview/malta-v1 --no-audit --no-fund`); same build then passed. No asset acceptance thresholds were relaxed. Initial copy helper encountered missing Japan tests.mjs; inherited canonical Iceland motion tests were used instead. There were no geometry/collision acceptance failures.

## Reproduce
Python with numpy, Pillow, Playwright; installed Edge; Blender 5.2.1; Node.js. From this directory:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` (BLENDER environment variable can override local Windows Blender path).
5. `python package_delivery.py`

`verify_all.py` reruns build, motion, independent source/parity/theme and browser/fallback gates, logging each output and failing on any nonzero exit. Authoring regenerates source/GLB/poster; preserve hand edits separately. Build may use sibling Iceland dependencies only if local dependencies absent. Offline HTML has no such dependency. ZIP excludes node_modules/cache/backups and its own inventory envelopes.

Local artwork only: no blockchain queries, nodes, keys, minting, transactions, public hosting, VPS or production changes. Collection direction: 201 equally one-of-one designs. Cosmetic lid opening is not opening an on-chain seal. Branch backup only; integration belongs to the final collection card.
