# Haiti v1 — Cut Steel & Garden

Open **haiti-v1.html** directly in Edge/Chrome: complete embedded interactive model, maps, runtime and real Blender-rendered poster. Drag/touch rotate, open/close lid, reset; reduced motion supported. Local art only, not minted, hosted, on-chain or a custody operation.

## Design and visual verdict
A wide hammered blue-charcoal steel keepsake box with warm brass fittings and an invented low-relief leafy garden, inspired by Haiti's Croix-des-Bouquets cut-metal tradition. See the pre-model research-backed `design-brief.md`. No copied artist composition, sacred motif, photographic texture or claim of Haitian artisan manufacture. Procedural Blender geometry and seeded generated maps, not hand-sculpted art.

Actual source and mobile screenshots were visually inspected. The box, motif, Haiti copy and controls are readable and unclipped. The metal is visibly blue-gray and mottled rather than convincingly hand-hammered dark steel. Leaves are angular, silver and folded-looking; the original openwork silhouette has real gaps down to a **solid** lid, not holes through the container. Low relief is approximately z 2.075 maximum against lid top 1.978. Brass is clean and uniform. Mobile fine details and dark feet have limited contrast. This is a stylized craft-inspired interpretation, not photoreal equivalence, geographic/botanical accuracy or an approved artisan reproduction. No per-asset human approval claimed; user waived review until collection integration.

## Verified
- Saved .blend independently reopened. 54 moving + 39 static meshes; 81 poses with **zero unintended surface intersections**. Latch-versus-lid included. Only explicit original mating bearings excluded. Ten fixed/moving hinge attachment contacts checked. Interior ray reaches floor z 0.265. Sampled surface checks, not continuous collision or manufacturing certification.
- Pivots compared independently to included mechanism.blend: maximum matrix error 0. Exact staged 80-degree latch release before 105-degree opening, tested at 81 progress values.
- Source/export nearest-vertex error 1.712013073529306e-7 (<1e-5). Three packed portable maps. Runtime GLTFLoader: 93 meshes, 15,500 triangles, four materials; zero nonfinite vertices or degenerate triangles.
- Twelve garden leaves, 38 garden meshes, all lid-owned; max ornament z 2.0749833583831787. Ray probes distinguish open gap from stem. Deliberately detached leaf rejected by the same ancestry assertion, then restored (in-memory test only). Invalid runtime-asset negative control also rejected.
- Actual 256px color/roughness/normal decoded ranges 35/50/19; roughness measured in glTF green channel. Actual rendered poster checked nonempty.
- Offline file:// Edge desktop 1440x1080 and touch-emulated 390x844: drag/touch rotation, native controls, open/close, interrupted reset, reduced motion, no HTTP requests, runtime errors or overflow. Open projection maximum absolute NDC ~0.8924. Actual corrupt GLB reaches parser and shows poster; no-JS poster tested. RTX 4060 desktop; mobile emulation is not phone hardware performance.
- `inventory.json` gives exact bytes and SHA-256; `delivery-check.json` validates explicit required artifacts and every archive entry by readback. ZIP includes source, GLB, maps, scripts, viewer and evidence; excludes dependencies and backups. `.gitattributes` preserves exact bytes.

## Failures / fixes
Optional Codex implementation lane exited with 401 refresh-token failure; no changes accepted, no credentials accessed or modified. Hermes authored and tested directly. Initial build failed because the specified main-checkout node_modules directory was empty; installed the pinned existing package dependencies only in this new preview folder, then rebuilt successfully. This was a tooling failure, not an acceptance waiver. Deliberate negative controls are regression proof, not claims of test-first authoring. No model collision or parity failure occurred.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge, Node.js with Three/esbuild (package-lock included). `npm ci --no-audit --no-fund` here. Node.js is build tooling only, never a blockchain node.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
5. `python package_delivery.py`.

Regeneration overwrites authored source, GLB, renders and evidence. The included mechanism is derived from the Japan pilot at base ff5d78f; viewer and validation lineage is Japan/Iceland. Source authoring is self-contained. Build prefers local dependencies and otherwise checks sibling Iceland dependencies; runtime has no external dependencies. Three.js license included. No shared kit, production directory, chain, VPS or other preview was modified. Branch backup only; integration/hosting is a separate task.
