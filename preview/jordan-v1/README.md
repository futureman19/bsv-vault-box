# Jordan v1 — Wadi Rum / Rose & Ochre

Open **jordan-v1.html** directly in Edge/Chrome. The complete 3D model, Three.js runtime, procedural textures and actual-source poster are embedded. Drag/touch to rotate; Open/Close lid; Reset view. No server or internet needed.

**HTML: 2,689,165 bytes. GLB: 1,461,768 bytes.** The HTML is below the strict 5,000,000-byte ceiling. This is one cosmetic inner collectible, not a custody container or a minted token. No production deployment, chain operation or on-chain storage was performed.

## Design and files

Research-backed `design-brief.md` was written before modeling. Wadi Rum's rose/ochre sandstone, fluted massifs, narrow siq and natural rock arches inform the design. This is not a scale replica of a named location or comprehensive representation of Jordan. No external photographs or generated promotional images are used.

- `jordan.blend`: packed, named editable Blender source; script-authored, not hand sculpted.
- `jordan.glb`: portable model, hollow interior, brass mechanism, embedded texture maps.
- `jordan-v1.html`: complete offline viewer.
- `maps/`: three independently generated 512x256 maps (body color/roughness, darker lid color).
- `poster.png`, `poster.jpg`: actual closed source render, not substitute concept art.
- `desktop-closed.png`, `desktop-open.png`, `desktop-open-rear.png`, `mobile-closed.png`, `mobile-open.png`: actual file:// browser captures.
- `mechanism.blend`, `lineage.json`: inherited trimmed articulation and input hashes from Japan v1 at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. Shared `art/vault-kit` remains unchanged.
- Scripts, JSON checks and raw output files contain reproducible acceptance evidence. `initial/` retains actual failed probes and the earlier obscured arch.
- `inventory.json` and `delivery-check.json`: exact SHA-256 and byte counts; archive readback evidence. Their self-referential envelopes are excluded from the payload inventory as documented by the packaging script.

## Verified technical acceptance

Actual Three GLTFLoader: **60 meshes, 17,092 triangles, 6 materials; zero nonfinite vertices and zero degenerate triangles**. All five terrain meshes are lid children. Decoded maps have measured variation (color red-channel ranges 73 and 49, roughness green-channel range 49); no runtime texture requests.

Saved-source independent reopening: continuous hollow floor ray at z=0.2650000155; ten hinge attachment pairs intersect as intended. **81 sampled poses across all 21 moving and 39 static meshes**, plus latch-versus-lid, show zero unintended surface intersections. Only explicit hinge leaf/barrel and latch bearing contacts are exempt. Motion releases latch 80 degrees before lifting lid 105 degrees. This is sampled surface collision evidence, not a continuous solid-volume/manufacturing certificate.

Source/export two-way nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. Three packed source images. Source theme test verifies original pivot, every terrain vertex within the declared envelope, arch aperture ray miss plus crown hit, arch clear of both massifs, and a **0.2051215693-unit** gap between massif X bounds. Deliberately detached terrain is rejected by the same ancestry assertion. Terrain is rigidly attached, not a physics simulation.

Offline Edge desktop 1440x1080 and 390x844 mobile touch emulation: real drag/touch rotation, open/close controls, reset during movement, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open projected extent is approximately 0.8924 NDC, below 1. Actual corrupted GLB bytes reach the loader and show the poster with disabled model controls; no-JavaScript poster also verified. Tests ran on a desktop RTX 4060, **not physical-phone performance tests**.

## Actual failures and fixes

The initial arch was hidden behind and intersected the east massif. `initial/theme-source-output.txt` records an actual assertion failure. It was moved to front-right, with unchanged size; the same clearance assertion then passed. This is the one bounded aesthetic correction, explicitly deviating from the brief's rear-right placement. The initial brief/poster remain preserved.

One inherited 60ms reduced-motion reset check failed; an unchanged bounded rerun passed. The final harness waits for actual animation frames rather than assuming wall-clock sleeps include a frame. Exact endpoint assertions remain. See `corrections.md` and retained failure output; no all-green-history claim.

## Visual verdict and limitations

Actual browser visual inspection: visible open arch, clear fluted massifs, wide warm box, brass fittings, seated terrain, full open silhouette and legible mobile controls. No conspicuous clipping in the inspected views. **Stylized sandstone-inspired art, not photorealistic, not reference equivalence, and not human art approval.** Strata are regular and may look wood-like on the rectangular body. Terrain transitions are abrupt on a flat sand panel, the arch is geometrically regular, and the winding siq is a thin dark inlay rather than an excavated canyon. The strong dark seam is intentional. The terrain is naturally behind the open lid from the front; the rear-open capture and ancestry checks show its attachment. No further aesthetic iterations were needed for the bounded v1 contract; per-asset human review was waived by the user.

## Rebuild

Blender 5.2.1; Python with numpy, Pillow and Playwright; installed Edge; Node.js with Three.js 0.180.0/esbuild 0.25.11. These are build/test dependencies only. `build.py` resolves this folder's node_modules or the linked sibling `iceland-pilot/node_modules`. For extracted sources, install dependencies in this folder. No dependency tree is included. `bootstrap.py` documents the initial copied lineage and is **not** a rebuild step (it would restore predecessor harness files).

From this folder:

```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
node --test tests.mjs
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme_source.py
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

Regeneration overwrites source/render outputs; preserve manual variants separately and refresh inventory afterward. Three.js license is included. Research links are factual inspiration, not embedded copyrighted imagery. Work is additive only in `preview/jordan-v1/`; branch `art/jordan-v1` is backed up, not merged or deployed. Integration into the full 201 equally one-of-one collection is a separate task. No accessories or signed authenticity records were created.
