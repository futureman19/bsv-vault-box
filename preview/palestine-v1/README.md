# Palestine v1 — Crimson Stitch

Open `palestine-v1.html` directly in Edge/Chrome. The complete viewer is **4,439,132 bytes**; GLB **2,732,592 bytes**. All runtime assets are embedded. Drag/touch to rotate, open/close the lid, reset and reduced motion are exercised offline.

## Design and limits
A warm wooden keepsake box carries a charcoal textile-inspired lid panel with 48 raised crimson cross stitches arranged around three geometric diamonds. UNESCO research and the pre-model contract are in design-brief.md. This is an invented digital arrangement inspired by embroidery, not an authentic regional pattern, artisan textile, photogrammetry or hand sculpture. No third-party pictures are embedded. Wood and hardware are collection-family design choices, not claims about Palestinian timber or metalworking.

Actual source render and mobile screenshots were visually inspected. The warm shell, brass and contrasting stitched panel read clearly and the closed box fits mobile. Fine weave and individual thread detail are limited at mobile size; perspective makes diamond outlines look somewhat rectangular/stepped, thread highlights appear coral, and the textile panel is surface-mounted rather than recessed. The low-sample source poster has visible grain. These are disclosed stylizations, not photoreal equivalence claims. Visual review is waived per collection directive, not falsely attributed to a human approval.

## Verification
- Independently reopened saved Blender source: 129 moving and 99 static meshes, **81 sampled poses**, zero unintended intersections; all moving thread geometry included. Only named mating bearing contacts excluded. Hollow interior floor ray z=0.2650000155. Sampled surface checks are not continuous mechanical certification.
- Source/export maximum vertex error **1.712013073529306e-7**, below 1e-5; five packed procedural maps.
- Theme: 96 diagonal thread segments / 48 crosses / three diamonds; all lid-owned; evaluated z range 2.0319998264–2.0499999523. A deliberate detached-thread negative control really fails `AssertionError: detached ornament`; delivered source remains untouched. This is post-build fault injection, not test-first evidence.
- Two motion/invalid-asset tests pass. Actual GLTFLoader checks zero nonfinite/degenerate geometry. Runtime map variation and dimensions checked, roughness sampled from green channel.
- Desktop 1440x1080 and touch-emulated 390x844 Edge over offline file://: drag, native open/close, interrupted reset, reduced motion, full-open framing, no external requests/errors/overflow. Actual corrupt GLB reaches parser and activates poster; no-JS poster passes. Emulation is not physical-phone performance.
- Delivery inventory SHA-256, explicit required artifacts, ZIP readback and staged Git blob hashes checked separately. Folder-local -text preserves exact bytes.

## Files and reproduction
`palestine.blend` editable source; `palestine.glb` portable model; `mechanism.blend` inherited trimmed Japan/Iceland articulation; maps/ contains generated textures; poster.png/jpg are actual renders; desktop/mobile captures are real browser evidence. JSON reports and raw text outputs document checks. No promotional AI image used.

Run Python maps.py, Blender 5.2.1 `--background --factory-startup --python-exit-code 1 --python author.py`, Python build.py; run Blender with verify_source.py, verify_parity.py and verify_theme.py; Node `--test --test-reporter=tap tests.mjs`; Python verify_browser.py and verify_extended.py; Python package_delivery.py. Scripts resolve this folder. `setup.py` records initial sibling-pilot adaptation only; do not rerun it to regenerate final hand-tuned viewer copy. Regeneration overwrites source edits.

Build dependencies: Python numpy/Pillow/Playwright with installed Edge; Node and pinned package.json/lockfile; Blender. Shared pilot dependency folder was empty, so pinned packages were installed within this folder only; node_modules is excluded. Source inherits compact wood-map filenames from Japan but palette and artwork are new. Three.js MIT license included. Source ZIP excludes dependencies and backups.

No blockchain, keys, wallets, minting, node startup, VPS, production files or deployment were touched. Branch backup only; final collection integration is separate.
