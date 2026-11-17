# The Moon v1 — Regolith & Impact

Open `the-moon-v1.html` directly in Edge/Chrome. Drag/touch to rotate, open/close the lid, reset, or use reduced-motion preferences. Everything needed at runtime is embedded: no server, external image, CDN, wallet or network connection. This is a cosmetic inner collectible study, not the functional outer custody container. Not minted, deployed, signed or stored on-chain.

## Design and provenance

The pre-model `design-brief.md` cites NASA's Moon Facts and Moon Composition for regolith, bright highlands, dark basalt maria and impact craters. No NASA images or logos are included. This is an independently generated, stylized composite, not a geographic model or a claim of lunar craft traditions. Gold hardware is collection fantasy. All designs in the planned 201-item collection have equal one-of-one edition scarcity.

A gray rocky box carries a continuous sculpted lunar surface with three unequal bowl craters, a dark main basin and subtly darker small floors. Actual crater diameters are 1.04, 0.51 and 0.38 units. Rim-to-floor relief is measured from saved geometry, approximately 0.18–0.21 units. Body is 3.72 units wide; lid is 2.38 deep. The inherited mechanical body's stone walls end at z=1.56, seam top about 1.672 and lid top 1.978: these retain the source mechanism instead of the brief's approximate 1.9–2.1 body-top wording. The finished closed form including terrain tops out near 2.21. No pivot relocation.

## What was verified

- Build exact HTML/GLB counts: `delivery-check.json`; standalone HTML strictly below 5,000,000 bytes.
- Actual Three GLTFLoader: 56 meshes, 26,524 triangles, 5 materials, zero nonfinite vertices or degenerate triangles. Portable color and roughness map ranges decoded from actual textures; roughness sampled from GREEN. Maps max 512px.
- Independently reopened `.blend` and independently imported GLB: bidirectional maximum nearest-vertex error 1.712013073529306e-7 units, below 1e-5. Four packed source images.
- Inherited hinge/latch matrices compared against included `mechanism.blend`; saved-source terrain parentage checked, detached-terrain negative control rejected. Geometric rays measure all three bowl floors and rims.
- 81 opening poses include all 17 moving meshes against all 39 static meshes, plus releasing latch against moving lid: zero unintended surface intersections. Only named coaxial hinge/latch mating bearings excluded. Ten actual intersecting attachment pairs connect body bridges, mounts, stems and moving leaves. Hollow floor ray hits z=0.265.
- Motion unit tests check first-quarter 80-degree latch release before 105-degree lid opening, clamped endpoints, and rejected missing/empty/nonfinite asset contracts.
- Actual offline `file://` Edge desktop and 390x844 mobile touch emulation: native open/close, drag/touch rotation, interrupted reset, reduced motion, full-open viewport fit, no horizontal overflow, no external HTTP requests or JS errors. A genuinely corrupted GLB reaches the loader and shows the source poster; no-JS poster checked separately.
- ZIP required-artifact inventory and every entry read back exactly. Byte-preserving folder-local Git attributes; committed/indexed inventory independently verified before push.

## Honest visual and technical limits

This is a stylized procedural product model, not photorealistic regolith, scan data or a scientific reconstruction. Broad mottling can read as marble/chalk; the small craters are subtle at phone size. Gold hardware is simplified, the long inherited latch is conspicuous when open, and the rear attachments can be hidden in a front view even though their geometry/contact checks pass. The dark area is a mare-inspired crater floor, not an accurately mapped broad lunar sea. Small-floor darkening is a readability accent, not measured lunar albedo. The source poster uses modest Cycles samples without denoising and retains slight grain.

Collision checks sample surfaces, not continuous or volumetric physics/manufacturing proof. Mobile is emulation on desktop RTX 4060, not physical-phone performance. Visual inspection is separate from numerical acceptance; there is no claim of prior human approval or exact reference equivalence.

## Real failures and bounded corrections

`initial/missing-toolchain.txt` preserves the first real build failure: the inherited node_modules directory existed but was empty, so esbuild could not load. Restored declared build dependencies locally in this new folder; no sibling files changed. Optional Codex lane exited with OAuth 401 before editing; direct Hermes implementation replaced it, and its failure log is retained without credentials.

`initial/poster-before-polish.png` retains the stepped dark-floor boundary from per-face material assignment. A terrain-local color map replaces that boundary while preserving the bowls. `initial/mobile-low-view.png` records the inherited low camera hiding crater floors. The final camera is higher; small floors also receive restrained contrast. These are visual corrections, not waived acceptance thresholds. All final checks ran again on the final bytes.

## Files and reproduction

`the-moon.blend` is editable script-authored Blender source; `the-moon.glb` is the standalone export. `poster.png` and `poster.jpg` are actual-source renders, never generated promotional substitutes. Browser PNGs are actual model captures. `inventory.json` records exact payload SHA-256/bytes; `delivery-check.json` records ZIP readback and envelope hash. `the-moon-v1-source.zip` contains source, maps, GLB, viewer and evidence but no dependencies, backups or caches.

Environment: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge; Node with the included package lock. From this directory:

```text
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python run_all.py
node --test tests.mjs
python package_delivery.py
```

`run_all.py` independently rebuilds the viewer and runs source, parity, theme, browser and extended checks; it does not regenerate geometry. `author.py` and maps operate using this folder only. `setup.py` documents the initial derivation from the sibling Japan pilot and is not required to rebuild the delivered source; it requires that sibling if intentionally rerun. Regeneration overwrites source/output and changes hashes; regenerate the inventory afterward. Three runtime MIT license included. Mechanism/viewer/test lineage is the Japan pilot at repository base ff5d78f1e0d486af5c882c184fc08049996ebdc8. No other previews, shared kit, production docs, minting or chain systems modified.

Next: integrate this backed-up branch with the full collection through the separately assigned final integration card, not a direct merge/deployment here.
