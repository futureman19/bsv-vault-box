# Ghana v1 — Kente & Brass

Open **ghana-v1.html** directly in Edge/Chrome: complete offline 3D model, runtime, maps and actual-source-render poster. Drag/touch rotates; Open/Close lid and Reset work; reduced motion snaps. Cosmetic collectible only—not minted, hosted, chain-verified or a custody operation.

## Deliverable
- HTML: **2,350,815 bytes**, strictly below 5,000,000.
- GLB: **1,138,916 bytes**; 90 meshes, 17,208 triangles, four materials.
- `ghana.blend`: packed editable source; `mechanism.blend`: inherited family hardware/interior baseline.
- `maps/`: original procedural wood, geometric strip color and roughness maps, at most 512 pixels per dimension.
- `poster.png/jpg`: real Blender source render, never AI promotional imagery.
- Desktop/mobile closed/open, no-JS and corrupt-input fallback screenshots are actual file:// browser evidence.
- `ghana-v1-source.zip`, `inventory.json`, `delivery-check.json`: source package and exact byte/SHA-256 readback inventory. Package deliberately excludes itself and its delivery envelope from recursive hashing.

## Design and cultural boundaries
Research and pre-model measurable contract are in `design-brief.md`, citing UNESCO's Ghana Kente craftsmanship inscription and descriptive captions. Eight original strip fields on the lid and coordinated body panels reference strip construction; they do not reproduce or name a traditional cloth pattern. Cocoa wood frame, brass feet and stepped diamond decoration are contemporary design extrapolations. No imported third-party pictures, sacred symbols, color-meaning claims or cultural authenticity certification.

## Executed acceptance
- Saved source independently reopened: hollow floor ray at z=0.2650000155; ten actual hinge attachment intersections; 29 moving and 61 static meshes tested over **81 poses**, zero unintended surface intersections. Includes all lid strips and ornaments, and latch-versus-lid tests. Only documented mating bearings excluded. This is sampled surface collision evidence, not continuous collision, physical volume containment or engineering certification.
- Saved-source/export nearest-world-vertex error **1.712013073529306e-7**, below 1e-5; three packed source maps. Geometry point-set parity is not proof of every UV/material property; runtime decoding checks those maps separately.
- Actual GLTFLoader: zero nonfinite vertices or degenerate triangles. Eight lid strips and three raised ornament pieces correctly parented. Decoded color maps <=512 pixels with nontrivial variation. Detaching a lid strip in a disposable browser scene causes the feature assertion to reject it.
- Motion unit test: 81 poses, latch reaches -80 degrees before lid leaves zero, lid reaches -105 degrees; three invalid-asset fixtures rejected.
- Offline Edge desktop 1440x1080 and touch-emulated 390x844 mobile: native open/close controls, rotation, interrupted reset, reduced motion, no overflow, no external HTTP requests/errors. Full-open projected vertices fit (max absolute NDC ~0.892365). Actual corrupted GLB parser input shows fallback; no-JS poster independently passed.
- Tests run on desktop NVIDIA RTX 4060. Mobile emulation is not physical-phone performance. No FPS certification.

## Actual failure and fix
`theme-initial-failure.txt` preserves the real decoded-map gate failure: wood red-channel variation was 19 while the fixed assertion required >20. Increased authored grain amplitude from 6/4 to 8/5, regenerated source/export/poster, and reran all final checks; assertion was not weakened. Negative controls are post-implementation regression probes, not test-first TDD. One final browser run exceeded a 180-second subprocess budget without output; the unchanged harness completed with a 600-second budget. The optional Codex lane failed authentication before editing anything; Hermes authored and tested directly, without touching credentials.

## Visual verdict / limits
Actual mobile closed and desktop open captures were visually inspected: complete framed silhouette, legible strips and hollow open body, no obvious major broken geometry. Stylized rigid inlay, **not real woven cloth or photorealism**. Repeated identical strips, regular wood grain and simplified clean brass are deliberate lightweight limitations. The dark reveal can read as a slightly raised lid; it preserves tested mechanical clearance rather than asserting a watertight closure. The stepped top diamond is decorative, not a handle or attributed symbol. Rear hinge attachment is tested numerically, not fully legible from the front beauty view. Technical completion is not user aesthetic approval; per-asset human review was waived for this batch.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/playwright; Node.js with dependencies in package.json; installed Edge. Only build-time dependencies; offline viewer requires none of these tools. `build.py` uses local node_modules or sibling `../iceland-pilot/node_modules`; archive users may install dependencies locally. Authoring uses only included mechanism source/maps. Do not rerun source authoring over manual edits without saving a copy.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with `verify_source.py` and `verify_parity.py` using the same flags.
5. `python verify_browser.py`; `python verify_theme.py`; `node test_motion.mjs`
6. `python package_delivery.py`

Lineage: copied read-only Japan family mechanism/viewer/verifiers from local base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8, with new Ghana authoring, maps, theme assertions and packaging. Three.js MIT license included. Nothing under art/, docs/, vault/, mint/ or other previews was modified. No wallet, key, node service, broadcast, chain query, VPS or external messaging. Branch backup is not publication or merge.
