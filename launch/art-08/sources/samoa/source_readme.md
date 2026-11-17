# Samoa v1 — Siapo & Lava

Open **samoa-v1.html** directly in Edge/Chrome. The actual GLB, Three runtime, maps and source-rendered poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. Cosmetic movement only; this is an inner collectible, not the custody container. No minting, blockchain/node access, hosting or production integration occurred.

## Deliverables
- `samoa-v1.html`: complete offline viewer, **3,418,632 bytes** (<5,000,000); exact hash in `delivery-check.json`.
- `samoa.glb`: portable model, **1,955,748 bytes**; `samoa.blend`: editable packed Blender source.
- `mechanism.blend`: included read-only-lineage trimmed Japan mechanism, reused for the family pivots/interior/hardware.
- Four procedural 512×512 maps in `maps/`; real source `poster.png` and compressed `poster.jpg`.
- Actual offline browser desktop/mobile closed/open captures, rear-open view and fallback captures.
- `design-brief.md`: written before authoring, sourced cultural/geological rationale and measurable contract.
- JSON checks and raw output logs; `inventory.json` SHA-256/byte ledger; `samoa-v1-source.zip` readback-verified source package. Dependencies/backups excluded.

## What was verified
The actual runtime GLTFLoader reports **63 meshes, 15,474 triangles, five materials**, zero nonfinite vertices and zero degenerate triangles. Four decoded colour/roughness images vary (roughness checked in glTF green channel). Four lid ornaments retain Lid_Hinge ancestry. Palette checks measure the authored map, not subjective cultural authenticity.

Independent saved-source reopening verifies a hollow floor at z=0.2650000155 and ten intersecting hinge attachment pairs. **81 sampled poses cover all 20 moving and 43 static meshes**, plus latch-versus-lid checks, with zero unintended surface intersections. Only explicit original mating bearing pairs are exempt. This is sampled surface clearance, not continuous collision/manufacturing certification. Source/export maximum nearest-world-vertex error is **1.712013073529306e-7**, below 1e-5. Original pivot matrices match the included mechanism. The lid cloth is actual waved solid geometry, not an image plane; three lava accent meshes move with the lid.

Motion tests assert 80-degree latch release before lid movement and 105-degree full lid opening over 81 progress samples. Three malformed geometry inputs are rejected. A deliberately detached cloth ornament is rejected by the source ancestry check; the restored scene is then checked. These are real negative controls, not claimed historical test-first failures.

Offline **file:// Edge** at desktop 1440×1080 and emulated mobile 390×844 passed native click/tap, mouse/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, zero external HTTP requests and zero unexpected runtime errors. Full-open maximum absolute NDC is approximately 0.8924. Corrupted embedded GLB reaches the actual loader and displays the real poster; no-JS poster also passes. Tested on NVIDIA RTX 4060; mobile emulation is not physical-phone performance.

## Visual verdict and limits
Actual source poster and mobile closed/desktop open screenshots were inspected. Whole-box front/side ink repeats, brass and dark shell are readable, with no major clipping or missing panels. The invented repeats are siapo-inspired, **not an authenticated traditional design**. The patterned material still reads like rigid decorative inlay rather than convincingly fibrous barkcloth; the low ripples and lid motifs are subdued at mobile size. The charcoal shell takes a cool blue-gray cast under the studio light; some surfaces read smoother than lava. The three lid stones are a generic geological accent, not an accurate Saleaula landform. Pattern crops at panel borders are intentional but not perfectly continuous. Reduced-sample source rendering retains fine noise.

The raised latch can look visually separated from the open lid from the front view; the inherited long articulated family hardware is mechanically positioned, not an exact manufactured clasp. Source hinge-contact tests and rear-open evidence are separate from this visual limitation. No claim of photorealism, traditional-craft reproduction, user visual approval, real-phone FPS or physical manufacturability. The task's explicit no-per-asset-review directive is honored; final collection integration/review is a separate card.

## Real failures and corrections
- Final brief audit added an explicit lower-bound check on the waved cloth's top vertices. It failed at minimum z=2.0040049553 against the prewritten 2.01 floor (`initial/cloth-height-failure.txt`). Raised the top by .007 units without changing its wave pattern or the gate, then reauthored/rerendered/re-exported and reran source, parity, theme and browser checks. This is a genuine post-implementation failure-and-fix, not a test-first claim.
- Initial build failed because the specified shared `iceland-pilot/node_modules` directory was empty, including in the main checkout. `initial/build-missing-deps.txt` retains the failure. Installed pinned Three 0.180.0/esbuild 0.25.11 locally in this new folder; build then passed. No shared preview files were edited.
- A background shell invocation of `node` returned `stdin is not a tty`. `initial/node-shim-failure.txt` retains it. Reran with the native Node executable; no test thresholds changed.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, and Node/npm. From this folder:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python verify_palette.py`; `node test_motion.mjs`; `python build.py`.
6. `python verify_browser.py`; `python verify_extended.py`.
7. `python package_delivery.py` (creates local archive/inventory; excludes its own mutable log and manifests to avoid self-hashing).

On this Windows host use the explicit native Node executable for shell background jobs. Build resolves local node_modules first; the optional Iceland fallback is only a build dependency, never runtime. `setup.py` records the one-time sibling-script adaptation and is NOT needed for normal standalone reproduction; do not rerun it over later edits. Reauthoring overwrites source/model/poster; keep manual variants separately. Generated HTML and artifact bytes are protected by folder-local `* -text` Git attributes and checked against indexed blobs before commit.

All art/map patterns are independently procedural, not scans or human hand-sculpture. No source images copied. Museum/tourism/NPS URLs inform factual inspiration; Three.js MIT license is included. Collection direction: 201 equally one-of-one designs, with accessories deferred. No asset has been minted by this work. Branch backup only; no merge or deployment.
