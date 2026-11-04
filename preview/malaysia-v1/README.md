# Malaysia v1 — Songket / Crimson & Gold

Open `malaysia-v1.html` directly in Edge/Chrome. Complete embedded offline 3D model/runtime/poster: **2,192,602 bytes**. GLB: **1,031,644 bytes**. Drag/touch rotation, zoom, staged Open/Close and Reset. Cosmetic inner collectible only; no transaction, seal or custody change. Not minted, hosted or deployed.

## Design and provenance
Research-backed written `design-brief.md` preceded modeling. Malaysian songket's supplementary metallic threads inspired crimson cloth-clad skins, procedural diagonal gold patterns and fifteen raised gold diamonds on the lid. Motifs are original geometric abstractions, not a named historic pattern or artisan textile. Source photographs are not embedded. Script-authored Blender source, not hand sculpture/scans. Family mechanism/viewer descend from Japan/Iceland pilots; `mechanism.blend` is included. Three.js MIT license included.

## Verified
- Build succeeds: HTML_BYTES 2192602 GLB_BYTES 1031644, strict HTML <5000000.
- Independently reopened source: 81 moving and 39 static meshes; all 81 staged poses collision sampled, no unintended intersections. Original named bearing contacts alone excluded; 10 hinge attachment pairs intersect. Hollow floor ray z=.265. Sampling is not continuous collision/manufacturing certification.
- Original pivot matrices independently compared with mechanism source. Sixty thread segments form fifteen diamonds, lid-parented; min/max z 1.995/2.025. A deliberately detached thread is rejected (postimplementation regression negative control, not test-first development).
- Source/export bidirectional nearest-vertex maximum error 1.712013073529306e-7, below 1e-5.
- Actual GLTFLoader: 120 meshes, 15,992 triangles, five materials, zero nonfinite vertices/degenerate triangles. Decoded color range 107 and roughness green-channel range 71; three packed maps.
- Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: drag/touch rotation, native open/close, interrupted reset, reduced motion, no external requests/errors/overflow. Full-open projection maximum |NDC| .892365. Real corrupted bytes reach GLTFLoader and display fallback; no-JS poster verified separately. RTX4060 desktop GPU, not physical-phone performance.
- Actual source poster and browser screenshots visually inspected. Exact inventory plus ZIP byte/hash readback in delivery-check.json. Motion unit tests exercise clamp/endpoints/order and malformed-asset rejection.

## Honest visual limits
Crimson/gold major patterns and hardware read at mobile size; fine weave does not resolve convincingly and remains stylized. Raised diamonds are separate outlines, not an interconnected lattice; body lattice is mapped. Some diamonds overlap visually in perspective. Pattern joins are discontinuous at skin/corner transitions. Dark seam and inherited long clasp are prominent; rigid metal ornament is enlarged compared with real textile threads. Source render retains sampling grain. No photoreal, reference-equivalence, authentic textile reconstruction or physical mechanical claim.

## Reproduce
Python with numpy/Pillow/Playwright; Blender 5.2.1; Node plus pinned package.json/package-lock dependencies; installed Edge. All paths resolve within folder, except optional assembly helper `setup_author.py`, which documents derivation from sibling Japan and is not needed to reproduce the included self-contained author.py.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`.
3. `python build.py`.
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
5. `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.

Shared pilot dependency folder was present but lacked esbuild. Initial build failure retained; pinned dependencies installed only inside this new folder. No art/acceptance assertion was relaxed. Node here is the JavaScript build/runtime tooling, not a blockchain node. Dependencies/backups excluded from archive and Git. Regeneration overwrites generated source and hashes; redo inventory after any change.

Only preview/malaysia-v1 additions. Branch backup only, no merge; collection integration is a separate dependent card. Human per-asset review explicitly waived for this batch; technical acceptance does not imply human aesthetic approval.
