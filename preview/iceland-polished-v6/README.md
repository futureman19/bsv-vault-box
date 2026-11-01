# Iceland / Basalt — Polished v6

A bounded refinement of user-liked v5, not a redesign or photoreal claim. Open `iceland-polished-v6.html` directly, offline. This is cosmetic collectible geometry, not a mint or custody implementation.

## Changed vs preserved

- Body rim and complete rigid lid/hinge/latch assembly raised 0.168; body cladding/liner extended progressively above floor. Approximately 12% of the prior 1.4 body height. Width/depth and lid thickness unchanged. Width/hinge-height changes 2.48 → 2.2302, remaining a wide chest. Equal-object-width promotional comparison suggested modest additional height; camera perspective is estimated, not recovered physical reference dimensions.
- Ice terrain refined from 15×9 to 25×15 irregular points at the same footprint; glTF transmission 0.68, roughness 0.12, IOR 1.31. River retains actual boolean channel, inset and edge cascade; transmission 0.40 and restrained emission. Both remain lid children.
- Rounded moss beads replaced by 233 compact merged patches of fine bent lancelets localized at the original broken ledges; small olive growth is less conspicuous, sometimes nearly invisible at normal scale. Not a photographic moss simulation.
- Brass sheet guards thinner (top 0.018, sides 0.020), rounded in-plane profiles, quieter brass color and roughness 0.36; all fasteners, handles, original clasp and plain medallion retained.
- Polished black lid roughness 0.085. Browser uses soft shadow mapping and a shadow-only floor, with modestly stronger lid environment response. Studio light repositioned to reduce warm lid wash. These presentation changes are disclosed, not attributed to geometry.
- Original `motion.mjs` byte-identical to v5. Staged latch release, lid opening, close, reset and reduced-motion behavior unchanged. Fixed bearing/bridge assembly translated coherently, not a floating replacement lid.
- Original v1–v5 and promotional files preserved by pre-pass SHA-256 snapshot.

## Verified final artifacts

- Standalone HTML **2,686,719 literal bytes**, GLB **1,461,104 bytes**. No remote assets. Poster is a compact JPEG rendered from the actual saved model, not the promotional image.
- 25,551 triangles; 399 runtime meshes; 15 materials. Real GLTFLoader finite-position/nonzero-area checks pass. 37,270 portable vertex normals finite and unit length; independent evaluated source normals also checked.
- Independent source reopening and glTF reimport: maximum bidirectional nearest world-vertex error 0.0000001712013; packed source image hashes and source/export material factors recorded. Three 128px stone maps decoded by real loader. This is vertex-set/factor parity, not exact topology or UV-corner parity.
- 81 staged BVH collision samples, no unintended intersections. No new exclusions or weaker thresholds. Ten explicit wall→bridge→mount→stem→bearing and moving leaf→lid contacts pass. Hollow floor ray passes. Sampled surfaces are not continuous solid-volume collision proof.
- Offline `file://` Microsoft Edge: desktop 1440×1080 and mobile-emulated 390×844; native mouse/touch rotation, open/close, full-open framing, reset during motion, reduced motion, zero external requests, zero normal-run console/page errors, no overflow. Corrupt actual GLB parsing selects poster fallback; no-JS poster and disabled control verified. Desktop RTX 4060, not physical-phone performance.
- `before-after.jpg`: actual v5/v6 GLBs under identical candidate camera and lights. `reference-comparison.jpg`: equal object width, without warping. `closeup.png` intentionally crops the lower extremity for detail; desktop/mobile open views show full silhouette.

## Visual disposition / limits

Vision review judged v6 visibly taller, cleaner and more cohesive than v5 rather than merely relit. Thin rounded guards and finer growth are real geometry changes. Ice has actual portable transmission but still reads opaque/faceted at normal viewing distance. River/cascade remains graphic; basalt remains strongly segmented. Growth is now arguably too sparse. Browser lid reflection is restrained; studio poster has a broad gray reflection despite the black material. Mobile hinge connection is visually subtle, although all ten attachment contacts and 81 pose samples pass. No claim of exact promotional parity, hyperrealism or physical hardware engineering.

One focused presentation/material correction after first visual inspection; no perfection loop. An initial rounded-sheet bevel produced degenerate triangles and was removed in favor of explicit rounded outlines, retaining strict area checks. A new exact decimal transmission comparison was corrected to float32 precision tolerance (1e-6); collision/area thresholds unchanged.

## Reproduce

Dependencies: Blender 5.2.1, Python with Pillow/Playwright and installed Edge, Node/esbuild/Three from `npm ci` here or existing `../iceland-pilot/node_modules`.

1. `python textures.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Same Blender flags for `test_features.py`, `verify_source.py`, `verify_parity.py`, `verify_materials.py`.
4. `python build.py`
5. `python verify_browser.py`; `python verify_extra.py`; `python verify_polish.py` (last replaces inherited comparison annotations and creates matched A/B).
6. `python package_delivery.py`

Regeneration overwrites only v6 output/manual source edits. Source ZIP inventory is suffix-allowlisted, excludes backups/dependencies/secrets and itself. Manifest hashes and delivery/ZIP readback are separate from visual/behavior tests. Nothing pushed, deployed, minted or connected to wallets/nodes.
