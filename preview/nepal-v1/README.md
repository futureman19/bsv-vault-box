# Nepal v1 — Himalayan Slate & Snow

Open **nepal-v1.html** directly in Edge/Chrome. Fully embedded offline collectible: **2,226,746 HTML bytes**, **1,067,188 GLB bytes**. Drag/touch rotation, staged Open/Close lid and Reset; reduced-motion preference and actual-source poster fallback. This is an inner cosmetic collectible, not the outer custody container. Not minted, hosted, chain-verified or deployed.

## Design and honest visual verdict
A slate-blue wide case with three faceted snowy Himalayan ridges and restrained satin brass. `design-brief.md` preceded model authoring and cites UNESCO Sagarmatha landscape descriptions. Mountains are invented miniature forms, not an accurate Everest model. No sacred symbols, third-party photographs, scans or AI promotional substitutes. Geometry and maps are script-authored, not artisan hand sculpture.

Actual source/mobile inspection confirms three separate visible snowy summits, seated terrain, readable case and unclipped default framing. The body remains visibly procedural: regular mineral bands can read as brushed/corrugated metal or wood grain rather than convincing natural slate. The dark seam and inherited long clasp are conspicuous; poster shadows retain render noise. This is a stylized first version, not photoreal equivalence. No per-asset approval is claimed; the explicit collection-wide no-review directive applies.

## Verified evidence
- `source-check.json`: independently reopened saved source, 19 moving and 39 static meshes, all **81 sampled poses**, zero unintended surface intersections. Includes every mountain and latch-versus-lid checks. Only named coaxial hinge leaf/barrel and latch knuckle/bridge/pin bearings exempt. Ten hinge attachment intersections; hollow floor ray z=0.2650000155. Sampling is not continuous mechanical certification.
- `parity-check.json`: bidirectional evaluated source/export nearest-vertex maximum error **1.712013073529306e-7**, under 1e-5. All three source maps packed.
- `theme-check.json`: three snow ridges, lid ancestry, seated roots, exact contracted peak heights, separate ornament bounds and two-material slopes. `theme-negative.json` and its raw output retain a real failing detached-mountain control; reopening the untouched source restores PASS. This is a post-implementation regression control, not test-first evidence or an art repair.
- `motion-output.txt`: two actual Node tests PASS; rejects missing pivot/nonfinite/empty asset; 80° latch first, 105° lid second.
- `browser-check.json`: actual GLTFLoader, 14,062 triangles / 61 runtime meshes / 6 materials; zero degenerate or nonfinite vertices. Desktop 1440×1080 and touch-emulated 390×844 offline file:// controls, drag, reset mid-motion, reduced motion, no external requests/errors/overflow. Open projection max |NDC| **0.8923646516630198**. Actual corrupt GLB parser input triggers poster fallback. `extended-check.json` verifies no-JS poster, country copy/aria-label and decoded base-color/green-channel roughness variation.
- Physical mobile devices/FPS, full continuous collision, hidden geographical correctness and manufacturing tolerances were NOT tested. Browser used desktop NVIDIA RTX 4060.
- `inventory.json` contains exact SHA-256/byte inventory. `delivery-check.json` verifies required source/GLB/HTML assets, all archived bytes and ZIP readback. `.gitattributes` preserves exact bytes in Git.

## Source and reproduction
`nepal.blend` editable packed source; `nepal.glb` portable model; `poster.png/jpg` actual source render; maps and scripts included. `mechanism.blend` is the unchanged Japan pilot's trimmed family articulation/interior/hardware. Shared art/vault-kit and previous previews remain unchanged. `adapt_author.py` records one-time lineage construction and requires sibling Japan; generated `author.py` itself is standalone.

Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node and pinned Three.js 0.180.0/esbuild 0.25.11. Shared pilot dependency folder was empty; dependencies installed only in this preview's ignored node_modules. Three MIT license included. Build dependencies are not runtime network dependencies.

```
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme.py
python build.py
node --test --test-reporter=tap tests.mjs
python verify_browser.py
python verify_extended.py
python package_delivery.py
```
Run from this folder, with Blender on PATH or its quoted executable path. Regeneration overwrites source/render/export and requires rechecking/repackaging. Negative control: run verify_theme.py with trailing `-- --negative`, expecting exit 1; normal rerun passes without weakening assertions. Optional Codex lane failed authentication before editing; direct Hermes implementation and verification followed. No credentials changed. Raw lane output is diagnostic only.

Next: integrate this backed-up asset branch in the separate collection integration card; no merge performed here.
