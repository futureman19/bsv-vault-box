# Mauritania v1 — Richat / Eye of the Sahara

Open `mauritania-v1.html` directly in Edge/Chrome: an offline, embedded 3D collectible with orbit, staged opening, reset and reduced-motion support. Cosmetic only; no mint, transaction, custody-state change or hosting.

## Deliverables and measurements
- HTML: **2,986,118 bytes**, strictly below 5,000,000 bytes, including runtime, GLB and source-rendered poster.
- GLB: **1,685,824 bytes**; real GLTFLoader reports 28,048 triangles, 56 meshes, five materials, zero nonfinite vertices or degenerate triangles.
- `mauritania.blend`: editable, packed Blender source. `mechanism.blend`: inherited trimmed mechanical base, not the Japan scenery. `maps/`: three original 512×256 procedural maps. `author.py` and helper/finish scripts regenerate the model and actual poster.
- `poster.png`/`.jpg`: actual source render, not AI promotional art. Desktop/mobile screenshots are actual offline browser captures.
- `inventory.json` and `delivery-check.json`: exact sizes and SHA-256 hashes, required-artifact inventory, archive readback and embedded payload identity. Source ZIP includes source, GLB, HTML, maps, scripts and checks; no dependencies or credentials.

## Brief and visual interpretation
The brief was written before modeling, drawing on NASA Earth Observatory's descriptions of the Richat Structure's eroded domed anticline, concentric cuestas and surrounding dunes. These textual sources are linked in `design-brief.md`. No NASA imagery, pixels, logos or third-party textures are used. This is one landscape interpretation, not a claim to represent all Mauritanian culture, historic craft, or measured geology.

Three irregular geometric ridge bands and erosion channels form the lid's eye. The relief reaches 0.329667 units above the slab; all terrain follows the lid. Body uses warm sand/ochre bedding, contrasting slate crests/feet and brass fittings. Source coordinates retain front -Y, hinge rear +Y, +X head-on right, Z up.

Actual-source and mobile/open screenshot inspection found the whole silhouette readable and unclipped, without obvious floating pieces or severe visible geometry failure. **Deliberately stylized, not photorealistic:** pale sandy lighting and regular mineral bedding can read as wood grain; ring crests are exaggerated and serrated, not accurate natural topography. The dark rim and corner blocks are conspicuous; hardware mounts are mechanically connected in the geometry but visually understated in the open view. The terrain is naturally mostly hidden behind the upright lid from the front. No image-reference equivalence is claimed.

## Verified evidence
- `source-check.json`: independently reopened saved source, hollow floor ray z=0.2650000155, 81 sampled poses, all 17 moving and 37 static meshes, zero unintended surface intersections. `hinge-attachment-check.json` confirms ten intersecting attachment pairs. Only explicitly named mating bearings are exempt. All terrain participates. This is sampled surface collision checking, not continuous clearance/manufacturing certification.
- `parity-check.json`: bidirectional saved-source/export world-vertex maximum error 1.712013073529306e-7 (<1e-5); three packed images. Not byte-identical Blender roundtrip certification.
- `theme-source-check.json`: actual geometry sampled at three crests and valleys; all crests exceed adjacent valleys by >0.07. A flattened-geometry negative control is rejected. It is post-implementation regression evidence, not test-first TDD.
- `motion-check.json`: 81 sampled runtime poses; 80° latch release before 105° lid rotation; invalid geometry rejected.
- `browser-check.json`: actual file:// Edge at 1440×1080 desktop and 390×844 touch-emulated mobile; native controls, mouse/touch orbit, open/close, interrupted reset, reduced motion, no overflow, no external HTTP requests or JS errors. Open projected maximum absolute NDC 0.892365. Genuine corrupt GLB reaches the parser and displays the actual poster.
- `extended-check.json`: all three runtime terrain material primitives have lid ancestry; decoded color/roughness ranges 62/75/77; no-JavaScript poster loads. `desktop-open-rear.png` shows the moving terrain from behind.
- Desktop NVIDIA RTX 4060 browser; mobile emulation is **not physical-phone performance testing**. No FPS, long-session reliability, wallet compatibility or on-chain storage verified.

## Real failures and fixes
Two failing extended checks are retained under `initial/`. The first incorrectly assumed glTF multi-material meshes retain the source object name on each primitive. It was fixed by checking the actual parent hierarchy. The second sampled roughness's red channel; glTF packs roughness in green. The test now decodes the correct channel, retaining the same >30 variation threshold. No geometry/size/clearance thresholds were relaxed. Original numpy map generation also hit host allocation pressure; deterministic Pillow/stdlib generation replaced it. One browser run timed out; the same bounded test subsequently completed. Optional Codex implementation lane failed authentication before making changes; all implementation and verification were performed directly by Hermes.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/Playwright, installed Edge, Node, Three.js/esbuild per package.json. Build resolves local node_modules or the sibling iceland-pilot toolchain (linked in this worktree); no dependencies are required to VIEW the HTML. For standalone source extraction install the declared npm dependencies locally. `setup.py` is lineage bootstrap only and requires the sibling Japan directory; normal rebuild does NOT run it and uses the included helpers/mechanism.

```
python run_checks.py
python package_delivery.py
```
Use `python run_checks.py --skip-author` to rerun build and all acceptance against the saved source. `BLENDER`/`NODE` override the default Windows executable paths. Regeneration overwrites assets; preserve manual edits separately. Run packaging last after documentation/evidence changes. Inventory excludes itself, delivery-check and ZIP to avoid recursive hashes.

Scope is additive under this directory only. No other preview, shared kit, production docs, mint/vault code, blockchain service, keys, VPS or deployment changed. Branch backup only; integration remains a separate collection task. Three.js license included. Technical acceptance is autonomous per collection directive; no per-asset human approval is implied.
