# Italy v1 / Florentine Stone

Open **italy-v1.html** directly in Edge/Chrome. All model, maps, runtime and real-source poster bytes are embedded. Drag/touch rotate, Open/Close lid and Reset; reduced-motion preference supported. Cosmetic motion only, not seal/custody interaction. Not minted, hosted or deployed.

## Delivery
- HTML **2,535,880 bytes**, strictly below 5,000,000.
- GLB **1,274,028 bytes**; actual runtime 10,944 triangles, 72 meshes, five materials.
- `italy.blend`: editable Blender source; `mechanism.blend`: included inherited mechanism. `maps/`: four original procedural 512-square images, not scans.
- `poster.png` and `poster.jpg`: actual source render. Desktop/mobile closed/open and rear-open images: actual offline browser captures.
- `design-brief.md`: research-backed contract written before model; `inventory.json`: exact payload sizes/SHA-256; source ZIP and `delivery-check.json`: archive readback evidence.

## Verified, with limits
Saved source independently reopened; ten rear-hinge attachment overlaps, hollow interior floor ray z=0.2650000155. All **37 moving and 35 static meshes**, at **81 sampled poses**, no unintended surface intersections. Latch against lid included. Only named coaxial hinge/latch bearing contacts excluded. This is sampled surface clearance, not continuous collision proof or engineering certification.

Source/export bidirectional maximum nearest-vertex error **1.712013073529306e-7**, below 1e-5. Packed stone/roughness maps independently found. Actual GLTFLoader reports no nonfinite vertices or degenerate triangles. Decoded color ranges 35/127/57; actual green-channel roughness range 60. Eight petals, eight leaves and all 21 inlay parts are lid-owned; petal and negative-space rays pass. Detached-petal negative control really fails ownership and exposure tests without modifying the saved source; final ordinary source passes. This is a post-implementation negative control, not a historical art defect or test-first claim.

Edge offline `file://`: 1440x1080 desktop and 390x844 touch emulation; native open/close, drag/touch rotation, interrupted reset, reduced motion, full-open framing (maximum absolute NDC 0.934110), no overflow, no external requests and no runtime errors. Genuine corrupted GLB reaches parser and shows fallback; no-JavaScript poster also tested. NVIDIA RTX 4060 desktop host, **not physical-phone performance**. Two motion unit tests pass, including invalid asset rejection.

## Visual verdict and deviations
A cohesive stylized pale-stone and green/brass collectible with a readable eight-petal flower, not museum-grade craftsmanship or photoreal equivalence. Original invented radial design is inspired by Florentine commesso; not a copied traditional pattern. Inlays are shallow applied mesh relief, deliberately not flush cut-stone joinery. Source rays establish seating but bright sides/shadows can make the small leaf pieces appear perched. Leaves were made **ivory rather than the brief's green** for contrast on the green lid. Green lid appears sage in the source render and warmer/muted gold under browser lighting. Veins are visibly procedural; the dark seam is visually heavy, corner assembly and long inherited latch remain simplified, and the source render has sampling grain. Full-open screenshot fits and shows the hollow interior, but the exposed rear gap can visually read as a floating hinge despite ten source attachment-overlap tests; mechanical visual realism is not claimed. No claim of human art approval; per-asset review waived for this collection batch.

## Reproduce
Blender 5.2.1, Python with numpy/Pillow/Playwright (installed Edge), Node with pinned Three 0.180.0 and esbuild 0.25.11. Shared baseline node_modules was checked and its esbuild entry was absent; pinned dependencies installed **only here**, excluded from Git/ZIP. No sibling toolchain modified. Source archive is self-contained apart from these build/test tools.

1. `npm ci --ignore-scripts --no-audit --no-fund` in this directory.
2. `python maps.py`
3. Blender `--background --factory-startup --python-exit-code 1 --python author.py`
4. Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` independently.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Optional negative check: Blender verify_theme.py with `-- --negative` must exit nonzero and writes theme-negative.json. Regeneration overwrites source; preserve manual copies separately. Mechanism/viewer/test lineage is repository Japan/Iceland; Three MIT license included. Exact bytes preserved by folder-local .gitattributes. No blockchain processes, keys, broadcasts, production files, shared kit or VPS touched. Branch backup only; integration is a separate task.
