# Ireland v1 — Connemara & Burren

Open **ireland-v1.html** directly in Edge/Chrome: a complete offline 3D collectible with rotate/zoom, staged Open/Close, Reset and reduced motion. HTML **3,179,700 bytes** (<5,000,000); GLB **1,748,608 bytes**. No server, CDN, wallet or chain connection is needed. No minting, public deployment or custody verification occurred.

## Design and files
The prewritten `design-brief.md` cites Geological Survey Ireland and Burren Geopark research. Folded green marble body and lid carry a pale, fissured limestone-pavement miniature. This is an invented combination of two western Irish geologies, not a mapped location, authentic craft artifact or geological reconstruction. No third-party photos/textures are embedded.

- `ireland.blend`: editable, packed, script-authored Blender source; `ireland.glb`: exported portable model.
- `mechanism.blend`: unchanged trimmed mechanism from the repository Japan pilot; 80-degree latch release precedes 105-degree rear-hinged lid opening. New terrain moves with the lid.
- `maps.py`, `author.py`, `maps/`: reproducible procedural geometry/materials, not scans or hand sculpture.
- `poster.png`/`poster.jpg`: actual final source render, not promotional AI imagery.
- Desktop/mobile closed/open screenshots and fallback screenshots: actual offline browser evidence.
- `source-check.json`, `parity-check.json`, `theme-check.json`, `extended-check.json`, `browser-check.json`, raw `*-output.txt`: verification evidence.
- `inventory.json`, `delivery-check.json`, `ireland-v1-source.zip`: exact SHA-256 inventory, required-artifact and archive readback checks. Folder-local Git attributes preserve bytes.

## Verified
- Independently reopened saved source: **81 sampled motion poses**, all **37 moving and 39 static meshes**, zero unintended intersections. Latch-versus-lid checks included. Only named inherited concentric mating bearings excluded. Ten hinge attachment pairs tested; floor ray hits hollow interior at z=0.2650000155. Sampled surface tests are not continuous collision or manufactured-mechanism certification.
- Source/export bidirectional nearest-world-vertex maximum error **1.712013073529306e-7**, below 1e-5. Original lid/latch local matrices compared independently against the included mechanism source.
- Twenty low irregular clints: source bounds, all twenty exposed center rays, sixteen grike-bed rays and lid ancestry pass. Detached-ornament negative control actually fails, then source is reloaded and passes; no mutation is saved. This is a deliberate postimplementation oracle test, not test-first history.
- Actual GLTFLoader: **18,056 triangles, 76 meshes, 4 materials**, zero degenerate triangles/nonfinite vertices. Loaded color maps have red-channel ranges 136 (marble) and 64 (limestone); roughness range 48 is measured in the glTF green channel. Mean marble G exceeds R and B. All maps <=512px.
- Offline `file://` Edge desktop 1440x1080 and touch-emulated mobile 390x844: drag/touch rotation, native Open/Close controls, interrupted Reset, reduced-motion endpoint, no horizontal overflow, zero external HTTP(S) requests or runtime errors. Full-open projected maximum absolute NDC **0.9127373079119276** (<1). Genuine corrupt GLB reaches the parser and displays the real poster; no-JS poster also passes. Desktop RTX 4060; **not physical-phone performance testing**.
- Two motion/invalid-asset unit tests pass. The validator rejects missing pivots, empty geometry and nonfinite bounds. Byte/archive gates use real assertions, not prefilled PASS records.

## Visual verdict and bounded refinement
The final mobile view is readable and unclipped with distinct green stone, pale relief and brass. One bounded refinement replaced regular four-sided pavers with asymmetrically chipped eight-sided outlines; the original render remains in `initial/pavement-regular.png`. Technical checks passed before and after; there was no unplanned failing gate to conceal. The deliberate detached-ornament failure is recorded in theme-check.json; corrupt-parser failure is recorded in browser-check.json.

**Remaining limitations:** marble veins are conspicuously rhythmic/procedural and can resemble malachite or painted waves. Limestone remains a stylized grid of raised blocks rather than convincing natural Burren terrain, despite chipped outlines and real gaps. Small-scale texture and hardware detail are subtle on mobile. Metalwork and feet are family-design extrapolations. Source Cycles render has sampling noise (denoising disabled); it is evidence, not photoreal equivalence. No claim of human art approval, botanical/geological accuracy, physical functionality, accessibility certification or frame-rate performance. Per-asset human review was explicitly waived for this collection batch.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node with pinned Three.js 0.180.0 and esbuild 0.25.11. The main checkout's suggested shared dependency directory did not contain esbuild; pinned dependencies were installed **only here**. `node_modules` is ignored/excluded, and no other preview was modified. Build-time dependencies are not runtime network dependencies.

From this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender likewise on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs` (save output as motion-output.txt).
6. `python build.py`, `python verify_browser.py`, `python verify_extended.py`.
7. `python package_delivery.py` after updating README measurements if changed.

Regeneration overwrites generated source/model/poster. Save manual variants separately. Verification scripts and build are folder-relative; use the included mechanism, not a shared asset. Three MIT license included. The source ZIP is a local reproducibility package, not a hosted product. The collection remains 201 equally one-of-one designs; accessories are deferred. Branch backup only; integration is a separate task.
