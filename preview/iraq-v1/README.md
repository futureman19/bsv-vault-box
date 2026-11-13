# Iraq v1 — Babylon / Cobalt & Ochre

Open **iraq-v1.html** directly in Edge/Chrome: complete embedded interactive model, runtime, maps and actual Blender-rendered poster. Drag/touch rotation, Open/Close and Reset; reduced-motion snapping and poster fallbacks. No server or internet needed.

- HTML_BYTES **2768622** (<5,000,000)
- GLB_BYTES **1512052**
- Editable `iraq.blend`, portable `iraq.glb`, generated maps, source poster, reproducible author/build/check scripts, screenshots and exact SHA-256 inventory included. `iraq-v1-source.zip` is the readback-verified source package.

## Design and provenance
Brief written before modeling: Babylon-inspired cobalt glazed-brick body, warm clay stepped architectural relief and geometric rosettes on the lid, restrained brass hardware. Research citations and numeric targets are in `design-brief.md`. This contemporary stylized miniature is not an archaeological reconstruction, religious representation, or comprehensive representation of Iraq. No third-party imagery used as textures; no AI promotional substitute. Geometry and compact maps are procedurally authored, not scans or hand sculpture.

Mechanical/runtime lineage is the repository Japan pilot at base ff5d78f1e0d486af5c882c184fc08049996ebdc8. Included trimmed `mechanism.blend` retains the hollow liner, bearing mounts, lid and latch pivots. Shared vault kit and previous previews are unchanged. Three.js runtime license included.

## Verified evidence
- Real GLTFLoader: **15,944 triangles, 274 meshes, four materials**, zero nonfinite vertices and zero degenerate triangles. Three packed maps; two decoded color maps are 512×256 with red range 25 and blue/ochre palette checks.
- Independently reopened saved source: hollow floor ray z=0.2650000155; ten explicit connected hinge attachment pairs. **81 poses, all 59 moving and 215 static meshes, zero unintended surface intersections**. Also latch vs lid geometry. Only named concentric bearing contacts excluded. This is sampled surface-intersection evidence, not continuous collision/containment or manufacturing certification.
- Source/export bidirectional maximum nearest-vertex error **1.712013073529306e-7** (<1e-5). This proves geometry correspondence, not byte-identical re-export or exhaustive material parity.
- Theme gate: 184 real brick meshes, three stepped tiers, all rosettes/borders/tiers lid-borne, original lid pivot and width, no inherited tree/moss. Deliberately unparented tier is rejected by the same validator before restored positive pass.
- Motion unit tests: two passed, including bad-asset negative controls; 80° latch release before 105° lid opening.
- Actual Edge offline `file://`: 1440×1080 desktop and 390×844 touch emulation, native open/close, drag/touch rotation, interrupted reset, reduced motion, no HTTP requests, no runtime errors, no horizontal overflow. Full-open vertex projection max |NDC| 0.892365. Corrupted actual GLB input reaches parser and produces poster fallback; no-JS poster also tested.
- RTX 4060 desktop GPU. Mobile emulation is **not physical-phone performance testing**. No FPS or broad browser compatibility claims.

## Visual verdict and limits
Actual source render and final mobile closed screenshot were visually inspected: coherent wide silhouette, seated stepped ornament, readable cobalt brick body, attached-looking brass clasp, unclipped model/UI. Dark seam deliberately reads pronounced; fine rosettes and glaze grain are small at mobile scale. This is clean stylized art, not photorealism or historical equivalence. Open/rear screenshots were captured and geometric framing/attachment gates passed, but the separate open-screenshot vision inspection failed because the vision service returned a billing error; no successful manual/vision inspection of that screenshot is claimed.

## Real failures and fixes
`initial/` preserves:
1. Near-duplicate floating-point brick cut at exterior boundary created a sliver and disabled bevel application. Fixed by an endpoint epsilon before creating brick geometry.
2. Initial HTML **5,833,530 bytes**, GLB **3,810,400 bytes** failed strict size gate. Reduced tiny cube bevels from three segments to one; retained silhouette, reran source/parity/collision/browser gates. Final cap was not relaxed.
3. Fixed 70ms reduced-motion sleep asserted before a rendered frame under load. Harness now waits at most two seconds for endpoint and samples frame progress, rejecting intermediate values. Viewer behavior unchanged.
Optional Codex lane exited 401 with no accepted edits; Hermes authored and tested directly. Credentials were not changed.

## Reproduce
Python with Pillow/numpy/playwright, Blender 5.2.1, Node/esbuild/Three build dependencies, installed Edge. Runtime HTML has no such external requirements. Build resolves local node_modules or sibling `iceland-pilot/node_modules`; isolated extraction may install dependencies from package.json. All source paths are folder-relative. Do not run simultaneous regenerations.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender likewise on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node --test tests.mjs`
5. `python build.py`
6. `python verify_browser.py` and `python verify_extended.py`
7. `python package_delivery.py`

Authoring overwrites generated assets; save manual modifications separately. Package omits .blend1 and caches. Inventory excludes itself, delivery envelope, source ZIP and package log to prevent recursive hashes; ZIP includes the explicit required artifact set and inventory, with all entries verified on readback.

Local art only: no mint, wallet, keys, chain query, node service, broadcast, VPS, production edit or deployment. Cosmetic lid opening does not open custody. Branch backup only; integration belongs to a separate collection card. User waived per-asset review; no user visual approval is claimed.
