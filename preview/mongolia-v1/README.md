# Mongolia v1 — Felt & Steppe

Open **mongolia-v1.html** directly in Edge/Chrome. Drag or touch to rotate, open/close the lid, reset; reduced motion snaps. Complete runtime is embedded; no server or network needed. Cosmetic inner collectible only, not a custody or seal operation.

## Delivered
- Standalone HTML: **2,685,461 bytes** (<5,000,000).
- GLB: **1,435,208 bytes**, embedded portable maps.
- `mongolia.blend`: packed editable source; `mechanism.blend`: inherited trimmed Japan/Iceland mechanical base.
- `poster.png` / `poster.jpg`: actual source render, not generated promotional imagery.
- Desktop/mobile closed/open and fallback screenshots, procedural maps, reproducible scripts, SHA-256 inventory and source ZIP.

## Design and visual limits
Research-backed brief was written before modeling. White felt/canvas and rope-bound round ger structure draw on UNESCO's Mongol Ger craftsmanship listing; rectangular chest, red frame, blue seam and green oval landscape are original interpretations, not traditional-pattern or geographic claims. No external photographs embedded.

Actual-source and mobile screenshot inspection found the ger, olive steppe relief, ivory/red box and brass fittings readable and unclipped. The open interior reads hollow and lid attached; the ger is naturally hidden on the exterior lid face when opened toward the viewer. Felt fiber is subtle at mobile scale, grass is a shallow stylized relief, and small ger details require zoom. No photorealism, artisan authorship or exact architecture claim. Render uses 24 Cycles samples without denoising; minor grain remains.

## Verification actually run
- Independent saved-source reopen: **81 poses**, **36 moving / 51 static meshes**, **zero unintended sampled surface intersections**. Every ger/steppe part included; latch-versus-lid tested. Only original named bearing contacts excluded. Ten hinge attachment pairs intersect correctly. Hollow-floor ray Z=0.2650000155.
- Source/export nearest-vertex error both directions: **1.712013073529306e-7**, under 1e-5. Three source maps packed.
- Real GLTFLoader: **87 meshes, 20,566 triangles, 7 materials**, zero nonfinite vertices or degenerate triangles.
- Theme: **20 lid-owned ornaments**, 12 roof cords, 2 wall ropes, ger placement, terrain root rays, exact inherited pivot matrices. Deliberately detached roof is rejected by ancestry gate (post-build negative control, not test-first TDD).
- Texture decoding: 256px maps, base-color ranges 30/44 and actual green-channel roughness range 55.
- Offline `file://` Edge, desktop 1440×1080 and mobile 390×844 touch emulation: native open/close, drag, touch rotation, interrupted reset, reduced motion, zero external requests/runtime errors/horizontal overflow. Full-open max abs projected NDC 0.892365. Real corrupt GLB reaches parser and shows poster; no-JS poster tested independently.
- Motion unit tests include invalid-asset rejection; two tests pass.
- `delivery-check.json` and `inventory.json`: exact bytes/hashes and ZIP content readback. Local `.gitattributes` prevents newline conversion; staged blobs are independently compared with inventory before commit.

Sampled surface checks do not prove continuous mechanical clearance or manufacturing suitability. Browser uses desktop RTX 4060; mobile emulation is not physical-phone performance. No chain, node, wallet, keys, mint, public deployment or VPS access. No external messaging. Branch backup only; integration is a separate task. Per-asset human review waived by user.

## Real failure and fix
`initial-build-failure.txt` retains MODULE_NOT_FOUND for inherited esbuild: the shared node_modules existed but was empty. The requested link produced an empty worktree placeholder; removed after inspection. Installed unchanged pinned Three 0.180.0 / esbuild 0.25.11 inside this new directory only. Subsequent build and all acceptance commands passed; no acceptance thresholds weakened. No geometry/collision failure occurred.

## Reproduce
Python with numpy, Pillow, Playwright; Edge; Blender 5.2.1; Node.js for build/test tooling only (not a blockchain node).
1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`; `node --test tests.mjs`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

Authoring overwrites output; preserve manual edits separately. `author.py` is standalone using included mechanism; optional `create_author.py` documents original helper extraction and needs sibling Japan source, but is not needed to rebuild. Runtime and archive exclude node_modules. Three MIT license included. Model, source and maps are procedurally authored, not scans. No storage/pinning guarantee or on-chain media exists. Collection scope remains 201 equally one-of-one designs.
