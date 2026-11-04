# Indonesia v1 — Wax & Copper

Open `indonesia-v1.html` directly in Edge/Chrome: all runtime code, GLB, textures and the actual-model poster are embedded. **HTML 2,799,626 bytes; GLB 1,486,092 bytes.** No server or network needed. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion supported.

## Design
A stylized Indonesian batik craft homage: indigo/ivory procedural resist loops and dots, with five raised copper four-petal ornaments. See the pre-model `design-brief.md` for UNESCO research and measurable design targets. Motifs are newly invented, not a named traditional pattern, artisan-made textile, sacred symbol, or comprehensive representation of Indonesia. Copper openwork evokes stamping material, not a usable batik cap.

The inherited wide box, brass clasp, medallion, ring and rear hinges are collection-family inventions. Pattern registration resets between panels; the blue renders lighter under studio illumination. The seam is pronounced and the clasp remains large. Small copper loops are less legible at mobile size than in source close viewing. Render sampling noise and stylized smooth fittings remain. No photoreal or historical-replica claim.

## Verified
- Blender 5.2.1 saved source reopened independently; hollow interior floor ray Z 0.2650000155 and ten physical hinge attachment pairs.
- 81 staged motion samples: 36 moving and 39 static meshes, including all ornaments; no unintended sampled intersections. Only named mating hinge/latch bearings excluded. This is sampled surface collision evidence, not continuous/manufacturing proof.
- Exact baseline pivot matrices; 80-degree latch release before 105-degree lid opening.
- Source/export maximum nearest-vertex error 1.712013073529306e-7 (<1e-5); three packed maps.
- Twenty petals on five lid-owned rosettes, physical bounds, gap-to-solid-lid ray and palette variation. Deliberately detached parent rejected by the actual feature gate; this post-implementation negative control is not test-first evidence. No accidental art-gate failure occurred.
- Actual GLTFLoader finite/degenerate geometry checks and decoded map variation, including correct green-channel roughness.
- Offline file:// desktop and 390x844 touch-emulated mobile: native controls, drag, interrupted reset, reduced motion, full-open projection <1, no overflow, no HTTP requests or runtime errors. Actual corrupted GLB reaches parser and shows poster; JavaScript-disabled poster tested. Mobile emulation is not physical-phone testing.
- Source poster and final mobile render visually inspected: complete framing and visible indigo/ivory identity. Counts and tests do not establish artisan fidelity or public art approval.
- SHA-256 inventory, explicit required artifact set, ZIP byte readback and staged Git blob comparison. Exact delivery bytes preserved with directory-local `.gitattributes`.

## Files / reproduce
`indonesia.blend` is editable packed source; `mechanism.blend` is the included trimmed baseline from Japan v1. `indonesia.glb` is portable geometry. `poster.png` is the real source render, not AI promotion. Browser screenshots and JSON checks are actual execution evidence. `indonesia-v1-source.zip` contains source, generated maps, viewer and evidence, excluding dependencies/backups.

From this folder: `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py`, `verify_pivots.py`; `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

Build prerequisites: Blender 5.2.1, Python Pillow/numpy/playwright, installed Edge, Node with package.json dependencies (`npm ci --ignore-scripts --no-audit --no-fund`). The prescribed shared node_modules target existed but contained no compiler; identical pinned dependencies were installed in this folder only. Runtime has no such dependencies. Regeneration overwrites generated source/render/GLB, so preserve manual edits separately. Repackage after rebuilding to update hashes.

Three.js MIT license included. No research photographs copied. No shared art kit or prior previews modified. Local art asset only: not minted, deployed, signed, on-chain, hosted or a custody proof. No chain queries, keys, nodes or VPS operations. Branch backup only; integration is a separate card. Per-asset human review was explicitly waived for this batch.
