# Spain v1 — Talavera / Cobalt & Clay

Open **spain-v1.html** directly in Edge/Chrome. All model, texture, runtime and poster bytes are embedded; no server or network is required. This original ceramic-inspired collectible is local art, not minted, hosted, signed, on-chain, or a custody proof.

## Delivery
- Standalone HTML: **3,677,992 bytes**, strictly below 5,000,000.
- GLB: **2,119,264 bytes**; 24,380 triangles, 105 runtime meshes, 7 materials.
- `spain.blend`: packed editable source. `mechanism.blend`: inherited trimmed mechanism from Japan; not Japan scenery.
- `maps/`: four original procedural 512px maps. Ceramic panel pattern is invented, not a copied historic pattern or artisan-certified Talavera.
- `poster.png` / `poster.jpg`: actual source render, not AI promotional artwork.
- `desktop-closed.png`, `desktop-open.png`, `mobile-closed.png`, `mobile-open.png`: actual offline browser screenshots. `mobile-fallback.png` and `mobile-nojs.png` exercise fallback states.
- `inventory.json` and `delivery-check.json`: exact file identities and verified ZIP readback. `spain-v1-source.zip` is generated locally and not committed (recreate with `python package_delivery.py`).

## Verified
Independent saved-source reopening confirms the hollow floor at z=0.2650000155, ten hinge attachment pairs, unchanged evaluated lid/latch pivot matrices against the included mechanism, and **81 sampled poses over all 66 moving and 39 static meshes**, including latch versus lid. Zero unintended surface intersections; only the named mating hinge leaf/barrel and latch knuckle/bridge/pin contacts are excluded. This is sampled surface clearance, not a continuous or manufacturing proof.

Source/export nearest-vertex error in both directions: **1.712013073529306e-7**, under 1e-5. Four packed source images. Runtime GLTFLoader reports zero nonfinite vertices and zero degenerate triangles. Source and runtime theme tests count eight raised cobalt petals, eight ochre beads, 32 border tiles, and 50 total lid ornaments. Every ornament belongs to the lid; a deliberately detached petal is rejected by the same validator. This post-model mutation is a negative regression control, not test-first TDD.

Real offline `file://` Edge checks at desktop 1440×1080 and mobile 390×844 touch emulation: native open/close buttons, drag/touch rotation, interrupted reset, reduced motion, zero external requests/JS errors/overflow. Open projection maximum absolute NDC is 0.892365. Corrupt GLB bytes reach the real loader and show the poster with controls disabled. No-JS poster is independently checked. Reduced-motion frame samples contain endpoints only. Emulation runs on desktop RTX 4060, not a physical phone; no performance guarantee is made.

## Visual assessment and limitations
Actual source poster and browser mobile-closed/desktop-open captures were visually inspected. The patterned ivory panels, terracotta frame and raised radial cobalt motif are distinct and readable on mobile; open interior and released latch fit the desktop frame with no obvious floating hardware. The source render is grainy, relatively matte, and its blue reads lighter than deep cobalt. The dark seam is deliberately conspicuous and may read as a slightly raised lid. The body panels are continuous patterned fields, not individual grouted tiles. The design is intentionally stylized, not photorealistic or authentic traditional-pattern reproduction. No supplied reference artwork or prior Spain approval is implied. Research and the pre-model contract are in `design-brief.md`.

## Real failures retained
1. `initial-build-failure.txt`: instructed sibling dependency path was empty; native esbuild module was absent. Fixed by installing the exact existing pinned Three/esbuild versions locally inside this preview (not changing sibling previews).
2. `initial-install-failure.txt`: inherited Japan package did not include a lockfile; `npm ci` correctly failed. `npm install --no-audit --no-fund` generated the local lockfile without version upgrades. Future rebuilds can use `npm ci`.
3. `initial-node-shim-failure.txt`: background shell `node` shim returned “stdin is not a tty”. Fixed by invoking the actual Node executable for motion tests.
4. Optional Codex input lane exited 1 with 401 token-refresh failure before edits. No Codex output accepted and no credential store accessed/changed; Hermes authored and tested directly. Logs are retained, not a blocker.
No geometric failures occurred in the completed source/collision/parity checks; none were invented.

## Reproduce
Requirements: Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node.js, pinned Three 0.180.0/esbuild 0.25.11. All commands run inside this folder.

```text
npm ci --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python verify_all.py
python package_delivery.py
```

`verify_all.py` rebuilds HTML and runs motion, independent Blender source/parity/theme, offline browser and extended checks. Override BLENDER/NODE environment variables for non-default installed paths. `build.py` resolves local node_modules first, sibling installed dependencies second. The archived source needs dependencies installed, but the HTML has no external runtime dependency. Authoring overwrites generated source/GLB/render; preserve manual edits elsewhere before regeneration. `setup.py` is historical scaffolding only: **do not rerun it**, as it copies the original Japan harness before Spain adaptations.

## Scope and rights
Only `preview/spain-v1/` added. Shared kit and other previews unchanged. No blockchain nodes, keys, queries, broadcasts, wallet actions, VPS changes, production edits or deployment. Branch backup is authorized separately; integration is another task. Collection direction: 201 equally one-of-one boxes (195 countries, five oceans, Moon). Geometry/maps are procedurally authored, not scans or hand sculpture; Three.js MIT license included. UNESCO sources inform the craft connection only; no photographs or third-party texture pixels are used.
