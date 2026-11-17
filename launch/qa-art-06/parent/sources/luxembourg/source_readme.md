# Luxembourg v1 — Mullerthal / Sandstone & Fern

Open `luxembourg-v1.html` directly in Edge/Chrome. Complete offline payload: **3,123,852 bytes**; GLB: **1,761,164 bytes**. All runtime/model/poster assets embedded. This is an inner cosmetic collectible study, not the outer custody container; no minting, blockchain access, hosting, signing or production changes.

## Design and files
The pre-model `design-brief.md` cites Luxembourg and Mullerthal tourism sources. Buff sedimentary stone carries a miniature cleft between two terraced outcrops, blue-green stream, small pinnate fern fans, dark olive seam and satin brass. It is a landscape interpretation, not a named-landmark replica or a complete representation of Luxembourg. Geometry/maps are procedurally authored in Blender, not scans or hand sculpture. `luxembourg.blend` is packed editable source, `luxembourg.glb` portable export; `mechanism.blend` is the read-only Japan-derived mechanical baseline copied locally. `maps/` holds generated 512px color, roughness and normal maps. Poster PNG/JPEG is rendered from the final actual source with bounded Cycles CPU settings; not AI promotional art.

## Verification actually executed
- Build prints `HTML_BYTES 3123852 GLB_BYTES 1761164`; strict complete-HTML limit 5,000,000 bytes.
- Independent saved-source reopen: 37 moving and 39 static meshes, 81 staged opening samples, zero unintended surface intersections. Exact inherited pivot matrices retained; 80° latch release precedes 105° lid opening. Explicit exceptions only for mating hinge leaf/barrel and latch pin/knuckle/bridge bearings. Ten hinge attachment intersection pairs and hollow-floor ray z=0.265 pass. This is sampled surface evidence, not continuous collision, solid containment or engineering certification.
- Source/export nearest-vertex maximum error 1.712013073529306e-7, below 1e-5. Three packed maps verified. Real browser GLTFLoader: 76 meshes, 15,656 triangles, five materials, zero nonfinite vertices and zero degenerate triangles.
- Theme checks: eight outcrop courses, twelve fern fans, all terrain parented to lid, relief/plan bounds and 0.40-unit clear gap between opposing outcrops, original pivots. Actual decoded GLB color/roughness/normal ranges 38/52/26; roughness measured from green channel. The gap test establishes geometry separation, not visual equivalence to a real ravine.
- Desktop 1440×1080 and mobile 390×844 touch emulation in offline Edge over file://: native rotation/open/close/interrupted reset/reduced-motion, no horizontal overflow, no external HTTP requests or JS errors. Full-open projection maximum 0.912 or less. Actual corrupt GLB reaches the parser and triggers poster fallback; no-JS poster also verified. RTX 4060 desktop hardware, not physical-phone performance.
- Negative regression control deliberately detaches an outcrop and exits nonzero with `Detached ornament rejected`. This is postimplementation regression evidence, not a claim of test-first TDD.
- `inventory.json` records exact byte/SHA-256 identities. `delivery-check.json` validates required artifacts, size, complete archive membership and each ZIP entry on readback. Inventory excludes itself and packaging envelopes to avoid circular hashes. `.gitattributes` preserves exact bytes through Git checkout.

## Visual assessment / bounded correction
Actual source poster and closed mobile/open desktop browser images inspected. The whole box and full-open silhouette fit; hollow interior and hardware are readable. First pass fern leaflets were tiny and lacked visible stalks. One bounded correction enlarged the fans, added rooted stalk strips and raised the browser viewing angle. Initial poster/mobile image retained under `initial/`.

The final result is deliberately stylized: pale layered rock masses still resemble stepped cut slabs, procedural body banding can read as pale wood, and the stream is a simple narrow rectangular inlay. Small-scale fern identity remains weaker than the text suggests; vegetation reads as fine green sprigs on mobile. Ravine depth is only partly visible from the hero angle. Terrain is naturally hidden behind the lid in a front open view. No photorealism, botanical accuracy or reference-equivalence claim. These are disclosed v1 visual limitations, not failed technical gates. Per-asset human review was waived for this collection batch.

## Real failure and fix
Initial build failed because the prescribed sibling node_modules target was empty. Raw failure retained at `initial/build-missing-dependency.txt`. Installed only this directory's declared build dependencies with `npm install --ignore-scripts --no-audit --no-fund`; local dependency resolution then passed. Optional Codex implementation lane failed authentication before producing edits; `lane-output.txt` preserves the failure. No credentials accessed or changed. Hermes authored and verified the result directly.

## Reproduce
Windows Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with Three/esbuild. Run from this directory:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_verification.py` (build, independent source/parity/theme, browser, maps/no-JS and negative control).
5. `python package_delivery.py` (inventory/ZIP/readback).

Regeneration overwrites generated source; preserve manual edits separately. The verification runner's Blender path is explicit for this workstation and should be changed for other installations. Three.js license included. Archives exclude node_modules, Python caches and Blender backups. All project additions confined to this directory; branch backup is not deployment. Collection integration belongs to the separate final card.
