# Senegal v1 — Saloum / Mangrove & Shell

Open **senegal-v1.html** directly in Edge/Chrome. Complete offline viewer **2,387,270 bytes**; GLB **1,198,000 bytes**. All runtime, geometry, maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close, Reset; reduced motion and poster fallbacks supported.

## Design and provenance
The pre-model `design-brief.md` cites UNESCO's Saloum Delta listing and the local interpretation centre. A warm shell-sand-inspired mineral body carries a teal, branching-water inset, three low closed banks, and six mangrove miniatures with twenty-four splayed roots. No cultural/funerary mound was reproduced. This is an invented landscape miniature, not geographic cartography, traditional craft, botanical simulation, shell scan or human hand sculpture.

`senegal.blend` is editable Blender 5.2.1 source with packed generated maps; `senegal.glb` is its export. `mechanism.blend` is the unchanged Japan pilot's trimmed family mechanism, derived from the Iceland lineage. Viewer, source/parity/browser harnesses adapted from Japan; motion tests from Iceland. Three.js 0.180.0 MIT license included; esbuild 0.25.11 build-time only. No external textures/images used. `poster.png` and JPEG are actual Cycles source renders, not AI promotional images.

## Verified, with actual evidence
- `source-check.json`: independently reopened saved source, hollow floor ray z=0.2650000155; **81 poses, 86 moving / 39 static meshes, zero unintended sampled surface intersections**, including every new tree/root/bank and latch against lid. Only named mating bearings excluded. `hinge-attachment-check.json`: ten connecting attachment pairs.
- `theme-check.json`: three banks, six trunks, twenty-four root end centres seated within 0.004001 units of a bank; all 70 themed meshes lid-owned. Thirteen exposed-water rays along the branching channel. Exact inherited closed pivot matrices (error zero). Deliberate detached ornament rejected by the same ancestry assertion, then restored: a real post-implementation negative control, not a claim of test-first TDD.
- `parity-check.json`: 9,056 source and 25,625 imported vertices; bidirectional nearest-vertex maximum error 1.712013073529306e-7 (<1e-5). Three packed maps. This is geometry parity, not byte-identical re-export.
- `motion-output.txt`: 2 tests PASS, 0 fail, staged latch 80° then lid 105°, clamped/reversed endpoints; missing/empty/nonfinite asset negatives rejected.
- `browser-check.json`: actual GLTFLoader 17,620 triangles / 125 meshes / 10 materials, zero degenerate/nonfinite triangles/vertices. Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: native Open/Close, drag/touch rotation, interrupted Reset, reduced motion, no overflow, no HTTP requests/errors. Fully open maximum absolute projected NDC 0.930595. Corrupt embedded bytes reach the actual parser and show poster with controls disabled.
- `extended-check.json`: no-JS poster, decoded 256px portable maps with color ranges 81/66 and roughness GREEN-channel range 78, visible and accessibility country-copy assertions. Actual browser rear-open capture included.
- `inventory.json` and `delivery-check.json`: exact SHA-256/byte identities, required-file coverage, ZIP readback, HTML cap. Folder-local `* -text` preserves bytes through Git checkout; staged-blob hashes checked separately before commit.

All authoring and checks were executed by Hermes directly. Optional Codex lane exited 1 before edits because token refresh returned HTTP 401; no credentials were accessed/changed and no Codex patch was accepted. Main checkout shared compiler was absent, so the exact pinned dependencies were installed **only in this new folder**, ignored from Git/archive. No art acceptance failure occurred in the initial successful build/check sequence; negative controls deliberately demonstrate rejectability. Inherited Japan copy was corrected before final build.

## Honest visual limits
Actual source and mobile closed/open captures were inspected. Branching teal channels and seated green trees read at mobile scale, and the fully open silhouette fits. Water reads as decorative resin/inlay rather than realistic water; angular banks read as miniature plates, and simple rounded canopy clusters can overlap at small size. Shell-sand is an inspired finish, not identifiable shell inclusions. Source poster retains some Cycles sampling noise. Mechanical sampling is not continuous collision proof or manufacturing certification. Desktop RTX 4060 mobile emulation is not physical-phone performance. No photorealism or supplied-art equivalence claimed.

## Reproduce (from this folder)
1. `npm ci --ignore-scripts --no-audit --no-fund` (build-only pinned dependencies)
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run the same Blender command for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`; `python build.py`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Python requires numpy/Pillow/playwright; browser checks require installed Edge. Build discovers local Node and local dependencies (sibling fallback only if available); source generation is self-contained in this folder. Regeneration overwrites source/render/export; protect manual edits first. ZIP excludes dependencies, .blend1 backups and itself. Inventory excludes its own envelope and delivery-check to avoid circular hashes. No separate copied-delivery claim: this folder's final HTML is the tested deliverable.

Local collectible art only: not minted, hosted, signed, deployed or stored on-chain; cosmetic opening has no custody effect. No wallet, keys, chain queries, broadcasts or VPS access. Launch direction remains 201 equally one-of-one designs. Branch backup only; final collection integration is separate.
