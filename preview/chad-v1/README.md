# Chad v1 — Ennedi Windstone

Open **chad-v1.html** directly in Edge/Chrome. Complete offline model, runtime and actual Blender-rendered poster are embedded. Drag/touch to rotate; Open/Close lid and Reset view. Cosmetic collectible only: not minted, hosted, signed, or a custody action.

## Delivery
- HTML: **3,067,251 bytes**, strictly below 5,000,000.
- GLB: **1,748,940 bytes**; 14,448 triangles, 61 meshes, four used materials.
- `chad.blend`: packed editable source; `mechanism.blend`: inherited trimmed mechanical source from Japan v1.
- `maps/`: three independently generated 512x512 maps, not photographs or scans.
- `poster.png` and `poster.jpg`: actual source render, no AI substitutes.
- Desktop/mobile closed/open screenshots plus parser-failure and no-JS fallback captures.
- Source, parity, theme, browser, fallback, inventory and delivery JSON evidence; reproducible scripts and source ZIP.

## Verified and limits
Independent saved-source reopening: **81 poses**, all **22 moving / 39 static meshes**, zero unintended surface intersections. Latch-vs-lid also sampled; only named mating bearing contacts excluded. Ten hinge attachment intersection pairs pass. Hollow floor ray z=0.2650000155. This is sampled surface clearance, not continuous collision or mechanical certification.

Both-direction source/export nearest-vertex error **1.712013073529306e-7** (<1e-5). This proves geometric proximity, not byte-identical re-export. Real GLTFLoader reports zero nonfinite vertices and zero degenerate triangles. All six Ennedi ornaments belong to the lid. Independent rays pass through the arch opening and hit its crown. A landmark-omission negative control fails with `Missing real arch`.

Actual offline file:// Edge: desktop 1440x1080 and touch-emulated mobile 390x844; native clicks/taps, drag/touch rotation, open/close, interrupted reset, reduced motion, corrupt-GLB parser fallback, no-JS poster, zero successful-run errors/network requests/overflow. Full-open projected extent <0.893 NDC. RTX 4060 desktop hardware, **not physical-phone performance**. The first browser pass failed a 70ms reduced-motion scheduling assumption; raw failure retained in `initial/`. The harness now waits for the requested endpoint with a bounded 1500ms timeout rather than assuming a frame occurs within 70ms. Viewer motion code was unchanged. This verifies reduced-motion completion, not a measured frame-latency guarantee.

## Visual assessment
The warm ochre box and true open arch are legible at mobile scale. This is a stylized landscape interpretation, not photorealism or an exact Aloba/other named arch replica. Arch can read as a decorative handle; sandstone bands still sometimes resemble wood grain. A bounded material correction replaced overly regular waves with uneven beds and mineral variation; initial render retained. Pitons/feet are faceted, fittings are clean rather than weathered. The long released family hasp projects above the open lid. The arch naturally hides behind the lid in the frontal open view. Hinges pass geometric attachment checks, though the deliberate rear gap can look detached at some angles. The unseen interior and brass fittings are collection extrapolations. No claim that this landscape represents every Chadian culture.

## Rebuild
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with Three/esbuild from package.json. Build resolves local node_modules, otherwise sibling `iceland-pilot/node_modules`; dependencies are not shipped. Recovery verification found the sibling compiler missing (retained in `initial/recovery-build-failure.txt`), installed the unchanged pinned package versions locally, and reran build, source/parity/theme, motion, offline desktop/mobile and fallback checks successfully. The local lockfile is included; node_modules is excluded from the archive. Standalone extraction: install package dependencies locally. `setup_author.py` is historical adaptation provenance and needs the sibling Japan generator; the resulting `author.py` is self-contained with the included mechanism and maps and does NOT need that setup step.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node tests.mjs`; `python verify_browser.py`; `python verify_fallback.py`
6. `python package_delivery.py`

Regeneration replaces authored outputs; preserve manual edits separately. Inventory excludes itself, delivery JSON and ZIP to avoid circular hashes; archive entries are read back and hash checked. No .blend1, dependency folders or secrets included. Only `preview/chad-v1/` is committed. Branch backed up, not merged. No blockchain/node/wallet/keys/VPS/public deployment accessed. Three.js license included. Source research and measurable design contract are in `design-brief.md`; prior-art mechanics/viewer/test lineage is Japan v1 on base ff5d78f1e0d486af5c882c184fc08049996ebdc8.
