# Japan / Cedar & Moss — bounded v2 refinement

Open **japan-cedar-v2.html** directly in Edge, offline. This is an actual interactive 3D model, not an image substituted for vegetation. Drag/touch to rotate, Open/Close lid, Reset view. Cosmetic motion only; no custody operation, mint, node, funds or deployment.

## Outcome and payload

| Artifact | V1 bytes | V2 bytes |
|---|---:|---:|
| Complete standalone HTML | 4,845,566 | **4,646,370** |
| Embedded GLB | 3,079,080 | **2,926,644** |

HTML includes unchanged bundled Three/loader, embedded textures and full-quality actual-model JPEG fallback. No remote dependencies, decoder, hidden requests, removed fallback or lowered viewer settings. Final bytes beat the 4.7 MB preference and strict <5,000,000-byte requirement. ZIP size/hashes are in delivery-check.json; the editable source is separate from default viewer payload.

Four-triangle/five-vertex foliage needles became two-triangle/four-vertex folded lancelets, using fewer but larger overlapping sprays. Thirty uneven branches replace 28 regular branches; asymmetric spreading tiers retain visible trunk and gaps, rather than opaque spheres/cones or texture cards. New conforming moss follows raycast stone heights with irregular bare windows and attached filaments. No alpha sorting or added translucent-shadow costs. Geometry: **39,916 triangles, 174 runtime meshes, 13 materials**, versus 48,664 / 200 / 11 in v1. The multi-material moss surface exports as three primitives under a lid-parented group.

## Visual result and limits

`before-after.jpg` compares actual browser models at exactly the same camera, lighting, pose and native crop scale. `mobile-before-after.jpg` contains full native 390×844 pages. `reference-comparison.jpg` is concept artwork versus actual Blender model at equal measured wood width, explicitly different lighting/camera. `poster.png` / `poster.jpg` are real model renders, not marketing illustrations. `references/primary-japan.png` is the unchanged primary marketing reference.

The same-camera comparison visibly improves canopy fullness and connected moss coverage while preserving the chest. The tree remains a stylized miniature conifer, not botanical/photoreal equivalence to the concept. At mobile scale it is still small and somewhat airy; moss reads as a connected green cap, not individually resolved plush fibers. Branch tiers can look planar and foliage remains stippled. No further art iteration was undertaken: initial attempt plus **one focused visual correction**, followed only by nonvisual source cleanup/test fixes.

### Measured feature gate

An authored test was executed RED against v1 before edits and on the insufficient first attempt. Final white-emissive isolated raster masks at the unchanged normal camera:

| Feature | V1 pixels | V2 pixels | Ratio |
|---|---:|---:|---:|
| Desktop foliage | 1,051 | 1,791 | 1.704× |
| Desktop moss | 725 | 1,331 | 1.836× |
| Mobile foliage | 334 | 580 | 1.737× |
| Mobile moss | 242 | 449 | 1.855× |

This is projected mesh silhouette-union coverage, **not** occlusion-aware beauty-image segmentation, biological density, or a realism score. The original predeclared minimums (1.65× foliage, 1.8× moss) passed without relaxing them. Actual beauty-image vision review separately confirmed improvement. RED outputs and first-attempt captures are retained.

## Verification

- Actual GLTFLoader parsed final embedded bytes: zero nonfinite vertices and zero degenerate triangles. Decoded color maps retain original ranges 89/35/143 and resolutions 512/256/256. No extra texture atlas or decoder.
- Independent source reopening: **138 unchanged objects**, with exact raw vertices/polygons/UVs, local transforms, parents, material node inputs/links and packed maps. This includes trunk/roots, body, wood, hardware, stone feet, green seam, lid dimensions, pivots and terrain granite. `viewer.js`, `motion.mjs` and compiled runtime are byte-identical to v1; same reflection/light/controls setup.
- Every tree/terrain mesh is descended from Lid_Hinge. Trunk placement is unchanged rear-right (+X,+Y in Blender); see placement-check.json and top-down-source.png.
- Reopened .blend: **81 motion poses, 73 moving meshes against 99 static meshes, zero unintended intersections**, plus releasing latch versus every moving lid mesh. Entire new foliage/moss included. Same narrow exclusions for intentional concentric hinge-leaf/barrel and latch-knuckle/bridge/pin bearings; no added exemptions. All ten hinge attachment contact pairs pass. Hollow floor ray z=0.2650000155. Sampled surface checks are not continuous collision/mechanical certification.
- Source/export bidirectional nearest-vertex maximum error **0.0000001712013** (<0.00001). The first source check found unused moss grid vertices omitted by glTF; these loose points were removed without changing surfaces. Failure retained in initial/.
- Independent re-export: JSON, positions, normals, indices and embedded images exact. Whole GLB is not byte-identical because saved/reopened UV values vary by up to 0.000000059604645 (explicit 0.000001 UV tolerance).
- Offline file:// Edge desktop and native-touch mobile emulation: drag/touch rotation, open/close, interrupted reset, reduced motion, full-open silhouette fit (max |NDC| 0.892365), no horizontal overflow, no HTTP(S) requests or unexpected errors. Actual corrupted embedded GLB invokes poster fallback and disables controls. No-JS poster checked independently, including decoded dimensions and zero external requests. Expected parser rejection is recorded, not counted as a successful-load error.
- RTX 4060 desktop GPU; mobile is browser emulation, **not physical-phone performance testing**.
- Original v1 tree of files, Iceland inputs, and primary reference hash-checked at packaging. Archive entries read back byte-for-byte and delivery copies hashed. See preservation-check.json, inventory.json and delivery-check.json.

## Files / reproduction

Main deliverables: HTML, japan.glb, japan.blend, baseline.blend (immutable approved starting source), poster PNG/JPEG, review PNG/JPEGs, maps/, references/, scripts, evidence JSON/TXT, inventory and source ZIP. No node_modules or .blend1 backups in package.

Use Blender 5.2.1, Python with Pillow/numpy/playwright, Node with package.json dependencies, and installed Edge. Install build dependencies locally if needed. build.py otherwise discovers the existing sibling iceland-pilot/node_modules as build-time fallback; **runtime needs neither sibling nor network**.

1. `blender --background --factory-startup --python-exit-code 1 --python refine.py`
2. `python build.py`
3. Run Blender with each: verify_source.py, verify_preservation.py, verify_parity.py, verify_reexport.py, render_review.py.
4. `python verify_browser.py`; `python verify_extended.py`; `python coverage.py`; `python compare.py`.
5. `python package_delivery.py --delivery <desired-output-folder>`.

Regeneration overwrites output; retain a separate copy for manual edits. baseline.blend already packs original maps and mechanisms; maps.py/mechanism.blend are lineage resources, not required by refine.py. setup.py is the original **local sibling migration/snapshot helper**, not a standalone reproduction prerequisite. coverage.py uses packaged before-coverage.json for final comparison; --baseline requires the original sibling v1. verify_preservation.py also requires the original sibling runtime for its byte comparison; the packaged report preserves that executed evidence for extracted archives. Original-path preservation checks label unavailable originals honestly rather than claiming a fresh comparison.

Geometry/maps are script-authored, not scans or human hand-sculpture. Three.js MIT license included. This pass does not alter production docs, push/deploy, start nodes, or begin Morocco.
