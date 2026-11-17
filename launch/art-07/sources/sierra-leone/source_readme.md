# Sierra Leone v1 — Gola Canopy

Open **sierra-leone-v1.html** directly in Edge/Chrome. Self-contained offline viewer: **3,312,325 bytes**; embedded GLB: **1,895,668 bytes**. Drag/touch rotates, Open/Close articulates the box, Reset restores the view. Reduced motion, corrupt-model poster and no-JavaScript poster are tested. No network/runtime downloads, blockchain operations or deployment.

## Design and provenance
The research-backed brief preceded authoring and survived interrupted attempts. Gola's Upper Guinean rainforest inspired three branched broadleaf trees, a green forest-floor island and lid, brown vertical earth/bark skins and raised furrows. This is invented landscape-inspired sculpture, not a specific tree species, traditional craft replica, geographical model, certified timber or conservation endorsement. The inherited tentative-list citation was corrected to UNESCO's 2025 Gola-Tiwai inscription during resumed research; the visual contract was unchanged.

Procedurally authored Blender geometry and maps, not scans or hand sculpting. Mechanism, interior, brass fittings and viewer/test lineage come from the repository Japan pilot and its included trimmed mechanism.blend. Shared kit and other previews are unchanged. Three 0.180.0 MIT license is included. No source photography or external artwork is embedded.

## Verified evidence
- `source-check.json`: independent saved .blend reopen; 110 moving and 75 static meshes, 81 sequence samples, zero unintended intersections. Includes all grove parts and latch-versus-lid; only named inherited concentric bearing pairs excluded. Hollow floor ray z=0.2650000155. Ten rear hinge attachment contacts independently checked.
- `parity-check.json`: source and imported GLB nearest-vertex max error **1.712013073529306e-7**, below 1e-5. Three packed images present.
- `theme-check.json`: 3 trunks, 18 buttress roots, 36 branches, 36 flattened broadleaf clusters in four green materials. Lid ancestry, bounded height, grounded trunk rays and at least 30 real body relief ribs pass. Deliberately detaching a trunk makes the same gate FAIL, then restoring parentage passes; this is a post-implementation negative control, not test-first evidence.
- `browser-check.json`: actual GLTFLoader sees 25,788 triangles, 185 meshes, 11 materials, zero degenerate or nonfinite triangles/vertices. Desktop 1440×1080 and touch-emulated mobile 390×844 run offline file://, drag/touch, open/close, interrupted reset, reduced motion, no horizontal overflow, no external requests/errors. Full-open projected maximum absolute NDC is 0.892365. Corrupt bytes reach the real parser and show the fallback.
- `extended-check.json`: 36 canopy meshes belong to the lid; portable color ranges 99 and 130, actual green-channel roughness range 59, maps at most 512px. No-JS poster decoded and visible. Visible and canvas-accessibility copy checked for country identity.
- `motion-output.txt`: two motion/invalid-asset tests pass, zero failures; 80° latch release precedes 105° lid rotation.
- `delivery-check.json` and `inventory.json`: exact bytes and SHA-256 inventory, explicit required artifacts, ZIP readback and hashes. Folder-local Git attributes preserve exact bytes.

## Visual verdict and limits
Actual source poster, desktop closed/open/rear and mobile closed/open images were inspected. Three broadleaf crowns and rooted trunks read clearly at mobile size; complete open silhouette fits and interior is hollow. Front-opening view naturally hides the grove behind the raised lid; rear-open image documents it. Stylized lobed foliage is not dense botanical rainforest. Body reads partly as scored wood rather than raw earth, with deeper front relief than sides; roots have blunt miniature-like ends. Lighting makes the green lid paler than its dark base-color value. Source poster has visible sampling grain because denoising is off. These are disclosed v1 aesthetic limitations, not claims of photorealism or human approval.

Collision checks are sampled surface intersections, not continuous mechanical certification. Mobile emulation ran on desktop RTX 4060, not physical-phone performance. No exact reference artwork was supplied, and no reference-equivalence claim is made. User waived per-asset review; integration is separate.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, Edge, Node.js (build tooling only). Pinned package manifest/lock included; `npm ci --ignore-scripts --no-audit --no-fund` in this folder restores local build tooling. Dependencies are excluded from Git/archive. Source uses only included files; do not rerun historical `setup.py` unless deliberately resetting templates from the sibling Japan pilot.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender with `verify_theme.py`, `verify_source.py`, `verify_parity.py` using the same flags.
4. `python build.py`; `node --test --test-reporter=tap tests.mjs`
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites generated files; save manual edits separately. `.blend` is editable packed source, GLB portable export, poster is a real source render. Prior `lane-output.txt`/`lane-prompt.txt` retain an optional Codex attempt that failed authentication and produced no accepted changes. Hermes authored and verified directly. No credentials were changed. No asset gate failures occurred in the direct implementation; the deliberate detached-trunk control and corrupt-parser test prove real rejecting paths.
