# Yemen v1 — Sana'a Gypsum

Open **yemen-v1.html** directly in Edge/Chrome. Complete offline viewer: **4,013,265 bytes**; standalone **yemen.glb: 2,402,476 bytes**. Drag/touch to rotate, Open/Close lid, Reset view. Reduced motion supported. No server, wallet or transaction. Branch-only art delivery, not minted, hosted, deployed or user-approved.

## Design and provenance
Sana'a's ochre earth/burnt-brick tower houses and white gypsum decoration inspire the warm mineral body, ivory diamond friezes and three lid houses. See the research-backed design-brief.md written before authoring. Geometry and three 256×256 maps are procedurally authored, not scans, historic reproductions or artisan-made craft. No research photographs are embedded. The inherited trimmed Japan mechanism.blend retains family pivots, hollow liner, brass and bearings; shared kit and prior previews are unchanged. Three.js 0.180.0 license included.

## Verified on final files
- Build PASS: HTML_BYTES 4013265 GLB_BYTES 2402476; strict <5,000,000 HTML limit.
- Saved Blender source independently reopened; same mechanism pivot matrices, 3 towers on moving lid, 24 front diamond segments plus 32 side segments, packed maps, hollow floor ray at z=0.2650000155, 10 hinge attachment pairs.
- **81 sampled poses**, all **55 moving / 107 static** meshes, **zero unintended surface intersections**. Latch versus lid included. Only specified mating bearing surfaces excluded. Not continuous collision proof or manufacturing certification.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5.
- Actual GLTFLoader: **162 meshes, 33,440 triangles, 6 materials**, zero nonfinite vertices or degenerate triangles. Portable color-map range 61; roughness green-channel range 86. Lid ancestry verified in runtime and source.
- Edge offline file:// desktop 1440×1080 and touch-emulated mobile 390×844: native controls, drag/touch rotation, open/close, interrupted Reset, reduced motion, full-open projected bounds <1 (max 0.892365), no horizontal overflow, external HTTP requests or runtime errors.
- Actual corrupt GLB parser error yields poster fallback; JavaScript-disabled poster verified. Poster is a nonblack render of actual final saved source, not AI illustration.
- Motion unit tests: 81 staged samples and rejected malformed geometry, zero failed tests. Deliberately detached tower rejected by theme test. Exact SHA-256 inventory and ZIP entry readback in delivery-check.json.

## Corrections and honest limits
Initial inherited UV projection collapsed side texture into streaks and read as wood; switched to dominant-face mineral projection (initial/poster-before-uv.png preserved). The saved-source side-frieze count actually failed before regeneration: initial/missing-side-frieze.txt records AssertionError for missing 32 segments. Added the side geometry rather than relaxing the gate. This was a regression check against the prior saved source, not a claim that the entire project was test-first. A transient patch indentation error was fixed before executing authoring.

Final visual inspection shows three legible terracotta towers, ivory bands/diamonds, intact wide box, and fully framed open pose. The finish remains simplified, mottled and clean; no exact architectural/historic fidelity or photorealism claim. Tower windows are applied dark inserts, not hollow interiors. The thick dark seam and long inherited latch are stylized family mechanics. The source poster retains sampling grain. Rear/underside visual inspection is limited; tests cover their geometry but do not replace full aesthetic review. Mobile emulation used desktop RTX 4060, not physical-phone performance.

## Reproduce
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1 and Node build tooling. Shared pilot dependencies were absent; pinned local package.json/package-lock.json dependencies were installed only here. No runtime dependencies are downloaded.

1. `npm ci --ignore-scripts --no-audit --no-fund` within this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs > motion-output.txt`
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`

Regeneration overwrites authored output; save manual edits separately. `.blend1`, node_modules and caches excluded from archive. Folder-local Git attributes preserve exact inventory bytes. Source ZIP includes .blend, GLB, viewer, maps, scripts, evidence and license. Inventory excludes itself and packaging envelopes to avoid recursive hashes. No blockchain, keys, nodes, minting, production docs, VPS or external messaging accessed.
