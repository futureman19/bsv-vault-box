# Panama v1 — Darien / Mangrove & Jade

Open `panama-v1.html` directly in Edge/Chrome. Complete offline interactive 3D with embedded model, runtime, maps and actual-source poster. Not minted, hosted, signed, or a custody verification. Cosmetic opening only.

## Delivered
- `panama-v1.html`: **2,861,782 bytes**, strictly below 5,000,000.
- `panama.glb`: **1,559,000 bytes**, portable mesh/maps.
- `panama.blend`: packed editable script-authored Blender source. `mechanism.blend` is the inherited trimmed articulation source.
- Generated `maps/`, `poster.png` and `.jpg`, desktop/mobile screenshots, independent verification scripts, check JSONs, SHA-256 inventory and source ZIP.

## Actual acceptance
Real GLTFLoader: 18,886 triangles, 110 meshes, 11 materials, zero nonfinite vertices and zero degenerate triangles. Independent source reopening: 71 moving and 39 static meshes sampled through 81 poses, no unintended surface intersections; explicit bearing exclusions only. Hollow floor ray z=0.26500001549720764 and ten hinge attachment pairs verified. This is sampled surface-intersection testing, not continuous or manufacturing certification.

Source/export nearest-vertex error in both directions: 1.712013073529306e-7, below 1e-5. Source pivot matrices independently compared against reopened mechanism. All 55 landscape meshes belong to lid. Forty connected water quads and fifteen root-ring centers seated on bank surface verified. A deliberately detached ornament fails the ownership test; real corrupt GLB fails actual loader and invokes poster fallback. These are post-implementation negative controls, not test-first TDD.

Offline `file://` Edge desktop and 390x844 touch-emulated mobile on RTX 4060: native open/close, drag/touch rotation, interrupted reset, immediate reduced-motion state, no HTTP requests/JS errors/overflow. Full-open projected geometry fits (<0.893 absolute NDC). No-JS poster tested separately. Portable roughness uses the glTF green channel. Source poster nonblank/alpha tested. Not physical-phone performance evidence.

## Visual verdict and limits
Research-backed invented miniature, not a reproduction of geographic Darien, traditional craft, or a named mangrove species. Jade is a palette choice, not a claim about local geology. Actual source poster visibly contains three spreading stilt-root trees and a sinuous inlet. Default mobile view overlaps two trees, so only two are distinctly countable there; rotate to resolve the third. Rear-open screenshot exposes the three clusters. Leaves/roots are stylized and angular, water is a shallow solid-color ribbon without simulated flow, and the terrain boundary is rectangular. Body mottling is procedural and cleaner than weathered natural stone. Low-sample source render contains visible grain. No photorealism or primary-reference equivalence claimed.

Image inspection found no obvious large holes, clipping of the overall model, or catastrophic defects. Actual ancestry, source collision sampling, and browser interaction evidence—not screenshots alone—support movement claims. User waived per-asset human review until collection integration.

## Reproduce
Python with numpy/Pillow/Playwright; installed Edge; Blender 5.2.1; Node.js, Three 0.180.0 and esbuild. `npm ci --ignore-scripts --no-audit --no-fund` installs local build tooling; no dependency downloads occur in the delivered viewer.
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`
`setup.py` records the original one-time adaptation from the read-only Japan pilot and is NOT part of regeneration (it would overwrite later viewer fixes). All normal rebuild inputs are included. Authoring overwrites source/export/poster; copy manually edited sources first. Node dependencies and backup .blend1 files are excluded from archive.

## Failures and lineage
Optional Codex input lane exited 401 before producing edits; Hermes implemented and verified directly, with no credential changes. Initial build failed because the requested main-checkout dependency directory existed but was empty. Installed exact declared tooling locally inside this preview; rebuilt successfully without changing sibling directories. No geometry/collision acceptance failures occurred. Corrupt-loader and detached-ornament failures are deliberate controls.

Mechanism/viewer/test lineage is the repository Japan/Iceland pipeline at base ff5d78f; shared vault kit unchanged. Three.js MIT license included. Ecological factual sources and pre-model visual contract are in `design-brief.md`; no borrowed photos, scans, AI artwork or promotional substitutes. All changes are additive under this preview. No blockchain nodes, keys, queries, mint, broadcast, production site or VPS accessed. Branch backup only; final collection integration is separate.
