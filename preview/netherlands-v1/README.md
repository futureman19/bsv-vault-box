# Netherlands v1 — Delft & Polder

Open `netherlands-v1.html` directly in Edge/Chrome: a self-contained, offline 3D collectible with drag/touch rotation, Open/Close, Reset and reduced motion. **HTML 2,983,539 bytes; GLB 1,629,036 bytes.** No server, wallet, blockchain node or network is needed. Not minted, deployed or merged.

## Design and visual result
An ivory/cobalt ceramic-inspired keepsake box with invented floral medallions, brass fittings, eight low field parcels, a blue canal grid and an abstract four-sail windmill. Research and the pre-model visual contract are in `design-brief.md`. No museum images, copied historic pattern, trademark or maker mark is embedded. This is procedural Blender geometry and generated maps, not hand-painted authentic Delftware, photogrammetry, a geographic survey, or a photoreal reconstruction.

Actual source poster and final desktop/mobile browser images were inspected. Broad ceramic motifs and the four-sail mill are legible; the full model fits the tested views. One bounded correction widened the canal gaps after initial mobile inspection. The final canal grid is visible but still pale/low-contrast at phone size. The box is cleaner and more regular than real handmade ceramics; miniature fields/mill are deliberately simplified, mill sails are static, and rear-open views crowd the mill near the lower lid edge. No human per-asset art approval or physical-phone performance claim is made.

## Verified on delivered bytes
- Actual Three.js GLTFLoader: **19,738 triangles, 91 meshes, 10 materials**, zero nonfinite vertices and zero degenerate triangles.
- Independently reopened `netherlands.blend`: **52 moving and 39 static meshes, 81 sampled poses, zero unintended surface intersections**. Includes all landscape/mill parts and latch-versus-lid tests; only the documented mating hinge leaf/barrel and latch knuckle/bridge/pin bearing pairs are exempt. This is sampled surface-intersection evidence, not continuous solid-volume or manufacturing certification.
- Original pivot matrices match included `mechanism.blend`; 80-degree latch release precedes 105-degree lid opening. Ten hinge attachment overlaps pass; hollow interior floor ray hits z=0.2650000155.
- Bidirectional saved-source/export nearest-vertex maximum error **2.384185791015625e-7**, below 1e-5. Two packed procedural 512×512 maps match the portable workflow. Runtime color red-channel range 217; roughness **green-channel** range 28.
- Independent theme checks: eight fields, four sails, 36 lid-owned ornaments, five exposed perpendicular-waterway rays, every field sampled by a world-coordinate surface ray, and no inherited cedar/moss/granite country ornaments. The real runtime mill was temporarily detached; ancestry validation rejected it and passed again after restoration.
- Offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: native Open/Close, drag/touch rotation, interrupted Reset, reduced motion, no overflow, zero external HTTP requests, zero runtime errors. Full-open maximum absolute projected NDC 0.892365. Real corrupted GLB bytes reached the loader and produced the poster fallback; no-JS poster separately checked.
- Browser ran on NVIDIA RTX 4060 via ANGLE/D3D11. Emulation is not a physical phone test, FPS benchmark or long-duration test.
- Poster rendered from the current Blender source (nonblack/nontransparent pixels checked), never an AI promotional replacement. Rear-open and mobile screenshots come from the actual offline HTML.

## Failures, fixes and provenance
`initial/theme-local-coordinate-failure.txt` retains a real assertion failure caused by querying child-local coordinates as world-space rays. The check now uses `matrix_world.translation` and exact field-name assertions. A second retained failure (`theme-sail-occlusion.txt`) hit the mill sail above one field; the sample was moved to a known exposed corner of every parcel, without weakening the surface-name gate. The initial narrow-canal mobile view is retained; wider parcel gaps are the only visual correction.

The requested shared dependency directory existed but was empty; initial build failed with missing esbuild. Exact pinned dependencies were installed locally in this new folder, not upgraded or written into another preview. The optional Codex lane failed HTTP401 before editing; `codex-lane.log` records that failure. Hermes authored and independently executed all final work; no Codex output was accepted.

Mechanism, generic helper/hardware functions, viewer, collision and parity harness lineage: repository Japan pilot at base commit `ff5d78f`, itself based on Iceland. The trimmed mechanical baseline is included. Theme geometry, maps and assertions are newly authored. Three.js 0.180.0 is MIT (`THREE-LICENSE.txt`); esbuild 0.25.11 is build-time only.

## Reproduce
Python with Pillow/numpy/playwright; Blender 5.2.1; Node; Edge. From this directory:

```text
npm ci --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python run_checks.py
python package_delivery.py
```

`run_checks.py` runs build, motion contract tests, independent saved-source collision/theme/parity checks, actual desktop/mobile browser and extended checks. It exits nonzero on failure and saves raw logs. Edit the Blender executable path if installed elsewhere. `build.py` prefers local dependencies, with sibling Iceland dependencies as an optional fallback; none are needed to view the final HTML. Authoring overwrites model/poster output—preserve manual edits separately. The archive contains the mechanical baseline, maps and scripts, not node_modules or .blend1 backups.

`inventory.json` gives exact byte counts and SHA-256 identities. `delivery-check.json` verifies the explicit required artifact set, archive entry set and every archived byte hash on readback. It excludes itself, inventory self-hashing, archive self-hashing and volatile packaging/git logs to avoid recursion. Folder-local `* -text` preserves exact Git payload bytes. Hashes prove integrity, not origin authentication, custody or durable hosting.

## Scope and next step
Additive-only `preview/netherlands-v1/`; backup branch `art/netherlands-v1`. No changes to other art/previews, production docs, vault, mint, evidence or VPS. Collection direction remains 201 equally one-of-one designs; this cosmetic inner box neither opens a seal nor changes on-chain state. Next: the separate collection integration card merges the backed-up asset branch and assembles the full review gallery.
