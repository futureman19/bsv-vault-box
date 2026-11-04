# Kiribati / Pandanus & Lagoon — brief-driven v1

Open **kiribati-v1.html** directly in Edge/Chrome. The complete model, textures, Three.js runtime and actual-source poster are embedded. Drag/touch to rotate, open/close the lid, or reset. Cosmetic movement only: this is an inner collectible art study, not the outer custody container.

## Delivered
- Standalone HTML: **2,372,100 bytes**, below the strict 5,000,000-byte ceiling.
- `kiribati.glb`: **1,154,512 bytes**, 14,912 triangles, 88 meshes, 10 materials as measured through actual GLTFLoader.
- `kiribati.blend`: editable named Blender source, packed maps. `mechanism.blend`: inherited trimmed family mechanism, copied without changing the shared kit.
- `maps/`: original procedural over/under fibre colour, normal and roughness at 512×256; coral-sand colour at 256×128. No harvested photographs, traditional pattern copies or scans.
- `poster.png` / `poster.jpg`: real Blender render; desktop/mobile closed/open screenshots and rear-open view are real offline browser captures. `review-board.jpg` combines those screenshots without changing their proportions.
- `kiribati-v1-source.zip`, `inventory.json`, `delivery-check.json`: source/evidence archive and exact byte/SHA-256 identities with every ZIP entry read back and checked. Archive excludes dependencies, caches and Blender backups.

## Design and visual judgment
The prewritten `design-brief.md` cites Tourism Authority of Kiribati material on atolls, lagoons, mat weaving and pandanus. `research-check.json` contains successful HTTP retrieval excerpts. The invented warm woven body, brown frame, teal lid and low C-shaped sand rim evoke that material/geographic combination; they are not an authentic traditional chest, a named island map, a specific weaving tradition, or a complete representation of Kiribati.

Actual desktop/mobile visual inspection accepts this as **stylized v1**, not photorealism or exact reference equivalence. Weave is regular and tile-like at close range; low vegetation is simplified rounded patches; the lagoon reads as a shallow decorative inlay. Coral-sand material identity is largely palette-based. The inherited long released clasp is conspicuous at full opening. Rear/interior and brass hardware are family fantasy details.

One bounded art correction replaced the initial rectangular turquoise outlet with a curved tidal passage and increased lagoon/lid colour separation. The initial poster/screenshot remain in `initial/`; no claimed prior user approval or supplied concept illustration exists. The final stills establish appearance only; execution tests below establish the separately tested interactions.

## Verified
- Independently reopened saved source, original lid/latch pivot matrices exactly matched to included baseline, 10 connected hinge attachment pairs, hollow floor ray z=0.2650000155.
- **81 sampled poses**, all **37 moving** and **51 static** meshes, zero unintended intersections. Latch-versus-lid also checked; only named original concentric mating bearings excluded. This is sampled surface-intersection checking, not continuous solid collision or manufacturing certification.
- Original motion: latch releases **80°** during first quarter, then lid opens **105°**; reverse closes lid first. Two Node unit tests pass, including malformed-asset negative controls and 101 pose samples.
- Source/export nearest-vertex error **1.712013073529306e-7** units, below 1e-5. Four packed maps in source. Geometry equality is tolerance-based, not binary-identical re-export.
- Real GLTFLoader: zero degenerate triangles, zero nonfinite positions. Runtime decoded weave colour/roughness/normal ranges 73/50/75; roughness measured in the correct GREEN channel. Sand colour range 18. Four woven panels and all 21 ornament meshes have correct lid ancestry.
- Independent rim/gap/lagoon rays and all 18 vegetation attachment rays pass; ornament z=1.9820–2.1936. Deliberately detached ornament rejected by the actual ancestry assertion. These are sampled structure/attachment tests, not ecological/hydrological validation.
- Offline `file://` Edge at desktop 1440×1080 and mobile 390×844 touch emulation: native buttons, pointer/touch rotation, opening/closing, reset during movement, synchronous reduced-motion pose, no horizontal overflow, no external HTTP requests or runtime errors. Open silhouette max absolute NDC 0.892365. Real corrupt-GLB input reaches loader and displays poster; no-JS poster also checked.
- Browser GPU: NVIDIA RTX 4060 via ANGLE D3D11. **Mobile emulation is not a physical-phone or FPS test.** No network access required by the viewer; research/build dependencies did use the network.

## Actual failure and fix
The first build genuinely failed with `MODULE_NOT_FOUND` for esbuild: the requested shared `preview/iceland-pilot/node_modules` location existed but was empty. `initial/build-missing-dependencies.txt` preserves the exact failure. Installed the pinned dependencies **inside this new preview only**, then reran the unchanged build-size gate successfully. No shared dependency directory or other preview was populated/modified. Initial geometry/browser gates passed; there was no hidden collision failure.

## Reproduce
From this directory, use Blender 5.2.1; Python with numpy, Pillow and Playwright; Node with the pinned package lock; installed Edge for browser tests. These are author/test dependencies, not viewer dependencies.

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py` and `python test_motion.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme_source.py`.
6. `python verify_browser.py` and `python verify_extended.py`
7. Inspect fresh screenshots and update visual verdict, then `python package_delivery.py`, `python verify_delivery.py`, and `python package_delivery.py` again to include copied-delivery evidence; finish with `python verify_acceptance.py`.

`delivery-copy-check.json` separately verifies the actual ZIP-extracted HTML offline on desktop and touch-emulated mobile, including reduced-motion open/reset and zero external requests/errors; its tested HTML SHA-256 is checked against the final inventory.

`author.py` overwrites generated source/export/poster; preserve manual edits separately. The authoring mechanism and maps are included, no sibling source needed. Build prefers local dependencies and retains the inherited sibling-dependency fallback. Blender rendering uses bounded four CPU threads, 24 Cycles samples, no denoising; mild sampling noise is expected. Viewer/runtime uses Three.js 0.180.0 (MIT license included), esbuild 0.25.11 build-time only. Mechanism/viewer/test lineage is the repository Japan pilot at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8.

## Scope and next step
Only `preview/kiribati-v1/` is delivered on `art/kiribati-v1`; branch backup is not a production deployment or merge. No blockchain, keys, funds, minting, public hosting, signed certificate, permanent storage or custody verification was performed. Proposed collection remains 201 equally one-of-one designs. User waived individual asset review; next step is the separately gated full-collection integration/review, not further polishing or deployment of this asset.
