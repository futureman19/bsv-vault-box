# Somalia v1 — Merka Dunes & Indian Ocean

Open **somalia-v1.html** directly in Edge/Chrome. All runtime assets are embedded. Drag/touch to rotate, Open/Close lid, Reset; reduced-motion preference supported. Local art only: not minted, deployed, hosted, signed or chain-verified.

## Delivery
- HTML **2,398,644 bytes**, strictly below 5,000,000.
- GLB **1,192,284 bytes**, with portable generated maps.
- `somalia.blend`: packed editable source; `mechanism.blend`: included inherited mechanical baseline.
- `poster.png` / `poster.jpg`: actual Blender source render, not AI artwork.
- Desktop/mobile closed/open, corrupt-model fallback and no-JS screenshots; scripts, maps, JSON evidence and source ZIP included.

## Design and visual limits
The pre-model brief cites the Merka red dune complex and Somalia's Indian Ocean coastal sediments. Three real raised, tapered rust-colored ridges sit above a teal-blue inset; pale mottled stone walls and an intentional teal seam replace Japan's cedar. The straight pale shore accent is an invented graphic abstraction, not a mapped coastline. Geometry/maps are procedural, not scans, human hand-sculpture or traditional-craft replicas.

Actual mobile visual inspection found all three ridges visible, readable primary controls and no clipping. Source render shows sampling noise and soft stone mottling; dunes read as smooth relief ribbons rather than realistic wind-eroded sand. The deliberately colored seam can look like a lid gap. Open-view image inspection questioned apparent hinge/latch separation; the independent geometric check establishes ten intersecting mount attachment pairs and preserved baseline pivots, but this does not claim engineering-grade or visually seamless hardware. Secondary mobile text is small. No supplied/approved concept image exists for this asset, and no photoreal or geographical equivalence is claimed. Human review is waived for this v1 batch by task directive.

## Verification actually run
- Source independently reopened: hollow floor ray z=0.2650000155; 21 moving and 39 static meshes; **81 motion samples, zero unintended intersections**. Every moving ornament included, plus latch-versus-lid checks. Only inherited named coaxial bearing contacts exempt. This is sampled surface intersection, not continuous solid-volume collision certification.
- Ten hinge/body/lid attachment pairs verified; baseline lid/latch matrices independently equal within 1e-7.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5; three packed images.
- Actual Three GLTFLoader: **17,804 triangles / 60 meshes / 6 materials**, zero nonfinite vertices or degenerate triangles.
- Theme tests: exactly three lid-parented ridges, measured bounds/heights, ocean and shore lid ancestry, no old cedar/moss objects. A deliberately renamed ridge produces `Exactly three dune ridges required`; restoring it passes. This is a postimplementation negative control, not test-first evidence. No accidental art/check failure occurred in this run.
- Portable 256px maps: limestone color range 70; roughness GREEN-channel range 98; dune color range 60. Actual source poster nonblank check.
- Offline `file://` Edge desktop and 390×844 touch-emulated mobile: native open/close, pointer/touch rotation, interrupted reset, reduced motion, no overflow, zero HTTP requests and JS errors. Full-open max absolute NDC 0.91565. Real corrupt embedded GLB invokes parser error and poster fallback; no-JS poster passes.
- Motion unit tests run against this directory's actual `motion.mjs`; raw output retained.
- SHA-256 inventory and ZIP readback in `delivery-check.json`; payload bytes preserved by local `.gitattributes`.

Mobile tests use desktop RTX 4060 emulation, not a physical phone. No performance/FPS claim. Tests prove stated bounded properties, not aesthetic approval or production readiness.

## Reproduction
Blender 5.2.1; Python with Pillow/numpy/playwright and installed Edge; Node with pinned Three 0.180.0 / esbuild 0.25.11. The provided shared node_modules directory had no actual compiler; dependencies were installed only in this new folder. They are build-only, ignored and excluded from ZIP.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Same Blender command for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

`author.py` is self-contained with the included mechanism. `make_author.py` records one-time adaptation from sibling Japan authoring code and is not needed for rebuilding; that development helper requires the repository. Author regeneration overwrites source/GLB/poster. Three runtime license included. Research links provide factual inspiration only; no third-party imagery is embedded. Prior previews and shared vault kit remain unchanged. Branch backup only; integration belongs to the final collection card.
