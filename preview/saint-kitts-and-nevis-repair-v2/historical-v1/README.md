# Saint Kitts and Nevis v1 — Twin Peaks & Narrows

Open **saint-kitts-and-nevis-v1.html** directly in Edge/Chrome. Complete model, runtime, maps and actual-model poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion users get an immediate pose change. This is local collectible art, not a wallet, custody action, mint, public deployment or on-chain asset.

## Delivery
- Standalone HTML: **2,522,267 bytes**, strictly below 5,000,000.
- GLB: **1,321,872 bytes**; 14,860 triangles, 64 runtime meshes, 10 materials through actual GLTFLoader.
- `saint-kitts-and-nevis.blend`: editable, packed Blender source. `mechanism.blend`: included trimmed inherited mechanical baseline.
- `maps/`: three original deterministic 384×384 stone color/roughness/normal maps, not scans.
- `poster.png` / `poster.jpg`: actual Blender source render, not AI promotional artwork.
- Desktop/mobile closed/open captures, rear-open view, corrupt-input fallback and no-JS captures are actual offline Edge screenshots.
- Source ZIP and `inventory.json`: explicit required artifacts, exact bytes/SHA-256, ZIP entry and byte-for-byte readback validation. `delivery-check.json` is outside its own archive to avoid recursion. Dependencies, backups and caches are excluded.

## Design and visual limits
The brief was written before modeling from cited research excerpts. A dark volcanic-stone-inspired box carries two separately modeled green islands in teal enamel: a broad depressed crater and a pointed cone, separated by a visible passage. Gold fittings are collection conventions, not claims about local traditional craft. No third-party imagery is embedded.

This is a stylized miniature, not a geographical map, literal elevation model or photoreal reconstruction. The smooth forest color patches and angular shores remain procedural; no individual trees are modeled. The teal passage reads as calm flat enamel water, not an animated/current simulation. The body can read as gray weathered metal or streaked stone under the bright studio lights, so material recognizability is not asserted as definitive basalt. The source poster has some low-sample grain. Small supporting mobile text is legible in the capture but is less readable than the heading/buttons.

Visual inspection of actual mobile closed and desktop open/rear captures found no obvious clipping or detached islands. Front-open hinges are partly occluded and can look suspended; the rear-open view exposes body-side tabs, while the independent geometric test verifies ten attachment/contact pairs. That combination is still not a mechanical engineering or manufacturing certification. Terrain becomes hidden behind the opened lid from the front as expected; rear-open capture shows it remains on the lid.

## Verified acceptance
- Saved source reopened independently. Original lid/latch matrices match the included baseline within 1e-7. Latch releases 80° before the lid opens 105°.
- **81 motion samples; all 19 moving and 36 static meshes; zero unintended surface intersections.** Latch-vs-lid also sampled. Only inherited named leaf/barrel and latch knuckle/bridge/pin mating bearings excluded. No terrain exemptions. Sampled surface collision testing is not continuous collision proof or a volume-containment test.
- Hollow interior ray reaches the floor at z=0.26500001549720764. Ten hinge attachment pairs intersect as intended.
- Source/export maximum bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5. Packed maps present. This is geometric parity, not exact re-export byte identity.
- Theme geometry: minimum separating X gap **0.27959872782230377**; crater center at least **0.20003843307495117** below sampled rim; two lid-owned islands, root bounds contact the sea inset, footprint/height contract passes. Real detached-ornament negative control is rejected. No source file is saved during this mutation test.
- Actual loader: zero nonfinite vertices and zero degenerate triangles. Decoded map ranges: color 53, roughness **green channel** 48, normal red 47; dimensions 384×384.
- Offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: native controls, mouse/touch rotation, open/close, interrupted Reset, reduced motion, no external HTTP requests, no runtime errors, no horizontal overflow. Full-open max absolute NDC 0.9195185009763714 (<1). NVIDIA RTX 4060; **not physical-phone performance testing**.
- Actual corrupted GLB bytes reach the loader and trigger the poster/disabled-controls fallback; no-JS poster is also visible. Three malformed geometry inputs are rejected by motion tests.

## Failures and bounded correction
1. Optional Codex lane exited 401 before making changes; no credential changes attempted. Hermes authored and verified all output directly.
2. First build failed because the supplied main-checkout dependency directory was empty. `initial/build-missing-dependencies.txt` retains the real failure. Installing pinned dependencies **inside this new folder** fixed it; no other preview files changed.
3. First motion-test shell invocation failed with `stdin is not a tty`; retained in `initial/motion-shell-shim-failure.txt`. Invoking the native Node executable passed unchanged tests.
4. One visual correction replaced alternating per-face green colors (initial poster retained) with larger coherent slope patches. All final source, parity, theme and browser checks were run after that change. No failing geometry thresholds were relaxed.

## Reproduce
Use Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge, Node.js, and pinned npm packages. From this directory:

```text
npm ci --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme.py
node tests.mjs
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

On this Windows host use `C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe` and `C:/Program Files/nodejs/node.exe` rather than the shell's non-TTY Node shim. Scripts resolve local paths; build optionally discovers sibling Iceland dependencies only if local `node_modules` is absent. Regeneration overwrites generated models/poster; save manual changes separately. Regeneration changes source hashes, so refresh inventories.

Mechanism, shell helpers, viewer and verification lineage: repository Japan v1 / Iceland pipeline at base commit ff5d78f. Shared `art/vault-kit/` was read only, never modified. Three.js 0.180.0 MIT license included; esbuild 0.25.11 build tooling. Collection scope remains 201 equally one-of-one designs. Branch backup only; no merge or public deployment. Per-asset human review was explicitly waived for this batch; this is autonomous brief acceptance, not a claim of human visual approval.
