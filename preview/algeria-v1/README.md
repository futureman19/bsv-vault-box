# Algeria v1 — Tassili Rock Forest

Open **algeria-v1.html** in Edge/Chrome directly from disk. Complete offline HTML: **3,434,966 bytes**. Embedded GLB: **2,032,836 bytes**. Drag/touch to rotate, Open/Close lid, Reset view. Reduced-motion preference snaps poses. No server, external asset requests or wallet is required.

## Design and files
Original script-authored sandstone geometry and generated maps, inspired by UNESCO's description of Tassili n'Ajjer's eroded sandstone rock forests. See `design-brief.md`, written before modeling, for factual source and measurable contract. No archaeological drawings or third-party photographs/textures are copied. This is an interpretation of one Algerian landscape, not a representation of every Algerian culture or a replica of a specific formation.

- `algeria.blend`: packed editable source; `mechanism.blend`: inherited trimmed articulation/interior source from Japan pilot.
- `algeria.glb`: portable geometry and three embedded 512px maps.
- `poster.png` / `poster.jpg`: actual Blender source render, not promotional AI art.
- `desktop-closed.png`, `desktop-open.png`, `desktop-open-rear.png`, `mobile-closed.png`, `mobile-open.png`: actual offline browser evidence.
- `maps.py`, `author.py`, `build.py`, `viewer.js`, `motion.mjs`: reproducible pipeline.
- JSON checks, raw output logs and `initial/`: executed evidence including failures. `inventory.json` hashes every packaged payload; `delivery-check.json` identifies the archive and exact delivery sizes.

## Verified
- Actual Three.js GLTFLoader: **114 meshes, 26,500 triangles, 4 materials**, zero nonfinite vertices and degenerate triangles.
- Seven uneven sandstone towers and sand apron attached to `Lid_Hinge`, 51 shallow body erosion flutes. Bounds and palette checked through actual loader. Color red-channel ranges 70 and 44; roughness green-channel range 39. Missing-tower mutation is rejected, then restored and accepted (post-implementation negative control, not TDD).
- Independent saved-source reopening: complete moving-descendant coverage, seven tower/apron surface contacts and apron/lid contact, hollow floor ray at z=0.2650000155 and ten hinge attachment pairs.
- **81 poses, all 24 moving and 90 static meshes**, including ornaments, checked for moving/static and latch/lid surface collisions. Zero unintended intersections. Only explicit concentric hinge leaf/barrel and latch knuckle/bridge/pin mating bearings excluded. Fixed intended body construction overlaps are not moving collisions. Sampled BVH surface checks are not continuous collision, containment or manufacturing certification.
- Exact inherited pivots and staged 80° latch release, then 105° lid lift. Node motion tests also exercise invalid asset contracts.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7** (<1e-5); all three source images packed. This is geometric parity, not identical Blender/browser shading or a byte-identical re-export claim.
- Offline file:// Edge at desktop 1440×1080 and touch-emulated 390×844: native open/close, drag/touch rotation, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Full-open projection maximum absolute NDC 0.892365. Real corrupted GLB reaches parser and displays disabled-control poster fallback; no-JS poster also checked.
- Tests ran on desktop NVIDIA RTX 4060. Mobile emulation is **not physical-phone performance testing**. No FPS guarantee.

## Failure-and-fix record
1. Optional Codex lane failed authentication (401) without edits. Hermes implemented directly; no credential changes.
2. First Edge launch crashed at new_page. Explicit D3D11 GPU launch and a nonconcurrent browser run succeeded. Exact initial traceback preserved; causality beyond the successful configuration is not claimed.
3. Initial rock profiles looked vase-like. One bounded silhouette correction replaced pinched rings with angular tapered buttresses and uneven tops; first source poster retained.
4. Actual runtime theme gate rejected tower 03 at **0.8187336922** high, above the 0.80 bound. Its nominal height was reduced from 0.74 to 0.70; final runtime height **0.7744777203**. The gate was not relaxed.
5. Texture gate initially read the red channel of glTF metallic/roughness, which is constant. Corrected to the standard **green roughness channel**, preserving the variation threshold. Tracebacks retained.

## Visual verdict and limits
Actual closed desktop and open mobile images were inspected. The chest and rock-forest motif read clearly, with no obvious floating parts or framing failures; the open view demonstrates the hollow interior. Not photorealistic or a calibrated site reconstruction. Body flutes remain somewhat regular/wood-like, towers are simplified and partly overlap from the default view, and the thin sand apron reads like an applied miniature plaque. Rear/interior/hardware are family design extrapolations, not an Algerian craft-history claim. Small mobile secondary text is readable but dense. Human per-asset review is waived for this collection batch; this is not user-approved visual equivalence.

## Reproduce
Blender 5.2.1; Python with numpy/Pillow/Playwright and installed Edge; Node with Three 0.180.0/esbuild 0.25.11. Build uses local node_modules or sibling `iceland-pilot/node_modules`; dependencies are not shipped. For standalone extraction, run `npm install` here. Included compiled runtime lets the viewer run without these tools.

```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
node --test tests.mjs
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
python verify_browser.py
python verify_theme.py
python package_delivery.py
```

Regeneration overwrites source/render outputs; preserve manual edits separately. Re-run checks and packaging after regeneration. Hash inventory excludes itself and archive/delivery envelope to avoid self-reference. ZIP readback checks exact entries and bytes; backups/caches/node_modules are excluded. Research text is inspiration only. Three.js MIT license included. Mechanism/viewer/test lineage: Japan cedar v1 on local base ff5d78f1e0d486af5c882c184fc08049996ebdc8; shared vault kit unchanged.

## Product boundary
Local inner collectible preview only, not the functional outer custody container. Cosmetic opening changes no seal or transaction. No blockchain node, keys, mint, sale, chain query, broadcast, website deployment or on-chain storage. Launch direction: 201 equally one-of-one designs (195 countries + five oceans + Moon). Future off-chain content-addressed storage and signed provenance remain unimplemented. This branch is backed up separately; no integration or merge is authorized here.
