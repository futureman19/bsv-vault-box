# Iceland v8 — bounded stone, river and glacier refinement

Open **iceland-stone-ice-v8.html** directly. It contains the actual GLB, Three.js viewer and rendered fallback. No server/network required. This is a cosmetic inner-collectible study, not minted, deployed, or a custody implementation.

## Delivered result
- Actual v7 packed source used as input, not reconstructed from a poster. Wide body, brass hardware, hollow liner, glossy black lid material, original camera/light and staged motion retained.
- Exterior cladding receives irregular tapered wedge cuts of varied depths, including larger selected missing shoulders. The continuous inner walls are untouched. Independent old/new surface rays measure changed recesses in **68 blocks**, across front/rear/left/right, with maximum measured recesses **0.2134 / 0.1902 / 0.1587 / 0.2059 scene units** respectively.
- Shared generated **512×512 color, normal and roughness** maps add mineral grain, not photographic scans. Existing moss remains visible; only v7 growth that protruded after cutting is re-seated.
- Original river route widened organically, with a darker center and narrow pale edge bands, in a real expanded shallow boolean inset. Six matching vertices join the channel and side cascade exactly. Glacier overlaps upstream water.
- Asymmetric connected serrated glacier ridge, interrupted crevasses, height-based portable vertex colors, transmission, and a thickened perimeter apron. All ice/water remains lid-parented.

## Measured acceptance
- Complete HTML **4,361,429 bytes**, under both 4.5MB target and 5,000,000-byte hard cap.
- GLB **2,690,800 bytes**, **38,535 triangles**, **459 loaded mesh primitives**, **19 materials**. Zero nonfinite positions and zero degenerate triangles under the unchanged browser threshold.
- Saved-source reopening: **81** staged motion samples, zero forbidden overlaps, same bearing exclusions; hinge attachment checks pass, hollow floor ray hits at z=0.265. This is sampled clearance, not continuous mechanical certification.
- **323** evaluated mesh records unchanged, including structural liner and hardware. **48** interior wall rays pass. No change to animation module.
- Independent source/GLB vertex parity max distance **1.712013073529306e-7**, under original 1e-5 tolerance.
- Real GLTFLoader decodes all 512px maps with nonconstant pixel values; glacier vertex colors vary and transmission is retained.
- Offline Edge desktop and emulated touch-mobile: rotate/touch, reset, open/close, reset mid-motion, reduced motion, corrupt embedded GLB fallback, no-JS poster, no horizontal overflow, zero external requests/errors. Full-open projected extent <0.893 NDC. Tests ran on desktop NVIDIA RTX4060, not a physical phone and not a performance benchmark.
- `delivery-check.json` and `inventory.json` give exact blend/ZIP/texture/image byte counts and hashes. ZIP inventory and every member read back; delivery copies read back; prior-input hash manifest rechecked.

## Visual judgment and limits
Primary AI promotional artwork was compared with the actual v7 browser render before authoring (`acceptance-gaps.md`). Final matched-camera front/rear/detail images and normal mobile view show finer stone grain, localized lost volume, a clearer wider river and a stronger jagged glacier. Two bounded visual corrections were made, then authoring stopped.

**Not promotional photorealism:** the long column rhythm remains; chips are localized, some break planes still look cut; grain is uniform at close range and mostly unresolved on mobile. Water is still a miniature inlay/ribbon with a deliberately short lid-attached cascade, not simulated flowing water. The glacier remains faceted and miniature-mountain-like; translucency is restrained. Moss remains somewhat leafy. The black lid can show a broad gray studio reflection in the Blender poster; browser material and lighting were not changed to hide geometry.

The first failed browser run found degenerate geometry. Diagnosis located collapsed old moss lancelets after attempted per-vertex reseating; those original lancelets are now left untouched. Boolean triangulation cleanup is applied only to changed cladding/slab. Final strict browser and independent parity tests pass; initial failure evidence is retained, not relabeled as success.

## Files
- `iceland.blend`, `iceland.glb`, `iceland-stone-ice-v8.html`: editable source, portable asset, self-contained viewer.
- `poster.png` / `poster.jpg`: actual Blender render, not AI artwork.
- `before-after.jpg`, `rear-before-after.jpg`, `detail-before-after.jpg`: v7 versus final v8 actual browser, identical camera/light per pair.
- `stone-closeup.png`, `ice-river-closeup.png`, desktop/mobile closed/open captures, no-JS/corruption captures.
- `reference-comparison.jpg`: labeled AI promotional reference against actual browser model at equal width; no proportion warping.
- `textures/`, `author.py`, `textures.py`, build/viewer/motion source; `approved-v7.blend` and `.glb` preserve portable authoring inputs.
- `*-check.json`, test scripts/output, `preserved-inputs.json`: measured evidence. `initial-poster.png`, `correction1-before-after.jpg`, failure logs are historical intermediate evidence, not current deliverables.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/playwright, Node, and Edge. The HTML itself has no installation requirements.

1. In this folder, run `npm ci` if dependencies are not already available in sibling `iceland-pilot/node_modules`.
2. `python textures.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender scripts `verify_geometry.py`, `verify_source.py`, `verify_parity.py`, `test_features.py` with the same background flags.
6. `python verify_browser.py`, `python verify_extra.py`, `python verify_comparison.py`, `python verify_loader_variation.py`.

Authoring overwrites candidate outputs. Do not rerun `setup.py` for a standalone regeneration: it is the original repository bootstrap/provenance capture. Old/new screenshot checks and source provenance checks intentionally refer to original sibling preview/reference locations; core authoring uses the included packed v7 source. Packaging uses this installation's explicit output path. No changes outside this new preview/delivery scope, no push/deploy/mint.
