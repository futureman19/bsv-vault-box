# Iceland / Basalt — realism study v2

Local-only, actual articulated 3D collectible. Not minted, signed, published or deployed. This is one inner collectible, not an outer custody container. No wallets or blockchain nodes used.

## Outcome and limits

A material/lighting upgrade of the approved v1 geometry and animation, **not a claim that hyperrealism has been achieved**. Added portable PBR textures, small eroded exterior bevels and sub-centimetric source-coordinate edge offsets, a quieter non-emissive mineral seam, explicit lid-side hinge straps/rivets, and a shadow-receiving studio floor. Kept original dimensions, scene scale, pivot transforms and motion source byte-identical; the original v1 directory is unchanged.

All twelve PNG maps are locally, deterministically generated procedural textures, not photographs, scans or hand-painted artist work. Three 2K material sets (basalt, polished lid, brass) and one 1K liner set each contain base color, tangent-space OpenGL normal and roughness. Source images are packed in the editable Blender file and actually embedded in GLB. glTF repacks roughness into its metallic/roughness green channel. No paid/external texture downloads. Three.js retains its accompanying license.

The intended surface features are small pores/fractures and restrained mineral tint, fine polishing scratches and brass roughness/tarnish variation. **Observed limitation:** macro inspection still reads broad mottling more strongly than fine pits/scratches. Brass tarnish is procedural variation, not curvature-baked recess-specific oxidation. The regular column spacing, uniformly rounded hardware, lid fit and small hinge scale retain a stylized-prop impression. The open lid still has a slightly hovering appearance despite connected straps and passing sampled clearance. Interior depth is visible, but the inset remains somewhat cloudy. This bounded pass stopped after one focused browser-review polish iteration; no assertion of photographic fidelity.

The source's pre-existing physical-coordinate scale is retained rather than silently resized. No engineering/manufacturing strength or continuous collision guarantee is implied.

## Deliverables

- `iceland-realism-v2.html`: standalone offline interactive viewer, embedded real GLB, renderer and fallback poster. Rotation/touch, zoom, staged latch/lid open-close, reset and reduced motion.
- `iceland.blend`: named editable geometry, packed images, source-only Cycles studio/camera.
- `iceland.glb`: portable articulated geometry with named `Lid_Hinge` and `Latch_Pivot`; animation is driven by unchanged `motion.mjs` in the HTML, not a baked GLB clip.
- `textures/*.png`, `generate_textures.py`: deterministic original image-map sources/generator.
- `author.py`, `upgrade.py`: reproducible Blender authoring. Regeneration overwrites v2 outputs only and will overwrite manual v2 edits.
- `poster.png`: actual Cycles model render, not substituted AI concept art.
- `comparison-closed.jpg`, `comparison-open.jpg`: real before/after browser GLBs at numerically matched cameras. Lighting/materials intentionally differ.
- `detail-basalt-brass.png`, `detail-lid.png`, `detail-hinge.png`: real browser detail views, not retouched photography.
- `desktop-*.png`, `mobile-*.png`: native Edge screenshots; mobile is desktop GPU device emulation, **not a physical phone**.
- `manifest.json`, `delivery-check.json`, `iceland-realism-v2-source.zip`: exact hashes, allowlisted inventory, ZIP readback and copy verification.

## Measured payload / download impact

Final GLB: **27,688,600 bytes**, 17,488 triangles, 80 mesh primitives, 5 materials, 12 embedded image maps. Original v1: 591,292 bytes / 9,632 triangles. Texture-source PNGs: 23,369,093 bytes; embedded exported image payload: 26,782,814 bytes. The geometry increase comes primarily from small bevels, not displacement tessellation.

Standalone HTML: **40,408,995 bytes**, versus v1 3,939,591 bytes. The GLB is approximately 46.83 times v1's payload; lossless textures and base64 HTML embedding are deliberately expensive. This is an uncompressed inspection/source delivery, not a production-optimized mobile asset. No FPS or device-memory performance claim. Final source-ZIP bytes/hash are in `delivery-check.json`. The ZIP exceeds 100 MB and is intentionally a local delivery artifact ignored by Git; the scoped source, model, textures, HTML and evidence are committed instead. No archive upload or publication is authorized.

## Verification actually executed

- Original-style `node --test tests.mjs`: 2/2 passed; unchanged latch-first motion contract and invalid-asset rejection.
- `python test_textures.py`: all 12 encoded source maps decoded; size and nonuniformity assertions passed. Test-first missing-map RED and initial insufficient normal-channel variation failure retained.
- Blender `verify_source.py`: saved source reopened, 17,488 finite nondegenerate evaluated triangles, UVs on all meshes, 12 packed images. **81 sampled poses, zero disallowed BVH intersections**, hollow-floor ray z=0.2650000155. Existing intentional bearing exemptions unchanged; added hinge straps/rivets are included, not excluded to pass. This is sampled surface-intersection testing, not continuous collision or physical tolerance analysis.
- `python verify_browser.py`: desktop 1440x1080 and native Edge mobile emulation 390x844 under offline file://; real GLTFLoader parsing, zero nonfinite/degenerate triangles, rotation/native CDP touch, open/close, mid-motion reset, reduced motion, no horizontal overflow, no external HTTP requests, no unexpected JavaScript errors. Full open silhouette inside frustum. Corrupted embedded GLB triggers real parser fallback and disables controls without an uncaught error.
- `python verify_pbr.py`: 12 actual loaded image maps, UVs and >=1K dimensions; nonuniform decoded normal XY and roughness green channels. All images embedded, no external image URIs. Fresh v1/v2 closed/open camera comparison within 1e-10. Initial exact-float equality failure preserved; only numerical camera tolerance corrected, not collision thresholds.
- `python verify_preservation.py`: all 40 captured v1 files unchanged, motion byte-identical, pivot transforms identical, closed envelope within 1e-6.
- Final visual inspection: actual Blender poster, browser macro, open-mobile frame and before/after comparisons. Remaining realism shortcomings stated above. First browser review screenshots and logs retained.

## Rebuild / rerun (Windows native paths)

From this directory, use Python with numpy, Pillow and Playwright, installed Edge, Node, and Blender 5.2.1. `npm ci` installs pinned-lock Three.js/esbuild dependencies if not already present; `build.py` also supports the original sibling pilot's existing dependencies. No server is needed.

```
python generate_textures.py
python test_textures.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python verify_source.py
node --test tests.mjs
python build.py
python verify_browser.py
python verify_pbr.py
python verify_preservation.py
python package_delivery.py
```

Before/after and preservation tests require the untouched sibling `../iceland-pilot` baseline; generation, texture/source checks and standalone browser lifecycle do not. `package_delivery.py` uses the explicitly scoped local output destination. Logs are raw captured outputs, including failures; no `.blend1`, node_modules, secrets or unapproved files belong in the archive. The manifest identifies delivered bytes, not a trusted authenticity certificate.
