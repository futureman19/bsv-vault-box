# Uganda v1 — Mutuba / Beaten Barkcloth

Open **uganda-v1.html** directly in Edge/Chrome. This is an embedded, offline 3D collectible study: drag/touch rotation, Open/Close lid, Reset and reduced motion. **HTML 3,164,852 bytes; GLB 1,806,436 bytes.** No installation or network needed to view it. Browser/WebGL required for interaction; a real-source poster remains available without JS or after load failure.

## Design and limits
The pre-model `design-brief.md` cites UNESCO's account of Baganda barkcloth made from Mutuba inner bark, beaten rather than woven. Procedural terracotta maps evoke short irregular fibers. The lid bears a low folded relief. This represents one specific tradition, not all Ugandan cultures. No traditional symbolic pattern, royal insignia, third-party photo or artisan-authorship claim is made.

Actual source/mobile image review found readable folds, brass hardware and unclipped mobile layout. **The thick-edged relief reads as a sculpted fold, not physically simulated soft cloth; fine fibers are subtle at mobile size.** Body remains rigid, the dark seam prominent, fittings cleaner/simpler than real handwork. Poster has visible sampling grain. These are accepted v1 visual limitations, not photoreal equivalence. No human per-asset art approval is claimed; the task explicitly waives it until collection completion.

## Evidence actually exercised
- `source-check.json`: independently reopened source; 81 poses, all 17 moving and 39 static meshes; zero unintended surface intersections. Latch-versus-lid tested separately. Only explicit coaxial mating bearings excluded. Hollow interior floor ray z=0.2650000155; ten hinge attachment contacts. This is sampled surface collision evidence, not continuous collision or engineering certification.
- `pivot-check.json`: exact inherited lid/latch world matrices and hierarchy, independently reopening the included trimmed mechanism and final source. 80° latch release precedes 105° lid opening; two Node motion/invalid-asset tests pass (`motion-output.txt`).
- `parity-check.json`: saved-source/export bidirectional nearest-vertex error 1.712013073529306e-7 (<1e-5); four packed procedural images. Not a byte-identical reexport claim.
- `theme-check.json`: saved-source ornament ownership, XY bounds, top extrema 2.04403448–2.16596556, upward top faces and skirt contact at z1.978. `negative-control.json` deliberately removes ornament ownership and **fails**; original source is not saved/altered. This proves a rejecting gate, not test-first development.
- `browser-check.json`: real GLTFLoader reports 17,084 triangles, 57 runtime meshes, five materials, no nonfinite vertices or degenerate triangles. Offline file:// desktop 1440×1080 and mobile 390×844 touch emulation: native controls, rotation, open/close, interrupted reset, reduced motion, zero external requests/errors/overflow. Full-open projected max abs NDC 0.892365 (<1). Genuine corrupt GLB triggers the parser's poster fallback. Physical-phone performance not tested.
- `extended-check.json`: actual decoded color/roughness map variation, roughness green channel, <=512px maps, runtime lid ancestry, correct visible/accessibility country labels and no-JS poster.
- `delivery-check.json` and `inventory.json`: exact byte/SHA-256 inventory, strict HTML cap, explicit required files, source ZIP readback and each archived byte checked. Package envelopes excluded from their own inventory to avoid circular hashing. Git byte-preservation check is reported separately.

## Real failure and fix
`initial-build-failure.txt` preserves missing esbuild in the provided shared pilot toolchain. The shared dependency tree was not modified; the same pinned Three 0.180.0/esbuild 0.25.11 dependencies were installed **only in this new directory**, excluded from Git/archive. Build and all final checks then succeeded. No model/collision failure occurred; the deliberately detached-ornament negative control is separately labeled.

## Files / reproduction
Editable `uganda.blend`, portable `uganda.glb`, actual-model `poster.png`/`poster.jpg`, closed/open desktop/mobile screenshots, maps and complete source/test scripts are included. `mechanism.blend` is the reused trimmed mechanical family source from Japan v1 at base commit ff5d78f; the shared vault kit and previous pilots are untouched. No AI promotional image is embedded. Three MIT license included.

Tools: Blender 5.2.1; Python with Pillow, numpy, Playwright; Node with pinned package-lock; installed Edge. From this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender likewise on `verify_source.py`, `verify_parity.py`, `verify_theme.py`, `verify_pivots.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python build.py`; `python verify_browser.py`; `python verify_extended.py`
7. Negative control: Blender with `verify_theme.py -- --negative` must exit nonzero.
8. `python package_delivery.py`
Regeneration overwrites outputs; preserve manual edits separately. Build prefers local node_modules, with historical sibling fallback. Source archive contains the necessary mechanism and scripts but not installed dependencies.

Local art only. Cosmetic opening is not a custody operation. No nodes, keys, blockchain queries, mints, broadcasts, public deployment or Hetzner access. Models remain local/off-chain; no persistence or signed provenance guarantee. Branch backup only; integration belongs to the collection's separate final card.
