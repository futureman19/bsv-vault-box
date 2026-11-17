# Saudi Arabia v1 / AlUla Sandstone

Open **saudi-arabia-v1.html** directly in Edge/Chrome. Complete offline 3D viewer with embedded model, maps, runtime and actual-source poster. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion preference supported. Cosmetic inner collectible only: not minted, hosted, signed, on-chain or a custody-container interaction.

## Delivered
- HTML **3,173,423 bytes**; GLB **1,802,900 bytes**. Strict HTML cap: <5,000,000 bytes.
- `saudi-arabia.blend`: packed editable Blender source; `saudi-arabia.glb`: standalone model.
- `mechanism.blend`: frozen Japan pilot's stripped family mechanism; shared base kit untouched.
- `maps/`: original procedural sandstone colour, roughness and darker foot atlas, each 512x512.
- `poster.png`/`poster.jpg`: real source render, not AI promotional imagery. Desktop/mobile closed/open and fallback PNGs: actual offline Edge captures.
- Source scripts, design brief, raw execution text, acceptance JSONs, exact SHA-256 inventory and readback-verified source ZIP.

## Verified
61 meshes, 17,920 triangles, four materials; actual GLTFLoader: zero nonfinite vertices or degenerate triangles. Three separately seated lid-owned outcrops; source roots at z=1.97, separated X bounds, tallest below 3.05. Inherited pivot translations independently compared with included mechanism. Packed images and runtime decoded variation verified, including glTF roughness green channel.

Saved source independently reopened: hollow interior floor ray z=0.2650000155; ten hinge attachment pairs. **81 sampled poses**, every one of **22 moving / 39 static meshes** included, zero unintended surface intersections. Latch-versus-lid sampled separately; only explicitly named mating bearings exempt. Motion tests verify initial 80-degree latch release before 105-degree lid opening. This is sampled surface-intersection evidence, not continuous or manufacturing certification.

Bidirectional source/GLB nearest-world-vertex maximum error **1.712013073529306e-7**, below 1e-5. Actual file:// Edge desktop 1440x1080 and touch-emulated mobile 390x844: native open/close, mouse/touch rotation, interrupted reset, reduced-motion endpoints, no horizontal overflow, no external HTTP requests or runtime errors. Full-open projection maximum absolute NDC ~0.9112. Deliberately corrupt GLB reaches the real loader and displays poster fallback; no-JS poster also tested. RTX 4060 desktop renderer, not physical-phone performance testing.

Theme negative control genuinely detaches an outcrop in memory and is rejected by the unchanged parent assertion. No accidental art/check failure occurred in this run; the negative control is explicitly post-implementation regression proof, not a fabricated pre-model failure. Shared pilot node_modules was inspected and contained no compiler, so pinned dependencies were installed only in this new directory. No sibling dependency tree was modified.

## Visual verdict and limits
Actual source render and mobile closed/open captures inspected. Three differently sized outcrops are seated and readable, the complete open pose fits, and the box is visibly hollow. This is an original stylized interpretation of AlUla sandstone, **not a site replica or photorealistic geological model**. Banding is repetitive and can read as wood; erosion is rounded and simplified. The bronze seam is conspicuous and the inherited long clasp's functional engagement is only suggestive. The round front boss is decorative, not a keyhole. Front-open presentation naturally hides the top ornaments behind the raised lid; verified ancestry keeps them attached. Unseen surfaces and hardware are design extrapolations. No sacred inscriptions or borrowed photographs are used. User waived per-asset review; final collection review remains separate.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/Playwright and installed Edge; Node with included pinned package manifest/lock. Build dependencies are not runtime dependencies and are excluded from archive. From this folder:

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run the same Blender invocation on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; repeat theme with `-- --negative`.
5. `node test_motion.mjs`; `python build.py`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Authoring executes the included helper files and uses the included frozen mechanism; no sibling art files are required. Regeneration overwrites model/poster, so preserve manual edits separately. Inventory excludes itself, the ZIP and delivery-check to avoid recursive hashes; ZIP contains inventory and every explicit required artifact. Folder-local Git attributes preserve exact bytes. Three.js MIT license included. No base kit, production code, chain, VPS, wallet, keys or other previews changed. Branch backup only; merge belongs to final integration.
