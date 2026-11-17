# Ecuador v1 — Toquilla & Volcanic Isles

Open `ecuador-v1.html` directly in Edge/Chrome. All runtime assets are embedded: no server or network needed. Drag/touch rotates, Open/Close stages the latch and lid, Reset cancels movement, and reduced motion snaps poses. This is cosmetic art, not custody or seal execution.

## Delivery
- Offline HTML: **3,118,630 bytes**, strictly below 5,000,000.
- GLB: **1,722,744 bytes**, 60 meshes / 16,014 triangles / 5 materials through actual GLTFLoader.
- `ecuador.blend`: packed editable Blender source; `mechanism.blend`: inherited trimmed family mechanism.
- `maps/`: original procedural straw color/normal/roughness and basalt color; no photo scans or third-party textures.
- `poster.png` and `poster.jpg`: actual Blender source render, not promotional illustration.
- Actual offline browser screenshots, source/check scripts, JSON reports, raw execution outputs, exact SHA-256 inventory and source ZIP.

## Design and visual limits
The brief was written before modeling and cites UNESCO's Ecuadorian toquilla weaving record and Galápagos Conservancy's volcanic history. The chest, weave approximation and three island shapes are invented; not an authentic traditional chest, named weave reproduction, geographic survey or exact named volcano. Mainland craft and island landscape are deliberately combined.

Actual source/mobile image inspection confirms a wide pale woven-looking body, teal inset, three stone islands, one depressed caldera, brass fittings and a hollow open interior. The largest caldera depression measures 0.24300003 units. The weave is regular and reads as fine cream fabric more than unmistakable individual straw strands at mobile size. The miniature shoreline is scalloped/stylized; the caldera reads partly as a notch at the hero angle. Dark seam/corner transitions are conspicuous; source render retains modest sampling noise. No photorealism or reference equivalence is claimed. This bounded v1 is complete under the collection's explicit autonomous/no-per-asset-review directive.

## Verified
- Independent saved-source reopening, hollow floor ray z=0.2650000155, ten hinge attachment intersections.
- Original mechanism pivot locations retained; latch 80 degrees before lid 105 degrees, tested at endpoints and 101 scalar progress values.
- 81 evaluated BVH poses: all 21 moving meshes versus 39 static meshes, plus latch versus lid. Zero unintended surface intersections. Only named mating hinge and latch bearings excluded. This is sampled surface evidence, not continuous collision/manufacturing certification.
- Source/export nearest world-vertex maximum error 1.712013073529306e-7, under 1e-5. Four packed maps. No nonfinite vertices or degenerate triangles in runtime loader.
- Three islets belong to the lid, stay inside the inset bounds, and the main summit has actual recessed geometry. Deliberate in-memory detached-islet mutation is rejected by the ancestry assertion; invalid asset contracts are also rejected in unit tests. This is post-implementation negative-control evidence, not TDD.
- Actual offline file:// Edge desktop 1440×1080 and mobile 390×844 touch emulation: native open/close, drag/touch rotation, interrupted reset, reduced motion, full-open projection inside viewport, no horizontal overflow, no external HTTP requests or runtime errors.
- Genuine invalid embedded GLB reaches parser and shows fallback; no-JS rendered poster also checked. Poster pixel coverage/nonblank checks pass. Runtime base/normal/roughness variation measured; roughness uses GREEN channel.
- Exact inventory and ZIP contents/bytes/hash readback checked. Folder-local `* -text` preserves delivered bytes in Git.

Mobile is desktop GPU emulation (RTX 4060), not physical-phone or FPS testing. UV/map variation is portability evidence, not material realism. Open front view naturally hides the islands behind the lid.

## Failures and recovery
Optional Codex implementation lane exited before work with token-refresh HTTP 401. No credentials were read/altered; no Codex changes were accepted. Hermes authored and ran all checks directly. Bootstrap initially looked for Japan's nonexistent tests.mjs; it was corrected to use Iceland's mechanism unit tests. The requested shared dependency directory was empty, so the first build failed MODULE_NOT_FOUND for esbuild. Installing the already-pinned dependencies locally in this new folder fixed the build. These were tooling failures, not waived art gates. See `initial/failures.md`. No model collision or geometry failure occurred.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright, Node.js, installed Edge. From this directory:

1. `npm ci --no-audit --no-fund` (Three 0.180.0 and esbuild 0.25.11; dependencies not included).
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_checks.py` (build, unit tests, independent source/parity/theme, browser and extended checks).
5. `python package_delivery.py` after updating README sizes if regenerated.

`run_checks.py` defaults to this host's Blender path; set BLENDER to another executable when needed. Scripts resolve assets relative to this folder; build can use local dependencies or sibling iceland-pilot dependencies. The included mechanism makes authoring independent of sibling source art. Regeneration overwrites authored files; preserve manual edits separately. Inventory excludes itself, delivery report/ZIP and active verification output to avoid circular/changing hashes. ZIP excludes node_modules, bytecode, Blender backups and optional failed lane logs.

Mechanism/viewer/test lineage is Japan and Iceland at base ff5d78f1e0d486af5c882c184fc08049996ebdc8; Three MIT license included. Source ZIP is off-chain local art only. No blockchain node, keys, mint, broadcast, chain query, wallet, VPS, public deployment or merge. Branch backup is not publication or minting. Final collection integration is a separate dependent card.
