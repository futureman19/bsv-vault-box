# Armenia v1 — Rose Tuff Arcade

Open **armenia-v1.html** directly in Edge/Chrome. Everything needed at runtime is embedded: actual GLB, textures, Three runtime, and an actual-source-render poster. Drag/touch to rotate, Open/Close lid, Reset view. Reduced motion snaps to endpoints. No network/server, wallet, mint or transaction.

## Delivered
- Standalone HTML: **2,233,011 bytes**, strictly below 5,000,000.
- Standalone `armenia.glb`: **1,138,116 bytes**.
- Editable packed `armenia.blend`, trimmed inherited `mechanism.blend`, procedural maps and reproduction scripts.
- Actual-source poster PNG/JPEG, desktop/mobile closed/open captures, rear-open, corrupt-loader and no-JS fallback captures.
- `inventory.json`: exact payload bytes/SHA-256. `armenia-v1-source.zip`: payload plus inventory; `delivery-check.json`: archive readback and final HTML check. node_modules and Blender backups excluded.

## Design and provenance
The prewritten design brief cites Smithsonian's account of Yerevan's volcanic tuff and the city's official description of pink tuff arcades. Three invented open arches sit on a rose-tuff-inspired wide stone box. This is an architectural abstraction, not a named building replica, sacred motif, material scan, artisan carving or geographic survey. Research photographs are not embedded. Mechanism/viewer/test lineage is the repository Japan pilot; its cedar/foliage was not reused as Armenia art. The shared vault kit was read only and unchanged.

## Verified evidence
- `source-check.json`: independent saved source reopening, hollow floor ray z=0.2650000155; **81 poses**, **25 moving + 39 static meshes**, no unintended sampled intersections. Includes all nine arch/piers. Moving/static and latch/lid checks only exclude explicit inherited mating hinge/barrel and knuckle/pin bearings. Ten actual intersecting hinge attachment pairs are listed separately.
- `theme-check.json`: three arches/six piers, all lid-parented, lower/upper ornament bounds 1.9779999256/2.7100000381. Three aperture rays clear and three crown rays hit stone. Detaching one arch genuinely fails ownership, then restoration passes (post-implementation negative control, not a claimed TDD failure). Exact baseline pivot matrices retained. Rose map mean red > green > blue.
- `parity-check.json`: source/export bidirectional nearest-vertex maximum error 1.712013073529306e-7 (<1e-5). Three packed procedural maps. Not an exact-byte re-export claim.
- `motion-output.txt`: **2 tests, 2 pass, 0 fail**, including invalid asset rejection and staged/clamped motion endpoints.
- `browser-check.json`: actual GLTFLoader **15,568 triangles, 64 meshes, 4 materials**, zero nonfinite/degenerate triangles. Desktop 1440x1080 and touch-emulated 390x844 over offline file://: native controls, drag/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open max absolute projected coordinate 0.911882 (<1). Actual corrupt GLB supplied to parser produces expected caught error and poster fallback.
- `extended-check.json`: loaded ornament ancestry, decoded 256px base-color/roughness-map variation (roughness GREEN), source poster nonempty, no-JS image, visible and accessible Armenia copy.
- All acceptance scripts completed on first execution; no actual failed art gate was hidden or invented. Deliberate corrupt-input and detached-ornament controls prove rejection paths. Inherited malformed mobile CSS was repaired during adaptation before testing.

## Visual assessment and limits
Actual source and mobile captures were inspected: pink stone-inspired body, three independently legible arch openings, visible brass hardware, no initial-frame clipping. This is deliberately stylized: arches are faceted individual loops rather than one shared-pier arcade; procedural stone reads softly mottled, not photoreal porous tuff; the dark lid seam is prominent; corner joins are stepped, hardware fine at mobile size, and the source render has sampling grain. No exact reference equivalence, physical engineering, continuous-collision proof or physical-phone performance claim. Mobile tests ran on a desktop RTX 4060.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/playwright, Edge, Node plus pinned Three 0.180.0/esbuild 0.25.11. Shared pilot node_modules existed without the compiler; dependencies were therefore installed **inside this folder only**, leaving other previews untouched. `npm ci --ignore-scripts --no-audit --no-fund` restores local build tooling; no runtime downloads.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender similarly with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node --test --test-reporter=tap tests.mjs`
5. `python build.py`, `python verify_browser.py`, `python verify_extended.py`
6. `python package_delivery.py`

`setup.py` documents the one-time adaptation and requires the sibling Japan/Iceland pilots; do not rerun it over customized output. Subsequent author/build/verification uses included source/mechanism/maps and local dependencies. Regeneration overwrites authored outputs and changes hashes; repackage afterward. Source render uses two CPU threads and no denoising. Three's MIT license is included.

Only this new directory is added. Branch backup is not production publication; nothing is merged, hosted, minted or stored on-chain. Next: collection-level integration and visual review after the full set exists.
