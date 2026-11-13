# Tuvalu v1 — Pandanus & Lagoon

Open `tuvalu-v1.html` directly in Edge/Chrome. Entire runtime, model, maps and actual Blender-rendered poster are embedded. **HTML 2,841,887 bytes; GLB 1,537,496 bytes.** Not hosted, minted or chain-verified.

## Design and limits
Research-backed original written brief preceded modeling. A woven pandanus-inspired shell with red fibre borders surrounds the inherited hollow liner; the lid carries a low irregular ivory sand footprint and turquoise lagoon inset. Geometry and maps are procedural Blender authorship, not hand weaving, scans, or photogrammetry. This is an invented decorative interlace, not a claimed family/ceremonial pattern or surveyed Tuvalu atoll.

Actual desktop/mobile visual inspection found clear whole-box framing, readable woven pattern and lagoon motif, and a visible hollow open interior with no obvious detached parts. The weave remains regular/molded-looking; water is opaque decorative turquoise rather than simulated ocean; the source poster is grainy (16 samples, no denoising), borders appear lighter coral-red under lighting than the dark base-color target, and the narrow dark seam is conspicuous. Irregular coral-colored feet and brass hardware are collection extrapolations. No photoreal-equivalence claim; mobile is desktop-GPU touch emulation, not physical-phone performance.

## Verified evidence
- `source-check.json`: independent saved `.blend` reopen, 81 staged poses, all 18 moving and 47 static meshes checked; zero unintended surface intersections. Narrow named mating-bearing exemptions only. Ten hinge attachment pairs and hollow floor ray at z=0.2650000155. Sampling is not continuous mechanical certification.
- `parity-check.json`: source/export nearest-vertex maximum 1.712013073529306e-7 (<1e-5).
- `theme-check.json`: exact inherited pivot matrices, lid-owned relief, all 144 lagoon vertices contained in sand polygon, relief height 0.0870000572; detached-parent and outside-point negative controls rejected. Portable color/normal/roughness maps all 512 square.
- `browser-check.json`: actual GLTFLoader, 15,924 triangles, 65 meshes, six materials; zero degenerate/nonfinite vertices. Offline file:// desktop and mobile touch rotation, native open/close/reset, reduced motion; no external requests, errors or overflow; full-open projection <1. Genuine corrupted GLB falls back to poster.
- `extended-check.json`: actual decoded map ranges (roughness GREEN channel), no-JS poster, source poster nonempty, no inherited Japan copy.
- `tests.mjs`: 81 staged motion samples, 80-degree latch before 105-degree lid, endpoint clamps and invalid-asset rejection.
- `delivery-check.json` and `inventory.json`: exact bytes/SHA-256 and archive entry readback. `.gitattributes` preserves bytes across Windows Git checkout.

## Failure history
Optional Codex lane failed authentication before edits; no Codex changes accepted. Hermes implemented and tested directly. The first build genuinely failed because the main checkout's dependency directory was empty despite the requested link setup; `build-initial-failure.txt` retains that failure. Installing the declared art-only dependencies locally via `npm install --ignore-scripts --no-audit --no-fund` fixed it without changing asset checks. No geometric or browser acceptance gate was relaxed. Corrupt GLB and theme negative controls deliberately fail their underlying validators and are expected tests, not production failures.

## Reproduce
From this folder, Python requires numpy/Pillow/playwright, Edge installed, Blender 5.2.1 and Node for the art bundler (not a blockchain node).
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node tests.mjs`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`.

`author.py` is self-contained with included `mechanism.blend`; regeneration overwrites output. `create_author.py` records the one-time derivation and requires the sibling Japan author script; it is not needed to reproduce. Viewer/mechanism/source-test lineage is Japan v1 from repository base ff5d78f1e0d486af5c882c184fc08049996ebdc8. Three MIT license included. Research facts/links are in the brief; no third-party photos embedded. Source ZIP excludes dependencies, backups and Codex operational logs. No shared base kit, production folders, wallets, keys, VPS or blockchain systems changed. Branch backup only, integration deferred to the collection card.
