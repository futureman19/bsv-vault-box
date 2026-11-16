# United States flag v8 — thin-shell body-wrap review

Open `united-states-flag-v8.html` locally; it is fully self-contained. This is an unminted inner collectible, not custody software. No site, docs or master changes.

## Result
Four physical LEFT stars (ring side) and five FRONT stars (latch side) now cross the top, fine bevel, vertical lid edge and mechanical seam into the **fixed main body**. Open front/left browser images independently show the body portions remaining behind. There is one shallow navy canton, no independent second star row or corner ghost. All top and edge stars use the same 0.145 world-unit radius, up from v7's 0.125. The tiny top portions are intentional: most of each folded glyph now occupies the side/body. Broad vivid red/ivory stripes and four solid-red feet remain.

This is a stylized enamel collectible, not photorealism or a claim to objectively be the best. Final normal mobile shows the shallow body stars, but the very thin seam is only a few pixels and ownership is clearer in the closed/open face views. Gold hardware remains simplified. Fireworks are separate depth-tested 3D viewer effects, not GLB geometry: 432 particles with soft generated radial sprites and 1,728 fine trail segments; no paid imagery, smoke simulation or full-screen bloom.

## Explicit geometry changes
V7 geometry was NOT frozen. Above z=1.56, closed-pose world Z is reprofiled by `1.56 + (z-1.56)*0.20`. Lid thickness changes from 0.30 to 0.06; its top is 1.6436. Upper and lower bevel horizontal radius changes from 0.045 to 0.012, with 0.009 vertical radius and actual chord-length unfolding. Existing modifiers are evaluated before deformation to preserve their shapes without bevel collapse. Affected pivot positions and gold fittings are re-seated in the closed pose. Lower body/feet retain their silhouette.

The first collision run exposed clasp-seat / rotating-knuckle interference and full-open moving-leaf / mounting-stem interference. The seat top was lowered to 1.53 and the mounting stem rear extent reduced from y=1.32 to 1.29. No collision category was waived. Hollow interior walls remain continuous; hinge attachment pairs intersect as intended. Source BVH checks sample 81 poses, not a continuous mathematical collision proof. Current actual transformed hinge axis is z=1.5816, y=1.32; numeric attachment tests operate on the reopened current source.

Paint uses one common world-metric star stencil. Body UVs are explicitly reprojected to remove inherited bevel interpolation offsets. Natural mechanical gaps remain unpainted space; no floating bridge or duplicate glyph is added. Three packed images are embedded in the saved source. Source/GLB parity is verified independently with 1e-5 tolerance.

## Bounded stages and retained failures
1. Analytic layout / actual geometry: `stage1-analytic-swatch.png` and `stage1-layout.json` are the **initial** thinner-shell estimate, not the final layout. Wide-bevel tests still spent too much glyph travel; final fine-bevel layout is in `wrap-layout.json` and `body-wrap-check.json`. Initial renders and failed collision/export runs remain.
2. Enamel and particles: added coat response, refined brass roughness, soft point sprites and density. Bright red remains red, not pink. The genuine Blender render is `blender-source-no-fx.png`; `hero-fireworks.png` is a real browser render, also embedded as fallback.
3. Integrated mobile: a larger/lower camera makes the body band more readable. Strict full-cycle particle bounds initially failed after reframing; burst spread was reduced, not the viewport assertion. Final default/full-open desktop/mobile projections pass. Native click/tap, drag rotation, open/close, interrupted reset, reduced motion, corrupt-GLB fallback, no-JS fallback and offline checks pass.

Additional retained failures include a nonexistent Blender Object.parent_recursive API, exported collapsed bevels before evaluating modifiers, inherited body UV mismatch, and a face-scan ray above the curved wall corner. The final full-face count scan stays below that corner bevel; separate per-glyph rays still reach the upper body. These are not hidden all-green histories.

## Evidence
- `body-wrap-check.json`: actual exported triangle ray samples; 4-left/5-front measured face spans, top and main-body pigment for each, metric UV errors, v7 zero-body negative control.
- `source-check.json`, `hinge-attachment-check.json`, `parity-check.json`: independently reopened source, 81 sampled poses, hollow floor, connected mounts, geometry parity.
- `browser-check.json`, `extended-check.json`, `fireworks-pixels-check.json`: real offline Edge on desktop RTX4060; mobile is emulation, not physical-phone performance. 52 rendered burst-phase comparisons against hidden-effects frames; reduced buffers freeze.
- `v8-front-view.png`, `v8-left-view.png`, their `-open` views, `mobile-closed.png`, `mobile-open.png`, `reference-comparison.jpg`: actual-browser evidence. Comparison shows v7/v8 default presentations (camera intentionally changed), not an exact camera-controlled material comparison.
- `inventory.json` and `delivery-check.json`: ZIP readback, required artifacts, copied bytes and copied-file offline mobile test.

## Reproduction
Python/Pillow/NumPy/Playwright Edge, Blender 5.2.1 and package-lock pinned Node build dependencies are required only to rebuild. Viewer needs none. Run `python maps.py`; Blender background with `--factory-startup --python-exit-code 1 --python author_v8.py`; then Blender scripts `verify_body_wrap.py`, `verify_source.py`, `verify_parity.py`; `python verify_paint.py`; `python build.py`; `python capture_fireworks.py`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`; `python capture_v8.py`; `node --test --test-reporter=tap tests.mjs`; `python package_delivery.py`.

`legacy-v7/` scripts are retained only as historical inputs, not runnable v8 instructions. The reproduction scripts include this machine's Blender/Node/profile conventions; adjust executable/output paths on other machines. The v7 comparison viewer is in the sibling baseline preview and not duplicated in the source ZIP; the standalone baseline GLB and packed blend needed for authoring and negative control are included. The ZIP excludes node_modules, caches and .blend1 backups. Review/approval remains with the owner.
