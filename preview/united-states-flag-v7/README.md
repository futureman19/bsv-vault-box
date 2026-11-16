# USA flag v7 — continuous top-edge stars (review candidate)

Open `united-states-flag-v7.html` locally. No server/network/install is needed for viewing. This is an unminted inner collectible study; cosmetic opening changes no custody state. No site files changed.

## Result and important limitation
Four physical **left** edge stars (ring-pull side) and five **front** edge stars (latch side) now each form a single white glyph across the horizontal top, actual bevel and vertical lid edge. All use the same **0.125 world-unit circumradius** as the retained fourteen interior top stars. The corner is deliberately empty: no extra split-star double count. V6's independent small lower stars are removed. The shallow continuous navy body band is retained, without lower navy patches.

**This does not satisfy literal star continuation into the body below the lid seam.** The unchanged lid is 0.30 units thick; a same-scale star is only 0.25 units in diameter. Body top is at 1.56 versus lid top at 1.978. A star centered on the top edge cannot also reach the body while retaining size and geometry. The glyphs end on the vertical lid; only the navy field continues below the mechanical seam. Nothing bridges the seam or floats between moving and fixed parts. This constraint is documented in the prewritten acceptance, not waived as a passing body-continuation gate. A larger star scale or thinner lid would require separate authorization.

The final front/left browser crops visibly show five/four continuous folds with no lower white echoes. A little of the extreme left front motif can be covered by existing gold corner hardware. At mobile scale, small folded tips and thin fireworks are less crisp than enlarged detail views. No claim of illustration-level realism or physical-phone performance.

## Scope and implementation
- Reopened the exact packed V6 source (`baseline-v6.blend`), not its geometry generator.
- Only lid UVs and two paint images changed. Geometry, all object transforms/parents, material ownership, hollow interior, hardware, red feet and mechanism are unchanged.
- Shared metric atlas: 300 texels per physical unit on both axes. Three existing bevel chords are unfolded by their actual lengths, not texture pixel counts.
- The same star stencil is evaluated for body-band coordinates; it has no support that far below the top. Body atlas changes only erase the V6 small white stars into the existing navy.
- Top stripes/palette preserved; underside UV allocation now develops past the lid thickness so edge stars do not repeat at the lower bevel. Its old projected top motif is correspondingly redistributed; underside geometry/interior remain untouched.
- Viewer, compiled bundle, motion, fireworks, template, roughness map and original mechanism bytes equal V6. Fireworks are separate presentation effects, absent from collectible geometry.

## Verification
- Independently imported actual V6 and V7 GLBs: 93,000 ray/UV samples per face per version. V6 has zero crossing components; V7 has four left/five front, each connected from top through bevel to vertical lid.
- Maximum developed-coordinate UV error below 0.000001; identical authored physical radius, not identical image-pixel radii. Measured raster extents differ slightly through antialiasing/sampling.
- 5,940 lower-bevel rays: zero white duplicate-star samples.
- Exact saved geometry/pivots/material ownership; exact exported positions and normals for all 13,324 triangles; node/material JSON unchanged. UV seams may split exported vertices without changing triangles.
- Packed source independently reopened; three packed images. Bidirectional source/export vertex distance 0.000000171202 units.
- 81 sampled collision poses, zero unintended collisions; narrowly documented bearing contacts only. Hollow floor ray and connected hinge checks pass.
- Offline Edge desktop and emulated mobile: native click/tap, mouse/touch rotation, open/close, interrupted reset, reduced-motion endpoints, full-open framing, corrupt-GLB and no-JS poster fallback. Zero external HTTP requests or unhandled JS errors.
- Fireworks: frozen reduced-motion buffers, animated normal buffers, full-cycle projected bounds, 52 phase/device/pose rendered visibility comparisons against effects-hidden control.
- Final copied HTML gets an additional offline mobile open/reset test. Inventory SHA-256 and ZIP readback checks are performed by `package_delivery.py`; exact sizes are in `delivery-check.json`.

## Evidence and bounded corrections
`hero-fireworks.png` is an actual browser stage capture, also used for fallback poster. `blender-source-no-fx.png` is separately labeled source-render evidence, not the delivered hero.

Use `front-edge-comparison.png`, `left-edge-comparison.png`, `v7-top-view.png`, `reference-comparison.jpg`, desktop/mobile screenshots and `features-check.json` for review. Initial/correction1 images and failed UV-test outputs are retained. Two corrections were used: (1) constrain unfolding by physical polygon normal to eliminate side-quad shear; (2) remove lower-bevel UV reset that created duplicate white slivers. No further visual changes after the agreed bound.

## Reproduction
Requires Python with Pillow, NumPy and Playwright/Edge, plus Blender 5.2.1. Scripts use folder-relative input paths; Blender executable commands below must be adjusted to the installation. The frozen JS bundle needs no build dependency installation.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author_materials.py`
3. Run Blender similarly with `verify_wrap.py`, `verify_identity.py`, `verify_source.py`, `verify_parity.py`, `verify_mechanism.py`.
4. `python build.py`, `python capture_fireworks.py`, `python build.py` (embed real browser poster), `python capture_details.py`.
5. `python verify_browser.py`, `python verify_extended.py`, `node --test --test-reporter=tap tests.mjs`.
6. `python package_delivery.py` (output path is explicitly this active Hermes profile; change it for another machine).

The archive includes baseline inputs under `baseline-v6/` plus the packed baseline source. Source regeneration overwrites the editable result. ZIP excludes node_modules, caches, `.blend1` and the archive itself. Review candidate only; not approved, published or minted.
