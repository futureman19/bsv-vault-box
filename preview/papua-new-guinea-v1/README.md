# Papua New Guinea v1 — Bilum & Highlands

Open **papua-new-guinea-v1.html** directly in Edge/Chrome. The actual GLB, maps, Three.js runtime and source-rendered fallback poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion snaps. No server or network is required.

## Delivered
- Standalone HTML: **3,169,901 bytes**, strictly below 5,000,000.
- `papua-new-guinea.glb`: **1,773,756 bytes**; 13,830 triangles, 62 meshes, 7 materials in actual GLTFLoader.
- `papua-new-guinea.blend`: packed editable Blender source; `mechanism.blend`: inherited trimmed articulation/interior baseline.
- Three generated 512×512 fibre maps; `poster.png` and `poster.jpg` are actual source renders, not promotional illustrations.
- Desktop/mobile closed/open, rear-open, corrupt-input and no-JS screenshots; JSON checks and raw execution output.
- Source ZIP and SHA-256 inventory with archive readback. Dependencies and caches excluded. All generated deliverables stay in this folder.

## Design and provenance
`design-brief.md` was written before modeling and cites Horniman, QAGOMA and Canterbury Museum descriptions of PNG bilum plant-fibre materials and looping. This invented vault uses ochre loop-pattern panels, a warm timber frame, green seam and three low highland-inspired ridges. It does not reproduce a particular maker's pattern, depict a named mountain, claim traditional chest construction or copy museum images. It is not the Indonesian Papua UNESCO noken element. Procedural maps are not scans or hand-woven fabric.

Mechanics/runtime and acceptance harness lineage: Japan Cedar & Moss v1 and Iceland pilot, present at starting repository commit `ff5d78f`. No shared pilot or base-kit art was modified. Three.js 0.180.0 is MIT (`THREE-LICENSE.txt`); esbuild 0.25.11 is build-time tooling only.

## Verified, with limits
- Independently reopened saved source: hollow interior floor at z=0.26500001549720764; ten hinge attachment contact pairs.
- **81 sampled poses**, all 19 moving and 43 static meshes, zero unintended surface intersections. Latch-versus-lid included. Only named intentional hinge and latch bearing contacts exempt. Sampling is not continuous collision/manufacturing certification; geometry contacts do not prove mechanical engineering.
- Original `Lid_Hinge` and `Latch_Pivot` matrices match independently opened mechanism baseline. Motion tests assert staged 80° latch release then 105° lid opening, including invalid-asset rejection controls.
- Source/export nearest-vertex parity maximum **1.712013073529306e-7** units both directions, under 1e-5. All three packed maps present. Not a byte-identical source re-export claim.
- Actual GLTFLoader: zero nonfinite vertices and degenerate triangles. All three ridges belong to the lid; relief dimensions and four fibre panels independently checked. Deliberately detached ridge rejected by the same ancestry assertion (post-implementation negative control, not TDD).
- Actual decoded base-color, roughness-green and normal-red ranges: **113, 44, 127**. 512×512 maps. Poster pixel coverage/nonblack checks pass.
- Offline `file://` Edge: 1440×1080 desktop and 390×844 mobile touch emulation; native button actions, drag/touch rotation, open/close, interrupted reset, reduced motion, no overflow, zero external HTTP requests and no runtime errors. Full-open projection maximum absolute NDC **0.892365**, under 1. Real corrupted GLB parser failure shows poster and disables controls; separate no-JS poster test passes.
- Tests used desktop NVIDIA RTX 4060. Mobile emulation is **not** physical-phone performance testing. No FPS or device-wide compatibility claim.

## Visual verdict
Actual source, mobile closed and desktop open images were inspected. Warm frame, repeated tan loops and three green hills are readable at mobile size. Complete opened silhouette and hollow interior fit the viewport. No obvious missing surfaces or gross rendering failure was seen. The top released latch looks visually separated by a small dark gap from one angle; its inherited bearing arrangement and hinge attachment checks are preserved, not redesigned.

This is **stylized**, not photorealistic or ethnographically authentic: loop maps can read as embossed repeated ovals, timber lacks detailed grain, and highland relief reads as rounded sculpted green hills rather than a faithful geographic landscape. Source poster retains some sampling noise. These are declared visual limits, not hidden behind technical PASS. The user waived individual human review until the full collection exists; this is not claimed human art approval.

## Actual failure and fix
The supplied shared `preview/iceland-pilot/node_modules` directory was empty. Initial build failed with `MODULE_NOT_FOUND` for esbuild (retained in `initial/build-missing-dependencies.txt`). Installed only the exact existing pinned dependencies into this new folder, then reran the unchanged size/build gate successfully. Optional Codex lane failed 401 token refresh before edits; no Codex changes were accepted, no credentials were changed. Its raw failure is retained. All implementation and verification were performed directly by Hermes.

## Reproduce
From this folder, using Python with numpy/Pillow/Playwright, installed Edge, Node and Blender 5.2.1:

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme_source.py`.
5. `node tests.mjs`
6. `python build.py`
7. `python verify_browser.py` and `python verify_extended.py`
8. `python package_delivery.py`

Use the installed Blender executable path where it is not on PATH. Authoring overwrites the generated blend/GLB/poster: save manual variants separately. Build prefers this folder's node_modules; sibling Iceland dependencies are an optional fallback, never a runtime dependency. Source authoring needs only the included mechanism. `* -text` preserves exact inventory bytes across Windows Git checkouts. The inventory excludes itself, ZIP and delivery-check to avoid circular hashes; delivery-check identifies the envelopes. Logs are raw, not reformatted.

Art preview only: no minting, blockchain node, keys, funds, broadcast, custody verification, deployment, public hosting, on-chain storage or production-site changes. Lid opening is cosmetic. Launch direction remains 201 equally one-of-one inner collectibles, distinct from outer custody containers. This branch is backed up only; final integration is a separate card.
