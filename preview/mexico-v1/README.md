# Mexico / Talavera & Agave — v1

Open **mexico-v1.html** directly in Edge/Chrome. It embeds the actual 3D model, maps, runtime and source-rendered poster. Drag/touch to rotate, Open/Close lid, Reset view. No network, server, wallet or transaction is needed.

## Delivered
- Offline HTML: **3,886,150 bytes**, strictly below 5,000,000.
- GLB: **2,266,880 bytes**; 29,108 triangles, 172 meshes, 8 materials through actual Three GLTFLoader.
- `mexico.blend`: editable named Blender source with packed maps. `mechanism.blend`: inherited trimmed family mechanism, included for reproducibility.
- `maps/`: independently generated ceramic color/roughness and terracotta color. `poster.png/jpg`: actual source render, not promotional AI imagery.
- Closed/open desktop/mobile and rear-open captures: actual offline file:// Edge. `design-brief.md` was written before authoring and cites UNESCO craft and landscape sources.
- Source ZIP and exact SHA-256 inventory, with archive readback checks. No dependencies/caches/secrets in the archive.

## Verification actually executed
- Independently reopened saved source; 10 intersecting hinge attachment pairs; hollow floor ray z=0.26500001549720764.
- **81 collision samples**, all 59 moving meshes against 113 static meshes, plus latch-versus-lid. Zero unintended surface intersections. Only explicit concentric hinge/latch bearing contacts exempt. Not a continuous collision/manufacturing proof.
- Hinge and latch world matrices identical to included baseline. Staged 80-degree latch release, then 105-degree lid swing.
- Bidirectional saved-source/export nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. Three packed source images. Zero nonfinite vertices or degenerate triangles in runtime.
- 78 real beveled body tiles, 18 lid border tiles, 24 tapered ridged agave leaves. All ornaments lid-owned; leaf apex z=2.93999981880188. Root-to-soil sample maximum absolute Z difference 0.007686138153076172. Deliberately detaching a leaf fails the ancestry gate; restoring it passes (intentional regression control, not a discovered art defect).
- Actual decoded map variation, including roughness GREEN channel. Original cobalt/ivory flower repeat, not a copied workshop design or authenticated Talavera craft.
- Desktop 1440×1080 and 390×844 mobile touch emulation: offline, native clicks/taps, drag/touch rotation, open/close, interrupted Reset, reduced-motion endpoint-only samples, no horizontal overflow, no external HTTP requests, no runtime errors. Full-open projected bound <0.893. Actual corrupt GLB reaches parser and displays poster; no-JS poster also passes.
- Browser was Edge on RTX 4060. Mobile emulation is not physical-phone performance.

## Visual verdict / limits
Closed mobile, source poster and desktop front/rear-open views were inspected. Coherent cobalt/ivory tile body, terracotta top and blue-green agave; complete framing and no gross missing geometry. Pattern repetition is intentionally regular; leaf shapes are faceted and stylized, not botanical precision. Source poster has minor sampling noise. Open front view hides the agave behind the flipped lid; rear-open evidence shows it remains attached. Hardware is family-scale simplified and not an engineered ceramic fastening design. Interior depth and fasteners are less legible at mobile size. No photorealism, traditional craft authenticity, all-Mexico representation or reference-equivalence claim.

## Failure and fix
The specified baseline dependency directory was empty. Initial `python preview/mexico-v1/build.py` failed with `MODULE_NOT_FOUND` for `preview/iceland-pilot/node_modules/esbuild/bin/esbuild`. Installed the pinned package.json dependencies locally in this new folder using `npm install --prefix preview/mexico-v1 --no-audit --no-fund`; unchanged build then passed. `failure-history.json` records the observed failure; no geometry/size gates were relaxed. No asset acceptance failure occurred. The detached-leaf and corrupt-GLB probes intentionally exercise failure paths.

## Reproduce
Requirements: Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node with pinned package-lock dependencies. From this folder:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`; `node tests.mjs`
5. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.
`setup.py` is one-time lineage documentation and requires sibling Japan pilot; do not rerun over customized files. All actual author/build/check scripts use included files or local dependencies. Reauthoring overwrites generated source/model/poster; save manual edits separately. Dependencies are not runtime downloads and are not archived.

## Rights / scope
Original procedural geometry/maps with inherited repository mechanism and Three.js 0.180.0 MIT runtime (license included). No research images embedded. Two distinct regional inspirations are combined as an invented collectible design. Local art only: not minted, signed, on-chain, hosted, publicly deployed or a custody proof. Cosmetic opening never changes a seal. Collection direction is 201 equally one-of-one designs; off-chain storage is still only a proposal. No blockchain/node/keys/VPS touched. Only this new directory is added; branch backup only, integration deferred to the existing final integration task.
