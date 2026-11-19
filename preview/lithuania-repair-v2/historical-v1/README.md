# Lithuania v1 — Curonian Dune & Lagoon

Open **lithuania-v1.html** directly in Edge/Chrome. Entire runtime, model, maps and real source-render poster are embedded. Drag/touch rotates, Open/Close stages the latch and lid, Reset restores the camera, reduced motion snaps. Cosmetic art only; no minting, chain query, wallet, deployment or custody action.

## Delivery
- Standalone HTML: **2,789,627 bytes**, strict ceiling 5,000,000.
- GLB: **1,457,040 bytes**.
- `lithuania.blend`: editable packed source; `mechanism.blend`: inherited trimmed mechanical baseline.
- `maps/`, `maps.py`, `author.py`: procedural—not photographic—materials and Blender-authored geometry.
- `poster.png`/`.jpg`: actual source render, not AI art. Browser screenshots are actual offline Edge captures.
- `design-brief.md`: sourced visual contract written before modeling.
- `inventory.json`, `delivery-check.json`, source ZIP: exact-byte inventory and archive readback.

## Verified evidence
`source-check.json`: independently reopened source, 40 moving and 35 static meshes, **81 sampled poses with zero unintended surface intersections**. Every dune/vegetation/inset mesh participates. Only named concentric inherited hinge and latch bearings are excluded. Ten hinge-attachment overlaps are recorded; interior ray reaches the floor at z=0.2650000155. Sampling is not continuous collision or manufacturing certification.

`parity-check.json`: bidirectional source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed source maps. Not a byte-identical re-export claim.

`theme-check.json`: dune spans X ±1.4, maximum z 2.3429551; 22 shoulder clusters and lagoon belong to lid; both pivots independently compared with the baseline.

`browser-check.json`: actual GLTFLoader sees **14,192 triangles, 75 meshes, five materials**, no nonfinite vertices or degenerate triangles. Offline file:// desktop 1440×1080 and touch-emulated mobile 390×844 pass native open/close, rotation, interrupted Reset, reduced motion, no overflow, no external HTTP requests, no runtime errors. Full-open maximum projected extent 0.919519 is inside viewport. Genuine corrupted GLB produces caught parser error and poster fallback. `extended-check.json` adds no-JS poster, nonempty source poster and real decoded texture variation (roughness measured in green channel).

A deliberate detached-dune negative control is rejected by runtime lid-ancestry validation; corrupt-GLB and invalid asset fixtures also demonstrate failure-capable checks. No unexpected gate failure occurred in this run; no fabricated failure-and-fix is claimed. `motion-output.txt` contains the actual staged motion and invalid-input test run.

## Visual verdict and limitations
Usable stylized coastal collectible, not photorealism or geographic reconstruction. Actual source and mobile images were visually inspected: complete closed silhouette and readable pale sand/teal inset/brass. The low relief reads as a manufactured sandbar applique more than a natural shoreline, the green shoulder is subtle, and fine body ripples can resemble pale wood grain. Source render retains mild sampling noise. These are disclosed visual limits, not evidence of exact Curonian topography, artisan craft or user approval. The Curonian Spit is shared with Russia; this design is a Lithuanian coastal interpretation, not an exclusive attribution. Mobile emulation ran on RTX 4060, not a physical phone. Human asset review is deferred to full-collection review per explicit task direction.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/playwright; installed Edge; Node with pinned package dependencies. The prescribed shared pilot dependency directory was empty (actual esbuild missing); dependencies were installed only in this new folder, not another preview. node_modules is excluded. No blockchain node was used.

From this directory: `npm ci --ignore-scripts --no-audit --no-fund`; `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

`setup.py` documents one-time derivation from the read-only Japan pilot; it is not needed for regeneration and requires the sibling files. Remaining authoring/build checks resolve local paths. Regeneration overwrites source/artwork; preserve manual changes separately. Three.js MIT license included. Research sources are factual inspiration, with no borrowed photos/textures. Source archive excludes dependencies and backups. Exact inventory excludes itself, ZIP and delivery-check to avoid recursive hashing.

Branch backup only: `art/lithuania-v1`; no merge or public hosting. Next step is the separately gated full-collection integration and visual review.
