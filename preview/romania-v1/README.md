# Romania v1 — Maramureș / Carved Timber

Open **romania-v1.html** directly in Edge/Chrome. Offline, self-contained, no server or network. **HTML 3,256,509 bytes; GLB 1,863,032 bytes.** Drag/touch to rotate, Open/Close lid, Reset; reduced-motion snap and real-model poster fallback.

Original procedural timber relief inspired by the UNESCO-listed wooden architecture of Maramureș; see the pre-authoring `design-brief.md`. This is not a replica of a church, an authenticated folk pattern, scanned wood, photorealistic artwork or a representation of every Romanian tradition. The low roof, compact spire (without religious icon) and geometric inlays are invented stylizations. Hardware/interior are inherited family extrapolations.

## Art and files
- `romania.blend`: packed editable Blender source; `romania.glb`: embedded-map export.
- `author.py`, `ornament.py`, `maps.py`, `mechanism.blend`: reproducible source. Mechanism adapted from repository Japan pilot, with new roof/spire/border and timber palette. No cedar tree/moss retained.
- `poster.png`/`.jpg`: actual source render, not AI promotion. Desktop/mobile screenshots show the actual offline GLB.
- `romania-v1-source.zip`: explicitly required deliverables plus source/maps/evidence, verified by ZIP readback. `inventory.json` records exact byte counts and SHA-256; `delivery-check.json` records the archive hash without recursive self-hashing.

## Verified
Actual Three GLTFLoader: **18,434 triangles, 291 meshes, 7 materials**, zero nonfinite vertices or degenerate triangles. Decoded grain/end-grain/stone texture variation and roughness GREEN-channel variation pass. All maps at most 512px. Saved-source reopens independently; source/export nearest-vertex error must remain below 1e-5. Theme checker compares original pivot matrices, counts 100 shingle plates / 56 diamond segments / 3 spire components and checks all 164 ornament objects belong to the lid; detached-parent negative control is rejected.

Source BVH test samples **81 poses**, all moving versus static geometry and releasing latch versus lid; no unintended intersections. Explicit inherited mating bearing contacts only are exempt. Ten hinge attachment overlaps and hollow interior floor ray pass. Runtime motion test samples 81 staged poses: 80-degree latch first, then 105-degree lid; three invalid-asset negative controls rejected. This is sampled surface evidence, not continuous physical clearance certification or manufacturing engineering.

Offline Edge file:// desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, drag/touch rotation, reset mid-motion, reduced motion, no horizontal overflow, zero external HTTP requests and no runtime errors. Full-open projected silhouette fits (maximum absolute NDC ~0.892365). Actual corrupted GLB parser input triggers poster fallback; no-JS poster also passes. These run on RTX 4060 desktop hardware, **not a physical phone performance benchmark**.

## Visual verdict and real corrections
Complete stylized timber chest, readable miniature roof/spire and contrasting geometric lid inlay at mobile size. Grain and shingles remain simplified; inlay is a delicate band, not deeply carved artisan detail; spire is compact rather than a scale architectural model. Roof hides some lid pattern and is behind the lid when opened from the front (rear-open capture supplied). No claim of photoreal equivalence. Source poster retains modest render noise.

1. Initial HTML **5,825,763 bytes** failed the strict <5,000,000-byte gate (GLB 3,789,020). Reduced redundant three-segment bevels to single-segment microbevels, retaining modeled shingles; tests rerun. Initial log retained. Initial diamond slopes formed crosses; reversed slopes to form closed diamonds.
2. Initial mobile inlay lacked contrast. Final bounded correction darkened the generated timber atlas by 0.72 and brightened inlay material. This deliberately departs from the original atlas color targets to compensate for bright studio/runtime lighting. Final mobile visual inspection found visible diamond outlines and full framing; no further polish loop.

The first build also exposed an empty shared node_modules target. Installed exact package versions locally in this directory; dependencies are not included in the archive or Git. Optional Codex implementation lane failed authentication before edits; all implementation/verification was performed directly by Hermes, no credentials modified.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/playwright, installed Edge, Node, and `npm ci` here. Source scripts use relative paths; build uses local dependencies or sibling Iceland dependencies if present. Runtime HTML has no dependencies.

```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme.py
node tests.mjs
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

Regeneration overwrites authored output. Packaging excludes dependencies, .blend1 backups, caches and optional-lane logs. Three.js license included. Folder-local Git attributes preserve exact bytes on Windows.

Local art only; no mint, funds, keys, blockchain nodes/queries, custody changes, hosting or deployment. Collection direction: 201 equally one-of-one boxes. Branch backup only; final collection integration is a separate task.
