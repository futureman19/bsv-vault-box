# Syria v1 — Damascus / Walnut & Pearl

Open **syria-v1.html** directly in Edge/Chrome. All runtime assets are embedded; no server or internet required. Drag/touch rotation, Open/Close lid and Reset view; reduced motion supported. Cosmetic movement only, not opening any custody seal.

- HTML: **4,011,089 bytes** (strictly below 5,000,000).
- GLB: **2,399,936 bytes**.
- Editable packed `syria.blend`, reusable `mechanism.blend`, procedural maps and reproducible scripts included.
- `poster.png` and its embedded JPEG are actual source renders, not promotional illustrations. Desktop/mobile PNGs are actual offline browser captures.

## Design and limits
Damascus-inspired walnut and pearl craft, grounded in the sources cited in the pre-model design brief. Three invented eight-point rosettes (24 solid pearl lozenges), 34 lid-border diamonds and 38 front diamonds. No third-party photograph/pattern was copied. The model is procedurally authored, not hand-crafted furniture or a reproduction of a historical chest.

Actual render inspection: coherent brown/cream/brass identity, readable ornaments at mobile size, no obvious detached parts or unintended clipping. The pearl is opaque satin, not spectral nacre; shallow applied ornament approximates inlay, not flush cut joinery. Wood remains regular/banded; dark seam is conspicuous; small stone feet are a family extrapolation. Fine rosette detail is small at mobile size. The fully released latch protrudes above the open lid and can look weakly seated at this scale; open-view visual inspection could not resolve every bearing contact, although saved-source attachment/collision checks pass. Not photorealistic or user-approved artwork. Initial front inserts appeared as tabs: corrected their rotation to face the front as diamonds. `initial-poster.png` preserves that earlier render.

Brief deviation: four compact maps are delivered rather than three (separate end-grain map retained). All are <=512 pixels per dimension and the payload cap remains strict. Rear/interior and hardware are family interpretations, not historical findings.

## Verified evidence
- `source-check.json`: saved-source reopened, hollow floor ray z=0.2650000155; **81 sampled poses**, **86 moving / 137 static meshes**, zero unintended surface intersections. Every lid ornament is included; only named mating bearings excluded. Ten hinge attachment pairs pass. Sampled surface testing is not continuous collision/manufacturing certification.
- `parity-check.json`: bidirectional world-vertex maximum error **1.712013073529306e-7**, below 1e-5; four packed source images. This is geometric parity, not byte-identical re-export.
- `browser-check.json`: actual GLTFLoader **28,540 triangles, 223 meshes, 6 materials**, zero degenerate/nonfinite geometry. Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: drag, native controls, open/close, interrupted reset, reduced motion, no horizontal overflow, zero external HTTP requests/errors. Full-open maximum absolute NDC **0.892365**. Real corrupt GLB reaches parser and falls back to source poster.
- `extended-check.json`: live loaded ornament counts and lid ownership, decoded base-color and roughness-green map variation; no-JS poster; rear-open capture.
- `theme-check.json`: source ornament bounds/ownership/counts; deliberately detached in-memory ornament correctly fails the same ownership assertion (source not altered). No inherited cedar/moss terrain.
- `motion-output.txt`: two passing tests, including invalid asset rejection and latch-before-lid choreography, 80° then 105° endpoints.
- `delivery-check.json` and `inventory.json`: exact bytes/SHA-256, archive readback. Inventory excludes itself and ZIP/report envelopes to avoid circular hashing.

All technical acceptance gates pass. Mobile is desktop RTX 4060 emulation, not physical-phone testing; no FPS/performance, authentic craft, or photoreal-equivalence claims.

## Failures retained
`build-initial.txt` records a real MODULE_NOT_FOUND: shared node_modules was empty. Installed the existing pinned build dependencies locally in this new folder only; shared previews were not repaired. `package-lock.json` retains versions; node_modules is ignored and excluded from archive. The deliberate detached-ornament negative control demonstrates a failing feature oracle, not test-first modeling history.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node and pinned npm dependencies. Commands run from this folder:

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Regeneration overwrites the generated source/model/poster. Mechanism, viewer and test lineage: Japan cedar v1 inherited from repository base ff5d78f; its input source is included. Three.js MIT notice included. No shared base-kit modification, production integration, deployment, blockchain query, wallet/key access, mint, broadcast, or VPS operation. Branch backup only; integration is a separate card.
