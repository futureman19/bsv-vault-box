# Finland v1 — Birch & Blue

Open **finland-v1.html** directly in Edge/Chrome: **4,409,811 bytes**, with the **2,711,868-byte** GLB, runtime, maps and actual-source poster embedded. No server or network needed. Drag/touch to rotate, Open/Close lid, Reset; reduced motion is supported. Cosmetic inner collectible only: no mint, wallet, chain action, hosting or custody-state change.

## Design and visual limits
A pale bark-inspired box with honey birch-wood lid, brass hardware, granite feet and a low blue lake medallion carrying three green islands. The pre-model `design-brief.md` cites ThisisFINLAND, Mustila and Visit Finland. These are material/landscape inspirations, not copied imagery or an authentic historical construction. All geometry/maps are procedural; no scans, AI poster, or human hand-sculpture claims.

Actual source and mobile screenshots show the complete box, exposed blue water and all three islands. Bark reads pale and horizontally marked, but at mobile scale can also resemble whitewashed boards; islands are deliberately simple flat-topped reliefs, not realistic forest. Lake is raised enamel-like decoration, not a physically recessed or transparent lake. Source render has sampling grain. Rear and interior are family-mechanism extrapolations. No photoreal equivalence or named-lake accuracy is claimed. Per-asset human review was waived; this is not an assertion of human art approval.

## Verified evidence
- `source-check.json`: independently reopened saved source; 32 moving and 99 static meshes; **81 sampled poses**, zero unintended surface intersections, named bearing exclusions only; hollow floor ray z 0.2650000155. Ten physical hinge-attachment pairs tested. Sampling is not continuous collision/mechanical certification.
- `parity-check.json`: source/export nearest-world-vertex error **1.712013073529306e-7**, below 1e-5; five packed source maps. Re-export byte identity is not claimed.
- `theme-check.json`: four lid-owned ornaments, three islands; original mechanism pivot positions retained; bounded silhouette/heights and five exposed-water ray checks.
- `negative-control.txt`: deliberately detaching one island produces **AssertionError: Ornament detached from lid**, nonzero Blender exit. This is a regression negative control, not a discovered art defect or test-first claim. Production source unchanged.
- `browser-check.json`: actual GLTFLoader, 131 meshes / 28,396 triangles / 8 materials; zero nonfinite vertices or degenerate triangles. Offline file:// desktop 1440x1080 and mobile 390x844 touch emulation: rotation, native buttons, open/close, interrupted reset, reduced motion, no overflow, no external HTTP requests, no JS errors. Full-open projected absolute NDC maximum 0.926991 (<1).
- Actual corrupt GLB reaches the parser and shows the poster with disabled controls. `extended-check.json` verifies no-JS poster, actual decoded color/green-channel roughness variation, lid ancestry and Finland copy/accessibility label.
- `motion-output.txt`: 2 tests pass, 0 fail; staged 80-degree latch then 105-degree lid and invalid-asset rejection.
- `delivery-check.json` / `inventory.json`: exact bytes/SHA-256 and ZIP contents readback. `.gitattributes` preserves bytes through Git checkout.

Browser ran Edge/RTX 4060; mobile is emulation, not physical phone performance. No FPS, long-duration reliability or general browser compatibility claim.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node and pinned package.json dependencies. Shared pilot node_modules was empty; `initial-build-failure.txt` retains the real MODULE_NOT_FOUND build failure. Installing the unchanged pinned dependencies **in this folder only** fixed it; node_modules is excluded from delivery. No sibling preview or base kit was modified.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this folder.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender the same way for `verify_source.py`, `verify_parity.py`, `verify_theme.py`. For the intentional failing control append `-- --negative`.
5. `node --test --test-reporter=tap tests.mjs`; `python build.py`
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`

`author.py` is self-contained with the included trimmed `mechanism.blend`; optional `adapt.py` documents the one-time derivation from the sibling Japan author and is not needed to rebuild. Regeneration overwrites generated outputs; copy the source before manual changes. Viewer/motion/verification lineage: Japan pilot on base ff5d78f; Three.js MIT license included. `poster.png` is rendered from the saved source, not a promotional substitute. `finland-v1-source.zip` contains source, standalone GLB/HTML, maps, scripts and evidence, excluding dependencies/backups.

Only this new folder is delivered. Branch backup is not a merge or deployment. Next: integrate with the full 201-piece collection in the separate final card.
