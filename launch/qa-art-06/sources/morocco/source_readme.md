# Morocco finish v6 — bounded visual candidate

Open `morocco-finish-v6.html` directly in a browser. It is self-contained/offline, with the actual-model poster and the same controls and fallback as approved v5. No mint, custody action, network dependency, deployment, or transaction occurs.

## Finish changes
- Body: original v5 image payloads and UV registration retained exactly. A neutral **0.90 linear-light multiplier** gives measured non-dark sRGB channel ratios **0.92836–0.95418**, with zero newly clipped channels. No new strata, recoloring, or noise.
- Only vertical wooden lid faces use the new warm-brown reference-extracted grain. The original central top, interior and rim materials remain unchanged. The source grain was rectified from the primary illustration, safely cropped away from metal, mirrored to repeat, and tone-normalized. This is illustration-derived grain, not a claimed cedar scan.
- Ceramic: one actual rosette patch from the primary was rectified and classified into emerald/ivory/near-black pigments. Its repeated atlas has mitered corner sampling. The first implementation kept tiny raised tessera and visibly fragmented the motif. The single permitted integrated correction replaced only those three ceramic mesh carriers with continuous thin panels. Existing tile beds, ridge, wood geometry, hardware, pivots and animation are retained.

## Visual result — partial, not new user approval
Same-camera v5/v6 screenshots and primary comparison are included. Body preservation and restrained darkening pass visual review. Vertical edges are visibly lighter and grained, but warmer/coarser than the original reference and stronger than the unchanged central top. The continuous ceramic carrier fixes the fragmented relief artifact, **but the final rendered motif still looks too pale/open, with weaker near-black contrast, less convincing angular interlocking, and imperfect corner resolution versus the marketing primary**. Technical/source correspondence is not visual equivalence. The agreed one correction was used; no further art iterations were made. Hardware and ridge differences from the primary are existing, intentionally untouched gaps.

## Executed verification
- Offline Edge desktop and 390×844 mobile-touch emulation: drag/touch rotation, native open/close, reset during motion, reduced motion, zero external requests/unhandled errors/horizontal overflow.
- Actual corrupted GLB parser input and JavaScript-disabled poster fallback, desktop/mobile.
- Runtime full GLB: 18,782 triangles, 63 render meshes, zero nonfinite vertices/degenerate triangles. Mobile is desktop-GPU emulation, not a physical-phone performance claim.
- Independent source reopening: 81 motion/contact/attachment poses, zero unexpected collisions; original narrow bearing exceptions unchanged; hollow interior ray verified.
- Source/export geometry parity maximum distance: 0.0000001712013073529306 units.
- 59 original mesh geometries retained; only the three named ceramic carriers changed. All node parents/transforms and original image payloads exact; body UVs and non-target attributes exact. Viewer bundle, controls, camera/light and motion source bytes exact.
- The photographic grain's single-pixel derivative test initially failed because pores contribute high-frequency variation. The retained failure is in `pre-correction`; the final directional test measures the explicit three-pixel grain scale, while independently checking within-row variation (not uniform stripes). These are post-implementation regression checks, not test-first development.
- Original v5 files are hash-readback checked as immutable.

## Rebuild
Python dependencies: numpy, Pillow, playwright. Blender used: 5.2.1 LTS. Node dependencies are pinned in `package.json`; `npm install` in this directory provides a portable local toolchain. The build also supports the existing sibling `iceland-pilot/node_modules` during local work. The included `baseline/` is the approved packed v5 source and GLB; no external art source is required.

1. `python materials.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python finalize_glb.py`
4. `python build.py`
5. `python verify_finish.py`, `python verify_browser.py`, `python verify_extended.py`, `python verify_fallbacks.py`
6. Run `verify_source.py`, `verify_parity.py`, and `verify_source_preservation.py` through Blender with the same flags.

`review.py` and immutable-v5 verification use the original sibling v5 directory for comparison; outside this repository that optional history comparison needs the v5 directory. The final source/GLB and new maps remain self-contained. Regeneration overwrites v6 generated output, not v5.

The source ZIP includes an explicit required-file inventory, scripts, maps, reference provenance, baseline, final HTML/GLB/packed blend, actual-model poster and test evidence. Backups, node_modules, caches, and the bulky failed candidate HTML/GLB are excluded; the failed candidate stays preserved locally in `pre-correction`.
