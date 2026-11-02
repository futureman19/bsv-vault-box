# Bahrain v1 — Pearl & Coral Stone

Open `bahrain-v1.html` directly in Edge/Chrome. All runtime assets are embedded. Drag/touch rotation, staged open/close and reset are cosmetic only. No wallet, node service, keys, chain query, mint, deployment or custody operation was involved.

## Delivery
- Offline HTML: **2,555,800 bytes**, strictly below 5,000,000.
- GLB: **1,380,956 bytes**.
- `bahrain.blend`: packed, editable, script-authored Blender source; `mechanism.blend`: inherited trimmed mechanical baseline.
- `maps/`: three original seeded 512px stone maps; no photographs or third-party image pixels.
- `poster.png` and embedded `poster.jpg`: actual source render, not promotional AI imagery.
- Desktop/mobile closed/open, rear-open, fallback and no-JS screenshots are actual offline browser captures.

## Verified
`python verify_all.py` passed motion, independent saved-source reopening, source/export bidirectional nearest-vertex parity below 1e-5, brief/theme dimensions and hierarchy, a deliberately detached-ornament negative control, build, browser and extended checks. The negative control exits 1 with `Ornament escaped lid hierarchy`; it does not modify the saved source.

81 opening poses include all 27 moving and 35 static meshes, plus releasing latch versus lid contents. Zero unintended surface intersections; only inherited mating hinge barrel/leaf and latch pin/knuckle/bridge contacts exempted. Ten hinge mounting contacts and four new ornament seating contacts are explicitly checked. Hollow floor ray lands at z=0.265. This is sampled surface-intersection evidence, not continuous collision or mechanical certification.

Actual Three GLTFLoader checks finite geometry, zero degenerate triangles, image decoding, all three ornament parents and full-open framing. Desktop and 390×844 touch-emulated mobile use offline file://: native controls, rotation, open/close, interrupted reset, reduced motion, zero external HTTP requests, zero runtime errors and no horizontal overflow. Corrupt bytes reach the real GLB parser and show the poster; no-JavaScript poster is checked separately. Emulation ran on a desktop RTX 4060, not a physical phone or performance benchmark.

## Visual verdict and limits
Original research-led interpretation of Muharraq coral-stone architecture and Bahrain's pearling heritage, not a historical chest replica. Cream stone, teal inset and pearl-bearing shell are legible at mobile size. The regular shell ribs are scallop-like rather than a biologically accurate oyster; the stone is a stylized porous cream material rather than a geological scan. Tiny brass seating details remain subtle on mobile. No photoreal equivalence, complete cultural representation or human art approval is claimed. Per-asset human review was waived for this collection task.

## Real failures retained
`initial/theme-width-failure.txt`: shell was about 1.655 units wide, exceeding the prewritten 1.45 limit. Narrowed actual geometry, without relaxing the contract. One bounded visual correction also added a brass cradle and shell hinge; all four seating contacts now pass. `initial/poster-before-seating.png` preserves the earlier render.
`initial/roughness-channel-failure.txt`: test read red rather than glTF roughness green channel; corrected channel semantics, retaining variation requirement. Final decoded ranges are color 69, normal 9 and roughness 55.
`initial/reset-timing-failure.txt`: fixed 60ms render-state observation raced; final check waits for actual reset state with a bounded 3s timeout, not a weakened expected state. Reduced-motion action remains the existing snap behavior.
Optional Codex CLI failed authentication before edits; Hermes implemented and executed all verification directly. No credentials were changed.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js and the package.json build dependencies. Build resolves local node_modules or sibling iceland-pilot/node_modules; the worktree uses the explicitly authorized main-checkout dependency link. No runtime dependency on any of these paths. The acceptance runner's Blender executable path is Windows-specific and must be adapted on other machines.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python verify_all.py`
4. `python package_delivery.py`

Regeneration overwrites outputs; preserve manual changes separately. Source lineage is Japan's trimmed mechanism/viewer at base ff5d78f1e0d486af5c882c184fc08049996ebdc8; research URLs and the pre-model visual contract are in design-brief.md. Three.js MIT license included. No shared kit or prior preview changed. Package checks verify every inventoried file by SHA-256 and bytes; inventory and delivery report exclude themselves to avoid recursive hashing. Git backup branch is separate from integration, hosting and minting.
