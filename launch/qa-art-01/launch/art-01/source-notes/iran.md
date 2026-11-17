# Iran v1 — Turquoise & Star

Open **iran-v1.html** directly in Edge/Chrome. All runtime code, model, textures and the actual Blender-rendered poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion is supported. Cosmetic animation only, not custody or minting.

## Delivered
- HTML: **2,582,271 bytes**, strictly below 5,000,000.
- GLB: **1,314,276 bytes**; real loader: 14,740 triangles, 93 meshes, 6 materials, zero nonfinite vertices or degenerate triangles.
- `iran.blend`: packed editable source; `mechanism.blend`: inherited trimmed mechanism, not Japan's tree or country artwork.
- `maps/`: two independently generated 512-square color/roughness maps. Real roughness decoded from glTF green channel: range 44; color red range 222.
- `poster.png` / `poster.jpg`: actual source render, not AI artwork. Desktop/mobile closed/open, corrupt-input fallback and no-JS screenshots are actual file:// captures.
- `iran-v1-source.zip`, `inventory.json`, `delivery-check.json`: explicit required files, exact bytes/SHA-256 and archive readback. Dependencies excluded.

## Design and verification
The prewritten `design-brief.md` cites Met Museum Kashan star/cross tiles and UNESCO Esfahan documentation. Geometry and textures are original procedural interpretation; no photographs, historic inscriptions or sacred text were copied. The fifteen raised eight-pointed stars, fifteen turquoise jewels and eight cobalt diamonds are lid-owned physical prisms; the body motifs are a printed-looking procedural map, not individual tile geometry.

Independent saved-source reopening verified original pivot matrices, 38 ornaments and Z range 1.9780000448–2.0480000973, hollow floor ray Z 0.2650000155, and ten hinge attachment intersections. All **54 moving and 39 static meshes** were included in **81 opening poses**, with no unintended surface collisions. Only explicit concentric mating bearings are exempted. Latch releases 80 degrees before lid opens 105 degrees. Source/export bidirectional nearest-vertex error: **1.712013073529306e-7**, below 1e-5. This is bounded sampled surface evidence, not continuous clearance or manufacturing certification.

Offline Edge desktop 1440×1080 and touch-emulated mobile 390×844 passed actual controls, rotation, open/close, interrupted reset, reduced motion, no overflow, no external HTTP requests and no runtime errors. Full-open maximum absolute projected coordinate: **0.926991** (<1). Actual corrupted GLB bytes reached the parser and triggered poster fallback; no-JS poster also passed. RTX 4060 desktop rendering is not physical-phone performance.

Tests are assertions that fail on violated bounds, geometry, parentage, intersections and bytes. A deliberate detached-ornament negative control was rejected; motion tests reject missing pivots, nonfinite bounds and empty geometry; corrupted GLB acceptance exercises a real parser error. These are regression negative controls, not claims of test-first TDD. No unintended art/test failure occurred in this run. The direct UNESCO research page returned 403 and the optional BeautifulSoup parser was absent; cited source facts instead came from retrieved search excerpts. The shared toolchain was empty at preflight, so pinned packages were installed only in this asset directory; no sibling dependencies were altered.

## Honest visual verdict
Source, mobile-closed and desktop-open images were visually inspected. The box, stars and hollow opening are readable and framed. This is stylized ceramic-inspired relief, **not photoreal ceramic or faithful historic mosaic construction**. The raised stars read as appliqué; the body pattern crops at panel boundaries, the glaze is satin, the feet/rim are chunky, and brass mechanism detail is simplified. Open-view hinge/hasp connections can look thin or slightly floating, although the named hinge attachments pass evaluated geometry intersection checks. No claim of user art approval or hardware engineering certification. Rear ornaments naturally face away when open.

## Reproduce
Python with Pillow/numpy/Playwright, installed Edge, Blender 5.2.1, Node build tools. `npm ci --prefix preview/iran-v1 --ignore-scripts --no-audit --no-fund` restores pinned dependencies. Three 0.180.0 is MIT; license included. Node is used only as a JS compiler/test runtime, never a blockchain node.

From repository root:
1. `python preview/iran-v1/maps.py`
2. Blender `--background --factory-startup --python-exit-code 1 --python preview/iran-v1/author.py`
3. Same Blender flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `python preview/iran-v1/build.py`
5. `node --test preview/iran-v1/tests.mjs`; Python `verify_browser.py`, `verify_extended.py`.
6. `python preview/iran-v1/package_delivery.py`

All working scripts use folder-relative assets. `setup.py` is historical scaffolding and depends on sibling Japan/Iceland files; it is not required to reproduce the included final author/viewer. Do not rerun it over later manual edits. Regenerating source changes hashes; regenerate evidence/inventory afterward. Rendering is CPU Cycles with two threads, no denoising, 24 samples; mild noise is retained honestly.

Scope is additive preview art only. No chain queries, keys, nodes, broadcasts, minting, production edits, hosting or VPS work. Branch backup is not public deployment. Collection context is 201 equally one-of-one designs; future off-chain media storage and issuance remain separate work. Per-asset review was explicitly waived for this batch; final integration/review is a separate card.
