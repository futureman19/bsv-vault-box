# Brazil v1 — Amazon / Forest & River

Open `brazil-v1.html` directly in Edge/Chrome. This self-contained **4,468,142-byte** HTML embeds the **2,754,184-byte** GLB, Three.js runtime and poster rendered from the delivered Blender source. No network, server, wallet or installation is needed to view. Drag/touch rotation, zoom, Open/Close and Reset work; reduced motion snaps the articulation.

## Design and files

A warm earth-brown wooden keepsake box with dark forest-green lid, brass fittings and a miniature winding teal river between low forest banks. Landscape research and the pre-model measurable contract are in `design-brief.md`. This is an invented Amazon-inspired diorama, not a geographic/botanical replica, a traditional Indigenous pattern, or a claim about sustainably sourced timber. Teal water is a deliberate readability choice, not a scientific representation of Amazon sediment color.

- `brazil.blend`: packed, editable Blender source; named body, hardware, river, banks, trunks and crowns.
- `brazil.glb`: actual exported geometry and portable color/normal/roughness textures.
- `mechanism.blend`: copied trimmed Japan mechanical baseline, with unchanged lid/latch pivots and interior.
- `maps.py`, `author.py`, `maps/`: reproducible procedural source, not scans or hand sculpture.
- `poster.png` / `poster.jpg`: actual source render, no AI promotional replacement.
- Desktop/mobile closed/open and rear-open screenshots: actual offline browser captures.
- JSON reports and output text: actual test evidence; `initial/` retains rejected river-readability images and failure notes.
- `brazil-v1-source.zip`, `inventory.json`, `delivery-check.json`: source delivery, exact per-file SHA-256/byte inventory and archive readback. The delivery report and inventory exclude themselves to avoid recursive hashes.

## Verified acceptance

`python run_verification.py` passed source, parity, theme, motion, build, browser and extended gates. `python package_delivery.py` checks required artifacts and every archived byte.

- Independently reopened saved source. Hollow interior floor ray: z=0.2650000155. Ten explicit intersecting attachment pairs connect rear hinge mounts and lid leaves.
- **81 opening poses, 103 moving meshes and 99 static meshes**, zero unintended sampled surface intersections. Every river/forest mesh is included; moving/static and latch/lid checked. Only inherited explicit coaxial bearing contacts excluded. This is sampled surface evidence, not a continuous collision proof, solid containment proof or mechanical certification.
- Preserved mechanical pivots compared by independently opening the included original mechanism. 80-degree latch release precedes 105-degree lid opening; motion endpoint/invalid-asset negative controls pass.
- Source/export nearest-vertex error **1.712013073529306e-7** in each direction (<1e-5). Packed images verified. Source mesh representation and split export vertex counts differ normally.
- 54 broadleaf canopy clusters, two banks, 18 trunks and one river travel with the lid. 61 vertical centerline rays hit the actual river; channel exceeds 1.8 length and .16 width. The deliberately detached river fails the ancestry predicate before restoration. These are sampled visibility/ancestry checks, not ecology simulation.
- Actual GLTFLoader checks finite vertices and bounds, zero degenerate triangles, and decoded nonzero color/normal/roughness variation. Roughness is measured from the correct green channel. Maps are <=512 per axis.
- Desktop 1440×1080 and touch-emulated mobile 390×844 over offline `file://`: native open/close, drag/touch rotation, interrupted Reset, reduced motion, no overflow, no external HTTP requests or unhandled errors. Genuine corrupt embedded bytes reach GLTFLoader and produce poster fallback. No-JS fallback passes. Full-open silhouette fits the reset view.
- Poster nonblank pixel/alpha check passed. Final mobile visual inspection recognizes the continuous winding teal river and unclipped chest after one bounded correction.

## Honest limits and failures

The asset remains stylized: sparse rounded broadleaf crowns, simplified banks/water, procedural grain, conspicuous inherited long brass hasp, and gray stone feet. The rear hinge connection is geometrically verified but reads subtly at normal size. Front-open views naturally hide the landscape behind the raised lid; rear-open evidence shows it. No photoreal equivalence, actual-phone performance or engineering certification is claimed.

Initial ochre river passed vertical rays but was visually weak on mobile. Retained images document this real finding; widened channel, outward/smaller crowns, teal water and higher browser camera fixed readability without changing mechanical pivots. First build failed because the shared dependency directory was empty; installing the pinned existing dependencies locally resolved esbuild lookup. Optional Codex failed authentication before editing; all accepted implementation and verification were performed by Hermes directly. See `initial/findings.md`.

## Reproduction

Tools: Blender 5.2.1; Python with Pillow, numpy and Playwright; Node.js with package-lock dependencies. Installed Edge is used for browser QA. Node.js here is only a JS build tool, never a blockchain node. No dependencies are in the source ZIP.

From this directory:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_verification.py` (adjust the explicit Windows Blender/Node paths on other hosts)
5. `python package_delivery.py`

Build supports local dependencies or the sibling Iceland pilot fallback. Source art itself is self-contained. Regeneration overwrites source/model/poster; preserve manual edits separately and refresh sizes/inventory after rebuilding. Three.js is MIT (`THREE-LICENSE.txt`). Viewer/mechanism/test lineage is Japan v1 on base commit ff5d78f; terrain/maps/theme tests are new. Research sources supply factual inspiration only; no third-party images are embedded.

Local collectible art only: no mint, transaction, chain query, key access, custody verification, deployment or public hosting. Branch backup is separate from collection integration. The full launch direction remains 201 equally one-of-one designs.
