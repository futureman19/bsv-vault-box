# Laos v1 — Bamboo & Karst

Open **laos-v1.html** directly in Edge/Chrome. The actual model, Three.js runtime, maps and source-rendered poster are embedded. Drag/touch to rotate, open/close the lid, reset; reduced-motion preference is honored. No server or external asset requests are required.

## Delivered
- Standalone HTML: **2,983,046 bytes**, strictly below 5,000,000.
- GLB: **1,668,488 bytes**; editable packed source: `laos.blend`.
- `mechanism.blend`: included trimmed reusable Japan mechanical baseline, not new Laos art.
- `maps/`: independently generated bamboo weave color/normal/roughness, dark frame grain, limestone color maps (512 or 256 pixels).
- `poster.png` / `poster.jpg`: actual Blender render of the exported source, not AI promotional artwork.
- Desktop/mobile closed/open, rear-open and fallback screenshots: actual offline Edge captures.
- `design-brief.md`: researched material/landscape interpretation and measurable contract written before modeling.
- `*-check.json`, raw `*-output.txt`: actual verification; `inventory.json` hashes deliverables; `delivery-check.json` records archive readback and extracted HTML browser test. ZIP excludes itself and delivery-check to avoid recursive hashes.

## Design and visual verdict
Warm honey basket-weave panels, dark binding frames, satin brass, three uneven limestone peaks and a jade Nam Song-inspired river inlay. All terrain, vegetation and river belong to the lid. Geometry/maps are procedurally authored, not scans or human hand sculpture. Source citations are in the brief; no third-party photographs or source patterns are copied. There was no supplied Laos marketing illustration to match.

Actual desktop closed and mobile full-open screenshots were visually inspected. This is a coherent **stylized miniature**, not photorealistic, an exact landscape replica or a representation of every Lao culture. The repeat weave is visibly regular and can read as tiles; limestone forms are intentionally faceted/generic, vegetation is clustered low-poly detail, and the river is a thin decorative inlay rather than simulated water. The green seam/stacked trim can appear layered rather than tightly sealed. These limits are disclosed rather than treating technical tests as photoreal equivalence. No obvious clipping or detached lid was visible. Rear-open capture shows ornaments naturally hidden behind the open lid in the front view.

## What was verified
- Real GLTFLoader: **19,526 triangles, 110 meshes, 7 materials**, zero nonfinite vertices, zero degenerate triangles. Decoded color maps vary and remain <=512px. Five maps embedded; normal/roughness are portable texture inputs.
- Independent saved `.blend` reopen: hollow interior floor ray z=0.2650000155, ten physical hinge attachment overlaps, exact inherited hinge/latch pivots. Lid dimensions 3.72 × 2.38 × 0.30; seam <=0.10. Three different peak heights and rear-half placement verified from geometry bounds.
- **81 staged poses**, all **59 moving / 51 static meshes**, zero unintended sampled surface intersections. Latch releases 80 degrees before lid opens 105 degrees. Only explicitly named mating bearing pairs are exempt. This is sampled surface clearance, not continuous collision/engineering certification; same-rigid-lid decorative contacts are intentional.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7** (<1e-5). Five packed images independently observed in saved source.
- Offline `file://` Edge: 1440×1080 desktop and 390×844 touch emulation; real click/tap open-close, mouse/touch drag, interrupted reset, reduced-motion snap, zero external HTTP requests or runtime errors/overflow. Full-open viewport maximum absolute NDC 0.8923646517. Actual corrupt GLB reaches parser and activates poster fallback; no-JS poster also tested.
- Two motion/asset-contract unit tests pass. Deliberate post-implementation negatives remove one karst name and set HTML to exactly 5,000,000 bytes: both fail with exit 1, then byte-exact restored originals pass. This is regression evidence, **not test-first TDD**. No accidental model-gate failure occurred in this bounded pass.
- Git packaging initially flagged trailing spaces inside bundled upstream Three.js GLSL strings. Those bytes were preserved, with narrow whitespace attributes for the two generated payloads; all files use `-text` so checkout line-ending conversion cannot invalidate the SHA-256 inventory. Source whitespace checking remains enabled. An independent staged-blob hash check then caught `author-output.txt` still normalized from the earlier staging; scoped `git add --renormalize -- preview/laos-v1` re-staged the untouched raw bytes. All inventory entries subsequently matched the exact Git index blobs. CRLF evidence is explicitly recognized with `whitespace=cr-at-eol`, not rewritten.
- Browser GPU: NVIDIA RTX 4060 via D3D11. Mobile is emulation on that desktop GPU, **not physical-phone performance**. No FPS claim.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with pinned package.json dependencies. Build uses local node_modules or the existing sibling iceland-pilot toolchain; dependencies are not archived. The standalone HTML needs none of these tools. On standalone extraction, install dependencies locally before building. Regeneration overwrites authored output; keep manual edits in a separate source copy.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. `node --test tests.mjs`
5. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_design.py`.
6. `python verify_browser.py` and `python verify_extended.py`
7. `python test_theme.py` and `python verify_negative.py`
8. `python package_delivery.py`

The source scripts are folder-relative. Toolchain installation and Edge are build/test dependencies only. Mechanism/viewer/test lineage: Japan Cedar v1 in repository base ff5d78f1e0d486af5c882c184fc08049996ebdc8; Three.js MIT license included. Research sources inform facts only and confer no claim to unrelated imagery.

## Scope
One local inner collectible preview; cosmetic opening does not alter custody. Not minted, signed, hosted, deployed, or stored on-chain. No blockchain node, keys, funds, chain queries, mint code, VPS or public site touched. Branch backup only; no merge. Per-asset human review is waived for this collection batch; this is autonomous technical/visual verification, not a claim of human art approval. Collection direction remains 201 equally one-of-one Boxes, accessories deferred.
