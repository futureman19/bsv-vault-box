# Cyprus v1 — Lefkara Linen

Open `cyprus-v1.html` directly in Edge/Chrome. Fully embedded, offline interactive model: drag/touch rotate, Open/Close, Reset, reduced-motion support. This is cosmetic collectible art only; not minted, hosted, signed or blockchain-verified.

## Delivery
- HTML **4,011,426 bytes**; GLB **2,381,956 bytes**. Strict HTML cap 5,000,000 bytes.
- `cyprus.blend`: editable named Blender source with packed maps; `cyprus.glb`: portable model.
- `mechanism.blend`: inherited trimmed mechanical source from Japan v1. Shared vault kit was read only, not altered.
- `maps/`: three independently generated 512x512 linen-inspired color/normal/roughness images.
- `poster.png` and JPEG: actual Blender source render, not AI illustration. Browser desktop/mobile closed/open captures are actual offline views.
- `design-brief.md`: sourced, frozen before modeling. Six invented nested ivory diamonds plus hemstitch-inspired border over a dark carrier; no traditional design copied or authenticity asserted.
- Check JSONs, raw outputs, inventory, and ZIP provide reproducibility and exact bytes.

## Verified evidence
- Independent source reopen: 131 moving and 39 static meshes sampled over **81 poses**, zero unintended BVH surface intersections. Includes every motif and stitch. Only named hinge/latch bearing pairs excluded. Hollow floor ray z=0.2650000155; ten hinge attachment pairs. This is sampled surface contact, not continuous collision or engineering certification.
- Original pivot matrices independently compared to included mechanism source. 80-degree latch release precedes 105-degree lid opening; motion tests include bad-asset rejection.
- Source/export maximum bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5.
- Six nested motifs (12 mesh outlines), proper lid ancestry, bounded relief, seated threads, and six open-center rays reaching the brown carrier. Negative control really detached one ornament and failed with `Detached cutwork ornament`; restored source passes. This is a deliberate post-implementation regression control, not a historical authoring defect.
- Actual GLTFLoader: finite geometry, no degenerate triangles. All three portable map kinds decoded with nonzero variation; roughness tested in GREEN channel. Base-map median RGB [113,76,45].
- Edge over offline file://: 1440x1080 desktop and 390x844 touch emulation, native controls, rotate, open/close, interrupted reset, reduced-motion endpoints, full-open viewport bounds, no HTTP requests/errors/overflow. Real corrupt bytes reach parser and show the actual-source poster. No-JS poster also checked. Mobile emulation is not physical-phone or FPS testing.
- Poster nonblack/alpha sanity and visual inspection of actual source, closed mobile and open mobile. No gross clipping or floating geometry observed.

## Honest visual limits
Stylized rigid box inspired by Lefkara's cotton-on-linen cutwork, NOT authentic Lefkaritika or artisan embroidery. The low ivory outlines are simplified geometric relief; open centers expose a solid brown backing, not holes through the box. Six motifs read at mobile size but fine stitch detail needs zoom. Body texture is regular/procedural and can read as ribbed wood at mobile scale rather than unmistakable linen. Brass latch is inherited family styling, not traditional Cypriot hardware. Fine Cycles sampling grain remains. No photorealism, historical pattern fidelity, cloth physics, physical-phone performance or user art approval is claimed. The task explicitly waived per-asset review.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node with pinned Three 0.180.0 and esbuild 0.25.11 (`npm ci --ignore-scripts --no-audit --no-fund` in this folder). Shared pilot dependency directory existed but lacked esbuild, so pinned dependencies were installed only here; no sibling toolchain was modified. Runtime requires no installed dependencies/network.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender in the same form with `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
4. `node --test --test-reporter=tap tests.mjs`
5. `python build.py`; `python verify_browser.py`; `python verify_extended.py`
6. Negative control: Blender `--python verify_theme.py -- --negative` must exit 1; it never saves the changed scene.
7. `python package_delivery.py` (local ZIP inventory/readback and aggregate assertions).

Regeneration overwrites generated output; preserve manual edits separately. The author and acceptance scripts resolve relative to this directory. Build fallback references sibling pilot only when no local node_modules exists; installing local pinned packages makes extraction self-contained. Three MIT license included. No source images or research-site assets are embedded. `.gitattributes` preserves exact bytes through Windows checkout. ZIP and delivery-check are excluded from their own payload inventory to avoid self-reference.

## Scope and next step
Only `preview/cyprus-v1/` additions; branch backup `art/cyprus-v1`, no merge or deployment. Final 201-piece gallery integration is a separate dependent task. Recommend inspecting the full collection together before optional material refinement.
