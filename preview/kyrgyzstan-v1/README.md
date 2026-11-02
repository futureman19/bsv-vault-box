# Kyrgyzstan v1 — Shyrdak / Crimson Felt

Open **kyrgyzstan-v1.html** directly in Edge/Chrome: the complete 3D model, runtime, maps and actual-source poster are embedded. No server or network is needed. Drag/touch rotates; Open/Close lid and Reset view work; reduced-motion preference snaps movement. Cosmetic movement only, not opening a custody seal.

## Delivered
- `kyrgyzstan.blend`: packed, named, editable Blender-authored source; `kyrgyzstan.glb`: portable model.
- `maps/`: three independently generated 256×256 felt base-color, roughness and normal maps.
- `poster.png`, `poster.jpg`: actual Blender source renders, not AI promotional art.
- `kyrgyzstan-v1.html`: **2,467,247 bytes**; GLB **1,278,304 bytes**. Exact current identities in `inventory.json` and `delivery-check.json`.
- Desktop/mobile closed/open, rear-open and fallback screenshots: actual offline Edge captures.
- `design-brief.md`: pre-model research and measurable visual contract; UNESCO/ICHCAP citations. No third-party imagery embedded.
- Author/build/check scripts, original failed-check evidence, dependency declaration and Three.js MIT license. `mechanism.blend` is the frozen Japan family mechanical baseline, not the Japan art.

## Verified
Actual Three GLTFLoader: 24,412 triangles, 81 meshes, five materials, zero degenerate triangles or nonfinite vertices. Three maps decode with nonzero variation; all eight lid horn meshes have the correct moving parent. Four mirrored ivory pairs and a central low-relief medallion form an original simplified design, not a copied artisan motif.

Independent saved-source checks: 29 moving and 52 static meshes, **81 opening samples with zero unintended intersections**, plus latch-versus-lid checks. Recursive ancestry includes all moving descendants. Only named hinge-leaf/barrel and latch knuckle/bridge/pin mating bearings exempt. Ten actual attachment contacts establish body bridge/mount/barrel and lid/leaf connections. Interior floor ray hits z=0.2650000155. This is sampled surface clearance, not continuous collision or mechanical certification.

Independent source/GLB import nearest-vertex parity: maximum error 1.712013073529306e-7 units in both directions, under 1e-5. Packed source contains all three maps. This verifies geometry, not byte-identical Blender round trips.

Offline `file://` Edge at desktop 1440×1080 and mobile 390×844 with touch emulation: native open/close, drag, interrupted reset, reduced motion, no overflow, no external HTTP requests or runtime errors. Full-open silhouette maximum absolute NDC 0.892365 (<1). Real corrupted bytes reach GLTFLoader and trigger poster fallback; no-JS poster also verified. Mobile uses desktop NVIDIA RTX 4060, not physical-phone performance testing.

All checks assert and fail nonzero. A deliberate detached-lid-ornament mutation is rejected by the actual theme gate. Motion tests reject missing pivots/empty/nonfinite geometry. The first build genuinely failed at HTML 6,590,610 bytes / GLB 4,372,016 bytes: redundant bevels on tiny stitches were removed while retaining all stitch blocks and the strict cap. An extended-map test initially sampled the wrong channel; glTF roughness is green, not red. The failure log remains, and the corrected channel check measures real variation. Initial side-panel UV collapse was corrected to use the side's longitudinal Y axis; relief was lowered into contact with its panel.

## Visual verdict and limits
Recognizable stylized crimson felt, ivory scrollwork, dark walnut and brass chest; not photorealistic, an ethnographic replica, artisan-endorsed work, or human hand sculpture. Wood is smooth rather than grain-rich; felt fibers are suggested by fine procedural texture; ivory applique is simplified rounded relief with crowded central joins. The inherited long family latch and rear/interior are artistic extrapolations. Front-open views can make the rear joint look offset: the rear-open capture improves legibility and contact checks verify its modeled connection, but small dark hardware interfaces remain visually ambiguous. The outside lid decoration is naturally hidden from front-open views, not missing. No human per-asset approval claimed; the user waived that gate for this collection batch.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge; Node with pinned Three/esbuild dependencies in package.json. Build resolves local node_modules or sibling `iceland-pilot/node_modules`; install dependencies locally for standalone source extraction. No runtime network dependencies. Default Blender executable in `run_checks.py` is the current Windows installation; override `BLENDER_EXE` elsewhere.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python run_checks.py` (build, motion, source, parity, theme, browser, extended)
4. `python package_delivery.py`

Regeneration overwrites generated outputs; preserve manual edits separately. Packaging checks explicit required files, hashes every payload, reads back every ZIP entry, and excludes backups/caches and recursive inventory/check/archive hashes. `delivery-check.json` is outside its own archive. The source ZIP is not part of the standalone viewing budget.

No blockchain nodes, keys, minting, broadcasts, chain queries, production edits, VPS access or deployment. Only the new preview directory changed. Branch backup is not publication or integration. Collection direction remains 201 equally one-of-one boxes; this is one offline art asset.
