# Philippines v1 — Cordillera / Contour & Paddy

Open **philippines-v1.html** directly in Edge/Chrome: fully embedded offline 3D viewer, **2,352,039 bytes**. GLB **1,193,180 bytes**. Drag/touch rotate, open/close and reset; reduced motion supported. Not hosted, minted, signed or chain-verified. Cosmetic opening only.

## Design and files
A regional Ifugao rice-terrace interpretation with six nested contour retaining tiers and six green field surfaces on a mineral keepsake box. Research and pre-model visual contract: `design-brief.md`. `philippines.blend` is the packed editable Blender source, `philippines.glb` the portable export, `maps/` the generated mineral textures. `poster.png` and JPEG are actual source renders, not AI images. Desktop/mobile PNGs are actual offline browser captures. `mechanism.blend` preserves the repository Japan pilot's trimmed inherited articulation. Shared vault kit and all prior previews are unchanged.

## Verified
- Source independently reopened: hollow floor ray z=0.2650000155, ten intersecting hinge attachment pairs. **81 poses, 28 moving and 39 static meshes, zero unintended surface intersections**; latch versus lid also tested. Narrow named bearing exclusions are documented in source-check.json. Sampled surface clearance is not continuous or manufacturing certification.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, threshold 1e-5. Three packed source maps; source and GLB geometry match within this tolerance (not asserted byte-identical re-exports).
- Actual GLTFLoader: **16,876 triangles, 67 meshes, 6 materials; zero nonfinite vertices and zero degenerate triangles**.
- Six tier heights 2.08–2.58, decreasing widths and twelve lid-parented terrace/field parts. Deliberately detached field was rejected by the same ancestry check: an exercised negative control, not a historical defect. Motion tests reject missing lid, empty geometry and invalid bounds.
- Offline `file://` Edge: desktop 1440x1080 and touch-emulated 390x844; native controls, rotate, open/close, interrupted reset, reduced motion, no overflow, zero external HTTP requests and zero errors. Full-open maximum absolute NDC 0.892365. Genuine corrupt bytes reach the GLB parser and show the poster; JavaScript-disabled poster separately tested. RTX 4060 host; no physical-phone/FPS claim.
- Actual-loader decoded color and green-channel roughness variation, map dimensions <=256, UI and canvas country-copy audit.
- Exact-byte SHA-256 inventory, ZIP content readback and staged Git blob comparison. Folder-local -text attributes preserve byte identities.

## Visual verdict and limits
Source and mobile screenshots were visually inspected. Terraces and brass fittings are readable with no obvious clipping. This is deliberately stylized: regular nested terraces can read as a contour maquette rather than a geographically specific landscape; no rice plants, forest watershed, water simulation or mapped named site is depicted. Paddy/stone contrast is restrained, body is lighter gray under studio lighting than the warm-gray target, and the low-sample actual source poster retains some render noise. No photorealism, reference equivalence, traditional artisan authorship or nationwide cultural representativeness is claimed. User waived per-asset human review for this batch; this is technical delivery, not human art approval.

## Reproduce
Blender 5.2.1; Python with numpy, Pillow, Playwright; installed Edge; Node with pinned package.json/package-lock.json. Shared baseline node_modules was empty (esbuild absent), so identical pinned dependencies were installed **only in this directory**, excluded from Git/ZIP. No sibling toolchain modified.

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender similarly with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Regeneration overwrites model/render outputs; preserve manual variants separately and regenerate all evidence/inventory. Tests are assertions capable of failing; no asset-gate failure occurred on this run. The intentional corrupt-input and detached-field controls are recorded as negative controls, not concealed failures. Initial direct research extraction backend was unavailable; factual citations were retrieved through search excerpts instead. Build/runtime license: Three.js MIT, included THREE-LICENSE.txt. No third-party research images/textures embedded. No blockchain, production site, shared-kit or VPS operations.
