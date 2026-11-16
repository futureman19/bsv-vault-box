# United States / Flag & Fireworks — v2

New additive art candidate based on `art/united-states-v1` at `57e7985`. Original USA asset and production website are unchanged. This is a cosmetic inner-collectible study, not minted, hosted, signed, or on-chain. No funds or custody operations.

## Art contract and outcome
Approved primary reference: `C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-usa-flag-fireworks/united-states-flag-fireworks.png` (1072 × 976). Reference inspected before authoring. Replace all canyon, river and geological materials/ornaments with smooth flag-inspired red/ivory horizontal bands, navy white-star canton extending onto the lid, red feet and polished brass. Preserve wide family silhouette, hollow liner, pivots and staged mechanism. Hidden back/interior pattern is extrapolated; this is not a regulation 50-star flag replica. Original hasp proportions intentionally retained rather than matching the illustration's shorter clasp.

`united-states.glb` contains the actual flag model only. `united-states.blend` is the independently reopened editable packed source, including studio scene. `poster.png` is an actual Cycles render of this model, without fireworks; it is not the marketing illustration. `poster.jpg` is its compact offline fallback. `mechanism.blend` is the byte-preserved original construction base.

`united-states-flag-v2.html` is fully self-contained: bundled Three.js, model, maps and fallback. The strict entire-file budget is <5,000,000 bytes, enforced by build and packaging. Build-time dependencies do not load at runtime.

## Presentation fireworks
216 bounded 3D particles and 648 line-trail segments across three bursts, red/ivory/blue with restrained gold. Positions have real depth and change over time; not billboards, solid landscape, or part of the GLB/collectible. They rise with the open presentation to avoid hiding the lid. Depth test remains enabled; the lid naturally occludes some lower sparks. Reduced motion snaps mechanism endpoints and displays a static spark arrangement. Fireworks do not intercept controls.

Visual limitations: lightweight thin trails are sparser and less luminous than the approved cinematic illustration; no smoke or bloom. Small stars and fine hardware soften at mobile size. Source poster retains modest Cycles sampling grain. Flag motif/palette and wide chest identity match the direction, but the final reference comparison remains a partial visual match, not close illustration equivalence: the body canton wrapping/placement, smaller body stars, broader/flatter family silhouette and more pronounced lid gap differ. Three bounded corrections are exhausted. User approval of this candidate is not implied.

## Verification
- Actual Edge GLTFLoader: finite bounds, 13,324 triangles / 55 meshes, zero degenerate triangles. Decoded color variation 227; roughness variation 5 from glTF GREEN channel. No geological names/materials remain in exported scene.
- Independent Blender reopening: bidirectional evaluated source/export vertex error <=1.72e-7 (gate 1e-5). Three packed images. All inherited mechanism object's raw geometry, transforms and parentage unchanged against included base; material changes intentional.
- 81 sampled staged poses: zero moving/static or latch/lid BVH intersections except narrowly documented concentric bearings. Ten explicit hinge attachment pairs remain in contact. Interior downward ray hits floor at z=0.265. Sampling is not continuous engineering certification.
- Offline Edge desktop 1440×1080 and touch-emulated mobile 390×844: native Open/Close/Reset, drag/touch rotation, reset during observed intermediate progress, reduced motion, no overflow, no external HTTP(S) requests or console errors. Corrupt actual embedded GLB reaches poster fallback. JavaScript-disabled page displays real poster and explanatory message.
- Every firework phase sampled at 0.05-second intervals over a full cycle for default closed/open views: maximum projected absolute NDC <0.935 on mobile, <0.921 desktop (must be <1). Whole open model max <0.758. User-driven extreme zoom is intentionally not auto-fit.
- Actual NVIDIA RTX 4060 via Edge; mobile is viewport/touch emulation, not physical-device performance testing.

## Bounded corrections / evidence
Initial authored model passed source, parity and browser mechanism tests. Presentation correction 1 strengthened blue/trails and lifted open fireworks. Extended phase gate then exposed maximum-expansion mobile clipping (1.072 NDC); retained `extended-failure-initial.txt` and `extended-failure-framing.txt`. Correction 2 reduced burst radius/spread; unchanged strict gate passes. Correction 3 enlarged stars, broadened painted stripes and aligned the body UV height more closely to the reference; earlier fine-stripe model screenshots remain in `prior/`. All source/export/mechanism/browser gates were rerun after the final material pass. Three-pass limit reached; final screenshots reviewed visually. Test diagnostics and JSON live beside sources.

## Reproduction
Blender tested: 5.2.1. Node dependencies pinned in package-lock.json. Python requires Pillow, numpy, playwright (with installed Edge).

```sh
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
node tests.mjs
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_mechanism.py
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

Use the discovered Blender executable's full path if not on PATH. Regeneration overwrites manual edits; source scripts use their own folder and included base, not sibling originals. Package excludes node_modules, .blend1 and caches. `inventory.json` identifies exact payload bytes; ZIP readback checks all entries and required GLB/BLEND/HTML/source files. SHA-256 is integrity, not issuer authenticity. Folder-local Git attributes preserve exact bytes across Windows checkout.
