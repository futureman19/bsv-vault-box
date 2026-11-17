# Cambodia v1 — Sandstone & Baray

Open **cambodia-v1.html** directly in Edge/Chrome. All runtime code, model, maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. This is a cosmetic collectible preview, not the outer custody container or a transaction.

- HTML: **4,497,154 bytes**, strictly below 5,000,000.
- GLB: **2,785,720 bytes**.
- Editable `cambodia.blend`, inherited trimmed `mechanism.blend`, three 256px generated maps, scripts, real source poster, desktop/mobile screenshots, raw outputs and acceptance JSONs are included.
- `cambodia-v1-source.zip` and `inventory.json` give reproducible payload inventory; `delivery-check.json` records ZIP readback. SHA-256 identifies bytes, not authenticity or storage availability.

## Design and provenance
The brief was saved before generating the model. Cambodian sandstone architecture and Angkor's reservoirs informed an invented sandstone chest with ashlar relief, shallow turquoise rectangular inlay and stepped architectural miniature. Research URLs and interpretation boundaries are in `design-brief.md`. No research photographs or sacred figures are copied. This is not a reconstruction of Angkor Wat or Beng Malea, or a traditional artisan-made object. Mechanism/viewer lineage is the repository's Japan pilot, base commit ff5d78f; the shared art kit is unchanged. Three 0.180.0 is MIT (license included); esbuild 0.25.11 is build-time only.

## Verified
- Saved Blender source independently reopened: hollow interior floor z=0.2650000155; ten real hinge attachment contacts; original lid/latch pivot matrices preserved.
- 81 staged poses, **34 moving and 159 static meshes**, zero unintended sampled surface intersections. Latch-versus-lid checks include every ornament. Only named concentric hinge/latch bearing contacts are excluded. This is not continuous collision or manufacturing certification.
- Source/export maximum nearest-vertex error **1.712013073529306e-7** (<1e-5), three packed maps. Actual browser GLTFLoader: **193 meshes, 39,256 triangles, six materials**, zero nonfinite vertices or degenerate triangles.
- Theme checks: 18 lid-owned ornaments, three tiers/five pinnacle layers, summit z=2.8615; nine exposed water rays at z=2.005; generated stone mean RGB (165.479,128.484,86.485); all loaded maps have nonzero variation. Roughness measured in glTF's green channel.
- Offline file:// Edge: desktop 1440×1080 and mobile 390×844 touch emulation. Native open/close, mouse/touch rotation, interrupted reset, reduced-motion endpoint, no overflow/errors/external HTTP requests. Open silhouette max absolute projected NDC 0.911769 (<1). Corrupt bytes reach the real GLTFLoader and show poster fallback; no-JS fallback independently verified.
- Two motion/asset contract tests pass, including invalid-input rejection. Deliberately detached water negative control fails `Detached ornament rejected`; unchanged real source passes. This is a post-implementation negative control, not a claimed test-first art failure. No art failure-and-fix occurred.
- Source/mobile closed/open images visually inspected: box and hardware remain framed, reservoir and tiers readable, no obvious detached components. Rear-open capture documents ornament on the back-facing opened lid.

## Honest visual and scope limits
Stylized, clean stone: the rendered palette is lighter/creamier than the raw tan map; cloudy microtexture does not reproduce weathered sandstone pores. The water is an opaque blue-green decorative inlay, not simulated transparent water. Green cushions can read as flattened stones/lily pads rather than moss. The tiered miniature is generic architecture, not historical fidelity. Source poster has visible sampling grain (24 samples, no denoising). The prominent olive seam and inherited long clasp are family design choices. Hidden faces and hardware cannot be certified from screenshots alone. Technical PASS is not photoreal-equivalence or human art approval.

Mobile is desktop RTX 4060 emulation, not physical-phone performance. No mint, chain query, key access, node, sale, deployment, on-chain storage or VPS work. Branch backup only; final collection integration is separate. Per-asset human review was explicitly waived.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node.js. Shared iceland-pilot dependencies were inspected and lacked esbuild; pinned dependencies were installed only inside this folder. No sibling was modified. node_modules is excluded.

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

`setup.py` records the initial adaptation and requires the sibling Japan/Iceland pilot; do not rerun it for normal standalone reproduction. The resulting author/build/check scripts use included files and local dependencies. Authoring overwrites source/model/poster; preserve manual edits separately. Refresh README sizes and inventory if regeneration changes bytes. Negative check: Blender `--python verify_theme.py -- --negative` must exit nonzero without changing the saved source.
