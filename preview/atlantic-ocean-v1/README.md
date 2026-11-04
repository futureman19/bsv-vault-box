# Atlantic Ocean v1 / Rift & Abyss

Open `atlantic-ocean-v1.html` directly in Edge/Chrome: complete embedded runtime, GLB, maps and actual-source poster. **HTML 2,017,782 bytes; GLB 940,488 bytes.** No network/server required. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion supported.

## Design and provenance
Brief-led interpretation of the Mid-Atlantic Ridge, sourced before modeling in `design-brief.md`: blue mineral enamel, a split low basalt ridge and turquoise axial channel. Procedural geometry/maps, not scans, exact geography, traditional craft or photorealism. No third-party research imagery used. Mechanism, runtime and verification lineage: read-only Japan cedar v1 from base commit ff5d78f. The trimmed mechanism is included. Three.js 0.180.0 MIT license included.

Final mobile visual review confirms two ridge shoulders and visible turquoise channel, partly occluded from the default oblique angle. Body patterns remain deliberately strong and stylized; reflected lid appears pale blue-gray, not uniformly navy. Hardware is simplified. In the open front view the tab/hinges can appear separated at this scale; ten saved-source attachment intersections and original pivots pass, but this is not mechanical engineering certification. The ridge sits on the outside of the lid and is naturally hidden in the open front view.

## Verification
- Saved source independently reopened. Hollow interior floor ray z=0.2650000155; ten hinge attachment pairs verified.
- **81 poses, all 19 moving and 39 static meshes; zero unintended surface intersections.** Latch against lid included; only explicit coaxial bearing contacts exempted. Sampled surface testing, not continuous/solid-volume clearance proof.
- Source/export geometry maximum nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed portable maps.
- Actual browser GLTFLoader: **14,476 triangles, 58 meshes, 5 materials**, zero nonfinite vertices/degenerate triangles. 256px color, roughness (green channel) and normal variation checked.
- Ridge gap minimum .3799999878; 24 interior channel ray samples visible; relief top 2.3108558655. Exact inherited pivot matrices preserved. Deliberately detached ridge rejected by ancestry test, then reloaded without saving mutation.
- Offline file:// Edge desktop 1440×1080 and mobile touch emulation 390×844: native open/close, drag/touch rotation, interrupted reset, reduced motion, no horizontal overflow, no external requests/errors. Full-open maximum absolute projected coordinate .926991 <1. Corrupt embedded GLB actually reaches parser and triggers poster fallback; no-JS poster also verified.
- Browser used RTX 4060, not physical phone performance. Source poster checked for nonempty actual rendered pixels. Exact SHA-256 inventory and ZIP byte readback are in delivery-check.json.

## Real corrections and limits
Initial mobile image in `initial/` hid most of the axial channel. Widened gap from .21 to .38 and raised viewer elevation; final screenshots show the split. Theme test initially ray-tested the channel boundary vertex at its far endpoint and hit the slab due to edge precision; raw failure retained. Corrected to one interior center ray per each of the 24 actual channel faces, without changing art or the visibility assertion. Missing inherited compiler dependencies initially prevented build; installed pinned dependencies locally inside this new folder. No fake output was substituted.

No photoreal/reference-equivalence, phone benchmark, mint, on-chain storage, custody, hosted release or deployment claim. This is one cosmetic inner collectible within the proposed 201 equally one-of-one collection.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node/npm. `npm ci --ignore-scripts --no-audit --no-fund`; `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`. Reopen checks: Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py`; then `python verify_browser.py`, `python verify_extended.py`, `python package_delivery.py`. Each command runs from this directory. Authoring overwrites source/export/poster; preserve manual edits separately. Local node_modules is build-only and excluded. No runtime dependency on sibling directories.

All deliverables and evidence are in this folder and source ZIP; no other preview, shared kit or production code was changed. Branch backup only; integration is a separate card.
