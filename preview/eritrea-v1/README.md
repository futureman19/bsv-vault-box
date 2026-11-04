# Eritrea v1 — Dahlak Reef Limestone

Open `eritrea-v1.html` directly in Edge/Chrome. All runtime assets are embedded: actual GLB, maps, Three.js and actual-source poster. Drag/touch to rotate, open/close the lid, reset; reduced motion is honored. **HTML 2,612,826 bytes; GLB 1,403,800 bytes.** No server or network required.

## Design and provenance
The pre-authored `design-brief.md` cites research on Eritrea's Dahlak carbonate shelf and flattened fossil reefs. Seven low irregular pale island forms sit on a petrol/teal enamel sea, framed by warm limestone and brass. This is an invented miniature arrangement, not a geographic map, archaeological replica, natural stone scan or harvested coral. Geometry and maps are procedurally authored in Blender. Family mechanics derive from the included Japan trimmed `mechanism.blend`; the shared vault kit and other previews are unchanged.

The original brief was recovered from the interrupted first attempt, along with authored source. Research was rechecked against the Springer result for *Present-day sedimentation on the carbonate platform of the Dahlak Islands, Eritrea* and the Naturalis seaweed survey https://repository.naturalis.nl/pub/524925/BLUM2005050001006.pdf, which independently describes fossil reef limestone and abrasion platforms. No research imagery is embedded.

## Verified evidence
- `source-check.json`: saved source independently reopened; 24 moving and 39 static meshes, 81 staged poses with zero unintended sampled BVH surface intersections. Includes all islands. Only named concentric hinge/latch bearing pairs exempted. Hollow floor ray z=0.2650000155; ten hinge attachment pairs.
- `parity-check.json`: bidirectional evaluated source/export vertex error 1.712013073529306e-7, below 1e-5; three packed source maps.
- `contract-check.json`: exact inherited world pivot matrices, seven lid-parented islands, low relief, 0.09 seam height, 3.72 × 2.38 lid. Deliberately detached island is rejected.
- `motion-check.json`: 81 motion-function samples; latch reaches 80 degrees before lid opens to 105 degrees; three invalid-geometry negative controls rejected.
- `browser-check.json`: actual GLTFLoader: 63 meshes, 14,674 triangles, four materials, zero nonfinite vertices/degenerate triangles. Offline file:// desktop 1440×1080 and touch-emulated 390×844: drag, native controls, open/close, interrupted reset, reduced motion, no overflow/errors/external HTTP requests. Full-open NDC maximum 0.892365. Real corrupt embedded GLB parser failure shows poster, disables controls.
- `theme-check.json`: seven low islands, moving parentage, two compact 512×512 color maps, color ranges 99 and 9; no-JavaScript poster works.
- `material-check.json`: actual glTF green-channel roughness range 40, nonblank actual-source poster 880×800, country accessibility copy.
- `delivery-check.json` and `inventory.json`: exact bytes and SHA-256 identities, required-file completeness, source ZIP readback. Inventory excludes itself and packaging envelopes to avoid recursive hashes.

## Failure and recovery
`author-output.txt` retains the real initial Cycles/OIDN out-of-memory failure. Final authoring disables denoising/compositing, uses two render threads and an 880×800 poster; `author-final-output.txt` records successful source export/render. No fake or promotional replacement was used. The optional Codex attempt failed authentication and contributed no accepted edits (`codex-output.txt`); Hermes completed and independently verified the work. Stale inherited Japan canvas copy was corrected before final checks. The historical setup generator is not part of reproduction.

## Honest visual limits
Actual source, mobile closed and mobile open images were inspected. Whole silhouette fits; low island/teal scheme reads clearly and interior is visible. Islands are angular/faceted, pale stone can read as chalk/plaster, water is flat enamel rather than simulated sea, hardware is chunky and the dark seam conspicuous. Fine render noise remains because denoising was disabled. Technical acceptance is not photorealism, geographic accuracy, continuous collision certification, physical-phone performance or human art approval. Individual review is waived by the collection directive.

## Reproduce
Requires Blender 5.2.1, Python Pillow/numpy/playwright, installed Edge, Node and pinned Three 0.180.0/esbuild 0.25.11. `build.py` finds local node_modules or the linked sibling Iceland toolchain. For extraction, `npm install` here restores package.json dependencies. Dependencies are build-time only and excluded from delivery.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_contract.py`.
4. `node tests.mjs`; `python build.py`
5. `python verify_browser.py`; `python verify_theme.py`; `python verify_material.py`
6. `python package_delivery.py`

Regeneration overwrites outputs; preserve hand edits separately. Three MIT license included. Source ZIP contains .blend, GLB, HTML, procedural maps, scripts and evidence; no dependencies/backups. Nothing minted, deployed, signed, chain-queried or merged. Branch backup only; collection integration is a separate card.
