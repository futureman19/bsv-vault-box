# Bosnia and Herzegovina v1 — Sarajevo Copper

Open **bosnia-and-herzegovina-v1.html** directly in Edge/Chrome. Complete offline 3D viewer: **2,420,909 bytes**, GLB **1,238,300 bytes**. Drag/touch rotation, staged open/close, interrupted Reset and reduced motion are supported. This is local collectible artwork, not minted, hosted, signed or blockchain-connected.

## Design and provenance
An original procedural tribute to Sarajevo's Kazandžiluk copperwork: satin hammered copper skins, an eight-petal outlined brass rosette on a circular tray, punched-bead perimeter, patina-colored seam and dark bronze interior/feet. Research and the pre-model measurable contract are in `design-brief.md`. No historic pattern or third-party image was copied. Not an artisan-made or culturally authenticated object, and not a representation of every community in the country.

`bosnia-and-herzegovina.blend` is the packed editable Blender 5.2.1 source; `.glb` contains portable geometry/maps. `poster.png` is an actual source render, not an AI illustration. `maps.py` authors three 256px maps. `mechanism.blend`, motion, viewer and verification lineage come from the repository's Japan/Iceland pilots at base ff5d78f, adapted in this new folder only. Three 0.180.0 MIT license is included.

## Verified evidence
- `source-check.json`: independently reopened saved source, hollow floor ray at z=0.2650000155; **81 poses, 104 moving meshes and 35 static meshes, zero unintended sampled surface intersections**. All lid ornament included. Only named concentric bearings exempt. Ten explicit hinge attachment surface pairs pass in `hinge-attachment-check.json`. This is sampled BVH evidence, not continuous mechanical or manufacturing certification.
- `parity-check.json`: source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5 in both directions; three packed source images.
- `theme-check.json`: eight petals, 76 border beads, bounded ornament height, lid ownership, exact inherited pivot matrices. A deliberately detached petal was rejected then restored; this is an exercised negative control, not a historical implementation failure.
- `browser-check.json`: actual GLTFLoader reports **23,364 triangles, 139 meshes, four materials**, no nonfinite vertices or degenerates. Offline file:// desktop 1440×1080 and touch-emulated 390×844 mobile: native open/close, drag, reset while moving, reduced motion, no external HTTP requests, no JS errors and no horizontal overflow. Full-open projection max absolute NDC <0.927. Genuine corrupted GLB input produces a caught parser error and poster fallback.
- `extended-check.json`: actual decoded color, roughness (green channel) and normal maps have nonzero variation; eight runtime petals remain lid descendants; no-JS poster loads, accessible canvas name and visible country copy checked.
- `motion-output.txt`: staged motion/clamps and invalid-asset negative tests. `delivery-check.json`: strict <5,000,000-byte gate, oversized negative control, required files and exact SHA-256 ZIP readback. `inventory.json` lists exact payload identities; inventory/archive/check envelopes exclude themselves to avoid circular hashes.
- Source poster, mobile closed and opened rear browser views were visually inspected. Complete framing, legible country title, readable rosette, no major visible broken geometry. The rear image partly conceals joints; attachment claims rely on independent source geometry checks, not an overclaimed screenshot.

## Honest visual and test limits
Stylized metalwork, not photorealism. The source render has visible sampling grain; copper reads partly as matte copper-colored coating, with schematic wire-outline petals rather than deeply embossed artisan relief. The cool seam is an intentionally decorative patina strip, not proof of a watertight seal. Hardware is inherited and simplified. No physical-phone performance, FPS, full continuous collision proof, historical-pattern fidelity or exact material-metrology claim.

No unplanned model/gate failure occurred during this run; deliberate negative controls prove selected assertions reject invalid inputs. Shared `iceland-pilot/node_modules` existed without its compiler, so pinned dependencies were installed **only in this new folder**, not into the shared preview. No dependency upgrade. No blockchain, VPS, production-site or sibling-preview changes.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge and Node.js. In this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python build.py`, `python verify_browser.py`, `python verify_extended.py`
7. `python package_delivery.py`

Build resolves local pinned dependencies, falling back to sibling pilot dependencies only if present. The delivered HTML never loads them or anything else from the network. `setup.py` records the initial adaptation of the base repository; **do not rerun it over final scripts**. Normal authoring uses the included mechanism and relative paths. Regeneration overwrites source/export/render: retain manual variants separately, rerun gates, update documented byte metrics and inventory. Source ZIP excludes dependencies/backups. Per-asset human review was waived for this collection batch; branch backup only, no merge. Final integration is handled by the pre-existing collection integration card.
