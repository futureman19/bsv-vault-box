# Japan / Cedar & Moss — finished review pilot v1

Open `japan-cedar-v1.html` directly in Edge. It contains the complete actual 3D model, runtime, textures and real-model poster. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion preference is honored. No server, network connection, mint, wallet or transaction is involved.

## Files
- `japan-cedar-v1.html`: self-contained review attachment, **4,845,566 bytes** (<5,000,000).
- `japan.glb`: portable mesh and embedded maps, **3,079,080 bytes**.
- `japan.blend`: named editable source. `mechanism.blend`: trimmed reusable source of the inherited articulation/interior/hardware, not an Iceland art model.
- `poster.png` / `poster.jpg`: actual source render; `desktop-closed.png`, `desktop-open.png`, `desktop-open-rear.png`, `mobile-closed.png`, `mobile-open.png`: actual offline browser captures.
- `reference-comparison.jpg`: original marketing concept vs actual model, uniformly scaled to equal measured wood width. Same front-left direction; lower comparison camera approximately matches reference elevation, not recovered exact camera calibration. No anisotropic warping. `comparison-method.json` records factors.
- `references/primary-japan.png`: unchanged user-provided original marketing concept, separate from runtime/model.
- `design-brief.md`: research links, interpretation and measurable acceptance.
- JSON checks and raw output text: actual evidence. `initial/` retains initial payload failure, collision regression, byte-roundtrip finding and early render.

## Verified
Actual Three GLTFLoader: 48,664 triangles, 200 meshes, 11 materials, zero nonfinite vertices or degenerate triangles. Real decoded texture ranges: wood 89, end grain 35, granite 143 (red-channel range); maps 512 or 256 pixels. All 4 foliage meshes, 28 branches and terrain belong to the lid. Physical trunk is +X/+Y (rear/right), not inferred from screen coordinates. See placement-check.json and top-down-source.png.

Saved-source reopening: genuine hollow floor ray at z=0.265, ten attachment pairs connecting hinge mounts/body and leaves/lid. **81 sampled opening poses, all 101 moving and 99 static meshes, zero unintended surface intersections**. All branches, foliage and terrain included. Only explicit mating hinge leaf/barrel and latch knuckle/bridge/pin bearings excluded. This is sampled surface-intersection evidence, not continuous collision or mechanical engineering certification.

Source/export nearest-vertex error 0.0000001713 units (<0.00001). Independent re-export after reopening preserves exact JSON, positions, normals, indices and embedded image bytes. Blender save/reopen changes some UV float32 values by at most 0.0000001193; documented 0.000001 UV tolerance. Re-export is NOT byte-identical; its initial strict-hash failure is preserved.

Offline `file://` Edge on desktop and 390×844 mobile touch emulation: native open/close taps/clicks, rotation/drag, reset during movement, reduced motion, real corrupt-GLB parser failure poster, and no-JS poster passed. No external HTTP requests, JS errors or horizontal overflow in successful runs. Full-open projected vertices fit (maximum absolute NDC about 0.8924). Rear-open screenshot shows the tree that is naturally hidden behind the lid from the front. RTX 4060 desktop browser; no claim of physical-phone performance.

## Visual verdict / deliberate differences
Recognizable reference-led cedar collectible, **not photorealistic or an exact replica**. Fine grain is real and portable but regular/procedural; lid grain is softer at normal/mobile size. Tree is restrained, branched and needle-leaved, but sparser and more generic than the dense aged cedar in the marketing art. Moss is present and enlarged in the final bounded correction, still less lush than the concept. Wood/brass are cleaner and lighter; stone feet flatter. Inherited staged latch is longer than the concept's compact clasp. Small brass corner caps are family extrapolations. The unexplained front circular hole is deliberately omitted; no invented function. Rear/interior details are extrapolated. The green reveal is a mineral/moss-inspired seam, not literal live moss sealing a real chest.

Two focused corrections: (1) denser/asymmetric tree, smooth needle normals to remove redundant export splits, darker/filled seam; (2) more visible moss and narrowed rear seam after actual hinge-contact failure. Stop here for user art review, not automatic further polishing or collection rollout.

## Reproduce
Use Blender 5.2.1, Python with Pillow/numpy/playwright, and Node with package.json dependencies. No node_modules in archive. Existing build uses local node_modules if present, otherwise the discovered sibling pilot's installed compiler dependencies; standalone extraction requires `npm install` in this directory. Source authoring itself needs no sibling paths.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. `python verify_browser.py` and `python verify_extended.py` (installed Edge required).
5. Run Blender as above with `verify_source.py`, `verify_parity.py`, `verify_reexport.py`, then `render_review.py`.
6. `python test_theme.py`; `python compare.py`; `python package_delivery.py`.

Regeneration overwrites authored output; make manual edits in a separate source copy. Provenance-preservation check references original local paths and only executes when those originals exist. Package delivery location can be supplied with `--delivery`; default is the active-profile delivery path used here.

## Rights and scope
Geometry and maps are procedurally authored for this pilot, not human hand-sculpture, scans, harvested Yakusugi or photogrammetry. The original reference is user-provided marketing artwork; no new license to its imagery is asserted. Mechanism, viewer and test lineage: repository Iceland v10 at commit 13f2881190b0cbe6cb4a278b086001464c7b734d, with frozen input hashes. Reused Three.js 0.180.0 runtime is MIT (THREE-LICENSE.txt); esbuild 0.25.11 is build-time tooling. Research URLs are cited for factual inspiration; no third-party forest photographs/textures are embedded.

Local art preview only. No production docs edit, public deployment, node startup, funds, token issuance or claim of on-chain storage/custody verification. Collection direction remains 201 equally one-of-one designs; no launch accessories.
