# Venezuela v1 — Tepui / Cloud & Cascade

Open `venezuela-v1.html` directly in Edge/Chrome. Complete runtime, model, maps and actual-source poster embedded: **2,891,909 bytes**, below 5,000,000. Standalone `venezuela.glb`: **1,586,348 bytes**. Drag/touch rotation, Open/Close, Reset and reduced motion. Local cosmetic art; no custody change, mint, chain query, keys, node, hosting or production deployment.

## Design and honest visual verdict
Research-backed Canaima sandstone/table-mountain interpretation, not a named mountain replica. Broad warm rust body, brass hardware, flat-topped miniature with muted summit vegetation and slim continuous cascade into an ornamental pool. Source is script-authored Blender geometry and generated maps, not scans or hand sculpture. Written contract predates modeling; see design-brief.md.

Actual mobile and desktop-open screenshots inspected. Box, flat summit and pale cascade are readable and unclipped. **Material identity remains ambiguous:** warm mottling and chest fittings can still read as wood/clay rather than sandstone. The waterfall is an opaque decorative ribbon and the pool is an inlay, not fluid simulation or a realistic contained basin. Summit greenery is a flat compact treatment, not modeled vegetation. Dark reveal is visually broad, and hardware remains the simplified family design. Poster has sampling noise (denoising disabled); no photorealism/reference-equivalence claim. One material correction retained in initial/. Accepted autonomously under full-collection no-review directive, not represented as individual user art approval.

## Verified final bytes and behavior
- Independently reopened saved source: 20 moving and 39 static meshes; all 81 staged poses, no unintended intersections. Every terrain/water part included. Explicit mating hinge/hasp bearing contacts alone excluded. Ten hinge attachment overlaps and interior floor ray z=0.265. Sampled surface intersections, not continuous clearance/manufacturing proof.
- Both pivot matrices match included original mechanism.blend. 80-degree latch release precedes 105-degree lid. Node test covers 81 progress samples/endpoints and rejects invalid asset input.
- Bidirectional saved-source/export maximum nearest-vertex error 1.712013073529306e-7 (<1e-5). Three packed images. Geometry parity is not byte-identical export proof.
- Actual GLTFLoader: 59 meshes, 14,133 triangles, five materials, zero nonfinite vertices/degenerate triangles. Maps 512x512 and 256x256; decoded color ranges 146/41 and true green-channel roughness range 76.
- Independent theme check: flat top, cliff bounds, continuous 14-vertex cascade, exposed front rays at three heights, full lid ownership. Detached-parent negative control rejected. Actual relief .85 versus approximate brief .87; width 2.016 versus approximate 1.8, within recorded gate 1.7–2.2.
- Offline file:// Edge desktop 1440x1080 and mobile 390x844 touch emulation: native controls, rotation, open/close, interrupted Reset, reduced motion, no horizontal overflow, external HTTP requests or successful-run JS errors. Full-open projection max absolute NDC ~0.8924. Corrupted bytes reach real loader and show poster; no-JS poster tested separately. Desktop RTX4060 browser, not physical-phone performance evidence.
- Actual 900x820 source render decoded nonblack; separate marketing imagery not used. Inventory lists exact file SHA256 and byte sizes; source ZIP explicitly contains HTML/GLB/BLEND/maps/evidence and is read back entry-by-entry. Package resides here, no external delivery copy implied.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node 24 and locked Three/esbuild dependencies. `npm ci --no-audit --no-fund` in this folder (shared dependency folder was empty). Runtime HTML needs none of those build dependencies.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender identically with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node tests.mjs` (Windows background shell requires native `C:/Program Files/nodejs/node.exe` rather than shell shim).
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Authoring overwrites generated outputs; save manual edits elsewhere first. setup.py is historical one-time bootstrap from read-only sibling Japan, NOT a regeneration step; normal source rebuilding needs only included mechanism/maps/scripts. Read iteration-notes.md for real setup/build failures and bounded visual correction. The motion shell shim additionally failed `stdin is not a tty`; raw failure retained and native Node ran unchanged tests successfully. No gate was relaxed.

## Files and lineage
Packed editable venezuela.blend, standalone GLB/HTML, reproducible author/maps/viewer/build/test/package scripts, mechanism.blend, actual-source poster, desktop/mobile closed/open/rear/fallback/no-JS captures, acceptance JSONs and raw logs. Folder-local .gitattributes preserves bytes across Windows checkout. node_modules, .blend1 and caches excluded. `delivery-check.json` and ZIP excluded from their own payload inventory to avoid recursive hashes.

Mechanical/viewer/test lineage: Japan Cedar v1 on base ff5d78f; no sibling art/evidence changed. Three.js MIT notice included. Research sources cited for factual inspiration only; no third-party landscape imagery embedded. This branch is backup for separate final integration, not merged or publicly hosted. Collection remains 201 equally one-of-one designs; no accessories or on-chain storage claims.
