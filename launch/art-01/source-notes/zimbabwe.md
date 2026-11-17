# Zimbabwe v1 — Granite & Kopjes

Open `zimbabwe-v1.html` directly in Edge/Chrome. Self-contained offline actual 3D model, not a promotional illustration. Drag/touch rotation, open/close, reset and reduced motion are supported. Cosmetic motion only; no wallet, chain, mint, node, deployment or custody operation.

## Delivery
- HTML: **3,281,668 bytes**, strictly below 5,000,000 bytes.
- GLB: **1,859,688 bytes**.
- `zimbabwe.blend`: editable, packed Blender source; `mechanism.blend`: inherited trimmed Japan mechanical source.
- `maps/`: independently generated compact granite color/roughness and dark liner maps.
- `poster.png` and embedded `poster.jpg`: actual Cycles source render, no AI substitute.
- Desktop/mobile closed/open PNGs and no-JS/corrupt-model fallback captures.
- `inventory.json`, `delivery-check.json`, source ZIP, scripts and raw `*-output.txt` evidence.

## Verified
Real GLTFLoader reports 27,724 triangles, 280 meshes, five materials, zero nonfinite vertices and zero degenerate triangles. Independent saved-source/export nearest-vertex discrepancy is 1.712013073529306e-7 units, below 1e-5. Three packed source maps; real loaded color/roughness variation tested (roughness green channel).

224 individual staggered masonry blocks; four smooth lid-borne boulders. Contact intersections establish crown/middle/base/ground seating, companion/ground seating and ground/lid seating. Maximum boulder z=3.05999994, below the 3.10 brief limit. A deliberately detached crown is rejected by the same theme validator. Inherited pivot transforms compared exactly against reopened mechanism source.

81 sampled poses include all 21 moving meshes against 259 static meshes, plus releasing latch against lid: zero unintended surface intersections. Only named mating bearings exempt. Ten hinge/body/lid attachment pairs and a hollow interior floor ray at z=.265 verified. Sampled surface intersections are not continuous collision, rigid-body or manufacturing certification.

Offline file:// Edge desktop (1440×1080) and touch-emulated mobile (390×844): native controls, drag/touch rotation, open/close, reset during motion, reduced-motion endpoint, no horizontal overflow, zero external HTTP requests and zero runtime errors. Full-open projection maximum absolute NDC .892365. Actual corrupt GLB reaches the parser and yields a poster fallback; no-JS poster separately passes. Tests executed on desktop RTX 4060, not a physical phone; no FPS claim.

## Visual assessment and limits
Actual source and mobile renders inspected: readable staggered masonry, three stacked rounded boulders plus companion, satin brass and complete uncropped silhouette. Pale stone reads as generic dressed masonry more strongly than diagnostic granite; small mineral grain is subtle at mobile size. The seam is pronounced; small hardware contact details are visually ambiguous at mobile scale despite attachment tests. Source render has modest sampling noise (24 samples, denoising disabled). Rounded kopje grouping and ochre oval ground are invented miniatures, not a specific landform, monument reconstruction, traditional artwork or cultural representation of all Zimbabwe. No sacred imagery copied. Not photoreal-equivalent or human art-approved.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/Playwright; Node plus pinned package.json build dependencies; installed Edge. Shared pilot node_modules was present but lacked esbuild, so dependencies installed only in this directory. Runtime remains fully embedded.

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs`.
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

`setup.py` records initial lineage adaptation only; do not rerun it on an edited delivery. The final author/build/check scripts use included local inputs. Regeneration overwrites model/render files and requires a fresh inventory. No implementation gate failed during this run; negative controls explicitly reject a detached ornament, corrupt GLB and invalid motion/asset inputs. The source template's pre-existing truncated mobile CSS was repaired before build. No fabricated failure-and-fix claim.

Three.js 0.180.0 MIT license included; esbuild build-only dependency. Procedurally authored geometry/maps, not scans or hand sculpture. Research references and pre-model measurable contract are in design-brief.md. Exact-byte Git attributes protect inventory across checkout. User waived per-asset review; integration into the 201-item collection is a separate card. Branch backup only, no merge or public hosting.
