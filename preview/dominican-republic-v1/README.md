# Dominican Republic v1 — Larimar / Caribbean Blue

Open **dominican-republic-v1.html** directly in Edge/Chrome. Entire viewer is embedded: **2,658,887 bytes**, GLB **1,403,740 bytes**. Drag/touch to rotate, Open/Close lid, Reset view. Reduced motion is supported. No server, wallet, network or blockchain operation is involved.

## Artwork
Blue/white cellular larimar-inspired stone references Barahona's blue pectolite. See the pre-model `design-brief.md` for cited research and dimensional contract. Geometry and maps are procedurally authored, not scans or human hand sculpture. Three rounded mineral cabochons sit in a white sculptural setting, all attached to the moving lid. Brass hardware/interior and staged articulation derive from Japan's trimmed mechanism at base ff5d78f. No shared kit or other preview was edited.

## Verified
- Independently reopened packed Blender source; hollow floor ray z=0.2650000155; ten hinge attachment contacts.
- **81 sampled poses**, every one of 24 moving and 39 fixed meshes included; zero unintended surface intersections. Latch-vs-lid also sampled. Only named concentric bearing contacts exempt. Sampled surfaces are not a continuous volumetric or engineering certification.
- Original lid/latch pivot matrices compared independently to mechanism.blend; unchanged. 80-degree release precedes 105-degree lid opening.
- Actual GLB imported and compared to evaluated source: bidirectional maximum nearest-vertex error **1.712013073529306e-7**, threshold 1e-5. Three packed maps; runtime decoded color/roughness/normal variation verified (roughness green channel).
- Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: real buttons, drag/touch, full open fit, close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or errors. Corrupted GLB actually reaches parser and triggers poster fallback; no-JS poster separately checked. Mobile emulation is not physical-phone performance.
- Theme-source gate rejects a deliberately detached ornament, then passes restored hierarchy. Motion tests reject empty/missing/nonfinite assets. Source-render pixel gate rejects blank/transparent posters. All tests have executable assertions, not hand-authored pass flags.
- Delivery inventory checks exact bytes/SHA256, explicit required artifacts and ZIP readback. Preview-local Git attributes preserve bytes across checkout.

## Actual failures and bounded correction
Optional Codex lane failed 401 authentication before any changes; no lane work accepted. Hermes implemented and independently ran checks. Initial build failed because the prescribed sibling node_modules directory was empty. `build-initial-failure.txt` retains the failure; installing declared build dependencies locally fixed it without relaxing the byte gate. An initial render showed irregular/faceted cabochons: retained as `initial-faceted-poster.png`; removed geometric jitter on the three blue stones, rerendered, re-exported and reran all gates.

## Honest visual limitations
Stylized collectible, not photorealistic gemstone or approved reference equivalence. White veining is dense and can resemble water caustics. Separate panel projections have visible joins; the intentionally dark teal seam is conspicuous. The three-lobed ornament remains visibly polygonal at some angles despite smooth normals. White mineral feet/setting are bright and hardware is simplified. Final desktop/mobile screenshots were visually inspected. No claim of a single continuous cabochon, real mineral manufacture, cultural completeness, phone FPS or launch readiness.

## Files and reproduction
`dominican-republic.blend` is editable source; `mechanism.blend` is retained baseline. GLB, maps, real source poster PNG/JPG, browser screenshots, scripts, license and JSON evidence are included in the source ZIP. No dependencies/caches/backups in the archive. Three runtime MIT license included. No third-party photos embedded. The HTML needs no installation.

Build prerequisites: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js with the package-lock dependencies (`npm ci`). Node.js is solely a JavaScript build tool here, not a blockchain node. From this directory:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender identically on `verify_source.py`, `verify_parity.py`, `verify_theme_source.py`.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Scripts use this folder; build falls back to sibling iceland-pilot dependencies only when local dependencies are absent. Regeneration overwrites outputs; preserve manual edits separately. Hash inventory excludes itself, ZIP, delivery-check and its live packaging log to avoid recursive identity. Not hosted, merged, minted, signed, chain-stored or deployed; branch backup only. The separate collection integration card owns aggregation.
