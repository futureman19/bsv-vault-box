# Arctic Ocean v1 — Floes & Blue Leads

Open `arctic-ocean-v1.html` directly in Edge/Chrome. Complete offline viewer: **2,647,487 bytes**; embedded GLB **1,402,140 bytes**. Drag/touch to rotate, Open/Close lid and Reset view. Reduced-motion preference supported. Editable `arctic.blend`, standalone `arctic.glb`, generated maps, authoring scripts and source-render posters are included.

## Verified technical gates
- Saved Blender source reopened: 39 moving meshes and 39 static meshes; **81 poses**, zero unintended surface intersections. Latch releases 80 degrees before lid opens 105 degrees. Only enumerated concentric bearing contacts excluded. Ten physical hinge attachment pairs and hollow floor ray at z=0.265 pass. Sampled surface evidence, not continuous collision or engineering certification.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, under 1e-5. Three packed maps. Pivots exactly match separately reopened mechanism baseline.
- Actual Three GLTFLoader: 13,600 triangles, 101 mesh primitives, seven materials; zero nonfinite vertices or degenerate triangles. Multi-material floes split into runtime primitives, hence different source mesh count.
- Twelve floes, two contained turquoise pond overlays, nine low ridge blocks (maximum z=2.3911252). All lid-owned; a real temporary detachment is rejected by ancestry predicate. Pond vertices tested against actual floe polygon edges.
- Three 512x512 maps decoded: base-color range 55, roughness GREEN range 60, normal red range 35. Independently generated textures, not scans or copied research imagery.
- Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: drag, native open/close, reset during movement, reduced motion, no overflow, no external HTTP requests or console errors. Full-open maximum absolute projected NDC 0.892365. Actual corrupt GLB reaches the parser and triggers poster fallback; no-JS poster also checked. RTX 4060/Edge, **not physical-phone performance**.
- Motion tests reject missing lid, nonfinite bounds, empty geometry. Theme negative control detaches a floe. Corrupt-GLB browser case tests actual loader failure. Checks are assertions, not unconditional PASS records.
- Exact-byte inventory and source archive readback in `delivery-check.json`; directory-local Git attributes preserve bytes.

## Visual verdict and limits
Actual source poster and mobile browser screenshot visually inspected. Readable blue ocean body, pale separate floes and warm brass; no evident framing/mesh break. Intentionally stylized enamel/porcelain, **not transparent ice, photorealism, geographic reconstruction or user-approved art**. Floes remain quadrilateral/tile-like; rear ridge blocks can read architectural. Pond overlays are geometrically contained but not clearly distinguishable as enclosed ponds at normal mobile size. The busy body tracery competes with small lid detail. Poster retains mild sample noise. These are disclosed v1 visual limitations, not evidence of photoreal equivalence. Source and runtime lighting differ.

## Failures and fixes
The inherited dependency directory lacked `esbuild/bin/esbuild`, so the first build failed with MODULE_NOT_FOUND. Installed the pinned package dependencies **only in this new folder**; build then passed. Browser verification prematurely launched after that failed build and genuinely failed ERR_FILE_NOT_FOUND; raw trace is preserved in `initial/browser-before-build.txt`. Re-ran after a confirmed successful build; all assertions passed. No geometry gates were relaxed or collision exclusions added.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright and installed Edge; Node with package.json pinned Three/esbuild dependencies. `npm ci` inside this directory, then:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Blender with `verify_theme.py`, `verify_parity.py`, `verify_source.py` (same flags).
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

`setup.py` is the one-time adaptation record and depends on the read-only sibling Japan pilot; **not needed for regeneration**. It can overwrite viewer/scripts with baseline copies, so do not rerun it for ordinary rebuilding. `author.py` is self-contained with included mechanism.blend and maps. Regeneration overwrites outputs; retain manual edits separately. node_modules, caches and Blender backup files excluded from source archive and Git.

## Provenance / scope
Research citations and pre-model contract: `design-brief.md`. Mechanism, viewer and harness adapted from Japan Cedar v1 on local base ff5d78f1e0d486af5c882c184fc08049996ebdc8; shared vault kit untouched. Script-authored Blender geometry and procedural maps, not hand sculpture. Three.js MIT license included. No external reference images embedded.

Local art only: cosmetic lid action changes no seal/custody state. No blockchain node, keys, broadcasts, minting, uploads, production integration or merge. Branch backup is the only remote publication authorized here. Final collection integration/review is a separate dependent card; per-asset human review waived.
