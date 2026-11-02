# Equatorial Guinea v1 — Bioko basalt & rainforest

Open **equatorial-guinea-v1.html** directly in Edge/Chrome. This self-contained collectible contains its real 3D model, maps, runtime and source-rendered poster. Drag/touch to rotate, open/close the lid, or reset. Motion respects reduced-motion preferences.

- HTML: **2,747,578 bytes**, strictly below 5,000,000.
- GLB: **1,519,756 bytes**.
- Editable packed source: `equatorial-guinea.blend`; reproducible geometry: `author.py`; generated color/roughness/normal maps: `maps/` and `maps.py`.
- `mechanism.blend` is the unchanged trimmed Japan articulation/liner baseline, not Japan's cedar art. All country-specific art is newly authored. Shared kit and older previews were not edited.
- `poster.png` and `poster.jpg` are actual Blender renders, not AI promotional substitutes. Desktop/mobile screenshots are actual offline Edge captures.

## Design and honest visual outcome

The prior-written `design-brief.md` cites Smithsonian GVP for Bioko's basaltic shields and broad Luba caldera, and an ecology overview for rainforest context. The low forested relief is an original compressed landscape synthesis, **not exact geography, a scan, species-specific forestry, or a comprehensive cultural representation**. Hardware is fictional collection styling.

Final source-render inspection found a coherent wide stone chest, low broad terrain, mostly exposed caldera rim and no obvious detached components. Remaining limitations: smooth clay-like terrain rather than detailed exposed basalt, abstract canopy cushions rather than individual trees, clustered rear-right foliage, a small shaded crease, and gray stone under bright studio lighting rather than deep black. No photorealistic/reference-equivalence claim. Independent source checks establish all 72 canopy meshes contact terrain. The last attempted automated visual reading of the mobile screenshot failed with provider HTTP 402; mobile DOM/geometry/interaction/screenshot checks passed, but no separate semantic mobile visual verdict is claimed.

## Verification actually exercised

- Saved source independently reopened: hollow interior floor at z=0.2650000155; ten hinge attachment pairs; original lid/latch pivot locations retained.
- **81 sampled staged opening poses, all 89 moving and 45 static meshes**, plus latch-versus-lid tests: zero unintended surface intersections. Only named hinge leaf/barrel and latch knuckle/bridge/pin bearings exempt. This is sampled surface-intersection evidence, not continuous collision proof or physical hardware certification.
- Real GLTFLoader: 22,556 triangles, 134 meshes, nine materials, zero nonfinite vertices/degenerate triangles. Actual decoded portable maps are varied and 512x256; all 72 canopy meshes and terrain remain attached to lid.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed maps. This is world-geometry parity, not exact material lighting equivalence or GLB byte-identical re-export.
- Caldera measured floor z=2.0205385685; minimum of four sampled rim elevations exceeds it by **0.2706515789**. Relief height and footprint, lid dimensions, map inventory and exact baseline pivots asserted.
- Offline `file://` desktop 1440x1080 and mobile 390x844 touch emulation: native open/close, touch drag/mouse rotation, interrupted reset, reduced motion, no overflow, full-open projected framing, no external HTTP requests or JS errors. Actual corrupt GLB parser failure shows poster; no-JS poster also verified. Mobile emulation on desktop RTX 4060 is **not physical-phone performance testing**.
- Node motion tests exercise 81 poses, endpoints and rejected invalid-asset negative controls. `package_delivery.py` checks acceptance JSONs, final embedded GLB/poster bytes, strict HTML cap, exact inventory and every ZIP entry on readback. Inventory excludes itself and delivery envelopes to avoid recursive hashes.

## Genuine failures and bounded correction

The initial independent theme check failed the predeclared relief-height ceiling (<0.65 above lid). `initial/theme-source-output.txt` retains that actual assertion failure; `initial/poster.png` and `initial/desktop-closed.png` retain the earlier visual. Reduced overlapping rim/shield amplitudes and moved canopy centers off the inner rim, then regenerated and reran every final gate; no threshold was relaxed. A temporary incomplete author-script edit also triggered syntax lint before execution and was fixed. A shell-shim Node invocation returned `stdin is not a tty`; the actual test rerun used the installed native Node executable. Optional Codex lane exited 1 with 401 refresh failure and produced no accepted changes; Hermes authored and tested this delivery directly. No credentials were altered.

## Reproduce

Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node with Three 0.180.0/esbuild 0.25.11. Build uses local `node_modules` when present, otherwise sibling `iceland-pilot/node_modules`. Install dependencies in this directory for standalone source reproduction; dependencies are not included in archive. All runtime dependencies are embedded in HTML. Three MIT license included.

Run from this directory:

```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
node --test tests.mjs
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme_source.py
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

On this Windows host Blender is `C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe`; native Node is `C:/Program Files/nodejs/node.exe`. Authoring overwrites model/poster; preserve manual edits separately. Package script never writes outside this asset folder. Logs and JSON evidence are in-folder; `inventory.json` lists exact SHA-256/bytes, `delivery-check.json` gives source ZIP identity and readback verification.

## Scope

Local art only: no blockchain node, keys, wallet, mint, transaction, deployment, VPS or custody verification. Cosmetic opening is reversible and does not break an on-chain seal. The 201-design collection remains one-of-one per design; this card neither issues an NFT nor merges into production. Branch backup only; collection integration remains separate. Per-asset human review waived by task directive, not claimed as human art approval.
