# Morocco Sandstone v3 — BODY ONLY

Open `morocco-sandstone-v3.html` directly, offline. No server or downloads are needed. Cosmetic interaction is not an on-chain operation.

## Result and limits
The body now uses original, seeded sandy mineral painting: muted clay/ochre coloration, irregular low-contrast bedding, granular flecks, shallow pore cues and portable normal/roughness variation. No scans or third-party stone imagery were used. Saturn was a palette/layer metaphor only.

Same-light browser comparison: `before-after-body-closeup.jpg`; normal view: `before-after-closed.jpg`. `poster.png` is the actual saved model rendered with the unchanged v2 studio, not AI marketing. `reference-comparison.jpg` labels the primary marketing concept separately.

Visual review: substantially less like printed waves and more like gritty sandy rock. It remains stylized: pale peach/beige under the preserved bright viewer lighting, with relatively even/coarse grain and some directional marks. It does NOT closely reproduce the original's richer terracotta/ochre and distinctive branching bands. Bedding was intentionally made subordinate to grain. No further visual iterations were performed after one focused correction.

## Scope preserved
All geometry, dimensions, transforms, parents, inner liner, cedar, tilework, ridge, clasp, corner guards, ring, lighting and motion are unchanged. Only five `Rose stone` objects' UVs and their shared material/images changed. No displaced geometry or new props. `verify_preservation.py` compares the approved GLB graph, every non-UV accessor, non-body material records and image bytes. `verify_source_preservation.py` independently opens both blends and compares geometry, non-body UVs/materials, transforms, lights and camera. Final GLB derives directly from the original bytes; it is not a lossy general re-export.

## Mapping and maps
One world/object XY angular coordinate and physical Z height is baked into UVs across all body pieces. The rear wrap is unwrapped per rear mesh and the painted maps have periodic endpoints. No independently reset front/side textures. All maps are 1024 x 128: the narrow strip approximates the body's circumference/height ratio, avoiding square-map grain being stretched into horizontal scratches. Base color and ORM are JPEG; normal is PNG. ORM green drives roughness; metal factor remains zero. The source uses the same packed bytes and equivalent nodes. Normal strength is 0.8. Lightly rounded preexisting geometry and panel junctions remain.

The initial pre-generation budget allowed ~1 MB body maps within the existing 4.19 MB viewer's 5,000,000-byte limit. Final body maps total 484,459 bytes. Final HTML: 3,930,956 bytes; GLB: 2,336,332 bytes. The entire runtime and poster fallback are inside HTML.

## Verified
- Test-first old-UV negative control retained in `negative-control.txt`; old mapping error 2.10388 vs new < 6e-8.
- Exact non-body source and exported geometry/material preservation; source/export position error < 1.8e-7.
- Actual GLTFLoader: finite vertices/UVs, no degenerate triangles; decoded color, roughness and normal variation; decoded normal lengths 0.9868–1.0082, nonzero normal scale.
- Real source BVH collision/attachment harness rerun over 81 motion samples: no unintended collisions. Only documented mating bearings excluded; not continuous-time proof.
- Offline Edge desktop and emulated-touch mobile: rotation, open/close, interrupted reset, reduced motion, intact open silhouette, no overflow, no external requests/errors. Actual corrupted GLB invokes poster fallback; no-JS poster checked. Emulation is not a physical-phone performance test.
- Package required-file inventory, ZIP byte hashes, copied delivery readback and delivery-folder HTML offline open/reset checked.

## Reproduce
Prerequisites: Blender 5.2.1, Python with numpy/Pillow/Playwright, Node with package.json dependencies. Run from this folder:

```
python materials.py
python finalize_glb.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
python verify_preservation.py
blender --background --factory-startup --python-exit-code 1 --python verify_source_preservation.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
python verify_browser.py
python verify_extended.py
python verify_material_runtime.py
```

`baseline/` contains the immutable approved blend and GLB required by the material-only author/finalizer. Install dependencies locally if the sibling iceland-pilot toolchain is unavailable. Build can use this folder's node_modules. Browser checks require installed Edge; review.py uses the prior sibling preview for its before image and the original local reference path. package_delivery.py has an explicit local delivery target. setup.py is historical setup, not needed for regeneration. `first-pass/` preserves the initial review images before the one grain-aspect correction. Source ZIP excludes backups, node_modules and credentials.

No docs, deployment, mint, node, wallet operation or push. Previous preview remains immutable. Parent independent review is still required before user-facing acceptance.
