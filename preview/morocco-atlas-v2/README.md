# Morocco / Atlas & Tile v2

Actual generated 3D collectible study, not minted, not deployed, not a custody interface. Complete offline HTML opens directly in a browser; no runtime server or downloads are required.

## Three focused passes
1. MATERIALS: replaced regular sinusoidal pink waves with nonuniform ochre/rose/cream deposition, local folds, fine granular inclusions, portable stone roughness and normal maps. Darkened cedar and reduced coarse striping to fine grain. Checkpoints: `checkpoints/pass1-materials.png`, `checkpoints/pass1-material-closeup.png`.
2. TILEWORK: replaced 270 coarse pieces with 1,080 disconnected ceramic prisms: eight-point emerald stars and complementary ivory/dark kites. Two-row perimeter includes four corners and real star-edge bevels. Checkpoint: `checkpoints/pass2-tilework.png`.
3. RIDGE/HARDWARE: four asymmetric terrain summits and deeper gullies, shortened moving hasp around preserved pivot, shaped low brass corner caps, ring relocated low on front-left, seated fasteners. Checkpoint: `checkpoints/pass3-ridge-hardware.png`.

One integrated final correction raised the keeper to match the shorter hasp visually, reduced the clasp seat, removed the terrain's rectangular perimeter, deepened emerald, and compacted the exported ceramic representation. Tile prisms are joined into three material batches, retaining 120/480/480 disconnected components. The first unoptimized v2 exceeded the HTML cap; that failed build is not delivered as final.

## Verified final artifact
- Complete HTML: 4,192,580 bytes (hard gate <5,000,000).
- GLB: 2,550,964 bytes; actual loader 52,814 triangles / 62 meshes / 8 materials; zero NaNs and degenerate triangles.
- Six packed compact generated maps, maximum dimension 512; not scans. Actual browser map/color/roughness/normal decoding checked.
- Independently reopened .blend geometry agrees with imported GLB both directions within 1.713e-7 world units (threshold 1e-5).
- 81 staged motion samples: zero tested intersections, preserved narrow hinge/latch bearing exclusions, hollow interior floor ray, hinge/ridge attachments. Samples are not continuous-motion proof. No new collision exemptions.
- Offline Edge desktop and mobile touch emulation: rotate, open/close, reset interrupted motion, reduced motion, real corrupt-GLB fallback, no-JS poster, no external HTTP requests/errors/overflow. Fully open projected silhouette fits. Mobile emulation is not a physical phone performance test.
- New six-feature regression gate passes v2 and rejects v1. These were post-implementation negative controls, NOT test-first TDD.
- Same-camera actual browser v1/v2 closed/open/details and equal-width primary concept comparison; no distortion. Concept reference remains illustration, not the delivered 3D object.

## Remaining shortcomings / partial requests
The result remains stylized, not photoreal or a close reproduction of every reference detail. Stone is less repetitive but still visibly banded, and its front/side transition is not seamless geological continuity. Cedar is deliberately subtle. Dense tile motifs compress at mobile size, glaze variation is limited and corners remain repeated units rather than bespoke corner rosettes. Terrain now has multiple summits but is sharper/spikier than the reference's eroded cluster. Brass corners and clasp remain simplified. Bearing contact is tested; visible keeper alignment is improved, but a physically engaging lock/contact mechanism is NOT established. These limitations are not waived by passing technical gates. No further art pass is included.

## Reproduce
Use Blender 5.2.1, Python with Pillow/numpy/playwright, Node with package.json dependencies. Install npm dependencies in this folder if not using the existing sibling iceland-pilot toolchain. Browser tests need installed Microsoft Edge.

1. `python materials.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. `python verify_browser.py` and `python verify_extended.py`
5. Run Blender as above with `verify_source.py`, `verify_parity.py`, `verify_features.py`.

`author.py` reopens the INCLUDED `mechanism.blend`; it overwrites manual edits to morocco.blend. The final generator defaults to pass 3. Historical pass screenshots are preserved evidence, not a promise that later final corrections are disabled by the pass flag. `refine.py` records the one-time transformation of the v1 script and is not a regeneration entrypoint. `review.py` needs sibling v1 and the original reference path to regenerate historical comparisons; core author/build scripts are folder-relative. No node_modules or credentials in source ZIP.

## Scope
Only preview/morocco-atlas-v2 and this delivery were authored. Prior Morocco v1, Iceland/Japan, production docs, chain nodes, funds, minting and deployment were untouched. Packaging asserts required files including GLB, reads each ZIP entry back, checks copied hashes, and opens the delivery HTML itself offline. See JSON evidence and inventory.
