# France v1 — Burgundy Glazed Tile

Open **france-v1.html** directly in Edge/Chrome. This standalone offline collectible contains the actual GLB, runtime and source-rendered poster: **4,937,632 bytes** (<5,000,000). The standalone **france.glb** is **3,107,424 bytes**. Drag/touch to rotate, Open/Close lid, Reset view. Reduced motion is honored. No server or network is needed.

## Design and source
A cream limestone-inspired keepsake box carries an original 160-piece polychrome diamond-pattern panel inspired by Burgundy's glazed roof tiles. The research-backed written `design-brief.md` was created before the source. No supplied France concept artwork exists; no claim of matching a previously approved image. Stone body, pattern and hardware combination are invented interpretations, not a replica of Hôtel-Dieu or a survey of all French traditions.

`france.blend` is editable, script-authored Blender source with named individual tiles. `mechanism.blend` is the unmodified trimmed Japan-pilot family mechanism. `maps/` holds three generated 256px stone color/roughness maps, not scans. No third-party reference photography is embedded. `poster.png` and JPEG are actual source renders, not AI art. Source and viewer scripts, MIT Three license, pinned build manifest and lockfile are included. The first pastel render is retained in `initial/`; one bounded palette correction deepened the green, burgundy and mustard without changing geometry.

## Verified on the final asset
- Actual Three GLTFLoader: **44,120 triangles, 216 meshes, 9 materials**, zero nonfinite vertices and zero degenerate triangles. All 160 tile meshes have lid ancestry. Decoded map variation: feet color 59, body color 69, roughness GREEN channel 41. Body map mean RGB approximately 197.77 / 179.84 / 143.97.
- Independently reopened source: inherited pivot matrices unchanged; 160 separately editable tiles; four nonmetallic glaze materials; tile bounds and surface seating meet the prewritten brief. The hollow-floor ray hits z=0.2650000155. Ten explicit intersecting hinge attachment pairs pass.
- **81 sampled poses**, all **177 moving** and **39 static meshes**, zero unintended surface intersections, plus releasing latch versus lid meshes. Only named mating bearings are exempted. This is sampled surface-intersection evidence, not continuous solid-volume proof or mechanical certification.
- Bidirectional source/export nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. Three packed maps present. This is geometry parity, not a byte-identical re-export claim.
- Motion tests: **2 passed, 0 failed**; staged -80° latch then -105° lid, clamp/reverse behavior and rejecting malformed asset contracts.
- Offline `file://` Edge at desktop 1440×1080 and mobile 390×844 touch emulation: native click/tap open/close, drag/touch rotation, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests and no runtime errors. Full-open maximum absolute NDC ~0.89236. Actual corrupt GLB reaches the parser and displays the source poster; no-JS poster also checked.
- A deliberately detached tile in an in-memory reopened scene makes the theme ancestry assertion fail and Blender exit 1 (`theme-negative-*`). The saved source was not modified. This is a post-implementation negative control, not a production failure or test-first claim. The unmodified source passes. No acceptance threshold was relaxed.
- Archive readback, required-file inclusion and SHA-256 inventory are checked by `package_delivery.py`. Folder-local Git attributes preserve exact bytes; staged Git blobs are compared with the inventory before commit.

## Visual verdict and limitations
Actual source and mobile closed/open screenshots were inspected. Wide cream box, brass fittings and green/red/ochre/ivory diamond panel are readable; no obvious floating tiles or clipped whole-object silhouettes. The first source render looked too pastel, prompting the retained palette correction. This remains a **stylized collectible**, not photorealistic glazed ceramic or historically exact masonry. Individual square tile prisms form diamond motifs; the tiles themselves are not diamond-shaped. Small tile/grout detail and glaze reflections are subtle on mobile. The dark lid seam is prominent and can look slightly lifted; soft shadows give light grounding. The pale procedural body may read as marble as well as limestone. The open front view hides the tiled exterior behind the lid, naturally. Mobile was emulated on an RTX 4060 desktop, not tested on physical phones; no FPS claim.

## Reproduce
From this folder, with Python + numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, and Node.js:

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test --test-reporter=tap tests.mjs`
7. `python verify_browser.py` and `python verify_extended.py`
8. For the expected failing control: Blender flags plus `--python verify_theme.py -- --negative-control` (expected exit 1).
9. `python package_delivery.py`

The prescribed shared pilot dependency location had no esbuild entrypoint. The exact existing Three 0.180.0 / esbuild 0.25.11 dependencies were installed **only inside this new folder**, with node_modules excluded from delivery. The local dependency fallback avoids modifying the shared pilot. Runtime has no dependency on that install. `build.py` can fall back to the sibling pilot's installed dependencies; local installation is recommended for standalone source reproduction. Rebuilding overwrites source/export/poster; preserve manual edits separately. Rendering is bounded to four threads, 24 samples, no denoising; some source-poster sampling grain remains.

## Scope
Only `preview/france-v1/` is added. The base kit and all existing previews are unchanged. Art branch backup only; no merge, production deployment, blockchain node, keys, wallet, minting, chain queries, broadcasts, funds, VPS or external messaging. Cosmetic opening does not alter any on-chain seal or custody state. Proposed collection remains 201 equally one-of-one designs (195 countries, five oceans, Moon). Local art and branch backup are not hosted or on-chain storage.
