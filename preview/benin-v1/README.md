# Benin v1 — Atakora Earth / Takienta

Open **benin-v1.html** directly in Edge/Chrome. The entire viewer is embedded: model, maps, Three.js runtime and an actual Blender-rendered poster. No server or network is required. Drag/touch to rotate, open/close the cosmetic lid, or reset. This is a local art asset, not minted, hosted, signed or deployed.

## Delivered
- Standalone HTML: **2,830,775 bytes**, strictly below 5,000,000.
- Portable `benin.glb`: **1,586,600 bytes**.
- Editable `benin.blend`, packed maps, `mechanism.blend` (frozen reusable family mechanism), procedural `maps.py` / `author.py`, viewer/build/test sources.
- Actual source render `poster.png` / `poster.jpg`; actual offline browser desktop/mobile closed/open captures, rear-open and no-JS/corrupt-GLB fallbacks.
- `design-brief.md` predates modeling and cites UNESCO/ICOMOS descriptions of the shared Batammariba earthen architecture of northwestern Benin and neighbouring Togo. No third-party photo/texture or sacred motif was copied. No concept illustration existed for this asset.
- `inventory.json`, `delivery-check.json`, `benin-v1-source.zip`: exact-byte hashes and archive readback; no dependency folders or credentials.

## Verified
Actual GLTFLoader: **14,392 triangles, 107 meshes, 5 materials**, zero nonfinite vertices and zero degenerate triangles. Three decoded 512×512 maps have nonzero ranges (earth color 35, earth roughness 27, straw color 33). Source earth median sRGB approximately (158,88,49).

Independent saved-source reopening confirms the exact original lid/latch pivots, 51 lid-parented architectural meshes, two roofed towers, one flat/open-roof tower, two connecting walls, shared terrace, 40 roof ribs, four static feet and four rounded buttresses. The ornament fits the brief's footprint and height. Four deliberately mutated theme records are rejected (missing roof, detached ornament, black palette, absent feet). These are post-implementation negative controls, not test-first TDD.

**81 opening poses**, all **67 moving** and **40 static** meshes, including all new architecture: zero unintended sampled surface intersections. Latch-vs-lid surfaces also checked. Only specific mating hinge leaf/barrel pairs and latch knuckle/bridge-to-pin bearings are exempt. Ten hinge attachment overlaps and a hollow-interior floor ray at z=0.265 pass. This is sampled BVH surface evidence, not continuous collision proof, solid-containment proof or manufacturing certification. The retained staged motion is 80° latch release then 105° lid opening.

Source/export bidirectional nearest-vertex maximum error **2.4575624024691933e-7 units**, below the 1e-5 gate. Packed source images and actual loaded runtime map variation checked; geometry parity does not claim Blender/Three lighting equivalence.

Offline **file://** Edge desktop 1440×1080 and **390×844 mobile touch emulation**: native open/close controls, mouse/touch rotation, interrupted reset and reduced motion pass. No external HTTP requests, runtime errors or horizontal overflow in normal runs. Full-open maximum projected absolute NDC about 0.8924. Actual corrupt bytes reach GLTFLoader and trigger the poster/disabled-controls fallback; no-JS poster decodes. Tests used desktop RTX 4060 hardware; no physical-phone performance claim.

## Visual assessment and deliberate limits
Actual closed desktop and open mobile/rear browser screenshots inspected. Warm earth, joined three-tower lid ornament, two straw-colored roofs and restrained brass are readable. All silhouette fits tested views and architecture remains on the opened lid. This is **stylized procedural collectible art**, not a photoreal reconstruction or community-endorsed cultural representation. Earth is smooth/mottled, roofs use visible geometric ribs rather than individual straw fibers, and rear-open architecture reads less clearly at that angle. The dark closed seam is conspicuous; it is intentional clearance, not a hermetic material seal. The inherited long clasp and interior/hardware are collection-family extrapolations, not traditional architecture. Doorway is relief and roof recess simplified; tower interiors are not functional rooms. No visual equivalence to a real dwelling is claimed.

## Failures retained honestly
- Optional Codex lane failed HTTP 401 before edits; no Codex code accepted and credentials were not modified. Hermes implemented and tested the asset directly.
- First theme assertion incorrectly expected 50 ornaments. Actual exported inventory contains 51: terrace + two towers + two roofs + 40 ribs + flat tower + recess + parapet + two walls + doorway. Corrected the count from explicit components, not the parenting requirement; initial assertion failure retained in `initial/theme-count-failure.txt`.
- One subsequent Blender theme-check process crashed with a C++ exception. The same check succeeded on a fresh invocation without changing the source/model; crash output retained. A combined foreground command also exceeded its 90-second harness timeout; no result was claimed from it. Final canonical suite has no automatic retries and must fully pass.

## Reproduce
Blender 5.2.1; Python with Pillow/numpy/Playwright; Node.js with Three.js 0.180.0 and esbuild 0.25.11; installed Edge. Node.js here is only local asset tooling, not a blockchain node.

From this folder:
1. `python maps.py`
2. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
3. `python verify_all.py` — builds HTML, runs motion, independently reopens source, checks parity/theme, browser and fallback/maps. Set `BLENDER` to override the local executable path.
4. `python package_delivery.py` — enforces required artifact inventory and verifies every ZIP entry's bytes/SHA-256.

Build discovers local `node_modules` or sibling `iceland-pilot/node_modules`; this worktree uses the authorized dependency junction. A separately extracted source archive requires `npm install` here plus the Python/browser/Blender dependencies. Runtime viewer needs none of those. Regeneration overwrites authored assets; preserve manual variants separately. Three.js MIT license included. Mechanism/test/viewer lineage: Japan cedar v1 from repository base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; only the new Benin directory changes.

User waived individual art review for the collection batch. This asset completes technical gates autonomously; integration into the full 201 set is a separate task. No changes to other previews, shared vault kit, production, chain systems or VPS.
