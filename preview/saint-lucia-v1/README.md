# Saint Lucia / Pitons & Caribbean — v1

Open **saint-lucia-v1.html** directly in Edge/Chrome. The complete 3D model, Three runtime, maps and actual source-render poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. No server or network required.

## Delivered
- Offline HTML: **2,955,177 bytes** (<5,000,000).
- GLB: **1,619,332 bytes**; actual loader reports 18,648 triangles, 60 runtime meshes, 6 materials, zero nonfinite vertices/degenerate triangles.
- `saint-lucia.blend`: editable packed Blender source; `mechanism.blend`: inherited trimmed family mechanism.
- Three procedural 256x256 maps, scripts, actual source poster, desktop/mobile closed/open/rear captures, machine-readable acceptance, byte inventory and source ZIP.
- Theme: two forest-clad Piton-inspired spires on an irregular coastal ridge over a teal lid, gray-green volcanic-stone-inspired body and warm brass fittings. Research and frozen pre-model contract are in `design-brief.md`.

## Verified versus claimed
Saved source independently reopened: hollow interior floor ray z=0.2650000155; ten hinge attachment pairs; **81 motion samples across all 19 moving and 39 static meshes**, no unintended intersections. Latch-vs-lid also tested, with only explicit mating-bearing exemptions. Staged 80-degree release then 105-degree opening; exact inherited pivot transforms independently compared. This is sampled surface testing, not a continuous collision/manufacturing certification.

Source/export nearest-vertex comparison threshold 1e-5; exact observed errors in `parity-check.json`. Runtime checks decode actual map images (roughness green channel), check lid ancestry including multi-material GLTFLoader groups, and enforce finite/nonnull geometry. The deliberately detached peak is rejected by the theme oracle; invalid/empty assets are rejected by motion tests, and genuinely corrupt GLB bytes reach the real parser and trigger the poster fallback.

Offline Edge `file://`: 1440x1080 desktop and 390x844 mobile touch emulation, native buttons/drag, full opening/closing, interrupted reset, reduced motion, no horizontal overflow, no external HTTP(S) requests, no runtime errors. No-JS poster tested. Maximum open projected coordinate approximately .892365, inside viewport. RTX 4060 host; **not physical-phone performance testing**.

## Visual acceptance and limits
Final actual mobile closed and desktop open screenshots were visually inspected. Two separated green peaks, organic rounded/irregular shoreline, teal surround, wide gray stone/brass chest and full open framing pass the stylized brief. The initial rectangular terrain pad was rejected in visual review and rebuilt as an irregular radial coastline; initial screenshots and technical results are preserved in `initial/`. The final lid terrain travels with the lid; front-open naturally hides it, so see `desktop-open-rear.png` too.

The surfaces are procedural and noticeably stylized: clean pale stone under strong lighting, sage/light forest slopes rather than dense individual trees, low-poly fluted mountain forms, simplified brass. This is **not photorealism, a surveyed Pitons model, a stone scan, historical craft reproduction or exact geographic scale**. Gray-green albedo targets are not rendered color calibration. Real Cycles poster has some sampling grain. Unseen interior and hardware are collection inventions.

## Real failure and fix
`initial-build-missing-deps.txt` preserves the first failed build: both the worktree and main checkout's advertised `iceland-pilot/node_modules` directories were empty. Rather than modifying other previews, installed the pinned Three 0.180.0/esbuild 0.25.11 dependencies **only in this new directory**. Final build and browser gates pass; `package-lock.json` records those dependencies. No collision/geometry gates were relaxed. Reduced-motion checks use a bounded observed-state wait rather than a fixed sleep.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node/npm for build tooling only (not a blockchain node).

1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
7. `python package_delivery.py` (exact inventory plus ZIP readback).

The one-time `setup.py` documents helper/runtime lineage and needs sibling Japan files; it is NOT required to regenerate the supplied standalone source. Re-running it would overwrite localized scripts; use the steps above instead. Authoring overwrites generated art: preserve manual edits separately. The offline HTML requires none of these build dependencies. Source archive excludes node_modules, cache, .blend1 backups. Folder-local `.gitattributes` preserves inventoried bytes through Git; staged blobs are compared before commit.

## Scope
This is an inner collectible **art pilot**, not the outer custody container. Cosmetic lid motion does not break an on-chain seal. No minting, keys, wallets, node startup, chain queries, VPS, sales, deployments or production edits. Branch backup only, no merge. Nothing is hosted or stored on-chain. Proposed collection: 201 equally one-of-one designs; no scarcity or custody claim from this file. User waived individual human review until full-set integration.

Lineage: Japan mechanism/runtime and Iceland motion tests from local base commit ff5d78f; Three MIT license included. Research provides factual inspiration only; no third-party photos/textures are embedded.
