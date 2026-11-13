# Jamaica v1 — Blue & John Crow

Open **jamaica-v1.html** directly in Edge/Chrome. The actual model, Three.js runtime, textures and source-rendered poster are embedded; no server or network is needed. Drag/touch to rotate, Open/Close lid, Reset view. Cosmetic movement only: nothing is minted, hosted, deployed, signed or on-chain.

## Delivered
- **HTML 2,926,486 bytes** (<5,000,000); **GLB 1,600,388 bytes**.
- `jamaica.blend`: packed, editable Blender source. `jamaica.glb`: portable actual geometry/maps. `mechanism.blend`: inherited trimmed articulation/liner source, not the shared vault kit.
- `author.py`, `maps.py`, compact procedural maps, viewer/build scripts, tests and raw outputs.
- `poster.png`/`poster.jpg`: actual-source render, not promotional AI art.
- Desktop/mobile closed/open, rear-open and fallback screenshots from actual offline browser runs.
- `inventory.json`: exact byte lengths and SHA-256 for all payload files. Source ZIP includes explicit required files; `delivery-check.json` verifies archive membership and readback hashes. Packaging envelopes exclude themselves to avoid recursive hashes.

## Verified
- Saved-source reopening: **112 moving / 39 static meshes**, **81 staged poses**, zero unintended surface intersections. Every lid terrain/canopy mesh participates. Latch versus lid is also sampled; only named concentric bearing contacts are excluded. Ten connected hinge attachment pairs and interior floor ray at z=0.2650000155 pass.
- Same original hinge/latch world matrices, 80° release before 105° opening, clamped endpoints and invalid-asset negative controls pass. This is sampled surface-intersection evidence, not continuous collision or mechanical engineering certification.
- Independent source/export nearest-vertex parity in both directions: **1.712013073529306e-7 units**, threshold 1e-5. Three packed source maps.
- Actual browser GLTFLoader: **20,488 triangles, 154 meshes, 9 materials**, zero nonfinite vertices or degenerate triangles. Geometry is split into material primitives in glTF, so source mesh counts differ.
- Connected relief: 2,689 vertices; sampled section has four maxima (three dominant peaks by design). 95 canopy centres independently ray-seated on terrain, all terrain owned by lid. Deliberately detached terrain is rejected by the ancestry test.
- Actual decoded limestone color red-channel range 71, roughness green-channel range 92, shale color range 110. All maps at most 512px.
- Offline `file://` Edge: 1440×1080 desktop and 390×844 touch-emulated mobile. Native controls, drag/touch rotation, open/close, interrupted Reset, reduced motion, no overflow, no external HTTP requests or unexpected JS errors. Open pose maximum absolute projected coordinate 0.892365 (<1).
- Real corrupt GLB bytes reach GLTFLoader and trigger poster fallback; no-JS poster works. Poster nonblank pixels are checked. GPU: RTX 4060; mobile emulation is **not physical-phone performance**.

## Design / honest visual limits
The prewritten research-backed `design-brief.md` is the primary reference; no supplied original Jamaica illustration existed. This is a stylized limestone-and-forest landscape keepsake inspired by the Blue and John Crow Mountains, not a geographic map, traditional artifact, botanical survey or photoreal reconstruction. UNESCO/UNEP facts inform material/ecology only; no third-party photographs or textures are copied. No Maroon or sacred symbols are reproduced.

Actual-source and browser visual inspection found clear pale stone/brass construction and connected multi-peak landscape. A bounded correction replaced the first faceted mosaic and abrupt pale wedge with smooth slopes, smaller exposed stone and low broadleaf canopy clusters; `initial/first-source-poster.png` retains the rejected first result. The final stone can read as marble, lit greens as teal/mint rather than deep forest, canopy as simplified rounded clusters, and the terrain apron is visibly stylized. Interior and brass mechanics are simplified. No claim of photographic equivalence or official approval.

## Failures and corrections
- Initial build failed with `MODULE_NOT_FOUND` for esbuild because the requested main-checkout dependency directory was empty. Installed the pinned package dependencies **inside this new folder only**; build then passed. No shared dependency directory was changed.
- Background shell `node` returned `stdin is not a tty`; preserved in `initial/node-shim-failure.txt`. Running the native `C:/Program Files/nodejs/node.exe` executed the unchanged motion tests successfully.
- Negative controls intentionally reject detached lid ornament, invalid geometry inputs, corrupted GLB and an oversized HTML payload. They are regression checks, not a claim of test-first authoring.

## Reproduce
Prerequisites: Blender 5.2.1; Python with numpy, Pillow and Playwright; installed Edge; Node. `npm ci --no-audit --no-fund` in this folder restores pinned dependencies. No dependencies are needed by the delivered HTML itself.
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node tests.mjs`, `python verify_browser.py`, `python verify_extended.py`.
6. `python package_delivery.py`.

Regeneration overwrites source/export/poster; preserve hand-edited variants separately and regenerate all evidence/hashes. `initial/prepare_author.py` is the historical one-time helper adapter, not the final generator; it reads the sibling Japan author. Final `author.py` uses only this folder. Cycles uses four threads, 24 samples, denoising disabled; some render noise remains. Runtime is Three.js 0.180.0 (MIT, license included), esbuild 0.25.11 is build-time only. Mechanism/viewer/verifier lineage is Japan v1 on base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8; no shared art kit or prior preview modified.

Branch backup only: `art/jamaica-v1`; no merge. Final collection integration/review is a separate task. This asset is one of the planned 201 equally one-of-one designs; art completion does not confer custody, issuance or authenticity.
