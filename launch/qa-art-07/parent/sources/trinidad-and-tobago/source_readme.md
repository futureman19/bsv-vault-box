# Trinidad and Tobago v1 — Scarlet Rhythm

Open `trinidad-and-tobago-v1.html` directly in Edge/Chrome. All model bytes, runtime, maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. Cosmetic movement only; no wallet, node, chain, minting, hosting or custody changes.

## Delivered
- HTML: **2,409,834 bytes**, strictly below 5,000,000.
- GLB: **1,228,448 bytes**; 21,652 triangles, 83 runtime meshes, 5 materials.
- Packed editable `trinidad-and-tobago.blend`; trimmed inherited `mechanism.blend`; author/map/build/test scripts; generated portable maps; actual-source poster; offline desktop/mobile captures.
- `inventory.json` records exact SHA-256 and byte identities. `delivery-check.json` verifies the source ZIP against that inventory. Local `.gitattributes` preserves exact bytes in Git. Dependencies and Blender backup files are excluded.

## Design and visual verdict
A scarlet enamel keepsake chest with two silver steelpan-inspired bowls, 22 convex note islands, rolled rims, black seam/feet and brass family hardware. The research-backed written brief predates modeling; no approved concept illustration was supplied. Steelpan is Trinidad and Tobago's national musical instrument. This is an invented decorative interpretation, not a playable/tuned instrument or a claim to represent every culture of both islands. Geometry and maps are script-authored, not scans or hand sculpture.

Actual mobile visual inspection: both bowls and the whole box are readable and unclipped; note islands are subtle, not individually countable at default mobile scale. Enamel has a visibly procedural rippled/hammered finish rather than flawless smooth lacquer. Brass clasp is deliberately inherited and bulky; the dark seam is prominent. Actual-source render has some sampling noise (denoising disabled). The open front view shows the hollow cavity and hinges but hides the top-side pans behind the lid; saved-source/runtime ancestry establishes that they remain attached. No photorealism, exact historical reproduction or physical-phone performance claim.

## Verification actually executed
- `source-check.json`: independently reopened packed source, hollow-floor ray z=0.2650000155; 10 hinge attachment pairs; 81 staged poses, all 44 moving versus 39 static meshes and latch versus lid, zero unintended surface intersections. Exemptions only for named original mating bearings. Sampled surface checks, not continuous collision/manufacturing proof; intentional co-moving skirt/bowl contacts are not classified as collisions.
- `parity-check.json`: source/export bidirectional nearest-vertex maximum error 1.712013073529306e-7 (<1e-5), three packed images.
- `theme-check.json`: two concave bowls, 22 notes, all 28 pan parts lid-owned, depth .20, upward playing-surface normals, exact baseline pivot matrices. Deliberately detached note rejected by ownership oracle.
- `motion-check.json`: 81 poses, latch 80° first then lid 105°; three malformed asset negative controls rejected.
- `browser-check.json`: Edge file:// desktop 1440×1080 and touch-emulated mobile 390×844 on RTX 4060; actual GLTFLoader: zero nonfinite/degenerate geometry; native open/close, drag/touch rotation, mid-motion reset, reduced motion, no overflow/external HTTP requests/errors; open maximum absolute projected NDC 0.892365. Actual corrupt GLB reached parser and displayed fallback.
- `extended-check.json`: nonblank source poster; real decoded colour/roughness channels vary, scarlet red dominance; 28 runtime lid-owned pan meshes; no-JS mobile poster. Mobile is emulation, not phone hardware.

## Real failure and correction
`theme-initial-failure.txt` retains an actual failing check: all 22 convex note meshes had downward quad normals. Reversed those quad windings without relaxing the test, regenerated source/GLB/poster, then reran theme, source, parity and browser checks successfully. Initial build also found the prescribed sibling dependency directory empty; installed the exact pinned dependencies locally in this new folder instead. No other preview was modified. Corrupted-GLB and detached-note negatives are intentional test cases, not shipped faults.

## Reproduction
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with pinned Three 0.180.0 and esbuild 0.25.11. Run in this directory:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Same Blender invocation for `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
5. `python build.py`; `node tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.
Build uses local dependencies, or the sibling Iceland toolchain if present. Included mechanism makes source authoring independent of sibling assets. Regeneration overwrites generated source/assets; preserve manual edits separately. Update documented sizes after regeneration. Three.js MIT license included. Model remains off-chain/local; branch backup is not publication, integration or art approval.
