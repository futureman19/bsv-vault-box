# Vanuatu v1 — Yasur / Ash & Ember

Open **vanuatu-v1.html** directly in Edge or Chrome. All runtime assets are embedded: actual GLB, Three.js runtime, maps and actual-source poster. No server, account or network is needed. This is a cosmetic inner collectible, not the outer custody container; nothing is minted, signed, hosted or chain-verified.

## Delivered
- Standalone HTML: **2,336,749 bytes**, strictly below 5,000,000.
- Portable GLB: **1,186,228 bytes**.
- `vanuatu.blend`: packed editable source. `mechanism.blend`: unchanged trimmed mechanism from repository Japan pilot.
- `author.py`, `maps.py`, three compact 256px procedural maps, viewer/build and verification scripts.
- `poster.png` / `poster.jpg`: actual corrected Blender source render, not promotional AI artwork.
- Desktop/mobile closed/open and rear-open screenshots, no-JS and corrupt-input fallback captures.
- Evidence JSONs and raw output, explicit SHA-256 inventory, readback-verified source ZIP. See `delivery-check.json` for exact archive bytes/hash and inventory count.

## Theme and visual verdict
Research-led interpretation of Yasur on Tanna: charcoal ash-stone shell, broad recessed crater, small warm orange basin, oxidized seam and inherited satin brass. Sources and pre-authoring dimensions are in `design-brief.md`. No supplied marketing illustration was assumed. Geometry and maps are procedural, not scans or traditional craft reproductions.

Final actual-source and mobile screenshot inspection confirms a visible orange interior and unclipped controls/model. **Stylized, not photorealistic or geographically accurate.** The crater is faceted, the ember is a flat partially occluded pool, and ash remains stone/concrete-like under strong lighting. There is no smoke, fluid eruption simulation or realistic dynamic lava-light spill. The raised camera makes the basin readable but foreshortens the wide box. The first source poster and low browser angle failed that visibility goal; preserved in `initial/`. One geometry/material correction and one browser-camera correction were made, with precise deviations recorded in `initial/failure-and-fix.md`. The final browser angle was raised from y=5 to y=7 without changing geometry. Source poster and browser use different lighting/camera; no render equivalence is claimed.

## Executed verification
- Actual GLTFLoader: **14,908 triangles, 57 meshes, 4 materials**, zero nonfinite vertices or degenerate triangles. Three 256px portable maps have variation ranges color=48, roughness GREEN=75, normal RED=52. Warm emission and both terrain meshes' lid ancestry verified.
- Saved-source reopening: unchanged original pivots, hollow floor ray z=0.2650000155, all ten original hinge-attachment pairs intersect as expected.
- **81 sampled poses**, all **18 moving / 39 static** meshes plus latch-vs-lid pairs: zero unintended intersections. Only original mating leaf/barrel and knuckle/bridge/pin bearing contacts excluded. This is sampled surface evidence, not continuous collision or manufacturing certification.
- Bidirectional evaluated source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5; three packed source maps. Not a byte-identical re-export claim.
- Saved-source dimension gates, crown/center rays (depth **0.4693133831**), ember crown-polygon containment, ancestry and original-pivot comparison pass. Deliberate post-authoring detached-ember and lifted-basin negative controls were actually rejected, then original source reloaded. Motion unit tests also reject invalid geometry contracts.
- Offline `file://` Edge, desktop **1440×1080** and **390×844 touch/mobile emulation**: native open/close, pointer/touch orbit, interrupted Reset, reduced-motion snapping, no horizontal overflow, no external HTTP requests, no JS errors. Full-open projected extrema <1 (max **0.9722438874**, limited margin). User-selected zoom/rotation may crop intentionally; Reset restores the tested view.
- Real corrupted embedded GLB reaches GLTFLoader failure and shows poster/disabled controls; no-JS poster works. Poster image decoded and checked nonblack.
- Browser ran on desktop RTX 4060. **No physical-phone performance, FPS, continuous clearance, geographic fidelity, mint/storage availability or custody verification claims.**

## Reproduce
Within this folder, install pinned package.json dependencies with `npm ci --no-audit --no-fund`. Needs Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1 and Node/esbuild. The requested baseline dependency link was empty on this machine; final build uses folder-local pinned dependencies (not archived). No runtime dependencies are external.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender as above on `verify_theme.py`, `verify_parity.py`, `verify_source.py`.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py` after refreshing evidence output files.

Regeneration overwrites source/GLB/poster. Keep manual edits in a separate copy. Authoring only depends on included trimmed mechanism; final source archive is not dependent on a sibling art file. Initial historical author script is evidence only. Logs can vary between runs; regenerate inventory after any change. `package_delivery.py` excludes itself-referential inventory/delivery envelopes and its active output log from payload hashing. Source ZIP contains inventory; delivery-check remains outside ZIP to avoid circular hashes. Folder-local `.gitattributes` preserves exact bytes through Git checkout.

## Scope and provenance
All additions are under `preview/vanuatu-v1/`; no shared kit, previous preview, vault, mint, docs, evidence, VPS, blockchain or credentials altered. Branch is `art/vanuatu-v1`, backed up without merging. Mechanism/viewer/test lineage: Japan pilot at local base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; Three.js 0.180.0 MIT license included. Research URLs inform design; no third-party photos embedded. Collection direction remains 201 equal one-of-one designs. Integration/gallery is a separate dependent task. Human per-asset review was explicitly waived; technical acceptance does not imply user art approval.
