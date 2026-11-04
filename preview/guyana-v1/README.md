# Guyana v1 — Kaieteur / Rainforest & Sandstone

Open **guyana-v1.html** directly in Edge/Chrome. Complete self-contained offline 3D collectible, **2,024,172 bytes**, with embedded **932,588-byte GLB** and actual-source poster. Drag/touch rotate, open/close and reset. Cosmetic movement only: not a seal/custody operation, minted NFT, hosted product or blockchain verification.

## Design and visual verdict
The sourced brief was written before authoring. Original procedural sandstone body, forest-green lid, sandstone plateau, amber upper Potaro-inspired river, pale 0.58-unit waterfall, lower pool and 12 clustered green canopy crowns. Brass articulation reuses the repository family mechanism. No external photographs, scans or generated promotional substitute. No sacred/craft pattern fidelity claim; this landscape does not represent all of Guyana.

Final mobile inspection reads the corrected material primarily as mottled sandstone, with residual wood-like streaks. The waterfall is a visibly solid stylized strip, canopy forms are rounded low-detail crowns rather than botanically accurate rainforest. Neither photorealism nor a geographic replica is claimed. Source render is 24-sample Cycles without denoising and has some grain. The inherited narrow rim/corner gaps are visible. At full opening the terrain faces away from the default front camera; rotate to inspect the outer lid (desktop-open-rear.png). Surface appearance and simple canopy density remain artistic limitations, not hidden behind passing tests.

One bounded visual correction replaced strongly wood-like regular bands with irregular mineral mottling/pores. Initial actual source/mobile images and maps are preserved in initial/. No per-asset human approval is claimed; review was explicitly waived for this batch task.

## Verified on delivered bytes
- Real Three.js GLTFLoader: **70 meshes, 9,216 triangles, 11 materials**, zero nonfinite vertices and degenerate triangles. Color/normal/roughness maps decoded at 512×256; ranges 105/17/47, roughness read from green channel.
- Independent packed .blend reopen and GLB import: nearest-vertex error both directions **1.712013073529306e-7**, below 1e-5. Three maps packed into source. This verifies evaluated geometry, not identical shading between render engines.
- **81 sampled poses**, **39 moving** and **31 static** meshes: zero unintended surface intersections. Every new terrain/water/canopy mesh participates. Explicit exceptions only inherited moving hinge leaf/fixed barrel and latch knuckle/bridge/pin mating surfaces. Ten hinge attachment overlap pairs verified; hollow floor ray z=0.265. Sampled BVH surface checks are not continuous collision, solid containment or manufacturing certification.
- Original Lid_Hinge and Latch_Pivot world matrices match exactly. 80° latch release precedes 105° lid opening. Two Node motion/invalid-geometry tests pass. Theme negative control deliberately detaches waterfall, confirms ancestry assertion rejects it, then reopens unchanged source. Upper river/curtain/pool surface connections and exposed water rays pass; all 23 theme meshes are lid-owned in actual loader.
- Actual offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native buttons, mouse/touch rotation, opening/closing, reset during motion, reduced-motion endpoints, no horizontal overflow, no external HTTP requests, no runtime errors. Fully open maximum absolute projected NDC 0.892365 <1.
- Actual corrupted GLB input triggers parser error and visible disabled-controls poster fallback; no-JavaScript poster also checked. Poster pixel checks reject blank images.
- SHA-256 inventory plus source ZIP readback and exact embedded GLB/poster comparison in delivery-check.json. Folder-local .gitattributes preserves bytes across Windows Git checkout.

Testing used installed Edge and desktop NVIDIA RTX 4060; mobile is emulation, **not physical-phone performance**, FPS, wallet compatibility or on-chain storage verification. No public deployment, keys, funds, chain queries, minting, VPS or other preview edits.

## Files and reproduction
`guyana.blend` packed editable source; `mechanism.blend` included trimmed inherited base; `guyana.glb`; generated maps/; actual poster.png/.jpg; desktop/mobile closed/open, rear and fallback captures; design brief; scripts; machine-readable check JSONs, raw logs; failures.md; byte inventory and source archive. Source/export/code lineage: Japan Cedar v1 mechanism/viewer/test patterns on local base ff5d78f1e0d486af5c882c184fc08049996ebdc8. Three.js 0.180.0 MIT license included.

Requirements: Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node/esbuild/Three pinned in package-lock.json. All assets stay in this folder; no absolute source-art path dependency. The task-prescribed sibling node_modules was empty; installed exact dependencies locally instead. Dependencies are excluded from archive/Git. Build prefers local dependencies then sibling fallback; offline HTML needs neither.

From this folder:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` (set BLENDER and NODE environment paths if not installed in the documented Windows defaults).

Regeneration overwrites authored assets: preserve manual edits separately. After regeneration update README byte counts, inventory and archive. Tests intentionally fail on violations; see failures.md for actual failed setup/visual attempts and negative controls. No credentials are required.

Next: separate collection integration card merges the backed-up branch with the other place assets; this task does not merge or publish.
