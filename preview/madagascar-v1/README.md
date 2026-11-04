# Madagascar v1 — Tsingy / Limestone Forest

Open `madagascar-v1.html` directly in Edge. Complete offline 3D viewer: **4,066,641 bytes**; embedded GLB **2,495,436 bytes**. Drag/touch rotation, staged Open/Close, Reset and reduced motion. No server or network required. Cosmetic movement only; not minted, hosted, signed or chain-verified.

## Source and visual contract
Research-backed `design-brief.md` preceded modeling. UNESCO's Andrefana Dry Forests entry describes western Madagascar's sharp limestone needles and contrasting forest greens. No source photographs, protected-site materials, logos or third-party textures used. All maps and geometry are procedural, not scans, manual sculpture or geographical reconstruction. Reused Japan's trimmed mechanism and Iceland-derived motion/viewer harness, not their country artwork. Shared vault kit unchanged.

28 irregular tapered limestone pinnacles and 18 sheltered green patches travel with the lid. Pale fluted body, dark continuous hollow liner, brass fittings and stone feet. `madagascar.blend` is editable and contains packed maps; `madagascar.glb` is portable. `poster.png` is a real Blender source render; JPEG is its compressed embedded derivative. Screenshots are actual offline browser captures.

## Verified
- Blender 5.2.1 independently reopened source: identical inherited pivots, ten hinge attachment pairs, floor ray z=0.2650000155.
- 81 motion poses, all 62 moving and 111 static meshes, no unintended moving/static or latch/lid intersections. Explicit mating bearing contacts only excluded. This is sampled surface collision evidence, not continuous solid-mechanical certification.
- Source/export bidirectional vertex error 1.712013073529306e-7 (<1e-5).
- Actual GLTFLoader: 28,988 triangles, 173 meshes, five materials, zero nonfinite vertices or degenerate triangles. Runtime ancestry proves all pinnacles/green patches travel with lid. Decoded color ranges 45 and 72, compact 256/512px maps.
- Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native buttons, drag/touch rotation, open/close, interrupted reset, reduced motion; no external HTTP requests, errors or overflow. Full-open projected silhouette within viewport. Actual corrupt GLB parser failure and no-JS poster fallback exercised.
- Motion unit tests reject missing/empty/nonfinite assets; theme negative controls reject absent and detached pinnacles. Exact bytes/hashes and required artifacts checked by `package_delivery.py`; ZIP independently read back.

## Real failure and correction
`initial/extended-failure.txt` retains the first failed runtime texture-variation assertion. The resized dark cleft map had insufficient contrast for the unchanged >30 channel-range gate. Increased its procedural contrast, regenerated source/GLB/poster/HTML, then repeated source, parity, theme and browser checks. Final dark-map range is 45; no threshold was relaxed. Prior optional Codex lane failed authentication before producing accepted work (`lane-output.txt`); recovered implementation was reviewed and executed directly by Hermes.

## Honest visual limits
Actual source and mobile/open screenshots inspected. Limestone/brass and pointed silhouette read clearly; green lid patches are subtle at mobile size, with the seam more conspicuous. Peaks form a somewhat regular field rather than a surveyed dense blade-like tsingy labyrinth. Body flutes are regular and can read as paneling; interior map has procedural wavy markings. Gully vegetation is shallow relief, not deep carved ravines. Front-open view naturally hides exterior ornament behind the lid; rear-open capture shows it. Not photorealistic, not a claim to represent all Madagascar, and not physical-phone performance testing. No per-asset human approval claimed; task explicitly waived that review.

## Reproduce
Use Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1 and Node.js. `package.json` pins Three 0.180.0 and esbuild 0.25.11; Three MIT notice included. Build uses local node_modules or sibling Iceland dependencies, never a runtime download. For extracted source, run npm install here. Run:

1. `python maps.py`
2. `blender --background --factory-startup --threads 2 --python-exit-code 1 --python author.py`
3. Same Blender invocation for `verify_theme.py`, `verify_parity.py`, `verify_source.py`.
4. `node --test tests.mjs`; `python build.py`
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites authored outputs. Inventory excludes itself, delivery report and ZIP to avoid recursive hashing; excludes backups/dependencies. Source ZIP includes explicit HTML/GLB/Blend/maps/evidence requirements. Folder-local Git attributes preserve exact bytes. Branch backup only: no merge, deployment, blockchain activity or shared-base changes.
