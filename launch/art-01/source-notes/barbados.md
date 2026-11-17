# Barbados v1 / Coral Terraces

Open `barbados-v1.html` directly in Edge/Chrome, offline. **HTML 2,171,585 bytes; GLB 1,038,656 bytes.** All runtime code, maps, model and actual-source poster are embedded. Cosmetic movement only, not an on-chain seal.

## Design and provenance
Research-backed brief was written before modeling. Ivory porous coral-limestone body, turquoise coastal enamel and three stepped lid terraces, warm brass hardware. Original procedural composition, not a geographic replica, photographic scan, hand sculpture or a reconstruction of supplied art. Research photographs are not embedded. Mechanism/viewer/check lineage: Japan v1 at repository base ff5d78f; frozen trimmed mechanism included. Shared vault kit untouched. Three.js MIT license included.

## Verified
- Saved Blender source independently reopened: 20 moving and 39 static meshes, 81 staged poses, zero unintended sampled surface collisions. Every coastal ornament participates; only explicitly named mating bearings excluded. Ten hinge mounting attachment pairs intersect. Hollow floor ray z=0.2650000155.
- Source/export maximum nearest-vertex error 1.7120130735e-7, below 1e-5. Baseline evaluated pivot matrices match exactly. 80-degree latch release precedes 105-degree lid opening.
- Three terrace tops z=2.16/2.32/2.49; all coastal geometry belongs to lid. Deliberately detached upper terrace is rejected by the theme oracle (post-implementation negative control, not TDD).
- Actual GLTFLoader: 59 meshes, 14,476 triangles, four materials, zero nonfinite vertices/degenerate triangles. All three portable maps 256x256; decoded color/roughness-green/normal variation ranges 92/43/42.
- Offline file:// Edge desktop 1440x1080 and touch-emulated mobile 390x844: native open/close, rotation, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Actual corrupt GLB parser failure and no-JS poster fallback passed. Open projection max absolute NDC 0.892365.
- Actual source poster nonblank; actual mobile closed and desktop open screenshots visually inspected. Packaging verifies explicit required artifacts, SHA-256 inventory and ZIP byte-for-byte readback. `.gitattributes` preserves exact bytes across checkout.

## Honest visual limits
A stylized miniature, not photorealism or a survey of Barbados. Stone pits are mostly subtle normal/color texture; terraces are compact and faceted rather than naturally eroded cliffs. Turquoise coastal inlay has a slight raised edge and reads as enamel, not transparent water. The seam is a decorative gasket. Source poster has sampling noise (bounded 24-sample render, denoising off); browser captures are cleaner. At full opening the lid ornament faces away from the front. Front-view hinge silhouettes alone do not establish attachment; independent source intersections provide bounded evidence, not engineering certification. Mobile emulation on RTX 4060 is not physical-phone performance. Sampled surface checks are not a continuous collision proof.

## Failures and fixes
Optional Codex CLI exited with authentication failure before implementation; no Codex code accepted and no credentials changed. Hermes authored and tested directly. Initial build failed because the requested sibling dependency directory lacked esbuild; original output retained in `initial-build-failure.txt`. Installed pinned package.json dependencies locally in this new folder, then reran build successfully without changing acceptance thresholds. All final art/geometry/browser gates passed; detached-terrace negative control proves the ancestry assertion can reject a defect.

## Reproduce
Python with Pillow/numpy/Playwright, Blender 5.2.1, Node and installed Edge required for authoring/testing only. Run `npm ci --ignore-scripts --no-audit --no-fund` here. Then `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Blender on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `node test_motion.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`. Run commands from this directory. Author overwrites generated outputs; preserve manual variants separately. `setup_author.py` documents initial adaptation and requires sibling Japan script; final `author.py` is self-contained with included mechanism/maps. ZIP excludes dependencies/backups.

No blockchain tools, keys, chain queries, minting, production edits, hosting or deployment. Branch backup only, no merge. Integration/gallery belongs to the pre-created final collection card; no per-asset review gate under the user's waiver.
