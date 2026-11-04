# Djibouti v1 — Assal Salt Rift

Open **djibouti-v1.html** directly in Edge/Chrome. Entire offline viewer: **2,376,340 bytes**. Embedded GLB: **1,226,808 bytes**. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion supported. Source render provides corrupt-model and no-JavaScript fallback. No network, wallet, minting, hosting or custody action.

## Design and files
Research-backed written brief predates the model. Lake Assal's volcanic rift, salt shore and brine inform an original miniature, not a survey or traditional craft replica. UNESCO source is a tentative-list submission, not an inscribed World Heritage property. Research URL rechecked during recovery on 2026-11-04. No third-party photographs or generated promotional art are embedded.

`djibouti.blend` is packed editable Blender source; `djibouti.glb` contains the model/maps. `mechanism.blend` is the inherited family articulation baseline. `maps/` contains procedural color, normal and roughness maps. `poster.png/jpg` are actual source renders. Desktop/mobile closed/open and fallback screenshots are actual offline browser captures. Scripts, JSON checks, raw output and exact SHA-256 inventory accompany the source archive.

## Verified
- Fresh saved-source reopen: 50 moving and 39 static meshes, **81 poses**, zero unintended sampled surface intersections, latch versus lid included. Only named mating bearing contacts excluded. Ten physical hinge attachment pairs. Hollow floor ray z=0.2650000155.
- Source/export nearest-vertex error both directions **1.712013073529306e-7**, below 1e-5. Four packed images; exported texture channel variation checked (roughness green).
- Real browser GLTFLoader: **14,396 triangles, 89 meshes, 5 materials**, zero nonfinite vertices or degenerate triangles.
- All **34** terrain meshes are lid children; pivots match mechanism baseline; shelf top normals face up; three lake surface rays clear; terrain max z=2.339848, lid footprint 3.72 × 2.38. Narrow mineral seams below 0.12.
- Desktop 1440×1080 and touch-emulated 390×844 mobile under offline `file://`: native buttons, drag/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or JS errors. Full-open maximum absolute NDC 0.892365 (within viewport).
- Actual corrupted GLB bytes reach parser, show poster and disable controls; JavaScript-disabled poster separately tested. Renderer reports RTX 4060; **not physical-phone performance testing**.
- 81 numerical motion poses verify staged 80° latch / 105° lid endpoints. Three malformed asset controls reject. Deliberately detached terrain fails source ancestry assertion (negative-control.txt), without saving the mutation.

## Recovery, corrections and honest limitations
An interrupted earlier run left source/export but no poster or completed checks. Its optional Codex lane failed HTTP 401/token refresh; no Codex work was accepted. This run reviewed/rebuilt directly, repaired inherited Japan copy/accessibility text and truncated mobile CSS, and replaced wood-oriented UV projection with dominant-face stone mapping. `author-output.txt` preserves earlier execution; `author-final.txt` records fresh source render/export. A bounded 24-sample, four-thread, no-denoise render avoids unnecessary memory pressure; residual render grain remains.

Actual source and mobile screenshots were visually inspected: salt lake is readable; silhouette/controls fit. This is a clean stylized collectible, **not photoreal equivalence**. The rear escarpment reads as a row of separate rocks rather than a continuous geological fissure. The pale seam is prominent, particularly at corners. Smooth oval lake and repeated salt crystals are invented simplifications. No geographic scale, full continuous collision proof or manufacturing certification. Technical completion under the user's no-review directive is not individual aesthetic approval.

## Reproduce
Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node with package.json dependencies. Build prefers preview-local node_modules, otherwise sibling iceland-pilot/node_modules (present in this recovery workspace). For isolated extraction install package dependencies locally; dependencies are build-time only and excluded from delivery. Three MIT license included.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
4. `node tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
5. `python package_delivery.py`.

Regeneration overwrites source, export and poster. Preserve manual edits separately. Inventory excludes itself and delivery envelopes to avoid circular hashes. ZIP contents are read back and SHA-256 verified. Folder-local Git attributes preserve exact bytes across Windows checkout. Branch backup only: **no merge or deployment**. Final collection integration is a separate dependent card.
