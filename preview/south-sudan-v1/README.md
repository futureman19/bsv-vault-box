# South Sudan v1 — Sudd & Papyrus

Open **south-sudan-v1.html** directly in Edge/Chrome. Offline interactive 3D, drag/touch rotation, Open/Close, Reset and reduced motion. Cosmetic inner collectible only: no mint, transaction, deployment or custody action.

## Delivered
- HTML **4,121,283 bytes**; GLB **2,495,892 bytes**.
- `south-sudan.blend`: packed editable Blender source; `south-sudan.glb`: exported mesh/maps.
- `poster.png` / `.jpg`: actual source render, not AI artwork. Desktop/mobile PNGs are actual file:// browser captures.
- Source scripts, generated maps, trimmed inherited `mechanism.blend`, MIT Three license, exact inventory and source ZIP.

## Verified
- Independently reopened source: 221 moving and 99 static meshes; 81 staged poses; zero unintended surface intersections. All 193 wetland/plant meshes are lid-owned. Only named mating hinge/latch bearings excluded. Hollow-floor ray z=0.2650000155; ten hinge attachment pairs checked.
- Geometry source/export bidirectional maximum vertex error 1.712013073529306e-7, below 1e-5. Four packed source maps; actual browser decoded color ranges 41, 194, 59 and roughness green-channel range 78.
- 21 papyrus stems and 3 low banks; maximum ornament Z 2.5555148125, within contract. Three downward rays hit exposed water between vegetation patches. This is sampled visibility, not hydrology/geographic fidelity.
- Real Edge file:// desktop 1440x1080 and mobile 390x844 touch emulation: actual GLTFLoader finite/nondegenerate geometry, drag/touch rotation, native Open/Close, interrupted Reset, reduced motion, full-open frame bounds, zero external HTTP requests and unhandled errors, no horizontal overflow. Corrupt actual GLB produces poster fallback; no-JS poster also checked. `browser-check.json` contains measured geometry and renderer.
- Motion unit tests: 2 pass, 0 fail, including invalid-asset rejection. Deliberately detaching one stem makes `verify_theme.py -- --negative` fail with `AssertionError: Detached wetland ornament` (preserved in theme-negative.txt). This is a post-implementation negative control, not a historical art failure or TDD claim. No positive acceptance failure occurred.
- Exact SHA-256 inventory, explicit required file set, ZIP byte-for-byte readback and staged-Git byte checks.

## Honest visual limits
A brief-driven stylized wetland keepsake, not a surveyed Sudd map, botanical specimen, traditional craft reproduction or photorealistic artwork. Water reads as a glossy turquoise inset with three planted islets rather than flowing channels. Umbrella papyrus is present but delicate at mobile size. Ochre silt-inspired fibre texture reads as woven/bamboo/wood-like material more than literal sediment; this ambiguity remains disclosed. Geometry and maps are procedural, not scans or hand sculpture. Render has light sampling grain. No prior supplied concept or user art approval is asserted.

Mechanism/body joinery/viewer lineage: Japan v1's trimmed mechanical base, with newly authored wetland ornament and surface maps. Legacy `cedar-*` map filenames are retained solely as generator interface names; no Japan tree/forest artwork is reused. Rear/interior and brass fittings are collection-family extrapolations. Collision checks sample surfaces, not continuous volumes/manufacturing tolerances; mobile emulation is not physical-phone performance.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/playwright; installed Edge; Node build tooling. Shared pilot node_modules was absent, so pinned package.json dependencies were installed only here; node_modules is ignored and never embedded as a directory. Viewer runtime assets are fully embedded.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs`.
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

`setup.py` records the initial adaptation from sibling Japan v1 and is not needed to rebuild this self-contained source folder. Regeneration overwrites editable source/render/export: preserve manual variants separately. Repackage after rebuilding because exact hashes change. The source ZIP excludes dependencies and .blend backups. No public hosting, chain storage or network persistence is claimed. Branch backup only; integration is a separate card. Per-asset review was explicitly waived until the complete collection exists.
