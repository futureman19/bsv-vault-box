# Southern Ocean v1 — Pack Ice & Polar Blue

Open **southern-ocean-v1.html** directly in Edge/Chrome. All runtime assets are embedded: real GLB, portable maps, bundled Three.js and actual Blender-render poster. **HTML 2,119,402 bytes; GLB 976,760 bytes.** Drag/touch to rotate, Open/Close lid, Reset view; reduced motion is supported. No network/server, wallet or transaction is involved.

## Design and provenance
The research-backed `design-brief.md` was written before authoring. Deep teal/polar-blue current-pattern enamel and a lid miniature of nine separated pack-ice floes and one flat-topped tabular iceberg express the Southern Ocean. The miniature is not a surveyed location or a climate model. No research photographs or AI promotional images are embedded. Geometry and maps are procedurally authored in Blender; not hand-sculpted, scanned or photorealistic. Hardware, hollow liner, pivot arrangement, runtime and test lineage come from repository Japan/Iceland pilots at base ff5d78f1e0d486af5c882c184fc08049996ebdc8. The included `mechanism.blend` is the trimmed mechanism, not the Japan tree/art asset. Three.js 0.180.0 is MIT; license included.

## Verified acceptance
- Independent saved-source reopening: 26 moving and 35 static meshes; 81 poses cover all moving-versus-static and latch-versus-lid pairs; zero unintended surface intersections. Only named coaxial mating bearings excluded. Ten hinge attachment pairs intersect as intended. Hollow interior floor ray z=0.2650000155. Sampled surface checks, not continuous collision/manufacturing certification.
- Exact baseline pivot matrices preserved. Runtime latch releases 80 degrees before lid opens 105 degrees; unit tests include clamping and invalid-asset negative controls.
- Source/export bidirectional nearest-vertex error 1.712013073529306e-7, below 1e-5. Three packed maps. This proves geometry agreement, not byte-identical re-export.
- Actual GLTFLoader: 10,124 triangles, 71 runtime meshes (multi-material source ice objects split into primitives), six materials; zero nonfinite vertices and degenerate triangles.
- Theme gates assert nine floes plus one iceberg, level plateaus, lid-root contact, separated XY bounds with exposed blue gaps, all ornament lid ancestry, iceberg height and baseline pivots. Deliberately detaching a floe is rejected by the same theme assertion. Runtime tests decode color, normal and roughness variation (roughness green channel), dimensions and blue-dominant palette.
- Offline file:// Edge: desktop 1440×1080 and touch-emulated mobile 390×844; real button click/tap, drag/touch rotation, open/close, reset during motion, reduced motion, no overflow, no external HTTP requests or JS errors. Entire open silhouette fits (max absolute NDC 0.892365). Actual corrupt GLB bytes exercise parser failure/poster fallback; no-JS poster separately verified. NVIDIA RTX 4060 desktop: mobile emulation is **not physical-phone performance testing**.
- Poster decoded as nonblack/nontransparent and inspected alongside actual mobile closed and desktop open screenshots. Model is fully framed and theme readable; no major visible clipping. Views and JSON evidence are in this folder.
- `inventory.json` records SHA-256/bytes; `delivery-check.json` proves ZIP membership and every archived hash, explicit principal artifact coverage, HTML cap and offline readback from the extracted archive. Local `.gitattributes` preserves exact bytes through Git.

## Real failure and fix
The supplied sibling `iceland-pilot/node_modules` directory was empty. The initial build genuinely failed with module-not-found (`initial/missing-toolchain.txt`). Installed the same pinned Three/esbuild versions into this new directory only, then rebuilt successfully. Optional Codex implementation lane failed authentication before making edits; its output is retained but no Codex work was accepted. Hermes authored and ran all delivered verification. The detached ornament test is an intentional negative control, not a falsely claimed accidental defect.

## Visual limitations
The body reads as saturated teal enamel with decorative currents, not literal water. Ice uses flat, clean polygonal plates and a faceted tabular berg, without physical transparency, erosion, submerged keels or water simulation. Floes are loosely spaced rather than densely packed. The long inherited latch is schematic family hardware; clearance is not real-world engineering certification. Lid ornament is naturally hidden behind the lid when viewed open from the front. No photoreal equivalence or user visual approval is claimed. The user waived individual asset review until collection integration.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/Playwright and installed Edge; Node with pinned package dependencies. From this directory:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` builds and independently runs motion/source/parity/theme/browser/extended checks.
5. `python package_delivery.py` creates the source ZIP, inventories it and opens its extracted HTML offline.

Blender/Node paths in verification are explicit Windows environment dependencies; authoring and assets otherwise resolve locally. Regeneration overwrites output; save manual edits separately. Source ZIP excludes dependencies, Python caches, .blend1 backups and itself. Inventory excludes packaging envelopes and actively written logs to avoid circular hashes. No mint, blockchain query, node startup, deployment, VPS or production edit occurred. Only this new preview directory is delivered. Branch backup is not publication; final collection integration remains a separate task.
