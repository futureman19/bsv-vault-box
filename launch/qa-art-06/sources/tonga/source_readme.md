# Tonga v1 / Ngatu & Ochre

Open `tonga-v1.html` directly in Edge/Chrome: a self-contained offline collectible preview. **HTML 2,962,887 bytes; GLB 1,631,436 bytes.** Drag/touch rotation, Open/Close lid, Reset view, reduced motion and actual-model poster fallback. No wallet, chain operation, mint, deployment or custody-state change.

## Design and provenance
The pre-model `design-brief.md` cites Te Papa research on Tongan ngatu, hiapo barkcloth, kupesi rubbing and collective decoration. All maps and geometry are procedural originals. The invented diamond composition is not a reproduction of a traditional kupesi, cultural endorsement or museum replica. No source photographs were copied. Six open-centered diamond outlines are actual shallow raised geometry attached to the moving lid, with a cream fibrous inset and brown patterned body panels. Brass, timber construction and mechanism are collection-family extrapolations.

The included `mechanism.blend` and viewer/test lineage come from the repository Japan pilot; source/existing previews and shared vault kit were not modified. Three.js 0.180.0 is MIT (`THREE-LICENSE.txt`); esbuild 0.25.11 is build-only.

## Verified gates
- Saved `.blend` independently reopened. All 27 moving and 47 static meshes included in **81 sampled poses**, no unintended surface intersections. Narrow named bearing contacts only are exempt. Ten actual intersecting hinge attachment pairs; hollow interior floor ray z=0.2650000155. Sampling is not continuous mechanical certification.
- Original pivot matrices match exactly; staged 80-degree latch release precedes 105-degree lid opening. Motion tests include rejected malformed/nonfinite assets.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed 512px maps, independently decoded runtime base-color ranges 25/124 and roughness green-channel range 57.
- Actual GLTFLoader: **74 meshes, 15,960 triangles, 6 materials**, zero nonfinite vertices and degenerate triangles. Six lid diamonds and their dimensions/ancestry tested; deliberate detached-diamond negative control rejected by the same gate.
- Offline `file://` Edge desktop 1440x1080 and 390x844 touch emulation: drag, native buttons, open/close, interrupted reset, reduced motion, no overflow, external requests or JS errors. Full-open projection max absolute NDC 0.892365. Actual corrupt GLB triggers the parser error and poster fallback; no-JS poster tested separately.
- Source poster is a real Cycles render (24 samples, two render threads, no denoising); nonempty pixels checked. Exact bytes/hashes and ZIP contents read back by packaging gate. Local folder `.gitattributes` preserves byte hashes through Git.

## Honest visual limits
Source poster, desktop-open and mobile-closed screenshots were inspected. Wide silhouette, six lid diamonds and geometric panels are readable, with no obvious detached decoration or major collision. Shallow relief reads more like an outline at default mobile size; microfibers are subtle. The inherited dark lid seam can make the closed box look slightly ajar, with pale rim edges visible below it. Brass is simplified and the un-denoised source poster has light sampling grain. These are disclosed visual limitations, not photoreal equivalence or human art approval. Mobile is emulation on RTX 4060, not a physical-phone or FPS test. Per-asset human review was explicitly waived for this batch.

## Actual failure and fix
Initial build failed with MODULE_NOT_FOUND because the provided sibling node_modules directory was empty. `build-initial-failure.txt` preserves it. Installed the exact declared Three/esbuild dependencies locally in this new folder; rebuild and all final gates passed without changing the size or validity thresholds. An extended browser check was also launched before the HTML existed and exited 1; its redirected log was overwritten by the final successful run (not preserved). Final checks were run only after the build completed. Detached-ornament testing is a deliberate post-implementation negative control, not a historical art defect.

## Reproduce
From this directory: `npm ci --no-audit --no-fund`, `python maps.py`, Blender 5.2.1 `--background --factory-startup --python-exit-code 1 --python author.py`, then `python build.py`. Run Blender with `verify_source.py`, `verify_parity.py`, and `verify_theme.py`; `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.
Python requires numpy/Pillow/Playwright and installed Edge. `setup.py` records initial adaptation from sibling Japan; do not rerun it on a final edited artifact. Final authoring uses the included mechanism and does not require the sibling. Build uses local dependencies first, then sibling fallback. Regeneration overwrites model/poster; refresh evidence and inventory after rebuilding. Dependencies and .blend1 backups are not shipped. Source ZIP contains source, model, viewer, maps, screenshots and checks; inventory and delivery envelopes exclude themselves to avoid recursive hashes.

Branch backup only: `art/tonga-v1`; no merge, public hosting or production edit. Next: the pre-created final collection integration card assembles this with the remaining assets.
