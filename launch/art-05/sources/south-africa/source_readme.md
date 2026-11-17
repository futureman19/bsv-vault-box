# South Africa v1 — Table Mountain & Fynbos

Open `south-africa-v1.html` directly in Edge/Chrome: embedded 3D model, runtime, maps and actual-source poster. Drag/touch rotate, Open/Close lid and Reset; reduced motion is supported. **HTML 3,064,643 bytes; GLB 1,720,352 bytes.** No hosting, minting, blockchain interaction or custody claim.

## Delivered
Editable packed `south-africa.blend`, standalone `south-africa.glb`, generated maps and reproducible authoring; `mechanism.blend` is the inherited Japan pilot's trimmed mechanical baseline. `poster.png` is a real Cycles render, not promotional AI imagery. Actual desktop/mobile closed/open screenshots, fallback screenshots, source/render/build/browser output and machine checks are included. Source ZIP excludes dependencies and backups. Three.js 0.180.0 is MIT; license included.

## Verified
- Independent saved-source reopen: hollow floor ray z=0.2650000155; ten hardware attachment pairs; **81 poses, 47 moving and 39 static meshes, zero unintended sampled intersections**. Latch-versus-lid included. Only named mating bearings exempt. This is sampled surface checking, not continuous/manufacturing certification.
- Independent source/export nearest-vertex comparison in both directions: maximum error **1.712013073529306e-7**, tolerance 1e-5.
- Mesa top z=2.67825–2.70199, 30 lid-owned plant clusters, preserved original pivot matrices. A deliberately detached mesa was rejected by the ancestry assertion: negative control, not an observed production defect.
- Actual browser GLTFLoader: **16,648 triangles, 86 meshes, 5 materials**, zero nonfinite vertices/degenerate triangles; decoded color/roughness maps vary (roughness tested in green channel).
- Offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: rotation, open/close, interrupted reset, reduced motion, full-open framing (maximum absolute NDC 0.892365), no horizontal overflow, no external requests, no runtime errors. Real corrupt GLB triggers poster fallback; no-JS poster separately tested.
- Motion endpoint/reversal and invalid-asset unit tests pass against the delivered local motion module.
- Exact SHA-256 inventory, explicit required-file inclusion, ZIP CRC/entry-byte readback, staged Git blob comparison. Folder-local `* -text` preserves bytes on checkout.

## Honest visual assessment
The wide pale stone box, warm brass hardware and flat-topped mesa are readable in the actual source render and mobile view. Stone can read as limestone/plaster rather than unmistakable sandstone; vegetation is stylized clustered greenery, not botanically faithful fynbos. Summit/cliff geometry is an invented regional silhouette, not surveyed Table Mountain. No supplied art reference or photoreal equivalence is claimed. Source render has mild sampling grain. Hidden views are not implied by one screenshot; open-state browser captures and sampled geometry tests provide separate evidence. Mobile tests ran on desktop RTX 4060, not a physical phone or performance benchmark.

## Reproduce
Python with numpy/Pillow/Playwright, Blender 5.2.1, Node, installed Edge. Within this directory: `npm ci --ignore-scripts --no-audit --no-fund`; `python maps.py`; run Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Blender on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

The shared toolchain directory existed but lacked compiler files, so exact pinned packages were installed only in this new asset folder; no sibling dependency repair. `setup_author.py` documents initial helper derivation from the sibling Japan source, but the delivered `author.py` is self-contained with the included mechanism and maps. Regeneration overwrites generated files; preserve manual edits separately. Re-run evidence and packaging after changes. Research sources and pre-model contract are in `design-brief.md`.

All acceptance runs passed without a production failure-and-fix in this run. Tests include a deliberate rejected detached-terrain control and actual corrupt-parser fallback; these are not fabricated failure history. User waived per-asset human review. Integration into the full collection is a separate card; branch backup is not deployment.
