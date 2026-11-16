# USA flag v6 — exact shallow-band stars / red feet

Material-only successor to approved v5 commit 32351fc6a0b5a98d4e85d6ca26325aff87eeb1ae. No site, master, mechanism, geometry, top-lid layout, stripe thickness or viewer behavior edits.

## Review
- `united-states-flag-v6.html`: completely self-contained offline interactive viewer, 1,801,298 bytes (<5,000,000).
- `hero-fireworks.png` / `poster.png`: actual Edge browser stage capture, fireworks visible. Embedded JPEG fallback comes from this actual browser capture.
- `band-front-close.png`: five unobstructed five-point stars on front (-Y) shallow band.
- `band-left-close.png`: four unobstructed five-point stars on physical left (-X) shallow band; both visible red feet in frame.
- `blender-source-no-fx.png`: separate genuine Cycles source render, no viewer-only fireworks, some sampling noise.
- `reference-comparison.jpg`: v5/v6 actual browser comparison.

Only nine white stars were added inside the existing navy band; all other wall-map pixels, navy footprint, lid map and roughness map remain unchanged. All four feet use one dedicated untextured red material on every face. No extra corner/seam stars or lower navy patches. The front stars occupy the existing partial-width navy canton left of the latch, not the whole front width. Default hero preserves the v5 camera; left-band stars are naturally foreshortened. Dedicated face views verify their counts. Closeups deliberately prioritize the box and may crop background fireworks; default hero/full-cycle tests retain all fireworks in frame.

## Verification
- Reopened saved source: exactly 5 front / 4 left white components sampled via actual surface rays and barycentric UVs, 26,880 rays per face with zero misses. Four entirely constant-red feet. Actual v5 negative control fails both requirements (0/0 band stars, texture-driven white feet).
- Exact saved geometry, UVs, transforms, parentage and pivots for all 57 collectible objects. Top texture, roughness, mechanism, motion, viewer source/bundle and fireworks bytes identical to committed v5.
- GLB: all nodes identical; 165 non-UV accessor buffer views exact; exporter UV roundtrip maximum 1.1920928955078125e-7 (<2e-7), with source UVs exact. Four exported red-foot materials verified. Exported base-color images equal authored maps.
- Saved-source/GLB geometry parity maximum distance 1.712013073529306e-7 (<1e-5), three packed source images.
- 81 sampled source collision poses without collisions, original narrow bearing exemptions; hinge attachments and hollow interior verified. Motion tests pass 81 poses plus invalid-asset negatives.
- Offline native Edge desktop and emulated-touch mobile: rotation, open/close, interrupted reset, reduced-motion endpoints, no overflow, no external requests or unhandled errors. Genuine corrupted embedded GLB fallback and no-JS poster pass. This is browser mobile emulation, not physical-phone testing.
- Fireworks: animated/static arrays verified; full-cycle default/open desktop/mobile bounds; 52 rendered phase pixel comparisons. Fireworks remain viewer-only, outside collectible GLB.
- Vision independently confirms front 5 and left 4 unobstructed stars, red feet, and visible hero fireworks. Zero artwork-count corrections were needed.

## Reproduce
Python requires Pillow, NumPy and Playwright with Edge. Blender used: 5.2.1 LTS. Node dependencies use the included pinned package-lock; install only in this folder. Run `python maps.py`, Blender background `--factory-startup --python-exit-code 1 --python author_materials.py`, `python build.py`, `python capture_fireworks.py`, `python capture_bands.py`, `python build.py`, then the verification scripts and `python package_delivery.py`. `author_materials.py` starts from included packed `baseline-v5.blend`; it does not regenerate geometry. Cross-version regression scripts and comparison capture expect the unchanged sibling `../united-states-flag-v5` from the art branch. Final viewer and packed source do not need that sibling.

The preserved `historical-regeneration-attempt.py` and initial failure log document an abandoned full regeneration: four objects had changed UV records despite identical geometry. Final material-only authoring fixes this by reopening v5. Another retained failure caught newline differences in copied runtime sources; final sources were restored byte-for-byte. Do not use the historical author script to reproduce the final asset.

`inventory.json` lists exact file bytes/SHA-256. Source ZIP excludes dependencies and .blend1 backups; includes GLB, packed editable source, baseline source, maps, scripts, review images and verification evidence. `delivery-check.json` records ZIP readback and copied-output hashes plus actual delivered HTML offline mobile open/reset. Git backup is restricted to art/united-states-flag-v6; no hosting, minting or website changes.
