# Portugal v1 — Azulejo / Atlantic Blue

Open `portugal-v1.html` directly in Edge/Chrome. Everything needed at runtime is embedded: model, maps, Three.js, controls and actual source-render fallback. This is local collectible artwork, not minted, hosted, signed or a custody operation.

## Delivery
- HTML: **2,515,474 bytes**, strictly below 5,000,000.
- GLB: **1,221,164 bytes**.
- `portugal.blend`: packed editable Blender 5.2.1 source; `mechanism.blend`: inherited trimmed articulation baseline.
- `maps/`: original procedural 512px ceramic color/roughness/normal images.
- `poster.png` and `.jpg`: actual source render, not promotional art.
- Desktop/mobile closed/open screenshots, corrupt-loader and no-JS fallbacks: actual offline browser evidence.
- `inventory.json`, `delivery-check.json`, source ZIP: exact byte identities and verified ZIP readback. These are integrity hashes, not authenticity signatures.

## Verified
`python verify_all.py` builds and executes motion tests, independently reopens saved source, compares source/export geometry, verifies theme and tests actual Edge over file:// on desktop and 390×844 touch emulation.

58 meshes, 14,488 triangles, six materials; zero nonfinite vertices and zero degenerate triangles through real GLTFLoader. Three wave meshes belong to the lid. Map variation: color 230, roughness green-channel 90, normal red-channel 18. Actual saved pivot matrices exactly match the included baseline (max error 0).

81 motion samples include all 19 moving and 39 static meshes, plus latch against lid: zero unintended intersections. Only named mating bearing surfaces are excluded. Ten hinge attachment pairs intersect as designed. Floor ray hits z=0.2650000155. This is sampled surface testing, not continuous collision/manufacturing proof. Bidirectional source/export nearest-vertex error: 1.712013073529306e-7 units, below 1e-5.

Desktop and emulated-mobile native controls, pointer/touch rotation, open/close, interrupted reset and reduced motion pass. Full-open projected bounds max absolute NDC 0.892365. No external HTTP requests, successful-runtime JS errors, or horizontal overflow. Real corrupted GLB bytes reach the loader and trigger poster fallback; no-JS poster also passes. Tests run on desktop RTX 4060, not physical-phone performance.

Negative controls reject missing wave parentage, invalid motion asset contracts and HTML at the exact forbidden 5,000,000-byte boundary. Assertions are executable, not static PASS labels.

## Visual verdict and limitations
Actual source render and desktop-open/mobile-closed captures inspected. Ivory/cobalt floral tiles and blue–ivory–blue wave relief are visible; complete framing and hollow interior are readable. The motif is an original stylized four-petal repeat, not a reproduced historic azulejo. The panels are continuous ceramic-inspired skins, not individually modeled tiles. Pattern clips at panel boundaries. Glaze is restrained; the waves look like chunky sculptural fins rather than fluid water. The pale central wave and exact three-wave count are less immediate at mobile scale. Source poster has visible low-sample render noise. Utility/disclaimer text is small. No photorealism or historical fidelity is claimed.

Research sources and pre-model measurable contract are in `design-brief.md`. No reference photographs or third-party tile patterns are embedded. Viewer/mechanical lineage: Japan/Iceland pilots on base ff5d78f1e0d486af5c882c184fc08049996ebdc8; Three.js license included. Art kit and previous previews were not modified.

## Failures and fixes
Optional Codex lane exited 401 before implementation; no Codex changes were accepted. Hermes implemented and verified directly. Initial bootstrap attempted a Japan motion-test file absent there; corrected to the existing Iceland test. Initial build failed because the supplied shared dependency directory was empty (`verify-0-failed.log`). Installed the exact existing pinned three 0.180.0 / esbuild 0.25.11 dependencies locally in this new folder, then reran all gates successfully; no upgrade or old-directory changes. No art collision failure occurred. Negative controls are explicit regression probes, not claimed test-first development.

## Reproduce
Install Node, Python with numpy/Pillow/Playwright and Edge, and Blender 5.2.1. Run `npm ci --no-audit --no-fund` here; dependencies are not archived. Run `python maps.py`, then Blender with `--background --factory-startup --python-exit-code 1 --python author.py`; `python verify_all.py`; `python package_delivery.py`. Wrapper uses the disclosed Windows Blender/Node executable paths; edit them for other machines. Source author/build scripts otherwise resolve this directory. No sibling art is needed for regeneration. Regeneration overwrites source/model/poster; preserve manual edits separately. Packaging intentionally excludes its inventory envelope, active aggregate log, ZIP, caches and node_modules from recursive hashing.

Scope: only this new directory; no chain queries, keys, node startup, mint, production site, VPS, messaging or deployment. Branch backup is separate from hosting. Integration is a separate collection card.
