# Morocco — Saturn atmosphere v4

Local interactive material-only study; not hosted, minted, or connected to custody. Open `morocco-saturn-v4.html` directly. All viewer assets are embedded; no runtime downloads.

## Result and limits
Body changed from granular brown sandstone to flowing creamy ivory/honey/ochre belts with muted terracotta accents. The flat texture was independently generated with xAI grok-imagine-image, reduced to 1024x256, smoothed lightly, contrast-adjusted for broad zones, and seam repaired. Two swatches A/B were inspected before export; B selected. One bounded targeted correction advected the existing painting through four sparse elliptical shear cells after the first actual-browser review looked too straight. No sinewave band synthesis, dense pits or new meshes. Fine normal slopes are capped at 0.05 per tangent axis and roughness lies around 0.70–0.765.

Final browser closeup reads as stylized Saturn cloud bands. Mobile shows cream/gold flow clearly, but small shear wisps remain subtle and the rigid box can still read as banded onyx. This is not an exact NASA atmospheric reconstruction or an unconditional visual-approval claim. Parent/user review remains appropriate.

## Reference / rights
First inspected NASA Cassini **Waves on Saturn**, PIA06655, credit **NASA/JPL/Space Science Institute**:
https://science.nasa.gov/resource/waves-on-saturn/
Image: https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/p/PIA06655.jpg
Rights guidance: https://www.nasa.gov/nasa-brand-center/images-and-media/
This infrared grayscale image supports morphology only, not color. Included solely as a factual informational comparison. No NASA pixels were put in the model maps, no endorsement is implied, and no commercial clearance is claimed. NASA guidelines include third-party exceptions and discourage NFT use of NASA imagery. The generated texture was text-only, not an image edit or NASA-image derivative. It is AI-generated art, not scientific data. Original Morocco concept is included for comparison and non-body feature preservation. Full generation prompt and source URLs are in references/.

## Preservation and verification
- All non-image GLB bufferViews are byte-identical to v3, including body UVs. Exact nodes, meshes, non-body material JSON and images. Existing continuous perimeter angular UVs retained; all three map endpoints match exactly.
- Viewer JS, compiled bundle, HTML template and motion module byte-identical to v3. Lighting, camera, dimensions and motion unchanged.
- Saved .blend independently reopened: 69 objects, original geometry/transforms/parents/camera/lights/non-body materials and UVs unchanged; packed maps match finalizer inputs.
- Fresh 81-pose mechanism/attachment sampling: no collisions beyond the original narrow intentional bearing exclusions. Source/export geometry roundtrip max error 1.712013073529306e-7.
- Real Edge GLTFLoader parses exported images/finite geometry/UVs; no degenerate triangles. Desktop and emulated-mobile offline file:// rotation, native taps/touch drag, open/close, interrupted reset, reduced motion, corrupt-GLB fallback, no-JS poster, no overflow, no external requests or unhandled JS errors passed. Emulation is not a physical phone benchmark.
- Final delivery HTML reopened after copying. ZIP inventory and SHA-256 readback verified for every entry and delivery copy. See delivery-check.json and inventory.json for literal byte counts/hashes.

## Files and reproduction
`morocco.blend` editable packed source; `morocco.glb` portable material; `poster.png/jpg` actual Blender model; desktop/mobile captures and camera-matched before/after are actual browser renders. `material-reference-board.jpg` labels each source explicitly. No generated box render is used.

Python needs numpy/Pillow; author/source checks require Blender 5.2.1; browser checks require Playwright + installed Edge. Build uses Node/esbuild/Three from local node_modules or repository sibling iceland-pilot/node_modules (dependencies not archived; package.json included). The existing compiled viewer bundle is included. Run:

1. `python materials.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python finalize_glb.py`
4. `python build.py`
5. `python verify_preservation.py`, Blender `verify_source_preservation.py`, `verify_source.py`, `verify_parity.py`
6. `python verify_browser.py`, `verify_extended.py`, `verify_material_runtime.py`

`review.py`/`final_audit.py` additionally compare with sibling morocco-sandstone-v3. `package_delivery.py` uses the explicit original Windows delivery location. `setup.py` is disabled historical scaffolding, not a rebuild step. AI generation is not deterministically reproducible, so the exact generated master is included and subsequent transformations are deterministic. Rebuilding author.py overwrites the authored source; preserve manual edits first. No docs/, production, funds, nodes, wallet, mint, push or deployment actions.
