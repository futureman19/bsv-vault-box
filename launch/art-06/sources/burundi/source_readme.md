# Burundi v1 — Sisal & Sweetgrass

Open `burundi-v1.html` directly in Edge/Chrome: an offline embedded 3D collectible with drag/touch rotation, zoom, staged Open/Close and Reset. HTML **2,955,082 bytes**; GLB **1,642,600 bytes**. Cosmetic only; not minted, hosted, deployed or a custody operation.

## Design and source
The research-backed `design-brief.md` preceded the recovered first-attempt model. Original geometric basketry-inspired panels and nested oval coils interpret sisal/sweetgrass traditions; they do not reproduce an artisan's basket or assert an exclusive national motif. Pale straw, charcoal and brick-red patterns sit in a dark frame with satin brass hardware. `burundi.blend` is editable, script-authored geometry with packed procedural maps, not hand weaving, scanning or photorealism. `poster.png` is an actual source render, not AI promotional artwork. See `lineage.json` for inherited Japan pilot mechanism and viewer provenance; shared source files were not modified.

## Verified on recovery
- Build: `HTML_BYTES 2955082 GLB_BYTES 1642600`; strict HTML ceiling 5,000,000 bytes.
- Source independently reopened: 35 moving and 50 static meshes, 81 poses, zero unintended sampled surface intersections. Latch releases 80 degrees before lid opens 105 degrees. Only named concentric bearings excluded. Hollow floor ray z=0.2650000155; ten hinge attachment contacts checked. This is sampled surface evidence, not continuous manufacturing certification.
- Source/export nearest-vertex error in both directions: 1.712013073529306e-7 (<1e-5); three packed maps retained.
- Actual GLTFLoader and theme checks: 18 coil/centre meshes, four woven panels, all coils lid-owned; maximum ornament height 2.0733580589 (<2.30). Three 512-square maps have nonzero decoded variation, reading roughness from GREEN.
- Desktop and 390x844 touch-emulated mobile over offline file://: rotation, native Open/Close, interrupted Reset, reduced motion, full-open frame fit, zero external HTTP requests, zero normal-path JS errors and no overflow. Real corrupt-GLB and no-JS poster fallbacks pass. Emulation is not physical-phone performance.
- Motion unit tests: 2 passed, 0 failed. A real loaded coil was detached in the extended negative control: the gate rejected it; restoring its parent passed.
- Preserved first-attempt failure in `initial/extended-failure.txt`: the inherited map probe read red rather than glTF roughness green. Correcting the channel, without weakening dimensions/variation assertions, passed. This is a harness fix, not an art defect.
- Delivery script verifies explicit required artifacts, exact byte/SHA-256 inventory and ZIP readback. Envelopes exclude themselves to avoid circular hashes.

## Visual limitations
Actual mobile screenshot inspected: entire closed box fits, broad diamond panels and oval coil motif read clearly; stylized angular forms and soft fine texture remain. Not a photoreal basket, fibre simulation, artisan endorsement or human aesthetic approval. Rear/interior are authored extrapolations. Full collection integration is separate; this branch is only an additive asset backup.

## Reproduce
Use Blender 5.2.1, Python with Pillow/numpy/playwright, Node, Three 0.180.0/esbuild 0.25.11 and installed Edge. Build uses local node_modules or the sibling pilot toolchain; dependencies are not runtime network requirements and are excluded from delivery. For standalone source extraction install package.json dependencies locally.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`; `node --test tests.mjs`
4. Blender with the same flags: `verify_source.py`, then `verify_parity.py`.
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Do not rerun `setup.py` for normal rebuilds: it is a historical one-time sibling lineage bootstrap and would overwrite country-specific adaptations. Authoring overwrites generated source/export/poster; preserve manual edits separately. Three.js MIT notice is included. All writes in this card are restricted to this folder; no chain, keys, production site, VPS or shared kit actions.
