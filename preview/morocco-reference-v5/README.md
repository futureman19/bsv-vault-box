# Morocco v5 — original-reference body finish

Local review candidate, not minted, deployed, published or approved by the user. Only the body material/UV changed. The functional v4 source is the mechanical baseline, not the visual target. The only art target is `references/primary-morocco.png`, identical to the user's original generated marketing art.

## Outcome and visual limits

The body now directly retains the original's reddish salmon/terracotta matrix, ochre/cream fine irregular strata, pale mineral flecks and conspicuous dark jagged upper-right vein. Final side-by-side vision review judged the color and layer structure substantially closer than v4, not an exact match. V5 remains somewhat lighter/pinker, with flatter fine surface depth, a more conspicuous pale front-left corner and local reconstructed patch transitions. Lighting/camera of the original cannot be recovered exactly; the actual v4/v5 browser comparisons use identical lighting/camera, equal object widths and proportional scale only. No perspective warping was applied to comparison screenshots.

Body-only scope means the pre-existing wood, ceramic, ridge, brass hardware, geometry, dimensions, viewer, lights and motion remain unchanged. Nonbody discrepancies with the marketing illustration remain deliberately out of scope.

## Method and provenance

- User-generated artwork, not a stone scan or scientific image. No NASA/v4 imagery was used to design the new body.
- Perspective rectification uses separate annotated front/left quadrilaterals. Exact coordinates, hardware/shadow masks, source hash and transformations are in `material-provenance.json`, `materials.py`, and `references/`.
- Two swatches only. A's horizontal interpolation produced visible smears and was rejected (`candidate-A-rejected-smears.jpg`). B replaces masks with intact, nearby same-height exemplar patches selected by boundary-color error; difficult boundary components use neighboring valid source pixels. The hidden regions are reconstruction, not recovered truth.
- Low-order illumination approximation removes edge shade and applies a side-face gain/partial median correction. Single-image intrinsic albedo is underdetermined: residual illumination may remain. Original dark left-face lighting is not blindly baked in as its intrinsic color.
- One post-model correction subdues milky peach/cream reflectance (luminance-weighted RGB attenuation up to 12/16/18 percent), and reflects narrow edge context rather than extruding a scanline. It does not create new strata or change scene lighting.
- Back/right faces are mirrored extrapolations, with visible repeat motifs possible. Narrow corner transitions are blended; exact geological continuation through every corner is not claimed.
- One 2112x256 perimeter color atlas plus same-size compact normal/roughness maps. Physical perimeter 13.2 units, height 1.6 units, 160 texels/unit in each direction; rectangular perimeter UV avoids angular sampling stretch. Rear endpoint pixels match exactly. Very low relief derives from source grain, not uniform procedural noise.
- `texture-swatch-board.jpg` shows original crop, cleaned intermediate front/left patches before final reflectance calibration, and the final calibrated perimeter atlas.

## Acceptance actually exercised

- Standalone offline HTML: **4,663,232 bytes**, below the strict 5,000,000-byte ceiling. GLB: **2,909,040 bytes**. All runtime assets are embedded; no network dependencies.
- Real Edge GLTFLoader: 62 meshes, 52,814 triangles, 8 materials; zero nonfinite vertices and zero degenerate triangles. Base/normal/roughness maps decoded and finite UVs checked.
- Saved editable source independently reopened. Geometry/source-export maximum world vertex error 1.712013073529306e-7. All source geometry, transforms, parents, cameras, lights and nonbody material/UV records preserved. All nonbody GLB bufferViews and viewer/motion/template/bundle bytes preserved exactly.
- 81 fresh motion samples: no unintended collisions; bearing and ridge contacts retained; hollow interior floor ray passes. These are sampled checks, not a continuous analytical proof.
- Desktop and touch-emulated mobile offline file:// tests: rotation, native controls, open/close, interrupted reset, reduced motion, no overflow, no external requests or runtime errors. Actual corrupt input reaches GLTFLoader and shows the poster fallback. No-JS fallback tested. Mobile emulation is not physical-phone performance testing.
- Reference-specific tests: 98,518 unmasked front pixels match declared calibrated source to mean absolute error 0.50057/255; horizontal detail correlation 0.99947; vertical palette profile correlation 0.9999999. Rejected v4 error is 71.3163/255. These prove source retention outside masks, NOT whole-render equivalence or accurate hidden reconstruction.
- Previous v4's 86 files and the original reference hash verified unchanged. Current working tree was clean before this isolated folder was created.
- First extended check failed its inherited 1024-per-dimension and >10 normal-range assumptions. The new aspect-correct strip uses only 540,672 pixels; the corrected check enforces <=1,048,576 pixels and <=2112 maximum dimension, and accepts subtle nonzero normal variation. The whole-HTML cap and all actual geometry/mechanism/browser gates remain strict.

## Files

Open `morocco-reference-v5.html` directly in a browser. `morocco.glb` is the standalone model, `morocco.blend` is packed/editable, and `poster.png`/`poster.jpg` are actual source renders of this material (not AI promotional replacements). `reference-comparison.jpg` and `body-closeup-comparison.jpg` compare original/v4/v5. The source ZIP includes the explicit required artifacts, maps, masks, source, baseline, scripts, evidence and exact inventory, including the standalone GLB. ZIP paths and every archived/copied hash are checked on readback.

## Exact principal SHA-256 hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| morocco-reference-v5.html | 4663232 | c08f7fe5129ee75691808f3137efa8a3f32e4ace1d2f1f7316d3d2b30695338d |
| morocco.glb | 2909040 | 7636595f8db0560387b2391cdbd5264509b3313e0decb839f269fd20d3a95417 |
| morocco.blend | 1816173 | 7038af7361d26aaec6c45e7f1ebef12f7d6ff6daebe513f334de0506706ee4c2 |
| poster.png | 1529244 | 76d92ae9e916e233162170402b9ac43de8449bea3c4ce6fab1ebbe5409cf03e4 |
| poster.jpg | 135564 | 707409bbe4dfc3f5881f48e94b983e0077f4c962c72f7c885289993f268ff309 |

Every other artifact hash is in `inventory.json`. Final ZIP size/hash and copied-delivery offline test are in `delivery-check.json` (kept outside its own ZIP to avoid recursive hashing).

## Rebuild

Python with numpy/Pillow; Blender 5.2.1; Node/esbuild/Three; Playwright with installed Edge. No image-generation API is needed. Baseline GLB/blend, original art and masks are included. Scripts resolve paths relative to this folder except the explicit delivery path; `review.py` and preservation history checks additionally use sibling v4. Build finds local node_modules or sibling `iceland-pilot/node_modules`; dependencies are not archived, but package.json and the compiled viewer are included. These are disclosed source-build environment dependencies, not offline viewer dependencies.

1. `python materials.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python finalize_glb.py` then `python build.py`
4. `python verify_preservation.py`; run Blender on `verify_source_preservation.py`, `verify_parity.py`, `verify_source.py`
5. `python verify_browser.py`, `python verify_extended.py`, `python verify_material_runtime.py`, `python verify_reference.py`, `python review.py`, `python verify_fallbacks.py`
6. `python package_delivery.py`

Authoring overwrites the generated source; preserve manual edits before rebuilding. Rebuilding changes source/render hashes; update this README/inventory after a new build rather than claiming old hashes. No docs/, public site, wallet, chain, nodes, deployment or push changed.
