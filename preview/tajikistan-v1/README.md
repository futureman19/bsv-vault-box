# Tajikistan v1 / Pamir Ridge & Alpine Lake

Open **tajikistan-v1.html** directly in Edge/Chrome. Complete embedded model, runtime, maps and actual-source poster; no server or network required. Drag/touch to rotate, Open/Close lid and Reset view. Reduced motion snaps the articulation. Cosmetic movement only, not a custody operation.

## Delivery
- HTML **3,193,523 bytes**, strictly under 5,000,000.
- GLB **1,779,636 bytes**; editable packed `tajikistan.blend` plus retained `mechanism.blend`.
- Procedural maps, author/build/verification scripts, actual source poster and desktop/mobile captures.
- `inventory.json` records exact SHA-256 and byte sizes; `delivery-check.json` verifies required artifacts and full ZIP readback. Folder-local Git attributes preserve bytes across Windows checkout.

## Design and provenance
The sourced contract in `design-brief.md` was written before modeling. UNESCO and IUCN descriptions of the Pamirs' juxtaposition of glaciated mountains, alpine-desert plateaux and lakes informed an invented miniature: three snowy summits and a blue lake on a gray mineral box. No third-party photographs, geographic meshes, scanned textures or sacred patterns are embedded. This is not a model of a particular summit or lake, or a claim to represent every Tajik tradition. Hardware is the collection's invented brass language.

Script-authored Blender geometry, not hand sculpture. The trimmed Japan mechanical source and viewer/test lineage were reused read-only, not its cedar/tree artwork. Three.js 0.180.0 is MIT (`THREE-LICENSE.txt`); esbuild 0.25.11 is build-time tooling. The shared pilot dependency directory lacked the compiler, so the same pinned packages were installed only inside this preview's ignored node_modules. No sibling preview was modified.

## Actually verified
- Independent saved-source reopening: **18 moving, 39 static meshes**, **81 sampled poses**, zero unintended moving/static or latch/lid intersections. Only explicit mating hinge leaf/barrel and latch knuckle/bridge/pin contacts excluded. Ten hinge mounting intersection pairs verified. Hollow floor ray z=0.2650000155. This is sampled surface collision checking, not continuous clearance or manufacturing certification.
- Inherited lid/latch world pivot matrices exactly preserved. Release 80 degrees first; lid opens 105 degrees after progress .25. Motion test samples 81 poses and rejects three invalid-asset controls.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed maps independently reopened. This proves geometric correspondence within tolerance, not byte-identical re-export.
- Actual browser GLTFLoader: **18,050 triangles, 58 runtime meshes, six materials**, zero degenerate triangles/nonfinite vertices. Ridge snow/rock export as separate mesh primitives beneath one terrain group. Portable map variation decoded, including roughness from green channel.
- Theme checks: three numeric summits, ridge height/footprint, snow/rock materials, upward lake normals, lake exposed by three downward rays, lid ancestry, inherited pivots. Detached-lake negative control rejected without saving the mutation.
- Offline file:// Edge: 1440×1080 desktop and 390×844 mobile touch emulation; native click/tap open/close, mouse/touch drag, interrupted reset, reduced motion, no overflow, no external HTTP requests or runtime errors. Full-open projected bounds maximum absolute NDC **0.912804** (rounded up). Actual corrupt GLB reaches parser and falls back to source poster; no-JS poster also checked. RTX 4060 browser, **not physical-phone performance**.

## Real correction and failure record
Initial source render had a repetitive crosshatch mineral texture. One bounded correction replaced sinusoidal waves with multiscale seeded mineral mottling; retained `initial/poster.png` and `initial/maps.py`. Final source/export/poster and browser tests were regenerated together.

The extended runtime check genuinely failed because it assumed every exported terrain mesh kept a Terrain-prefixed name. The two-material ridge is a named group with differently named primitive children. `initial/extended-name-assumption-failure.txt` and the failed verifier preserve this. The corrected verifier walks ancestry and still requires all three primitives, lid ownership and map variation. No model geometry or threshold was relaxed to hide that harness failure.

## Visual acceptance and limits
Final source and actual desktop/mobile closed/open captures inspected. Three snowy summits, blue lake, gray mineral body and brass fittings are legible, and the open silhouette fits. The look is deliberately stylized, not photorealistic. Snow edges are angular; the terrain footprint is regular; the lake is a thin blue relief/inlay rather than a carved basin with simulated water. The mottled body is lighter/cloudier than raw alpine rock. Hinge connections pass geometric attachment probes but can look sparse from the open front view; hardware is decorative, not engineered. There is no supplied original illustration to claim equivalence to. Full-open front view naturally hides the mountain tops behind the lid; `desktop-open-rear.png` shows the carried relief.

## Reproduce
Use Python with numpy/Pillow/Playwright, Blender 5.2.1, Node and installed Edge. From this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with `verify_theme.py`, `verify_source.py`, `verify_parity.py` in the same way.
5. `node test_motion.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`; `python verify_acceptance.py`

The generated `author.py` is self-contained with the bundled mechanism/maps. `setup_author.py` is a historical derivation helper requiring the repository Japan script, and is not needed for regeneration. Regeneration overwrites assets; preserve manual edits separately. Build/test dependencies are not runtime downloads and are excluded from ZIP/Git. The archive excludes itself, inventory self-reference, delivery envelope, and active packaging/Git logs.

## Scope
Additive preview only. Branch backup authorized; no merge, public deployment, wallet/key access, node startup, chain query, mint, broadcast, sale, VPS operation or on-chain storage. Collection direction remains 201 equally one-of-one designs. User waived per-asset review for this batch; passing these gates is not a claim of human art approval. Next step is the existing final collection integration card, not another automatic polish loop.
