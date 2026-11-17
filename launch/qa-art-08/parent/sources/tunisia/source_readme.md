# Tunisia v1 / Sejnane Clay

Open **tunisia-v1.html** directly in Edge/Chrome. Standalone offline preview: **2,889,913 bytes**; embedded standalone GLB: **1,573,396 bytes**. Drag/touch to rotate; Open/Close lid; Reset view. Reduced motion and poster fallback are supported. No server or network connection is required.

Inspired by the cream clay, red ochre and black decoration of the women potters of Sejnane; sources and the pre-model measurable contract are in `design-brief.md`. The chevrons and dish layout are invented abstract designs, not reproductions of traditional symbols. This is procedurally authored Blender art, not pottery made by those artisans, a scan, an endorsement, or a representation of all Tunisia.

## Verified results
- Real GLTFLoader: 17,644 triangles, 68 meshes, seven materials, zero nonfinite vertices and zero degenerate triangles.
- Independent saved-source reopening: 29 moving meshes against 39 static meshes over **81 poses**, plus latch-vs-lid checks; **zero unintended surface intersections**. Only specified coaxial bearing surfaces excluded. Ten hinge attachment pairs intersect as intended; interior downward ray hits floor z=0.2650000155.
- Source/export nearest-vertex error in both directions: **0.0000002384185791**, below 0.00001. Three packed maps; decoded roughness checked in glTF green channel.
- Exact inherited lid/latch pivot matrices; staged 80° latch release before 105° lid opening. Two motion/asset tests pass, including invalid-input rejection.
- Real concave dish: radius .73, floor 2.0150001, rim 2.2000000; depth .18499994; 480 top faces point upward. Twelve lip accents and dish travel with the lid in saved source and actual browser hierarchy. Deliberately detaching the dish triggered the ancestry assertion; restoring it passed. This is an explicit regression negative control, not a prior production defect or a claimed test-first history.
- Offline `file://` Edge: 1440×1080 desktop and 390×844 touch-emulated mobile. Native open/close, drag/touch rotation, reset during movement, reduced motion, no overflow, no external HTTP requests and no unexpected JS errors. Full-open maximum absolute projected coordinate .9110183 (<1). Genuine corrupt GLB reaches the loader and falls back to the actual render; no-JS poster also checked.
- `material-check.json` validates actual embedded texture variation, poster nonempty pixels, runtime ancestry and Tunisia visible/accessibility copy.
- `inventory.json` records exact bytes/SHA-256; `delivery-check.json` records archive readback and size gate. Folder-local Git attributes preserve bytes across Windows checkout.

## Honest visual limits
The shallow dish is legible in source and mobile renders. Cream/red/charcoal decoration, brass and terracotta feet are visible; fine pattern contrast is subdued on mobile. Cream surfaces remain smooth and can read as painted material rather than handmade clay. The dark seam is prominent and can read as slightly ajar; the inherited hinge connections were geometrically checked, not engineering-certified. Source poster has sampling noise (denoising deliberately disabled). Hardware remains the stylized family mechanism, not a historical Tunisian fitting. Dish exterior is naturally hidden behind the open lid from the front.

No photorealism, reference-art equivalence, authentic symbolic pattern, continuous collision proof, physical manufacture, or physical-phone performance is claimed. Browser evidence uses desktop RTX 4060 hardware with mobile viewport/touch emulation. No per-asset human approval is claimed; the user waived it until collection integration.

## Files and reproduction
`tunisia.blend` editable source; `tunisia.glb` portable export; `mechanism.blend` included trimmed family mechanism; `maps.py` and `maps/` independently generated maps; `author.py` reproducible author/export/source render; `poster.png` and JPEG actual-model render, never AI marketing. Screenshots are actual offline browser views. JSON and `*-output.txt` files contain execution evidence. `tunisia-v1-source.zip` excludes dependencies and backups.

Build-time requirements: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with pinned Three 0.180.0/esbuild 0.25.11 (`npm ci`). The prescribed shared dependency path had no esbuild executable; identical pinned packages were installed only in this new folder. Nothing in another preview was repaired or modified. Runtime assets are embedded regardless of build environment.

From this folder:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python verify_browser.py` and `python verify_materials.py`
7. `python package_delivery.py`

`setup.py` is the one-time adaptation helper and requires repository Japan/Iceland sibling sources; it is not needed for the included self-contained author/build/test scripts. Authoring overwrites generated source/output; preserve manual edits separately. Three MIT license included. Mechanism/viewer/test lineage is the repository Japan pilot, inherited from Iceland.

## Scope
Local art asset only, not minted, hosted, signed or deployed. Cosmetic lid motion does not alter a chain seal or custody. Collection direction: 201 equally one-of-one designs; no launch accessories. Only `preview/tunisia-v1/` was added. Branch backup is `art/tunisia-v1`; integration is a separate task. No shared vault kit, other preview, chain software, keys or VPS was touched.
