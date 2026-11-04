# Nicaragua v1 — Ometepe / Twin Volcanoes

Open `nicaragua-v1.html` directly in Edge/Chrome. The actual GLB, runtime, maps and source-render poster are embedded. Drag/touch to rotate; Open/Close lid; Reset. No server or network dependency.

HTML **2,200,901 bytes**; GLB **1,075,524 bytes**. Editable packed source: `nicaragua.blend`; procedural maps and generator included. `mechanism.blend` is the unchanged trimmed Japan family mechanism, not Japan landscape art. Three.js license included.

## Verified
- Independently reopened source: hollow floor z=0.2650000155; ten hinge attachment pairs; 81 motion samples including all 20 moving and 39 static meshes, zero unintended intersections. Only explicit mating bearings excluded. Staged 80-degree latch then 105-degree lid.
- Bidirectional source/export nearest-vertex maximum error 1.712013073529306e-7 (<1e-5); three packed maps.
- Two genuine recessed crater meshes and connected island/lake all parented to lid. Deliberately detaching Maderas fails the ownership assertion; restoring it passes (postimplementation regression negative control).
- Real GLTFLoader geometry validation, finite vertices and zero degenerate triangles. Nonconstant portable color and green-channel roughness maps.
- Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: rotation, native open/close, interrupted reset, reduced motion, full-open projection, no horizontal overflow, no external requests or runtime errors. Actual corrupted embedded GLB exercises parser/poster fallback; no-JavaScript poster also checked.
- Poster is rendered from saved Blender source, not generated promotional art. Inventory/archive hashes verified on readback; final staged Git bytes checked separately.

## Visual limits and correction history
Original sourced written brief is the design reference; there is no user-approved Nicaragua concept image. Twin peaks, green connecting island, blue lake inset and dark granular stone read clearly. Geometry is intentionally faceted, lake is enamel-like, and body grain is procedural rather than scanned lava. Crater recesses are proven geometry but remain subtle at normal mobile size even after widening the openings and raising the viewing camera. Do not call this photorealistic, geographically exact or visually human-approved. From the open front view the landscape is naturally hidden behind the lid. The upright released hasp can appear detached at a distance; source bearing hierarchy and sampled attachments are checked, not manufacturing-certified.

`initial/narrow-craters-mobile.png` retains the initial visual weakness. The build initially failed because the mandated main-checkout dependency directory was empty; an npm install timed out. Recovery copied already-installed compiler dependencies into this preview's ignored node_modules; no shared files changed. The final build uses these local dependencies. No asset/clearance gate was waived. Reduced-motion assertions wait for observed endpoint state, rather than assuming an overloaded browser renders within 70ms.

Mobile is desktop touch emulation, not physical-phone performance. Collision results are sampled surface checks, not continuous clearance. Art is not minted, hosted, signed, deployed or on-chain; no wallets, keys, node services or chain queries were accessed. Only this new preview folder is delivered. No merge authorized.

## Reproduce
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, and Node with Three/esbuild dependencies from `package.json` required only for build/test. Run `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Blender separately on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`. Regeneration overwrites generated assets. `author.py` retains family helper naming such as Cedar/clasp seat internally; these are stone-assigned mechanical parts, not wood art.

Source archive excludes node_modules and Blender backup files. Exact nonrecursive hashes are in `inventory.json`; `delivery-check.json` covers ZIP readback. Next: integrate this backed-up branch with the full collection, without interpreting this art check as any custody approval.
