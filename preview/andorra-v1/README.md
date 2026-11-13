# Andorra v1 / Madriu Stone

Open **andorra-v1.html** directly in Edge/Chrome. Entire offline viewer **3,891,932 bytes**, embedded GLB **2,311,640 bytes**. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion preference supported. Local collectible art only: not minted, hosted, signed or stored on-chain. Cosmetic opening does not change custody.

## Design and files
Research-backed `design-brief.md` was written before authoring. Inspired by the Madriu valley's stone construction, pastoral land use and Pyrenean terrain, not a literal survey/map or historic artifact. Eighty physical granite masonry blocks surround the hollow liner. Two rocky flanks, muted pasture and fifteen pale path stones travel on a slate-colored lid. Brass is fictional family hardware. Geometry/maps are script-authored, not scans or hand sculpture.

- `andorra.blend`: editable packed source; `andorra.glb`: portable standalone model.
- `mechanism.blend`: unchanged inherited Japan trimmed family mechanism, source lineage from the repository Iceland pilot.
- `maps/`, `maps.py`, `author.py`: reproducible generated materials and geometry.
- `poster.png` / `poster.jpg`: actual Blender source render, not promotional AI art.
- Desktop/mobile closed/open screenshots: actual offline Edge viewer. `mobile-nojs.png` and `mobile-fallback.png`: genuine fallback cases.
- JSON checks, raw `*-output.txt` and `initial/`: verification and retained rejected probes.
- `inventory.json`, `delivery-check.json`, source ZIP: SHA-256 payload inventory and archive readback.

## Verified
- Saved source independently reopened: original pivot matrices match mechanism source; 18 lid-owned ornaments, 80 masonry blocks, all 15 path centres hit the path before terrain in downward rays.
- **81 sampled poses, 34 moving meshes, 115 static meshes, zero unintended surface intersections.** Moving/static and releasing latch/lid checks include all new ornaments. Only explicit original mating bearings are exempt. Ten hinge attachment pairs intersect as expected. Floor ray z=0.2650000155 confirms hollow cavity. This is sampled surface evidence, not continuous collision/manufacturing certification or co-moving terrain self-intersection proof.
- Source/export maximum nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed maps independently reopened.
- Actual GLTFLoader finite/degenerate geometry checks pass. Export multi-material flanks become named groups with child primitives; runtime checks include group ancestry rather than wrongly requiring each source object to remain one named mesh. Portable color and green-channel roughness variations verified.
- Offline file:// desktop 1440×1080 and mobile 390×844 touch emulation: native button input, drag, open/close, interrupted reset, reduced motion; no external HTTP requests, page errors or overflow. Full-open projection max absolute NDC **0.912343**, below 1. Real corrupt GLB reaches parser and shows poster; no-JS poster tested. Mobile emulation is not physical-phone performance.
- Motion unit tests: 2 pass, 0 fail; invalid geometry rejected. Deliberately detached ornament negative control fails with `Detached ornament rejected` (regression control, not test-first TDD).

## Actual failure and correction
`initial/extended-failure.txt` and `extended-mesh-only.json` preserve the real failing runtime probe: mesh-only traversal found 16 ornaments because GLTFLoader represents the two multi-material flanks as groups. Corrected traversal examines named groups and verifies lid ancestry; no geometry or count gate relaxed. Initial rendered side textures stretched because inherited wood UVs collapsed one axis on side faces. Corrected to dominant-normal planar projection with equal physical scale; retained `initial/poster-before-uv-fix.png`. Final source/export/poster/browser checks were rerun.

## Honest visual verdict
Readable stylized masonry chest and paired mountain valley with a central stone track. Source and final mobile/open browser images inspected. Rocky slopes are strongly faceted, green boundaries angular, and slate/interior pattern repetition remains visible. The path is small at phone size and its front continuation is less clear. The exposed family latch is long and hinge attachment is not visually obvious from every angle, although numeric attachment tests pass. No photorealism, exact geographic fidelity, authentic traditional craft, physical hardware function, FPS guarantee or visual human approval is claimed. User waived per-asset review until collection completion.

## Reproduce
Python with numpy/Pillow/Playwright; Blender 5.2.1; Node with package-lock dependencies. Shared Iceland node_modules was empty (esbuild entry absent), so identical pinned package dependencies were installed only in this new folder. No sibling files were changed. `npm ci --ignore-scripts --no-audit --no-fund` here restores local dependencies. Node_modules is not delivered.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender identically for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node --test --test-reporter=tap tests.mjs`
5. `python build.py`, `python verify_browser.py`, `python verify_extended.py`
6. `python package_delivery.py`

`verify_theme.py -- --negative` under Blender intentionally fails without modifying saved source. Regeneration overwrites art; preserve manual edits separately. Build resolves local dependencies first and otherwise the inherited sibling toolchain; browser tests require installed Edge. No source authoring depends on a sibling asset. Three.js MIT license included. Runtime assets are embedded; build dependencies are not runtime network dependencies. SHA-256 identifies bytes, not authenticity or availability. 201 equally one-of-one launch designs remain a collection plan; no chain activity or production edits occurred.
