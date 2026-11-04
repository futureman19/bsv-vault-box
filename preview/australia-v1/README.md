# Australia v1 — Bungle Bungle

Open **australia-v1.html** directly in Edge/Chrome. Complete offline interactive collectible, **3,361,160 bytes**; standalone **australia.glb: 1,914,724 bytes**. Drag/touch to rotate, Open/Close lid, Reset view, reduced-motion snapping. Nothing is minted, on-chain, signed, deployed or hosted. This is the inner collectible artwork, not outer custody enforcement.

## Design
An invented sandstone keepsake chest inspired by Purnululu's orange and dark banded domes: five individual eroded ring-loft forms, wide stone body, three portable procedural color/roughness/normal maps and restrained brass family hardware. Research and the pre-model measurable contract are in `design-brief.md`. No third-party images, scans, Indigenous designs or sacred symbols are used. This selected landscape does not represent all Australia. The brief—not an imagined pre-approved illustration—is the design reference.

## Files
- `australia.blend`: packed editable, Blender-script-authored source, not hand sculpture. `mechanism.blend`: unchanged trimmed inherited family mechanism. `author.py`, `maps.py`: reproducible generators.
- `australia.glb`: portable mesh/maps; `australia-v1.html`: all runtime bytes embedded.
- `poster.png` / `poster.jpg`: real source render; browser desktop/mobile closed/open, rear-open, corrupt-loader and no-JS screenshots.
- Acceptance JSONs and raw output TXT files. `initial/` preserves the missing-dependency failure and rejected low-camera presentation.
- `inventory.json`: exact per-file SHA-256 and bytes. `australia-v1-source.zip`: source/assets/evidence, excluding dependencies/backups. `delivery-check.json`: verified ZIP readback, explicit required-file inventory and exact principal bytes/hashes. Hash envelopes avoid circular self-reference.

## Verified, with bounded claims
- Actual Three.js GLTFLoader: **21,314 triangles, 60 meshes, 3 materials**, zero nonfinite vertices or degenerate triangles. Three decoded 512×512 maps; color range 155, roughness **green-channel** range 81, normal red-channel range 86.
- Independently reopened saved source: **21 moving + 39 static meshes**, all included in **81 motion samples**, zero unintended surface intersections. Only original named concentric hinge/latch bearings exempt. Ten hinge attachment contacts and hollow floor ray at z=0.2650000155 pass. This is sampled surface collision evidence, not continuous collision/manufacturing certification.
- Same inherited pivot matrices; latch releases 80° before lid opens 105°. Motion tests exercise 81 poses, clamped endpoints and invalid-runtime-asset negative controls.
- Source/GLB nearest-vertex parity both ways: maximum **1.712013073529306e-7** units, below 1e-5. Three packed maps independently reopened.
- Five lid-owned domes, separated XY footprints, heights ≤2.85; deliberate detached-ornament negative rejected. Foreground footprint slightly exceeds the initial nominal -0.65 Y target (to -0.69545), disclosed rather than disguised; still comfortably inside lid and full clearance sample.
- Offline **file:// Edge**, desktop 1440×1080 and touch-emulated mobile 390×844: native controls, rotation, open/close, interrupted reset, reduced motion, zero external HTTP requests/JS errors/overflow. Actual corrupt GLB reaches parser and triggers poster; no-JS poster decodes. Full-open projection max absolute NDC **0.97184214365**, under 1. NVIDIA RTX 4060 desktop GPU; no phone-performance claim.
- Exact byte ceiling negative control rejects 5,000,000 bytes; ZIP readback validates every inventoried entry. Scoped `* -text` preserves bytes through Git; staged blobs are checked independently.

## Failure and correction history
1. Build genuinely failed: instructed shared `preview/iceland-pilot/node_modules` existed but was empty. Raw failure retained in `initial/build-missing-deps.txt`. Installed pinned Three/esbuild dependencies **inside this new directory only**, then build passed. No shared dependency contents or prior art changed.
2. Initial mobile visual review could identify only four of the five domes because the inherited low camera hid one. Retained `initial/mobile-four-visible.png` and initial passing technical browser report. Raised viewer camera from (-5,3.7,7) to (-4,5.8,7), rebuilt and reran all browser/extended tests. Final actual mobile review identifies three rear and two front domes. Geometry and poster were not substituted.

## Honest visual limits
Technical gates pass; this is **stylized art, not photorealistic or geographically exact**. Bands are stronger/more regular than natural weathering and can resemble painted wood in the source render; the browser has a more sandstone-like appearance. Rounded domes remain simplified, fittings blocky, and the dark mineral seam pronounced. Dome contours overlap slightly from the hero camera but all five are countable. Lid-top artwork faces away in the front open pose; rear-open evidence shows it. Hardware is cosmetic, not engineering certification. No human per-asset approval is claimed; task explicitly waived that review until collection completion.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/playwright; installed Edge; Node.js with pinned Three 0.180.0 and esbuild 0.25.11. Build-time dependencies only; delivered HTML has none. Three MIT license included.

From this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Repeat Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme_source.py`.
5. `node --test tests.mjs`
6. `python build.py`
7. `python verify_browser.py` and `python verify_extended.py`
8. Inspect actual screenshots; `python package_delivery.py`.

Build uses local node_modules first, sibling pilot fallback second. All source-authoring inputs are included; no sibling art file is required. Authoring overwrites source/export/poster; preserve manual variants separately. Browser/render evidence and hashes must be regenerated after changes. `lineage.json` records original mechanism/viewer/test input hashes.

Scope: only `preview/australia-v1/` additions, on `art/australia-v1`; branch backup authorized, merge deferred to collection integration. No production docs, shared art kit, previous previews, chain/node/wallet/key systems, funds, VPS or external messaging touched. Collection direction remains 201 equally one-of-one designs, accessories deferred.
