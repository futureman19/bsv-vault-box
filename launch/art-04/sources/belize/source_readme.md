# Belize v1 — Blue Hole & Reef

Open `belize-v1.html` directly in Edge/Chrome: all runtime code, model, maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. Cosmetic collectible only; not minted, hosted, signed or a custody-state change.

## Delivered
Editable `belize.blend`, portable `belize.glb`, procedural 256px stone maps, real Cycles `poster.png`/JPEG, standalone HTML, source archive, reproducible author/build/check scripts, exact SHA-256 inventory and checks. Final exact byte counts are emitted in `build-output.txt` and `delivery-check.json`. Source lineage: Japan pilot's trimmed `mechanism.blend`, mechanical/viewer verification and Iceland motion tests from base ff5d78f. Shared sources are unmodified. Three.js 0.180.0 MIT license included.

## Verified
- Independently reopened saved source: 28 moving meshes, 39 static meshes, 81 poses, zero unintended sampled intersections. Ten hinge attachment contacts, original pivots, hollow floor at z=0.265. Explicit mating bearings only are excluded. This is sampled surface clearance, not continuous physics/manufacturing certification.
- Source/export maximum nearest-vertex error 1.712013073529306e-7 (<1e-5). Three packed generated maps. Actual GLTFLoader: 67 meshes, 14,728 triangles, six materials, zero nonfinite vertices/degenerate triangles.
- Twelve terrain parts all move with lid. Hole diameter 1.04 units, floor below raised reef, footprint and height gates; upward-facing reef normals. Deliberately detached ornament is rejected by the same ancestry gate (post-implementation negative control, not TDD).
- Native desktop and touch-emulated mobile file:// opening/closing, drag, interrupted reset, reduced-motion snap, no overflow or external requests/errors. Full-open projection stays within viewport. Actual corrupted GLB reaches parser and activates poster; no-JavaScript poster tested. RTX 4060 Edge emulation, NOT physical-phone performance.
- Generated base-color/roughness/normal map variation decoded through the actual browser; roughness checked in green channel. Nonblack/opaque source poster validated. Motion endpoints/sequencing and bad-asset rejection tested.
- Archive entry inventory and SHA-256 read back; complete HTML strictly below 5,000,000 bytes.

## Visual result and bounded corrections
The research-backed written brief is the primary reference, not supplied concept artwork. Pale stone-like body, turquoise enamel lid, navy circular Blue Hole motif, irregular pale reef ring and green caye are readable at mobile size. This is intentionally stylized, not photorealistic, geographic/bathymetric reconstruction, or traditional-craft replication. Stone can read as ceramic; mangrove crowns are simplified clusters without root ecology; the shallow relief reads more as a graphic inset than great underwater depth. The ring is continuous and irregular rather than a literal fractured coral survey. Gold family latch is relatively chunky. The low-sample source poster retains grain. No human art approval is claimed; review was waived for this batch.

Initial poster had excessive reflection washing out the navy floor; final navy roughness/specular and annular face winding were corrected. `initial-poster.png` retains the earlier image. Theme harness initially rejected the sand caye's intentionally embedded underside: its minimum bound was corrected from z=1.97 to 1.90 to permit attachment within the existing lid, without changing the maximum height/XY/clearance tests. Raw failure is `initial-theme-failure.txt`. Build initially failed because the supplied dependency directory was empty; pinned local dependencies fixed that (`initial-build-failure.txt`). Optional Codex lane failed authentication before making edits; Hermes authored and verified directly, without altering credentials.

## Reproduce
Python with numpy/Pillow/Playwright; installed Edge; Blender 5.2.1; Node with pinned dependencies. In this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`
Authoring overwrites the generated source; preserve manual edits separately. Compiler fallback uses sibling Iceland dependencies only when no local install exists; offline HTML has no such dependency. The archive excludes dependencies/caches/backups and optional lane logs. Inventory excludes itself and packaging envelopes to avoid recursive hashes. Folder-local attributes preserve exact bytes across Windows Git checkouts.

No blockchain node, funds, keys, minting, production site, VPS, or shared kit changes. Branch backup is separate from publication. Next: collection-wide gallery integration and the final full-set review.
