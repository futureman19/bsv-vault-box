# Iceland physical back-right v10 — local review only

Open `iceland-backright-v10.html` directly offline. No installation or external resources. This is the actual interactive collectible, not the marketing illustration. No mint, chain, wallet, node, deployment, or custody change.

## Correction
Front latch is Blender Y=-1.29; rear hinge Y=+1.32. Right viewed head-on at the latch is +X. The entire glacier footprint is X=0.86–1.65, Y=0.38–0.98, Z=1.977–2.267: physically BACK-RIGHT, not front-right or a screen-X substitution. glTF coordinates are (X,Z,-Y); the actual GLTFLoader check converts back before checking both axes.

River upstream endpoint is X=1.25,Y=0.68 inside that footprint. The terminal inlay rises into the ice: actual evaluated triangle intersection is asserted, not just overlapping projected bounds. The slab was rebuilt with the exact previous outer dimensions/bevel, replacing the old Boolean cut with one new incision. Rays verify the old front-right channel is filled and the new diagonal channel is cut. Exactly two river meshes remain: channel and connected original-position left cascade.

Glacier is a new closed, faceted, asymmetric low ridge (0.79 wide, 0.60 deep, 0.29 high), with uneven connected crests rather than a symmetric spike cluster. Existing portable ice material/color range retained. No camera changes in viewer or saved source; top-down diagnostic is a separate temporary render.

## Preserved
425 other named source object geometry/topology, parent and world-transform records match v9 exactly, including body rock, moss, gold, shell, rear mechanism and camera. Material factors are not redesigned. Viewer and motion choreography remain the v9 implementation; motion.mjs is also byte-identical to approved v4. Previous source/delivery files are SHA-256 checked at packaging.

## Executed checks
- Independent saved-source reopen: 81 real BVH motion samples, zero collisions, unchanged bearing exclusions. Hollow floor ray Z=0.265; all ten previous hinge attachment contact pairs retained.
- Glacier has no intersection with rear mechanism or corner caps. Nearest sampled glacier-vertex/hardware surface distance ~0.03372; this is not a continuous minimum-clearance certificate.
- Actual GLTFLoader: finite/nondegenerate triangles, decoded nonempty texture maps, physical X/depth bounds. Source/export bidirectional geometry error <=1.7121e-7.
- Offline file:// Edge desktop and touch-emulated mobile: rotate, native touch rotate, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests/errors. Corrupt embedded GLB exercises real loader/poster fallback.
- Full-open projection fits viewport. Ice is occluded by open lid in primary view; physical clearance comes from real geometry samples, not that screenshot.
- ZIP inventory/readback hashes and delivered-file hashes checked by package_delivery.py. No .blend1 backups are archived.

## Exact payload sizes
- Standalone HTML: **4,126,142 bytes** (hard limit 5,000,000).
- GLB: **2,530,076 bytes**.
- Editable Blender: **865,672 bytes**.
- Source ZIP final byte size and all hashes: `delivery-check.json` / `inventory.json` (outside the self-contained archive to avoid self-reference).

## Files and reproduction
`author.py` reopens immutable `approved-v9.blend`, changes only glacier/channel/slab, saves source, exports GLB and poster. Blender 5.2.1 uses --background --factory-startup --python-exit-code 1 --python author.py. Run build.py using sibling iceland-pilot/node_modules (Three/esbuild), then verify_browser.py, Blender verify_source.py / verify_parity.py / verify_physical.py, verify_runtime_physical.py and package_delivery.py. Tests require Python Pillow/Playwright and local Edge. This toolchain is development-only; delivered HTML has all runtime bytes embedded.

`desktop-closed.png`, `mobile-closed.png`, open poses, `poster.png`, `before-after.jpg`, `reference-comparison.jpg`, and `top-down-diagnostic.png` are separate review images. Marketing is clearly labeled illustration in comparison, not claimed as model detail.

## Honest remaining limits
Physical placement and connected source are corrected. Glacier is broader/lower and asymmetric, but at normal viewer scale still reads as a small stylized angular icy ridge, not the marketing image's natural microdetail. Portable transmission is configured, not proof of photoreal glassiness. No optional art iteration performed. Collision proof is 81 sampled states, not continuous physics; mobile is desktop Edge touch emulation, not physical-phone performance. Delivery is local only.
