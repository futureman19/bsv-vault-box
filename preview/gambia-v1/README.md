# Gambia v1 — Tanbi Tidal Bronze

Open **gambia-v1.html** directly in Edge/Chrome. The complete model, textures, Three.js runtime and actual Blender-rendered fallback poster are embedded. Drag/touch rotates; Open/Close lid and Reset view work offline. Cosmetic motion only; this inner collectible is not the outer custody container.

## Delivered
- HTML: **2,896,762 bytes**, strictly below 5,000,000.
- GLB: **1,552,360 bytes**; named editable `gambia.blend`, packed procedural maps, reproducible generator and included `mechanism.blend`.
- `poster.png` and `poster.jpg`: actual source render, not AI promotional imagery.
- Actual offline browser screenshots: desktop/mobile closed/open, rear-open, corrupt-input fallback, no-JS fallback.
- `inventory.json` and `delivery-check.json`: exact byte counts and SHA-256 inventory; source ZIP verified entry-by-entry. Hashes prove byte integrity, not authenticity or availability.

## Design and visual verdict
Research-backed brief was written before modeling: Tanbi's mangroves and sedimentary estuary inspire a warm ochre/bronze box carrying a continuous enamel channel and tributary, low silt banks, three mangrove trees with 15 exposed prop roots, and three broadleaf canopies. Bronze is an artistic material choice, not a historical Gambian craft claim. No research photographs or third-party texture imagery are embedded.

Actual source and desktop/mobile views were inspected. The wide silhouette, blue-green water, exposed roots and crown grouping are readable. This is deliberately stylized, **not photorealistic, a botanical reconstruction, or a surveyed map**. Wavy body lines can read as wood grain rather than sediment bronze; banks look like discrete stones and tree bases like small pads. Channel ends are blunt, the tributary shallow, and leaves simplified. Some hinge/rim joints look segmented despite verified physical attachment intersections. Fine roots/hardware require zoom on mobile. No claim of exact reference equivalence or user visual approval; per-asset human review is waived for this batch.

## Checks actually passed
- `source-check.json`: independent saved-source reopening, genuine hollow floor ray z=0.2650000155, **81 sampled poses, 91 moving meshes and 39 static meshes**, no unintended surface intersections. Every new moving ornament included; latch tested against lid. Only explicit inherited mating bearings excluded. Ten hinge/body/lid attachment pairs intersect. Sampled surface evidence, not continuous collision/manufacturing certification.
- `parity-check.json`: bidirectional nearest-world-vertex source/GLB error **1.712013073529306e-7**, below 1e-5; three packed maps. This proves geometry correspondence, not byte-identical reexport or shader equivalence.
- `source-theme-check.json`: exact inherited lid/latch local matrices, 3.72×2.38 lid, ornament bounds/parentage, <=0.10 seam, connected tributary mouth, linked portable body color/roughness.
- `browser-check.json`: actual GLTFLoader **19,400 triangles / 130 meshes / 9 materials**, zero degenerate triangles/nonfinite vertices. Edge offline `file://` desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, mouse/touch drag, reset during motion, reduced motion, no overflow, no external requests or successful-run JS errors. Open projection max abs NDC 0.892365. Corrupt embedded GLB really reaches the parser and shows fallback with controls disabled.
- `theme-check.json`: actual loaded 3 trunks, 15 roots, 3 canopies, 2 channels, all lid parentage; decoded 512px body and 256px bank color maps have nonzero ranges. Missing-root negative control rejected. No-JS poster verified.
- `tests.mjs`: staged 80° latch then 105° lid, endpoints/clamping and invalid-asset negative controls pass.
- All browser results used NVIDIA RTX 4060 / Direct3D11. Mobile is emulation, **not physical-phone performance**; no FPS or long-duration stability claim.

## Real failures and corrections
`initial/render-memory-failure.txt` preserves Cycles OIDN out-of-memory failure. Disabled denoising and limited render threads to two; author/export/render then completed with exit 0. Poster retains some sampling grain. Initial foreground browser run exceeded its 180-second wrapper without results; a tracked background run using explicit D3D11 completed all assertions. No acceptance was weakened. Optional Codex lane exited 1 with authentication failure and contributed no edits; Hermes implemented and verified directly, without touching credentials.

## Reproduce
Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node.js with Three 0.180.0/esbuild. These are author/test dependencies, not viewer network requirements. Build resolves local `node_modules` or sibling `preview/iceland-pilot/node_modules`; this worktree links the latter to the main checkout as requested. Package metadata and Three MIT license included. No source references need other country's artwork; only the compiler dependency installation is shared.

From this folder:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_source_theme.py`.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_theme.py`
6. `python package_delivery.py`

Regeneration overwrites authored source/output. Preserve manual edits separately. Inventory excludes its own envelope, ZIP, delivery report, generated backups/caches and final Git log to avoid circular hashes. Source ZIP includes explicit required assets and is read back to verify every entry.

## Provenance and scope
Mechanism, viewer and verification lineage: Japan cedar v1 and Iceland pilot from local base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; no prior evidence copied as new results. Original procedural Gambia maps/ornaments, no scans or hand-sculpture claim. Only `preview/gambia-v1/` is added. No shared base kit or earlier previews edited, no production deployment, merge, blockchain/node daemon, keys, minting, broadcasts, VPS or chain queries. Branch backup only. Off-chain local files; storage/persistence and NFT issuance are not implemented here. Launch direction remains 201 equally one-of-one designs.
