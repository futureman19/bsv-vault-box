# Indian Ocean v1 — Atoll & Abyss

Open `indian-ocean-v1.html` directly in Edge/Chrome. **HTML 2,587,892 bytes; GLB 1,353,500 bytes.** Everything needed at runtime is embedded. Drag/touch to rotate, open/close, reset, and reduced motion work offline. This is local collectible art, not minted, hosted, signed or a custody-state transition.

## Design and provenance
The pre-model `design-brief.md` cites UNESCO's Indian Ocean Aldabra raised-atoll description. Four separate irregular ivory limestone arcs encircle a low turquoise inlay; deep-blue flowing mineral maps cover the hollow chest body. Pale limestone feet and satin brass fittings complete the family silhouette. Geometry and maps are script-authored, not scans, harvested coral, hand sculpture or a geographic replica. No third-party photographs are embedded.

The packed `mechanism.blend`, viewer and verification lineage come from repository `preview/japan-cedar-v1/` at base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`. Japan's cedar, joints, tree and moss are not reused. Shared kit and earlier previews are untouched. Three.js licensing is retained in `THREE-LICENSE.txt`.

## Verified on the delivered model
- Actual GLTFLoader: **15,016 triangles, 60 meshes, 6 materials**, zero nonfinite vertices and degenerate triangles. Base-color, roughness (green channel) and normal maps have measured nonzero variation.
- Saved source independently reopened; **21 moving and 39 static meshes, 81 opening poses, zero unintended sampled surface intersections**. Hinge attachments are checked at ten named contact pairs. Explicit original bearing contacts alone are exempt. Hollow floor ray reaches z=0.2650000155.
- Source/export nearest-vertex error in both directions: **1.712013073529306e-7**, below 1e-5. Four packed images preserved in source.
- Source theme checks prove four separate reef meshes, exposed center and four water passes, elevated crowns, lid ownership and original pivot matrices. Detaching one reef in-memory makes the ancestry gate fail (`ornament detached`), then restoring it passes. This negative control was added after implementation, not claimed as test-first development.
- Motion unit tests: 80-degree latch release before 105-degree lid opening; clamped endpoints and malformed/empty/nonfinite asset rejection, **2 tests passed**.
- Desktop 1440×1080 and touch-emulated mobile 390×844 over offline `file://`: native controls, mouse/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, zero external HTTP(S) requests or successful-path errors. Full-open maximum projected coordinate 0.930594 < 1.
- Actual corrupted GLB bytes reach the parser and activate the poster fallback. No-JS poster tested separately. Source-rendered poster has nonblank pixels. `browser-check.json`, `extended-check.json`, and screenshots retain actual outcomes.
- `inventory.json` records exact byte counts and SHA-256s; `delivery-check.json` proves required artifact presence and full ZIP readback. Folder-local `* -text` preserves exact Git bytes.

## Visual verdict and limits
The actual desktop/mobile model reads as a stylized ivory-atoll ocean chest, not photorealism. The lagoon is an opaque shallow inlay, not transparent simulated water. Its four channels pass geometry checks but are not equally obvious in the default small view. Lighting makes the blue body brighter and the lid paler than the dark target palette. Feet are intentionally irregular pale rock. The inherited hinge connection is numerically attached but can look floating from the front-open perspective. Poster is an actual 24-sample source render with some grain; no AI image replaces it. No physical-phone performance, continuous collision proof, engineering, exact geology or photographic fidelity is claimed.

One bounded visual correction widened the reef gaps and separated the lid enamel from body marbling; the earlier mobile view is preserved under `initial/`. Source/material inspection and screenshot review are separate from user art approval; per-asset human review was explicitly waived for this collection batch.

## Failures and fixes
The optional Codex lane failed before implementation with HTTP 401 token-refresh errors; it produced no accepted changes. Hermes implemented and tested directly without touching credentials. Its raw failure log is retained.
The required main-checkout dependency directory existed but was empty. First build genuinely failed with `Cannot find module .../iceland-pilot/node_modules/esbuild/bin/esbuild`. Installing the existing pinned package dependencies inside this new preview folder fixed the build; no sibling package or dependency upgrade was made. `dependency-install.txt` retains install output. No collision or geometric acceptance failure occurred. Negative controls are distinguished from these incidental failures.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/playwright, installed Edge, Node.js and the pinned npm dependencies. From this folder:

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with those same flags on `verify_source.py`, `verify_parity.py`, `test_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Build finds local dependencies before the historical sibling path. Source generation uses only this folder and overwrites generated assets: preserve manual edits separately. The source archive omits node_modules, caches and Blender backups. Packaging is entirely in-folder. Inventory excludes itself, ZIP and delivery-check to avoid recursive hashing. No deployment, blockchain/node/keys/funds/mint/broadcast, VPS, external messaging or merge was performed. Branch backup is authorized separately.
