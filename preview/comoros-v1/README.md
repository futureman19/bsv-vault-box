# Comoros v1 — Karthala & Perfume Isles

Open `comoros-v1.html` offline in Edge/Chrome: drag/touch rotation, open/close, reset and reduced-motion handling. Cosmetic inner collectible only; not minted, hosted, signed or a custody action.

HTML: **3,205,552 bytes**. GLB: **1,856,292 bytes**. All runtime assets embedded. `comoros.blend` is editable packed source, `comoros.glb` portable geometry, maps are procedural originals, and poster.png/jpg are actual Blender source renders. Source and evidence are packaged in comoros-source.zip with read-back SHA-256 inventory.

## Verified
- Independently reopened saved Blender source; hollow floor ray z=0.2650000155; ten hinge attachment pairs.
- 81 sampled poses, 64 moving / 39 static meshes, zero unintended intersections. Latch release 80 degrees before lid opening 105 degrees; named mating bearing contacts only excluded. Sampled surface tests are not continuous/manufacturing certification.
- Bidirectional evaluated-source/GLB vertex parity below 0.00001 units; packed maps and theme-specific crater depth, 18 petals, lid ancestry and seam bounds checked.
- Real GLTFLoader finite vertices and nondegenerate triangles; offline file:// desktop and 390x844 mobile touch emulation, native controls, drag, interrupted reset, reduced motion, full-open framing, zero HTTP requests/errors/overflow. Actual corrupted GLB invokes poster fallback. Separate no-JS poster check.
- Map variation, nonblank source poster, 81 staged runtime motion samples, invalid-pivot/nonfinite negative controls, strict HTML budget, ZIP/readback byte hashes.

## Visual limits
Original stylized interpretation of volcanic Comoros and ylang-inspired blossoms, not a traditional Comorian craft object or accurate topographic/botanical replica. The crater is visible but subtle at mobile size; flowers are simplified ribbons, vegetation small faceted patches and basalt broadly mottled rather than scanned. Turquoise seam and brass family hardware are invented design choices. Mobile emulation runs on desktop hardware, not a phone performance test. Human review was explicitly waived for this asset; technical acceptance does not imply photoreal equivalence.

## Reproduce
Python with Pillow and Playwright, installed Edge, Blender 5.2.1, Node with pinned package.json dependencies. Build uses local node_modules or sibling iceland-pilot node_modules; these are build-time only, not included in ZIP. `npm install` locally restores pinned dependencies if needed. `setup.py` is historical initial scaffolding requiring the Japan sibling; do not rerun over completed authored files.

Run `python maps.py`; Blender background with `--factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Blender on verify_theme.py, verify_source.py, verify_parity.py; `node tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`. Authoring overwrites generated files; preserve manual edits separately. Read recovery-notes.md for real failures and bounded camera correction. Three.js MIT license included. No blockchain, VPS, other previews or shared kit modified.
