# United Kingdom v1 — Slate & Walled Meadows

Open `united-kingdom-v1.html` directly in Edge/Chrome. Complete offline HTML **3,062,051 bytes**; GLB **1,707,576 bytes**. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion supported. Cosmetic collectible only, not a custody operation.

## Design and files
Research-backed written brief preceded modeling. Welsh slate and Yorkshire dry-stone field landscapes informed this selective UK interpretation; not a geographic replica or representation of every UK nation. Script-authored Blender source, generated portable maps, original compositional design. No scans, third-party photographs or AI promotional image substitutes.

- `united-kingdom.blend`, `united-kingdom.glb`: editable source and portable export.
- `mechanism.blend`: unchanged trimmed Japan mechanism; shared base kit remains untouched.
- `poster.png` / `.jpg`: actual source render. Desktop/mobile closed/open/rear/fallback screenshots: actual offline browser.
- `design-brief.md`, scripts, maps and JSON/raw-output evidence included.
- `inventory.json`: exact bytes/SHA-256; `delivery-check.json`: source ZIP readback, required artifact coverage and archive hash. Inventory excludes itself, archive and delivery envelope to avoid self-reference.

## Verified
- Independently reopened source: 81 opening poses, all **117 moving and 155 static meshes**, zero unintended surface intersections. Latch-versus-lid tested. Only named coaxial bearing pairs excluded. Ten hinge attachment overlaps and hollow floor ray at z=0.2650000155 passed. Sampling is not continuous collision or manufacturing proof.
- Exact inherited pivot matrices checked. A deliberately detached wall is rejected by the theme oracle. Runtime motion tests reject absent pivots, empty geometry and nonfinite bounds; staged 80-degree latch / 105-degree lid endpoints pass.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7** (<1e-5). Three packed images; browser decodes varying color and green-channel roughness maps.
- Real GLTFLoader: **22,320 triangles, 275 meshes, 8 materials**, zero nonfinite vertices or degenerate triangles.
- Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, drag, interrupted reset, reduced motion, no horizontal overflow, no external requests or errors. Full-open projection max absolute NDC <0.893. Corrupt actual GLB bytes produce a caught parser error and poster fallback; no-JS poster tested.
- Browser used desktop RTX 4060. No physical-phone, FPS, continuous clearance or photorealism claim.

## Visual verdict and limitations
Complete silhouette and pale field boundaries read on mobile. Body reads as regular slate-tiled masonry rather than fractured natural slabs. Meadow is shallow, smooth and stylized; relief is less evident at mobile scale. Upright coping is conspicuous and can read as a stone palisade rather than fine traditional dry-stone craft. Gold hardware is simplified; green seam is an invented decorative mineral reveal, not living grass sealing a box. Poster retains modest Cycles sampling noise. These are disclosed v1 art limitations, not reference-equivalence claims. No supplied/previously approved UK artwork existed to match.

## Failure retained
Initial build failed because the prescribed main-checkout dependency directory was empty. `initial/build-missing-toolchain.txt` retains the real failure. Installed the pinned package dependencies inside this new folder, reran unchanged build and all browser gates successfully. Negative controls are deliberate postimplementation regression checks, not test-first development.

## Reproduce
Python with numpy/Pillow/playwright, installed Edge, Blender 5.2.1, Node.js build tooling (not a blockchain node). Run `npm ci --ignore-scripts --no-audit --no-fund` in this folder, then `python maps.py`, Blender `--background --factory-startup --python-exit-code 1 --python author.py`, and `python build.py`. Run Blender on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; run `node --test tests.mjs`, `python verify_browser.py`, `python verify_extended.py`, and `python package_delivery.py`.

`setup.py` records the initial mechanical/viewer adaptation and requires sibling Japan input; it is not required for rebuilding the included standalone author/viewer scripts. Regeneration overwrites generated outputs; preserve manual edits separately. Three runtime MIT license included. node_modules, caches and Blender backups are not delivered. All runtime bytes are embedded; build dependencies are not runtime requests.

No minting, keys, wallet/node startup, chain queries, uploads, deployment or on-chain storage performed. Branch backup only; integration into the 201-design collection is separate.
