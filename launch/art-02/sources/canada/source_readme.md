# Canada v1 — Maple & Shield

Open **canada-v1.html** directly in Edge/Chrome. The complete 3D model, runtime, maps and actual-model poster are embedded. Drag/touch to rotate, Open/Close lid, Reset; reduced motion is honored. This is local collectible art, not a minted item, public deployment or custody proof.

## Delivered
- Offline HTML: **4,309,123 bytes** (strictly below 5,000,000).
- `canada.glb`: **2,652,076 bytes**; `canada.blend`: packed editable source.
- `mechanism.blend`: inherited trimmed articulation/interior baseline, included for reproducibility.
- Original generated maps, author/build/verification scripts, actual Blender `poster.png`/JPEG, desktop/mobile closed/open/rear/fallback screenshots.
- `design-brief.md`: sourced visual contract written before authoring. No supplied Canada concept image existed.
- `inventory.json`, `delivery-check.json`, `canada-v1-source.zip`: exact byte identities and archive readback evidence. ZIP and delivery-check excluded from their own payload inventory to avoid circular hashes.

## Verified, independently exercised
- Real Three.js GLTFLoader: **39,232 triangles, 161 meshes, 11 materials**, zero nonfinite vertices and zero degenerate triangles.
- Saved-source reopening: **81 sampled opening poses, all 62 moving and 99 static meshes**, zero unintended surface intersections. Latch versus lid ornaments also checked. Only original named concentric hinge/latch bearings are exempt. Ten hinge attachment pairs intersect; hollow interior floor ray z=0.2650000155.
- Mechanism pivots match the included baseline exactly within 1e-7. 80° latch release precedes 105° lid opening; endpoint/clamping and invalid-asset rejection unit tests pass.
- Bidirectional saved-source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Four packed source maps. This is geometric parity, not byte-identical re-export.
- All **34 lake/shore/pine meshes** belong to the lid in source and actual loader. Pine top z=2.93401432, three low granite outcrops, five roots and trunk intersect the rear-right rock. A deliberately detached trunk was rejected by the same ownership assertion and restored in memory; delivered source was not mutated by this negative control.
- Actual decoded maple color range 31 and roughness GREEN-channel range 31; endgrain 17, granite 125. Maximum map dimension 512. Procedural maps, not scans.
- Offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: native clicks/taps, mouse/touch rotation, open/close, interrupted Reset, reduced motion, zero HTTP requests, zero JS errors and no horizontal overflow. Full-open projection maximum absolute NDC 0.892365. Real corrupted GLB reaches parser and displays poster; no-JS poster checked separately. RTX 4060 desktop GPU; **not physical-phone performance**.
- Actual source poster checked for nonblack pixels/alpha coverage. Source poster and real mobile/desktop screenshots visually inspected; full silhouette and main controls readable.

## Honest visual result
Light honey wood, real corner joinery, subdued green seam, brass fittings, blue lake inset, three granite outcrops and one asymmetric pine are visible at mobile size. This is a stylized regional maple/Canadian Shield interpretation, not a geographic reconstruction or a representation of all Canadian cultures. Wood species and granite geology cannot be identified reliably from the rendering alone.

The lake is intentionally a rectangular shallow inlay, not a natural shoreline simulation; under studio/browser lighting it reads bright turquoise rather than the brief's deep-blue aspiration. Rocks are rounded and pale, pine foliage is sparse, wood grain regular, and the undenoised source render has fine noise. Small secondary mobile copy is less comfortable than the main title/buttons. Terrain is naturally hidden behind the opened lid from the front; a rear-open screenshot documents it. No photoreal equivalence, botanical fidelity, manufacturing feasibility or continuous collision proof is claimed.

## Real failure and fix
`initial/build-missing-dependencies.txt` retains the first build failure: the prescribed sibling node_modules directory existed but was empty, so esbuild could not be resolved. Installed the pinned Three 0.180.0/esbuild 0.25.11 dependencies **inside this new preview only**, then the same build and offline tests passed. No criteria were relaxed. Browser reduced-motion tests wait for observable endpoint state instead of assuming a fixed 70ms sleep always receives a frame.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge, plus Node.js/npm for build-time bundling only. All asset paths are folder-relative; no sibling art is needed for normal regeneration.

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Authoring overwrites generated source/export/poster. Keep hand edits in a separate copy. Build prefers local node_modules, with the inherited sibling fallback; dependency folders and .blend1 backups are excluded from delivery. `.gitattributes` preserves exact artifact bytes through Windows Git checkout. Mechanism/viewer/check lineage is the repository Japan pilot at base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; body joinery follows that family pattern, while maps and the Shield lake/rock/pine layout are authored for Canada. Three.js MIT license included. Research text/images are not embedded as textures.

Only `preview/canada-v1/` is added. No shared kit, other preview, production site, blockchain, keys, minting, broadcasts or VPS touched. Branch backup only; integration and full-collection review belong to the existing final integration card.
