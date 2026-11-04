# Latvia v1 — Linen & Amber

Open **latvia-v1.html** directly in Edge/Chrome: fully embedded, offline 3D collectible. **HTML 3,979,743 bytes; GLB 2,407,672 bytes.** Drag/touch rotates; Open/Close lid and Reset work; reduced-motion preference snaps the animation. No server, wallet, blockchain node, signing, minting or deployment.

## Design and visual result
Warm finger-jointed wood carries a raised cream/carmine linen-inspired panel and three honey-colored cabochons in brass settings. `design-brief.md` was written before authoring and cites Latvia’s tourism descriptions of material crafts. The motif is invented, not a copied regional textile, sacred symbol or claim of artisan production. No supplied reference artwork existed.

Actual source poster and closed/open desktop/mobile screenshots were visually inspected. The complete silhouette and three domes are readable on mobile; the open body is hollow and no obvious detached hardware was seen. **Limitations:** the weave is too fine to resolve convincingly at normal mobile size and the rigid panel can read as an insert; amber is deliberately opaque, not realistic translucent resin; the lid seam is conspicuous; the source render retains sampling noise. Lid ornaments naturally face away in the front open view. No photorealistic equivalence, physical-phone speed or manufacturing validity is claimed.

## Actual verification
- Blender 5.2.1 reopened packed source independently. 81 opening samples, all 35 moving versus 99 static meshes plus releasing latch versus lid: **zero unintended surface intersections**. Only specified concentric hinge/latch bearing pairs exempt. Ten hinge attachment intersections and hollow-floor ray z=0.2650000155 passed. Sampled surfaces are not continuous collision proof.
- Same saved-source pivot matrices as included mechanism baseline. Exact panel bounds/three cabochon placements and lid ownership passed. Missing-one-cabochon negative control actually failed as expected (`theme-check.json`).
- Bidirectional saved-source/export nearest-vertex maximum error **1.712013073529306e-7**, threshold 1e-5. Six packed source maps.
- Real Three GLTFLoader: **29,724 triangles, 134 meshes, 7 materials**, zero nonfinite vertices or degenerate triangles. Actual decoded base-color and green-channel roughness variation passed. All ornaments attached to lid. Linen atlas has 21.09375% carmine and 78.90625% cream pixels.
- Edge offline `file://`: 1440×1080 desktop and 390×844 mobile touch emulation, rotation, native buttons, open/close, reset during movement, reduced motion, no horizontal overflow, zero external HTTP(S) requests and zero unexpected JS errors. Full-open max absolute projected NDC ~0.892365 (<1). RTX 4060 desktop GPU; not a physical handset test.
- Real corrupted embedded GLB reaches parser, produces expected caught error and displays poster/disabled controls. No-JS poster also tested.
- Two motion/invalid-asset unit tests pass. Source/theme/runtime/package assertions are executable and can fail; source missing-ornament negative and invalid-asset tests prove rejection paths.
- A real extended-test failure is preserved in `initial/extended-uint8-failure.txt`: unsigned-byte multiplication overflow misclassified cream as red. Fixed the oracle by converting to float before multiplication, unchanged palette thresholds and artwork; rerun passed.
- `inventory.json` identifies exact delivered payload bytes/SHA-256. `delivery-check.json` verifies ZIP readback, explicit required artifact set and the size gate. Folder-local Git attributes preserve exact bytes; indexed Git blob comparison is reported in the handoff.

## Source and reproduction
`latvia.blend` is editable packed, script-authored source; `latvia.glb` portable model; `mechanism.blend` the trimmed inherited hardware/interior; `maps/` generated PNGs; `poster.png` actual Cycles source render, `poster.jpg` compressed viewer poster. No AI promotional substitute, scans or downloaded texture pixels. Three.js 0.180.0 MIT notice included; esbuild 0.25.11 is build-time only.

Run in this folder with Python (Pillow, numpy, Playwright), Blender 5.2.1, Node and installed Edge:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python build.py`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

The supplied shared pilot dependency directory contained no esbuild, so pinned dependencies were installed only in this new folder. node_modules is ignored and excluded from delivery; viewer runtime has no dependencies outside its HTML. Build can fall back to sibling pilot dependencies if local install absent. Authoring overwrites generated files; preserve manual edits separately. Update checks/inventory after regeneration.

Only `preview/latvia-v1/` added. Art branch backup only, no merge or public hosting. Inner collectible cosmetic motion is not an on-chain seal operation. Collection direction remains 201 equally one-of-one Boxes. Next: independent final collection integration after all asset cards complete, per the user’s waived per-asset review directive.
