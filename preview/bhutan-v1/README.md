# Bhutan v1 — Painted Timber & Mountain Cornice

Open **bhutan-v1.html** directly in Edge/Chrome. The complete model, runtime, procedural textures and actual-source poster are embedded. Drag/touch rotates, Open/Close articulates the lid, Reset cancels motion, and reduced-motion preference snaps the animation.

- HTML: **3,652,860 bytes** (strictly below 5,000,000).
- GLB: **2,177,608 bytes**.
- Actual-loader geometry: **28,076 triangles, 146 meshes, 8 materials**; no nonfinite vertices or degenerate triangles.
- Editable source: `bhutan.blend`; mechanical baseline: `mechanism.blend`. All four 256px authored maps are packed and also provided separately.
- `poster.png` / `poster.jpg` are actual Blender renders, not AI promotional illustrations. Desktop/mobile PNGs are actual offline browser captures.

## Design and limits

The pre-model `design-brief.md` cites Smithsonian and Global InCH descriptions of Bhutanese timber architecture, painted cornices and earth/stone construction. This is an original stylized interpretation, not a replica of a named building, authentic craft object, sacred symbol or named mountain. Pale plaster-like panels, red painted framing, dark timber, teal/ochre border and an asymmetric mountain ornament distinguish it from the reused Japan mechanism. No Japanese tree or moss artwork is retained.

Visual inspection of actual source and browser images found the theme coherent and the full silhouette contained on desktop/mobile. The red reads more muted brick-red than deep oxblood under studio lighting; the pale body reads plaster rather than raw rammed earth. The mountain is a visibly faceted applied miniature on a rectangular base, not photoreal terrain. Its relief is within the declared 0.6-unit height cap but can read tall. The dark seam and sparse exposed hinge leaves can make the open lid appear visually detached; independent geometric attachment checks pass. The stone-like feet and long brass clasp are family extrapolations, not historical joinery claims. There is no original Bhutan marketing image to match. Human per-asset review was explicitly waived, not performed.

## Verification actually exercised

- Reopened saved source: hollow floor ray z=0.2650000155; ten hinge attachment pairs intersect as intended. Exact pivot matrices match the trimmed mechanism.
- **81 sampled poses**, all **91 moving** and **55 static** meshes, zero unintended intersections. Includes every mountain, cornice and painted border mesh plus releasing latch against lid meshes. Only inherited named mating hinge and latch bearings are exempt. This is sampled surface evidence, not continuous collision, containment, manufacturing or structural certification.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. This proves sampled mesh vertex parity, not byte-identical re-export or exhaustive shader equivalence.
- Saved-source theme assertions: dimensions, pigment factors, ridge bounds, expected feature counts, packed images, complete collision-parent coverage and lid ancestry. Real post-implementation negative control detaches the mountain **in memory**, causing exit 1 with `AssertionError: ('lid ancestry', 'Mountain /')`. The unmodified source passes. This is a deliberate regression control, not a spontaneous implementation failure or test-first claim.
- File:// Edge desktop 1440x1080 and touch-emulated mobile 390x844: real GLTFLoader, native open/close, mouse/touch drag, interrupted reset, reduced motion, no overflow, no external HTTP requests or unexpected errors. Full-open maximum absolute projected NDC approximately 0.892365.
- Corrupt embedded GLB reaches the real parser, shows poster and disables controls; the caught parser error is expected. No-JS poster independently verified.
- GPU reported NVIDIA RTX 4060 via ANGLE/D3D11. Mobile is viewport/touch emulation, **not physical-phone performance**. No FPS or broad browser compatibility claim.
- `acceptance-check.json`, raw output logs, source/parity/browser/extended/theme checks retain results. `inventory.json` gives exact SHA-256/bytes; `delivery-check.json` verifies ZIP membership and entry bytes. Inventory and delivery envelopes exclude themselves to avoid recursive hashes.

## Reproduce

Build environment: Blender 5.2.1; Python with numpy, Pillow and Playwright; installed Edge; Node/esbuild/Three as declared in package.json. Build resolves local node_modules first, then read-only sibling `preview/iceland-pilot/node_modules`. Install dependencies locally for an extracted archive. Runtime HTML has no such dependency. `BLENDER` can override the Windows Blender path in the verification runner.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python verify_all.py` (build, motion, source, parity, theme, deliberate negative, browser, extended)
4. `python package_delivery.py`

Regeneration overwrites source, model and poster. Preserve manual changes in a separate copy. Source geometry is script-authored, not hand-sculpted, scanned or photogrammetry. Viewer, mechanics and test lineage derive from the repository Japan/Iceland pilots at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8; Three.js license included. No third-party reference imagery is embedded. Optional Codex implementation lane failed authentication and contributed no code; Hermes implemented and verified directly.

## Scope

Local collectible art only; reversible lid movement is not opening an on-chain seal. No wallet, keys, blockchain nodes, minting, broadcasts, chain queries, public hosting, VPS or production changes. Only `preview/bhutan-v1/` is added. Branch backup is authorized; no merge. Collection direction is 201 equally one-of-one designs. This pilot does not assert on-chain storage, custody acceptance or public availability.
