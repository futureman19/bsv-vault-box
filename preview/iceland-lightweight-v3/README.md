# Iceland / Basalt — lightweight v3

Material-only refinement of the approved ORIGINAL v1, not the large v2. Preview only; no minting, chain activity, deployment or custody functionality.

## Open

Open `iceland-lightweight-v3.html` directly. It embeds the complete Three.js runtime, GLB, textures and updated rendered fallback. No server, CDN, HDRI or network access is needed. The original procedural room reflection environment and all interactions are retained.

## Exact payload weights (literal bytes)

| File | Bytes |
|---|---:|
| Complete offline HTML | 1,757,676 |
| Portable GLB | 727,772 |
| Editable packed Blender source | 260,899 |
| Actual updated source-render PNG | 1,910,776 |
| Embedded fallback JPEG | 138,416 |
| Shared 256px base-color JPEG | 8,499 |
| Shared 256px packed roughness/metalness JPEG | 6,133 |
| Shared 256px tangent normal PNG | 73,312 |
| Original unchanged viewer bundle | 595,162 |

Hard HTML limit: 5,000,000 bytes. GLB target: 1,200,000 bytes. The fallback is a quality-92 JPEG of the actual updated source render; the full PNG remains supplied. The source ZIP is a separate editing/archive deliverable, not required by the HTML and not subject to its size ceiling. `delivery-check.json` records the ZIP's measured size and hash.

## What changed / what did not

Five basalt facet materials share restrained, locally generated procedural maps, with planar UVs at two repeats per model unit. Maps are real embedded glTF images, not Blender-only nodes. They are not photographic scans. A lossless normal PNG avoids lossy tangent-vector artifacts; normal strength is 0.35. Roughness occupies green and metallic multiplier occupies blue in the shared packed map.

The entire original geometry binary prefix, original position/normal/index accessors, nodes, transforms and pivots are retained. Only basalt UV attributes, textures and material references are appended. The polished blue-black lid is the ORIGINAL unchanged material: roughness 0.28999999165534973 and metalness 0.2800000011920929, no cloudy color map or normal map. All non-basalt materials are unchanged. `viewer.js`, `viewer.bundle.js`, and `motion.mjs` are byte-identical to v1, retaining staged latch release, lid lift, reverse, reset and reduced-motion behavior. No lighting overhaul was needed.

Actual GLTFLoader result: 9,632 triangles, 217 mesh primitives, nine materials; no nonfinite or degenerate triangles. Bounds and wide rectangular proportions exactly match v1.

## Verification

- Test-first `budget-red.txt` rejects the actual oversized v2 HTML/GLB and non-original cloudy lid; it fails material/budget assertions, not a missing module. `budget-green.txt` passes v3.
- `browser-check.json`: offline Edge `file://`, desktop 1440x1080 and emulated mobile 390x844; native mouse/touch rotation, opening/closing, reset during motion, reduced motion, no overflow, no external requests, no JavaScript/console errors. Real corrupted bytes entered GLTFLoader and selected the rendered fallback with disabled controls, no unhandled error.
- `pbr-check.json`: actual decoded 256x256 color/normal/roughness maps and UVs on all five basalt materials; original glossy untextured lid, matched bounds and cameras. Actual desktop/mobile browser screenshots and matched original/v3 closed/open/closeup comparisons supplied.
- `preservation-check.json`: binary geometry prefix, transforms/pivots, non-basalt materials and full viewer/motion byte identity.
- `editable-check.json`: independent source reopening, all original object matrices/parents/vertices/faces identical, packed images and UVs present.
- `source-check.json`: independent saved-source BVH clearance at 81 motion samples, zero nonbearing intersections; intentional mating-bearing exclusions explicit. Hollow interior floor ray lands at z=0.26500001549720764. Sampled, not continuous physical collision certification.
- `motion-green.txt`: both original motion/asset-contract tests pass.

## Visual limits

Matched-camera normal-distance and closeup review confirms preserved softly glossy lid and no blanket noisy/cloudy finish. The basalt change is deliberately subtle and barely visible at normal distance; this is preservation with fine surface refinement, not a photoreal makeover. Repeated angular columns, broad facets, very clean brass and luminous seam remain stylized. Broad lid reflections are not mirror-sharp. Emulated mobile ran on desktop RTX 4060, not a physical phone. Closeup comparison intentionally crops the base to emphasize surfaces. No extra polish iteration was warranted for this bounded pass.

## Rebuild / edit

Python dependencies: Pillow and Playwright; Blender 5.2.1; Node for the motion tests. Original immutable inputs are included in `original/` so regeneration does not require v2 or sibling folders.

1. `python generate.py` appends portable maps/UVs to the archived original GLB.
2. `blender --background --factory-startup --python-exit-code 1 --python refine_source.py` independently reopens archived original source, adds UV/material nodes, packs images, saves editable source and renders the poster. No geometry changes.
3. `python build.py` embeds existing byte-preserved viewer bundle, updated GLB and fallback.
4. Run `python test_budget.py`, `python verify_preservation.py`, `node --test tests.mjs`, `python verify_browser.py`, `python verify_pbr.py`; use Blender with the same safe flags for `verify_source.py` and `verify_editable.py`.
5. `python package_delivery.py` rebuilds the allowlisted ZIP and matching output copy/hash manifest.

Source geometry remains individually named/editable. Regeneration overwrites v3 edits; save manual edits separately. `original/author.py` is historical provenance, not the v3 build entrypoint. Original source/HTML are retained for reproducible comparisons. Viewer source plus original pinned dependency lock and license remain included; rebuilding that bundle is unnecessary for material refinement.

Old deliverables and production `docs/` are untouched. Source archive excludes backups, secrets and node_modules.
