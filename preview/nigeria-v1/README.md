# Nigeria v1 — Indigo & Resist

Open `nigeria-v1.html` directly in Edge/Chrome: all runtime assets embedded, no server required. **HTML 3,261,757 bytes; GLB 1,846,528 bytes.** This is a local cosmetic collectible study, not minted, hosted or a custody operation.

## Design and provenance
Yoruba àdìrẹ indigo resist-dye traditions inform independently generated irregular rings and woven grain, with three brass-ringed enamel lid ornaments. Sources and the pre-authored contract are in `design-brief.md`; V&A article and collection O147380 were independently reconfirmed during recovery. No museum image pixels are included. This does not represent all Nigerian cultures or reproduce a historical textile. Script-authored Blender geometry, not artisan-produced cloth, scans or photorealism. Mechanism inherited from Japan's trimmed source; shared kit unchanged. Three.js MIT license included.

## Verified
- Saved Blender source independently reopened; packed color/roughness/normal maps; original pivot matrices compared with included mechanism source.
- 81 sampled poses: 25 moving and 39 static meshes; zero unintended surface intersections. Latch releases 80 degrees before lid opens 105 degrees. Only specified coaxial bearing contacts excluded. Ten hinge attachment pairs intersect; interior floor ray z=0.2650000155.
- Source/GLB bidirectional nearest-world-vertex error 1.712013073529306e-7 (<1e-5).
- Real browser GLTFLoader finite/nondegenerate geometry; all three discs/rings follow lid. Decoded 512px maps have color/roughness/normal ranges 182/42/20 (roughness green channel). Indigo-dominant coverage 93.08%, pale resist 6.92%.
- Offline file:// desktop and 390×844 touch-emulated mobile: native open/close, drag/touch rotation, interrupted reset, reduced motion, full-open framing, no horizontal overflow, HTTP requests or unexpected JS errors. Actual corrupted GLB parser failure and no-JS poster tested.
- Motion tests include invalid geometry rejection controls. All checks use executable assertions; no acceptance failures occurred during this resumed verification. Copy audit corrected an inherited Japan error string before final rebuild. Shared dependency folder was empty; pinned dependencies installed only here.
- Inventory and source ZIP read back and hashes checked. Folder-local Git attributes preserve exact bytes. Poster is the actual source render, not AI art.

## Visual verdict and limits
Actual mobile and source renders inspected: cohesive blue resist-ring pattern, gold fittings, complete visible silhouette. Clean stylized chest, not photographic cloth. Repeating rings and conspicuous seam remain deliberate abstractions; physical material/cloth behavior and phone GPU performance are not verified. Three enamel backing discs use radius .32 instead of the brief's .25 center radius (brass ring .29 retained). Render lighting makes source blue paler than browser blue. Collision sampling is not continuous mechanical certification. No human art approval claimed; per-asset review was explicitly waived.

## Reproduce
Python with Pillow/numpy/playwright, Blender 5.2.1, Node with pinned package-lock (`npm ci` here), installed Edge. `python maps.py`; Blender background factory-startup with `--python-exit-code 1 --python author.py`; `python build.py`; Blender likewise for `verify_source.py`, `verify_parity.py`, `verify_source_theme.py`; `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_theme.py`; `python package_delivery.py`.

Regeneration overwrites generated source/export/poster. Build falls back to sibling pilot dependencies only when local dependencies absent. Editable source, standalone GLB/HTML, maps, scripts, evidence and screenshots are in the ZIP; node_modules/backups excluded. No production paths, blockchain, secrets, VPS or external messaging used. Branch backup only; integration belongs to the separate collection card.
