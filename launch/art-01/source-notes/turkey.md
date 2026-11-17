# Turkey v1 — Iznik Tulip

Open **turkey-v1.html** directly in Edge/Chrome. All geometry, maps, Three runtime and actual-source poster are embedded. Drag/touch rotates; Open/Close stages the latch before the lid; Reset restores the initial view. Cosmetic inner collectible only, not an on-chain seal or outer custody box.

## Delivered
- Standalone HTML **2,351,465 bytes**, strictly below 5,000,000.
- `turkey.glb` **1,108,460 bytes**; named editable `turkey.blend` and trimmed inherited `mechanism.blend`.
- Three procedural maps, source/render/build/test scripts, actual source poster and desktop/mobile closed/open screenshots.
- `inventory.json` contains exact bytes/SHA-256; `turkey-v1-source.zip` is independently read back by `package_delivery.py`. Inventory excludes itself and delivery envelope to avoid circular hashing.

## Design and limits
Research-backed brief written before authoring: ivory ceramic-inspired body, cobalt/turquoise original floral medallions, three scarlet tulip reliefs on an ivory lid inset, cobalt trim/feet and satin brass. See `design-brief.md` for museum sources. Text-only research; no third-party museum pixels/textures embedded. Geometry and maps are script-authored, not artisan-made, scanned, photogrammetric, or an antique reconstruction. Relief flowers reinterpret painted Iznik motifs; this is one interpretation of Turkey, not comprehensive national representation.

Actual final mobile and open-desktop captures were visually inspected: three tulips visible, clean corner treatment, readable controls, hollow interior and entire open silhouette in frame. Floral body patterns remain repetitive and light; leaves/tulips are angular and toy-like, glaze fairly matte in the browser, hardware simplified, and the source render retains sampling grain. No claim of photorealism or historical-pattern fidelity. The exposed blue panel in the open front view is the lid underside; flowers travel behind it normally.

## Verified final candidate
- Reopened saved source, same baseline lid/latch pivot matrices, 3 tulips, 6 leaves, 59 bounded lid-owned ornament meshes, no inherited cedar/granite theme.
- Source/export nearest-world-vertex error **1.712013073529306e-7**, below 1e-5. Three packed maps. Actual loader: **16,056 triangles, 114 meshes, 7 materials**, zero nonfinite vertices/degenerate triangles.
- **81 collision samples, 75 moving and 39 static meshes**, including every ornament; no unintended intersections. Latch-to-lid also sampled. Only named original concentric bearings exempted. Ten hinge/body/lid attachment pairs overlap; hollow-floor ray z **0.26500001549720764**. This is sampled surface clearance, not continuous simulation/manufacturing certification.
- Actual offline `file://` Edge desktop 1440x1080 and mobile 390x844 touch emulation: native controls, drag/touch rotation, close/open, mid-motion reset, reduced motion, no horizontal overflow, zero external HTTP requests/runtime errors. Open silhouette maximum absolute projected NDC approximately **0.8924**. Real corrupt GLB parser input shows fallback; JavaScript-disabled context displays poster.
- Actual decoded 512px color map red range **207**; 256px roughness green-channel ranges **21** and **29**. Native Node motion tests: **2 pass, 0 fail**; invalid assets rejected.
- Negative control deliberately detached a tulip and rejected it with `Ornament missing lid ownership`; no defective scene was saved.

## Real failure and fix
Initial source render showed black corner strips. Body front/rear skins overlapped side skins, producing coplanar outer faces. A new independent overlap regression failed on the actual initial saved source: overlap dimensions **[0.23000001907348633, 0.19000005722045898, 1.4599999785423279]**. `initial/` retains that render and assertion trace. Front/rear skins shortened to 3.26; side panels preserve assembled width 3.72. Final source/GLB/poster regenerated and every gate rerun successfully. No collision exemptions or tolerances loosened.

## Reproduce
Build/test dependencies: Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node with exact Three 0.180.0/esbuild 0.25.11 pins. Shared pilot compiler was absent; packages installed only within this new preview folder. No sibling dependencies changed. `node_modules` and `.blend1` backups excluded. Runtime itself needs only a WebGL browser.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Repeat Blender command for `verify_theme.py`, `verify_source.py`, `verify_parity.py`.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.

`author.py` is standalone using included mechanism source. `setup.py` documents initial adaptation from the repository Japan pilot and needs that sibling only if reassembling the author/helpers; ordinary rebuild does not run it. Regeneration overwrites generated source/export/render and requires renewed hashes. Three MIT license included.

Mobile emulation ran on desktop RTX 4060, not a physical phone or FPS benchmark. No mint, keys, blockchain node/query, network deployment, VPS operation or public-site edit. Branch backup only; integration is separate. All changes confined to this folder. Autonomous technical/visual completion under the explicit no-per-asset-review directive, not a claim of human art approval.
