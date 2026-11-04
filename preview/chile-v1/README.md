# Chile v1 — Atacama Salt & Copper

Open **chile-v1.html** directly in Edge/Chrome. All runtime code, model, textures and the actual-source poster are embedded. This is a local cosmetic collectible study, not minted, hosted, on-chain, signed or production custody evidence. No chain tools, keys, broadcasts, VPS or production files were used.

## Delivery
- Standalone HTML: **2,934,137 bytes**, strictly below 5,000,000.
- GLB: **1,612,128 bytes**.
- `chile.blend`: editable, packed Blender source; `mechanism.blend`: frozen inherited articulation baseline.
- `maps/`: generated 512×512 mineral color, roughness and normal maps.
- `poster.png`/`poster.jpg`: actual source render, no AI illustration.
- Actual offline browser captures: desktop/mobile closed/open, rear open, corrupted-input fallback and no-JS poster.
- `inventory.json`: exact byte lengths and SHA-256; `chile-v1-source.zip`: explicit required payload, scripts and evidence; `delivery-check.json`: archive readback proof. Hash envelopes exclude themselves to avoid circularity. Folder-local `* -text` preserves Git bytes.

## Verified
`run_checks.py` independently rebuilds and exercises all seven acceptance groups. Source reopening and parity operate on actual saved Blender source and imported exported GLB, not generation-time objects.

- 14,460 triangles, 82 runtime meshes, seven materials through actual Three GLTFLoader; zero nonfinite vertices or degenerate triangles.
- Source/export maximum nearest-vertex distance in both directions: **1.712013073529306e-7**, below 1e-5. Three packed source maps; runtime color/normal/roughness ranges 93/11/40. Roughness measured from its actual green channel.
- Same inherited lid/latch pivot matrices, 80° latch release before 105° lid opening. **81 sampled poses, all 41 moving and 39 static meshes, zero unintended surface intersections**. Latch-versus-lid tests included. Only named inherited hinge/barrel and latch/pin mating bearings excluded. Ten hinge attachment pairs intersect as intended. Hollow floor ray hits z=0.2650000155.
- 25 landscape meshes belong to the moving lid. Basin approximately 2.04×0.91 units; ridge relief 0.499/0.709 above lid. Three source-camera rays hit salt crust. Deliberately detached and undersized basin mutations both fail the real theme assertions, then restored state passes. Three invalid-asset motion negatives rejected. No untested hard-coded PASS substitutes.
- Offline file:// Edge: desktop 1440×1080 and 390×844 touch-emulated mobile. Native open/close, pointer/touch rotation, interrupted reset, reduced-motion endpoints, no horizontal overflow, no external HTTP requests or runtime errors. Full-open maximum absolute projection 0.915648, inside viewport. Actual corrupted GLB reaches parser and triggers the poster; no-JS poster also checked. RTX 4060 desktop hardware, **not physical-phone performance**.

## Visual result and limits
The pale cracked salt pan, two asymmetrical rear ridges and terracotta body are visible in actual mobile framing; no obvious floating ornament appears in source or open-rear browser views. This is stylized procedural mineral art, not a scan, photoreal reconstruction or exact map of a named salar. No traditional craft authenticity is claimed. The salt pan is a thin raised crust insert rather than a deeply excavated basin. Fine cracks are subtle at mobile size, terrain faces deliberately low-poly, and body bands regular/wavy rather than geologically exact. Hardware reads warm brass/copper-colored, not pure polished copper. The dark gasket remains visibly pronounced. Hidden latch engagement is not mechanical engineering certification. Collision checks are discrete surface samples, not continuous swept-solid proof. No artwork was supplied; the sourced pre-model written brief is the design reference.

## Failures preserved / corrections
- Optional Codex CLI exited 1 with expired authentication (401); its output is preserved in `initial/codex-auth-rejected.txt`. No Codex edits accepted and no credentials changed. Hermes authored and checked the deliverable directly.
- First build failed because the required main-checkout `iceland-pilot/node_modules` directory existed but was empty. `initial/build-missing-deps.txt` preserves the real failure. A Windows junction was verified, then the unchanged pinned Three 0.180.0/esbuild 0.25.11 dependencies were installed **only in this new folder**. Build then passed without changing the payload gate.
- Theme/motion deliberate negative controls are regression tests, not claims of pre-implementation TDD. No art/collision acceptance failure occurred in the first authored candidate.

## Reproduce
Requirements: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js. No blockchain node. `npm ci --no-audit --no-fund` from this folder restores pinned build dependencies (excluded from ZIP/Git). Scripts resolve artifact paths relative to this directory; `run_checks.py` contains the documented Windows Blender executable path, adjust for another installation.

1. `python maps.py`
2. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
3. `python run_checks.py`
4. `python package_delivery.py`

Authoring overwrites generated source/export/poster; save manual changes elsewhere before regenerating. Build uses local node_modules, with the sibling Iceland toolchain as a fallback only. No-JS and corrupted GLB screenshots deliberately show poster fallback rather than working 3D. Rebuilding changes hashes; repackage afterward.

## Provenance and scope
Research URLs and interpretation are in `design-brief.md`, written before authoring. No third-party terrain photos/textures embedded. Authoring, mechanism, viewer and check lineage: Japan Cedar v1 in base commit `ff5d78f`; country-specific geometry/materials and checks authored here. Three.js MIT license included. No edits to shared base kit, previous previews, vault, mint, docs or evidence directories. Branch backup only; final collection integration is a separate dependent card. Launch direction remains 201 equal one-of-one designs: 195 countries, five oceans and Moon.
