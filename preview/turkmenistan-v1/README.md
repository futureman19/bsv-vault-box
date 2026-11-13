# Turkmenistan v1 / Crimson Weave

Open `turkmenistan-v1.html` directly in Edge/Chrome: drag or touch to rotate, Open/Close lid, Reset view. All runtime assets are embedded; no server or network needed. Cosmetic animation only, no custody state change.

## Delivery
- Standalone HTML: **3,362,615 bytes** (<5,000,000).
- Embedded/standalone `turkmenistan.glb`: **1,946,032 bytes**.
- `turkmenistan.blend`: packed, editable Blender-authored source. `mechanism.blend` is the trimmed inherited mechanical source, not the new artwork.
- `maps/`: original procedural textile color/roughness and stone maps; unused edge swatch retained as authoring input.
- `poster.png` and compressed `poster.jpg`: actual final source render, not AI promotional art.
- Actual offline desktop/mobile closed/open, rear-open, no-JS and corrupt-file fallback captures.
- Reproducible author/build/check scripts, exact SHA-256 inventory and source ZIP with verified readback.

## Design and provenance
Research-backed written brief was saved before model authoring; see `design-brief.md`. UNESCO and UN Turkmenistan identify dense wool textiles and clear linear geometric patterns as part of Turkmen carpet-making. The three octagonal ornaments, diamonds, border and fringe are original interpretations, **not authentic tribal motifs, museum copies or artisan-woven objects**. No third-party photos, carpet patterns or scans are embedded.

Source/mechanism/viewer/check lineage is the repository Japan pilot at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8; all adaptations are confined here. Three.js 0.180.0 is MIT (included license); esbuild 0.25.11 is build-only. No shared kit or sibling preview was modified.

## Verified
- Independently reopened Blender source: original pivot matrices retained; 58 lid-borne carpet components, three octagonal medallions and 38 fringe bars; maximum ornament z=2.054. Deliberately detached ornament is rejected by the ancestry test.
- 81 sampled motion poses, **74 moving and 39 static meshes**, no unintended surface intersections; all new carpet parts included. Also latch-vs-lid tested. Only named mating hinge/barrel and latch pin/knuckle/bridge bearings excluded. Hollow floor ray z=0.265. Ten connected hinge attachment pairs verified.
- Source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed source images independently found.
- Actual GLTFLoader: **23,268 triangles, 113 meshes, six materials**, zero nonfinite vertices and zero degenerate triangles. Decoded color and roughness variation checked; roughness uses the glTF green channel.
- Offline file:// Edge: desktop 1440x1080 and touch-emulated mobile 390x844; native controls, mouse/touch drag, open/close, interrupted reset, reduced motion, full-open framing (max absolute NDC 0.892365), no horizontal overflow, no external HTTP requests, no runtime errors. Actual corrupt GLB reaches the parser and shows the poster; no-JS poster also verified.
- Two motion/validation unit tests pass, including invalid geometry negatives. Test assertions are capable of failing, not unconditional status files.
- Explicit required artifact inventory, archive readback, SHA-256/byte counts, and staged-Git-byte verification are included.

## Failure and fix
`initial-build-failure.txt` preserves the real MODULE_NOT_FOUND failure: the supplied shared node_modules was empty. Installed the unchanged pinned toolchain inside this new preview only; package-lock retained, dependencies excluded from Git/ZIP. Successful build output retained. No acceptance geometry assertion was relaxed. The temporary empty sibling link directory was removed after verification.

## Visual verdict and limits
Actual source and mobile renders were inspected. The crimson chest, three ivory medallions, shallow carpet relief, brass hardware and fringe are visible without clipping or obvious floating parts. The result is deliberately stylized: studio lighting makes crimson read dusty rose; the carpet/fringe is rigid relief rather than soft wool; mobile weave detail is subtle and the title supplies country identification. Seam is conspicuous, hardware simplified, and source render has sampling noise. No photorealism, authentic textile fidelity or prior human art approval is claimed. Per-asset human review is waived for this collection batch.

Collision checks are sampled surface intersections, not continuous mechanical certification. Mobile emulation ran on an RTX 4060 desktop, not a physical phone. No minted NFT, on-chain storage, signature, hosting, public deployment or custody validation exists here. Collection direction remains 201 equally one-of-one designs; this is one local art asset.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node and pinned npm packages. Run from this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender the same way on `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
5. `node --test tests.mjs`; `python build.py`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Regeneration overwrites generated source/render/model/evidence. Preserve manual edits separately. Authoring requires only included mechanism source; local build dependencies are not runtime dependencies. Inventory and delivery-check exclude themselves/packaging envelopes where necessary to avoid recursive hashes. Integration into the full collection is a separate card; this branch must not be merged here.
