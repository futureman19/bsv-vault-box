# Lebanon v1 — Cedar & Limestone

Open `lebanon-v1.html` in Edge/Chrome. Entire runtime, GLB, maps and actual-source poster are embedded: **2,729,848 bytes**. Standalone GLB: **1,483,576 bytes**. Drag/touch rotation, Open/Close and Reset; reduced-motion preference supported. No server or network needed.

## Design and provenance
The pre-model `design-brief.md` cites UNESCO's Qadisha and cedar-forest account plus the ICOMOS/IUCN limestone description. Original procedural interpretation, not a surveyed landscape, traditional craft replica, scan, photogrammetry or harvested cedar. No source photographs are used. Pale stratified limestone body, warm wood lid, muted green seam and brass fittings support a broad, tiered cedar miniature. Six generated 256px maps are packed into the editable source and GLB.

Mechanism/interior/hardware and viewer/test lineage are adapted from repository Japan pilot at base commit ff5d78f. The new tree comprises a trunk, six roots, fifteen branches and sixteen flattened canopy pads. Its rocky base intersects the lid; all 39 ornament meshes belong to the lid. `mechanism.blend` is included for reproducible authoring. `setup.py` records initial adaptation only: do not rerun it over later edits. Three 0.180.0 MIT license included; esbuild 0.25.11 is build-time tooling only.

## Actual verification
- Blender 5.2.1 saved source independently reopened; exact inherited pivot matrices; hollow floor ray z=0.265; ten tested hinge attachment contacts.
- 81 sampled motion poses, 67 moving and 39 static meshes, zero unintended surface intersections. Includes all new tree/terrain meshes and latch-vs-lid checks. Exceptions only named concentric hinge/latch bearings. Sampled surface tests are not continuous mechanical certification.
- Source/export bidirectional nearest-vertex error 1.712013073529306e-7 (<1e-5); six packed source images.
- Real GLTFLoader: 106 meshes, 18,826 triangles, 11 materials, zero nonfinite vertices/degenerate triangles. Portable color/roughness maps decoded; roughness variation sampled in the actual green channel.
- Theme: canopy width 1.4248889684677124; height above lid 0.9431926460266113. A deliberately detached ornament was rejected by the same ancestry assertion. Motion unit tests also reject absent pivots, invalid bounds and empty geometry. No genuine geometry/build acceptance failure occurred; negative controls are deliberate regression probes, not fabricated test-first history.
- Edge offline file:// desktop 1440x1080 and touch-emulated mobile 390x844: drag/touch rotation, native open/close, reset during animation, reduced motion, no overflow, no external requests or unexpected runtime errors. Open projection maximum absolute NDC <0.893. Actual corrupt GLB parser failure and no-JS poster tested separately.
- `package_delivery.py`: required artifact set, exact bytes/SHA-256 inventory, ZIP readback. Inventory excludes itself, ZIP, delivery report and final staging evidence to avoid circular hashes.

## Honest visual limits
Actual source render and mobile screenshot inspected. Wide silhouette, contrasting stone/wood/brass and cedar-inspired flattened boughs read clearly; no clipping or major layout defect. This remains stylized: canopy pads are rounded, not individually resolved cedar needles; pale limestone can read as ceramic/plaster; lid is light peach-brown, not rich dark cedar; stone feet and long inherited clasp are family extrapolations. Root bed is a decorative miniature, not a biologically viable planter. Poster retains low-sample render grain. No photorealism, exact botanical identity, source-image equivalence, physical-phone performance or user visual approval claimed.

## Reproduce
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, Node and package-lock dependencies required for build/tests only. Shared pilot dependency directory contained no compiler, so pinned dependencies were installed locally in this new folder; no sibling preview modified.

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`; `node --test tests.mjs`
5. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

Regeneration overwrites outputs and requires fresh evidence/inventory. Source archive excludes dependencies, backups and caches. Optional Codex implementation lane failed authentication before edits (exit 1, retained output); Hermes authored and ran every implementation/acceptance step directly. No credentials were inspected or altered.

Local art only. No blockchain/node/keys/mint/broadcasts, production docs, VPS or shared kit changes. Branch backup is not hosting, integration, minting or on-chain storage. Full-collection integration/review is a separate downstream task; per-asset human review was explicitly waived.
