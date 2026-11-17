# San Marino v1 — Titano / Three Stone Towers

Open **san-marino-v1.html** directly in Edge/Chrome. Offline, fully embedded viewer: **1,933,034 bytes**; GLB **867,572 bytes**. Drag/touch rotation, zoom, staged Open/Close and Reset; reduced motion honored. Cosmetic inner collectible only, not a custody action. Not minted, hosted or deployed.

## Art and evidence
Pale procedural stone chest with blue-gray seam, antique brass, a connected crag ridge and three miniature crenellated towers. The sourced written `design-brief.md` preceded authoring. Architecture is freely interpreted, not a scale replica; textures are generated, not scans. No research photographs embedded. Broad body surfaces are deliberately simple and mottled rather than literal historic masonry; windows are dark relief details, not hollow apertures. Pale towers blend somewhat with their terrain at mobile size; miniature detail and small supporting text require zoom. The open front view hides the exterior towers behind the lid, as expected. No photorealistic/reference-equivalence claim.

`san-marino.blend` is packed editable Blender source; `mechanism.blend` is the unchanged trimmed Japan mechanism baseline. `author.py` regenerates geometry, GLB and genuine source-render `poster.png`. Three 0.180 runtime license included. No AI promotional substitute. Modest 24-sample source render retains some noise. Two rocky saddles were added after the initial render read as disconnected pedestal masses (`initial/discontinuous-ridge.png`).

## Verified with real execution
- Saved source reopened; exact baseline pivot transforms retained. All tower/crag/wall/scrub objects belong to the lid. Three tower root rays meet actual crag surfaces, 12 battlements; deliberately missing-tower input rejected.
- 81 staged poses, **65 moving / 37 static meshes**, zero unintended sampled surface intersections; latch-versus-lid included. Exemptions only named concentric hinge and latch bearings. Ten hinge/body/lid attachment pairs intersect. Hollow floor ray z=0.2650000155. Sampled surface checks are not continuous mechanical certification.
- Actual GLTFLoader: **102 meshes, 9,800 triangles, five materials**, zero nonfinite vertices and degenerate triangles. Base/normal/roughness maps 256×256; actual channel ranges 41/8/41. Roughness tested in green.
- Independent source/imported-GLB nearest-vertex parity <0.00001 units; see parity-check.json for exact distance. Packed maps retained.
- Real offline file:// Edge: 1440×1080 desktop and 390×844 mobile touch emulation; native buttons, drag/touch rotation, open/close, interrupted reset, reduced motion, zero external HTTP requests, zero runtime errors/overflow. Full-open projection maximum abs NDC 0.892365. Real corrupt GLB parser fallback and no-JS poster pass. RTX 4060 desktop, not physical-phone performance.
- Source-render/mobile-closed/desktop-open images inspected. All three towers distinguishable, full box framed, no gross open-pose failure. Tests establish technical acceptance, not user aesthetic approval (individual review waived).
- `inventory.json` hashes payload files; `delivery-check.json` records exact byte counts and ZIP readback. ZIP excludes itself/inventory envelopes, dependencies, backups and caches. Git bytes checked independently before commit.

## Real failures retained
Optional Codex lane exited 401 before edits; no Codex output accepted. Hermes implemented and ran all gates directly. `initial/theme-local-coordinate-failure.txt`: root-ray probe initially used parent-local tower coordinates as world coordinates; corrected to matrix_world translation, same attachment threshold. Missing sibling esbuild caused initial build failure (`initial/missing-dependency-build.txt`); installed pinned local build dependencies, no dependency upgrades. No model collision/size failures were hidden.

## Reproduce
Python with Pillow/numpy/playwright, Blender 5.2.1, Node.js build tooling, installed Edge. Run in this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Repeat Blender command for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`

Build uses local node_modules, or sibling Iceland dependencies when actually installed; no dependencies are included in ZIP or runtime network requests. Regeneration overwrites source/export/poster; preserve manual edits separately. Blender exports may change byte hashes; rebuild inventory after regeneration. Only this new preview directory is committed; shared kit, other previews, production, blockchain and VPS untouched. Branch backup is not website publication.
