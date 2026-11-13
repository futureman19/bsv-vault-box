# Pacific Ocean v1 — Abyss & Atoll

Open **pacific-ocean-v1.html** directly in Edge/Chrome. All runtime code, GLB, maps and the actual-source poster are embedded. Drag/touch to rotate, open/close the lid, reset; reduced motion is supported. No web server or network is needed.

## Delivered
- Standalone HTML: **2,615,340 bytes**, strictly below 5,000,000 bytes.
- GLB: **1,390,032 bytes**, 15,284 triangles, 58 meshes, 6 materials via the actual Three GLTFLoader.
- `pacific-ocean.blend`: editable named source; `mechanism.blend`: inherited trimmed family mechanism, not a second themed model.
- `maps/`: deterministic authored ocean color/roughness and volcanic basalt maps. Not scans or third-party imagery.
- `poster.png` / `poster.jpg`: actual Blender source renders, not AI illustrations.
- Desktop/mobile closed/open, rear-open, corrupt-parser fallback and no-JS captures: actual offline Edge screenshots.
- `design-brief.md`: pre-model visual contract and NOAA research sources. No supplied original illustration was assumed.
- Reproduction scripts, checks, exact SHA256 `inventory.json`, source archive and `delivery-check.json`.

## Verified
`run_checks.py` independently reopens the saved source and runs all final source/parity/theme/build/motion/browser/extended gates. `package_delivery.py` checks explicit required artifacts and reads every ZIP entry back against the inventory.

- **81 sampled poses**, all **19 moving / 39 static** meshes, no unintended surface intersections. Latch-to-lid tested separately. Only named hinge leaf/barrel and latch knuckle/bridge/pin mating bearings are exempt. Ten explicit hinge/body/lid attachment intersections, hollow interior floor ray z=0.2650000155. This is sampled surface clearance, not continuous collision proof or manufacturing certification.
- Same inherited pivot matrices. 80-degree latch release first, then 105-degree lid opening. Node motion tests reject invalid inputs and check sequencing/endpoints.
- Saved-source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, tolerance 1e-5; three packed source maps. Real loader finds zero nonfinite vertices and zero degenerate triangles.
- All three lid ornaments belong to the lid. Lagoon boundary: **192 vertices** inside the actual irregular ring polygon, central water ray visible, **32 ring rays** hit sand. Detached-lagoon and displaced-lagoon negative controls both reject. Pivot equality checked by separately opening/updating the mechanism source.
- Offline `file://` Edge desktop 1440×1080 and 390×844 touch emulation: native controls, drag/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests and no JS errors. Full-open projected silhouette maximum absolute NDC about .8924. Actual corrupt GLB bytes reach the parser and show the source poster with disabled controls; separate no-JS poster passes.
- Actual runtime color and green-channel roughness image variation checked, all maps <=512px. Visible copy regression excludes inherited Japan/Cedar/Yakushima wording.
- Exact artifact bytes preserved with local `.gitattributes`; inventory/archive checks exclude self-referential envelopes and dependency directories. Hashes identify bytes, not issuer authenticity or long-term availability.

## Visual acceptance and limits
Final mobile closed and desktop open screenshots were inspected. The ring/lagoon reads clearly, the open cavity and hardware remain visible, primary controls are readable and the default framing is unclipped. The design is intentionally stylized: a thick pale faceted ring, shallow pale turquoise lagoon and separate dark crater miniature, not a geographical reconstruction. Body reads petrol/teal rather than deep navy under studio light; visible panel seams and smooth procedural currents are not photoreal ocean material. Source poster has some sampling grain. No exact-reference equivalence, continuous collision clearance, ecological accuracy or physical-phone performance is claimed (mobile is emulation on NVIDIA RTX 4060).

The real initial lagoon-containment failure is retained in `initial/lagoon-containment-failure.txt`. Lagoon radii were reduced from .60/.39 to .57/.37 without relaxing the test, then source/export/poster and all final checks were regenerated. Other bootstrap/toolchain failures and optional rejected Codex lane are recorded in `failure-history.md`.

## Reproduce
Use Python with numpy/Pillow/Playwright and installed Edge, Blender 5.2.1, Node.js, and the pinned package dependencies. From this folder:

```text
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python run_checks.py
python package_delivery.py
```

`run_checks.py` contains explicit Windows Blender/Node paths; change those paths for another workstation. Build prefers local dependencies, with the original sibling Iceland dependency directory as fallback. Source/maps/mechanism are included; dependency folders are not. Regeneration overwrites generated outputs and may change bytes; rerun checks and packaging after edits. Preserve any manual Blender edits separately.

## Scope and provenance
Procedurally script-authored Blender work by Hermes, reusing Japan's family mechanism/viewer and Iceland's motion tests from base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. Three.js 0.180.0 MIT license included; esbuild 0.25.11 build-time only. NOAA text informs original procedural geography, not copied photographs, textures or traditional cultural motifs.

This is a local **inner collectible art preview**, not the outer custody container. Cosmetic lid motion changes no chain state. No mint, keys, nodes, signing, broadcasts, VPS, production website or custody implementation touched. The branch backup is not hosting or a mint. Launch direction remains 201 equally one-of-one designs; this file establishes no on-chain storage or off-chain persistence service. User waived per-asset human review; collection integration/review is a separate downstream task.
