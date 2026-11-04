# Hungary v1 — Pécs Lustre

Open `hungary-v1.html` directly in Edge/Chrome. Entire viewer is embedded: **2,316,754 bytes**, including **1,161,688-byte GLB**, runtime, maps and actual-source poster. Drag/touch rotate, Open/Close, Reset, reduced-motion and fallback supported. Local art only; not minted, hosted, on-chain or a custody action.

## Design and files
Original jade ceramic / golden floral relief informed by Pécs decorative ceramics; source links and pre-model measurable contract in `design-brief.md`. Five rosettes, 40 petals, eight leaves and four stems are real geometry owned by the lid. This is procedural Blender authorship, not hand sculpture, a historical pattern reproduction or an authentic Zsolnay product. Metallic/roughness shading approximates lustre, not optical eosin iridescence. No research images copied into the asset.

`hungary.blend` is editable source; `hungary.glb` portable export; `mechanism.blend` is the inherited trimmed Japan-pilot mechanism. `maps/` contains original compact generated maps. `poster.png/jpg` are actual Blender renders. Desktop/mobile PNGs are actual offline Edge captures. `hungary-v1-source.zip`, `inventory.json` and `delivery-check.json` contain byte-identifiable delivery with archive readback. No dependencies, backups or keys included.

## Verified
- Build: `HTML_BYTES 2316754 GLB_BYTES 1161688`; HTML strictly below 5,000,000.
- Saved-source independent reopen: 73 moving and 39 static meshes, 81 sampled poses, zero unintended surface intersections. Ten hinge attachment pairs verified. Hollow floor ray z=0.2650000155. Only explicit mating bearings excluded. This is sampled surface collision evidence, not continuous collision or engineering certification.
- Inherited pivot matrices exact; 80° staged latch release precedes 105° lid opening. Entire floral relief remains on lid.
- Source/export bidirectional nearest-vertex maximum error 1.712013073529306e-7, below 1e-5. Three packed maps.
- Actual GLTFLoader: 20,604 triangles, 112 meshes, four materials, zero nonfinite vertices and zero degenerate triangles.
- Offline file:// Edge desktop 1440×1080 and mobile 390×844 touch emulation: real buttons/touch rotation, reset mid-motion, reduced motion, full-open framing (maximum |NDC| 0.892365), zero external requests, runtime errors or overflow. Actual corrupt GLB parser failure shows poster; no-JS poster separately exercised. Desktop RTX 4060, not physical-phone performance.
- Decoded 256px maps vary: color ranges 32 and 15; roughness GREEN-channel range 38. Visible and accessible text audited for stale country copy.
- Motion tests: 2 passed, 0 failed. Intentional detached-rosette negative control raises `AssertionError: Detached ornament`; normal saved-source theme check passes. This is a post-authoring regression control, not test-first history.

## Real failure and fix
First HTML build failed with `MODULE_NOT_FOUND` for inherited esbuild. The shared baseline node_modules had no compiler. Installed the existing exact Three 0.180.0/esbuild 0.25.11 pins inside this new directory only; retained lockfile and failed output. No sibling preview dependencies changed. Inherited template contained a literal CSS truncation marker; repaired during setup, before browser acceptance (not claimed as an executed red test).

## Visual limits
Actual source/mobile/open captures inspected. All five flowers read on mobile; glazed green body and ivory/gold relief are stylized and somewhat angular. Small supporting text is fine-sized; broad reflections are mottled. Poster retains visible sampling grain (24 samples, denoising off). Dark seam and open hinge gap are visually pronounced despite measured connected mounts. Petals/stems are shallow raised appliqué with small clearances rather than simulated ceramic bonding. Lid flowers are naturally hidden behind the raised lid from the front. No photorealism, optical-glaze equivalence, exact traditional motif or physical mechanical-function claim.

## Reproduction
Blender 5.2.1; Python with numpy/Pillow/Playwright and installed Edge; Node build tooling. Run from repository root:

1. `npm ci --prefix preview/hungary-v1 --ignore-scripts --no-audit --no-fund`
2. `python preview/hungary-v1/maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python preview/hungary-v1/author.py`
4. Same Blender flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python preview/hungary-v1/build.py`
6. `node --test --test-reporter=tap preview/hungary-v1/tests.mjs`
7. `python preview/hungary-v1/verify_browser.py` and `verify_extended.py`.
8. `python preview/hungary-v1/package_delivery.py`.

`setup.py` records original scaffold adaptation from sibling Japan; it is not needed for reproduction from this delivered source and would overwrite authored scripts. Build needs local installed dependencies; runtime does not. Regeneration overwrites generated art/evidence; update inventory afterward. Three MIT license retained. Only this new preview directory is added; shared vault kit and all chain/production systems untouched. Branch backup only, no merge/deployment. Next: include this branch in the separate full-collection integration pass.
