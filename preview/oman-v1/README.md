# Oman v1 — Aflaj & Limestone

Open `oman-v1.html` locally in Edge/Chrome. Entire runtime, model, maps and actual-source poster are embedded. HTML **2,428,551 bytes**; GLB **1,241,480 bytes**. No server, network, wallet or installation required for viewing. Cosmetic opening does not change custody.

## Design and visual limits
Research-backed brief was written before authoring; UNESCO references are in `design-brief.md`. This is an invented six-bed irrigation-garden miniature, not a scale reconstruction of any named falaj. Pale mottled stone, olive garden insets, a turquoise central channel and bronze fittings. All 15 terrace/channel parts move with the lid. Procedural Blender geometry/maps, not scans or human hand sculpture. No source photographs used.

Actual source render and mobile screenshot were visually inspected. Six beds are visible and no obvious floating/missing geometry was observed. The channel is narrow and understated at mobile size; its entire route is not visually traceable from the default angle, though seven vertical source rays verify exposure along it. Green beds are flat stylized insets, not modeled crops. Stone is clean/simple; source poster has residual sampling noise. No photorealism, traditional craft fidelity or geographic accuracy claim.

## Verified evidence
- `source-check.json`: independently reopened packed source, hollow floor z=0.2650000155, ten hinge attachment pairs; all 31 moving / 39 static meshes included in **81 poses**, zero unintended surface intersections. Original bearing exclusions only. This is sampled surface clearance, not continuous/mechanical certification.
- `parity-check.json`: source/export bidirectional maximum nearest-vertex error **1.712013073529306e-7**, under 1e-5; three packed maps.
- `theme-check.json`: six stepped garden beds, 15 lid-owned ornaments, bounds, seven exposed water rays, original pivot locations compared independently with mechanism. A deliberately detached ornament was rejected and then restored; a post-implementation negative control, not TDD.
- `browser-check.json`: actual GLTFLoader **16,672 triangles / 70 meshes / 6 materials**, zero nonfinite vertices or degenerate triangles. Offline file:// desktop 1440×1080 and touch-emulated mobile 390×844: drag, native open/close, interrupted reset, reduced motion, no overflow/errors/external requests. Maximum full-open projected coordinate 0.92330 (<1). Genuine corrupt-GLB parser fallback passed.
- `extended-check.json`: runtime ornament ownership, decoded texture variations (roughness green channel), copy/accessibility label and no-JS poster. Source-derived poster is embedded, not an AI promotional substitute.
- `motion-output.txt`: two motion/invalid-asset tests pass. Tests explicitly reject missing lid, empty geometry and nonfinite bounds.
- `delivery-check.json` and `inventory.json`: strict HTML budget, source/poster validity, archive readback and exact SHA-256/byte inventory. Folder-local attributes preserve bytes in Git.

All checks are executable assertions capable of failing. No unexpected acceptance failure occurred in this run; deliberate negative controls were exercised. Recovery corrected a literal truncated CSS fragment inherited from the old template before first build (not a claimed failing test). Shared pilot node_modules existed without esbuild; installed the same exact pinned build dependencies inside this folder, leaving other previews untouched.

Mobile tests use desktop RTX 4060 with touch emulation, not a physical phone or FPS benchmark. Visual inspection is not human approval; per-asset review is waived for this batch.

## Files and reproduction
`oman.blend` is named editable packed source; `oman.glb` portable export; `mechanism.blend` trimmed inherited mechanics from the Japan pilot; `poster.png/jpg` actual Blender output; screenshots actual browser output. Source ZIP includes scripts/maps/evidence and excludes node_modules, caches and blend backups.

Build dependencies: Blender 5.2.1, Python with numpy/Pillow/playwright, installed Edge, Node, pinned Three 0.180.0 and esbuild 0.25.11 (`npm ci` in this directory). Three MIT license included. `setup.py` documents initial adaptation from sibling Japan files; already-adapted delivered scripts are self-contained and do not require rerunning setup.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender likewise with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node --test --test-reporter=tap tests.mjs`
5. `python build.py`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Authoring overwrites generated source/export/poster; preserve manual edits separately. Repackage after regenerating evidence. The brief and new scripts are Oman-specific; mechanics and browser test lineage are inherited with scoped adaptation. Only `preview/oman-v1/` was added. No blockchain node, keys, chain queries, mint, broadcasts, production changes or deployment. Branch backup only; final collection integration is separate.
