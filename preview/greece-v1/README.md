# Greece v1 / Tinian Marble

Open **greece-v1.html** directly in Edge/Chrome. Complete embedded interactive 3D viewer: **2,628,731 bytes**, with **1,358,352-byte GLB**. Drag/touch rotation, open/close, reset and reduced motion. No runtime network, server, wallet or transaction.

## Design and provenance
A wide ivory/gray-veined marble box with blue seam/inlay, satin brass fittings and a fanlight-inspired openwork relief mounted over a solid lid. The pre-model `design-brief.md` cites UNESCO's Tinian marble-craft listing and committee decision. This is an invented design inspired by the tradition, not an authentic historic motif, sacred symbol, artisan-made work or scan. Three generated 512px color/roughness/normal maps; named editable Blender 5.2.1 source. Mechanism/viewer/test lineage is the repository's Japan/Iceland pilot. Three 0.180.0 MIT license included; esbuild 0.25.11 build tooling.

## Actual acceptance
- `source-check.json`: independent saved-source reopen; 81 motion samples, all 30 moving and 38 static meshes, no unintended intersections. Hinge mounting attachment contacts verified; only named hinge/latch bearing contacts exempt. Hollow floor ray z=0.2650000155. Sampled surface intersections, not continuous collision or manufacturing certification.
- `parity-check.json`: source/imported GLB maximum nearest-vertex error 1.712013073529306e-7 (<1e-5); three packed source maps.
- `theme-check.json`: seven ribs, six independent gap rays reaching the solid lid, fourteen lid-owned ornament/inlay meshes, relief z1.978–2.085, original pivot matrices preserved. Deliberately detached rib is rejected by the ownership gate. This negative control is post-implementation regression evidence, not test-first development.
- `motion-output.txt`: 2 tests pass, 0 failures, including malformed asset rejection and staged 80° latch / 105° lid endpoints.
- `browser-check.json`: actual GLTFLoader, 14,020 triangles, 68 meshes, four materials; zero nonfinite vertices/degenerate triangles. Desktop 1440×1080 and mobile 390×844 touch emulation over offline file://: native open/close, drag/touch rotation, reset during movement and reduced motion pass. Zero external requests, JS errors or overflow. Open projection max absolute NDC 0.93754 (<1). Real corrupt parser input reaches caught failure and shows poster.
- `extended-check.json`: no-JS poster, country/canvas copy, real decoded map ranges (color 96, roughness GREEN 55, normal 20), all maps 512px, nonblack source poster.
- `delivery-check.json` / `inventory.json`: exact SHA-256 and bytes, required files and ZIP readback. Folder-local Git attributes preserve exact bytes across checkout.

All acceptance scripts exit nonzero on assertion failure. No accidental failing geometry/build/browser run occurred in this pass; deliberately malformed GLB, detached ornament and invalid asset tests demonstrate rejection. Shared baseline node_modules existed without the compiler; pinned build dependencies were installed only inside this new directory, never into a sibling preview. Dependencies are not runtime downloads and are excluded from delivery.

## Visual limits
Actual poster and offline mobile screenshots were inspected. The full silhouette and controls are readable. White-on-white fanlight relief remains subtle on mobile and can read as a shallow decorative fan; it is explicitly NOT a pierced container. The dark blue reveal is intentionally prominent and can read as an unseated lid; corner joints and inherited long clasp are stylized rather than fine stonework. Veining is procedural and source render retains sampling grain. No photoreal-equivalence or human art-approval claim. Emulated mobile ran on desktop RTX 4060, not a physical phone or FPS benchmark. Per-asset human review was explicitly waived; later collection review remains separate.

## Files and rebuild
`greece.blend`, `greece.glb`, `mechanism.blend`, maps, scripts, actual source `poster.png/jpg`, desktop/mobile closed/open/fallback screenshots and evidence are included in `greece-v1-source.zip`. No AI promotional image substitutes.

From repository root, with Python (numpy/Pillow/Playwright), installed Edge, Blender 5.2.1 and Node:
1. `npm ci --prefix preview/greece-v1 --ignore-scripts --no-audit --no-fund`
2. `python preview/greece-v1/maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python preview/greece-v1/author.py`
4. Run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap preview/greece-v1/tests.mjs`
6. `python preview/greece-v1/build.py`
7. `python preview/greece-v1/verify_browser.py` and `verify_extended.py`
8. `python preview/greece-v1/package_delivery.py`

Regeneration overwrites output; preserve manual changes separately. No other preview, shared vault kit, production code, VPS, chain, keys or minting touched. Branch backup only, no merge/deployment. The collection plan is 201 equally one-of-one designs; this local artwork makes no custody/storage/issuance claim.
