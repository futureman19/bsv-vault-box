# New Zealand v1 — Fiordland / Stone & Tide

Open **new-zealand-v1.html** directly in Edge/Chrome. Entire runtime, model, maps and actual-source poster are embedded. Drag/touch to rotate, open/close the lid, reset view; reduced-motion preferences snap movement. No server or runtime network is required.

- HTML: **3,135,783 bytes**, strictly below 5,000,000.
- GLB: **1,745,764 bytes**.
- Editable packed source: `new-zealand.blend`; included inherited `mechanism.blend` is the mechanical starting point.
- Maps: generated gneiss color, roughness and subtle normal at 512px; rock color at 256px. No scans or copied photography.
- Poster: `poster.png` and embedded `poster.jpg`, rendered from the actual source using Cycles (900×800, 24 samples, denoising off).
- Browser captures: desktop/mobile closed/open, rear-open, corrupt-input fallback and no-JavaScript fallback.

## Verified

`run_checks.py` rebuilds the HTML and executes real tests, stopping on any failure:

- Actual Three GLTFLoader: **14,572 triangles**, **60 runtime mesh primitives**, six materials; zero nonfinite vertices and degenerate triangles. Multi-material ridge meshes become separate primitives in the loader.
- Saved source reopening: 19 moving and 39 static source meshes, **81 motion samples**, zero unintended surface intersections. Latch versus lid also checked. Only inherited explicitly named mating bearings excluded. Ten physical hinge attachment pairs overlap. Hollow interior ray reaches floor at z=0.2650000155.
- Independent source/GLB nearest-vertex parity in both directions: max error **1.712013073529306e-7**, below 1e-5.
- Independent exact inherited pivot matrix/parent comparison against the included mechanism source.
- Two lid-owned asymmetric ridges with peaks below 2.80 and outer edges seated into the lid. Continuous water ribbon and 17 unobstructed centreline water rays. Real detached-ridge negative control fails the same ancestry assertion.
- Portable color/roughness/normal variation decoded in-browser. Roughness sampled from green, its actual glTF channel. Poster pixel-content check and absence of inherited Japan/Cedar copy.
- Offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, drag/touch rotation, interrupted reset, reduced motion, no horizontal overflow, zero external HTTP requests, zero unexpected JS/console errors. Fully open projected geometry fits viewport (max absolute NDC ~0.916).
- Actual GLB parser receives corrupted bytes and falls back to the poster with disabled controls; no-JS poster also tested.
- `inventory.json` gives exact SHA-256/bytes. `delivery-check.json` records required files, ZIP readback and byte ceiling. Git staging hashes are independently compared before commit.

## Visual limits and scope

A stylized Fiordland-inspired collectible, **not photorealism, a surveyed Milford Sound model, traditional craft, or human-approved artwork**. The frozen research-backed brief preceded modeling. Green slopes suggest forest without individual trees. The water reads as an inset turquoise channel rather than physically simulated deep water. Pale faceted ridges and repeated foliation are visibly procedural; the body pattern can read as wood grain. Terrain and water are lightweight open relief surfaces, not watertight manufactured solids. In the front open view the thin inherited hinge/strap connectors are visually inconspicuous, despite passing attachment tests. All lid ornament is behind the raised lid from that angle; rear-open capture shows it remains attached.

Collision evidence is sampled surface intersection, not continuous swept-volume/engineering proof. Mobile is emulation on desktop RTX 4060, not physical-phone performance. No FPS or on-chain/custody verification claimed. This is the inner collectible; lid motion is cosmetic. No keys, chain nodes, mint, broadcasts, VPS, deployment or production files were touched. Collection direction: 201 equal-edition one-of-one designs, with no launch accessories.

## Reproduce

Requires Blender 5.2.1, Python with Pillow/numpy/Playwright and installed Edge, and Node build tooling. The runtime HTML requires none of those build dependencies. From this folder:

```text
npm ci --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python run_checks.py
python package_delivery.py
```

Adjust the Blender path in `run_checks.py` on another system. Source and tests resolve inputs relative to this directory. Regeneration overwrites editable output; preserve manual edits separately. `prepare.py` was a one-time adaptation helper and is not part of the deliverable. Mechanism/viewer/test lineage is Japan Cedar v1 on base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8; source scripts are included locally. Three 0.180.0 MIT license is included. No dependencies or credentials included in archive.

`failures-and-limits.md` describes the genuine missing-esbuild failure/fix and optional Codex auth failure. All accepted implementation and verification was performed directly by Hermes; no Codex changes were accepted. The final asset branch is backed up only; integration is a separate task.
