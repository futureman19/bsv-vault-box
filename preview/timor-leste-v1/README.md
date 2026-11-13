# Timor-Leste v1 — Tais & Indigo

Open **timor-leste-v1.html** directly in Edge/Chrome. This local, self-contained inner collectible needs no server or network. Cosmetic Open/Close, drag/touch rotation, zoom and Reset do not change a seal or custody state. Not minted, hosted or deployed.

## Delivered
- Offline HTML: **3,911,364 bytes**, strictly below 5,000,000.
- GLB: **2,303,284 bytes**; editable packed `timor-leste.blend`.
- Three original procedural 512×512 maps: cotton stripes, cotton roughness and timber grain.
- Real source-rendered `poster.png`/`poster.jpg`, actual desktop/mobile closed/open screenshots, corrupt-parser and no-JS poster screenshots.
- Reproducible author/build/test scripts, trimmed inherited `mechanism.blend`, exact SHA-256 `inventory.json`, readback-verified source ZIP and `delivery-check.json`.

## Design and provenance
The pre-model `design-brief.md` cites UNESCO's Tais listing and UNESCO ICHCAP's craft discussion. Timor-Leste's cotton weaving and yarn-pattern traditions motivate this design; the rust/indigo/ivory stripes and interrupted lines are **invented**, not a copied community motif or a representative national pattern. No third-party photograph, sacred figure or textile scan is embedded. The dark timber frame and brass hardware are collection fiction.

Geometry is script-authored in Blender, not human hand sculpture or a real artisan textile. The waved runner is solid low relief with 56 fringe strands; it is rigidly attached to the lid, not cloth simulation. Existing Japan/Iceland mechanism, viewer and test patterns were reused, not the cedar/tree art. Three.js 0.180.0 is MIT; license included. esbuild 0.25.11 is build-time only.

## Verified acceptance
- Actual GLTFLoader: **27,196 triangles, 116 meshes, 5 materials**, zero nonfinite vertices or degenerate triangles. Decoded textile base-color range 210, actual roughness GREEN-channel range 36, timber range 29.
- Saved source independently reopened: **81 poses, 73 moving and 43 static meshes**, no unintended sampled surface intersections. Latch-versus-lid tests include runner/fringe; only explicit inherited mating bearing pairs are excluded. Ten hinge attachment overlaps and hollow floor ray at z=0.2650000155 pass. This is sampled surface evidence, not continuous collision or manufacturing certification.
- Source/export geometry maximum nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed images present.
- Runner x ±1.55, y ±.82; measured top z **2.0100893974–2.0499105453** inside the prewritten interval. All 56 fringe strands and the runner have lid ownership. Four body cloth panels and inherited lid pivot verified.
- Two motion tests pass, including staged 80° latch / 105° lid endpoints and rejection of missing/nonfinite/empty asset contracts.
- Offline `file://` Edge desktop 1440×1080 and touch-emulated mobile 390×844: real drag/touch rotation, native open/close controls, interrupted reset, reduced motion, no overflow, zero external HTTP requests and runtime errors. Full-open projection max absolute NDC 0.892365. Real corrupted GLB reaches the parser and displays the fallback; no-JS poster separately passes.
- Theme negative control deliberately detaches the runner in memory and exits 1 with `runner_lid_parent=false`; original source remains unchanged. This is post-implementation rejection evidence, not a claimed test-first failure. No actual art failure-and-fix occurred in this run.
- Tests ran on desktop Edge / NVIDIA RTX 4060. Mobile emulation is **not physical-phone performance**; no FPS claim.

## Visual verdict and limits
Source poster, mobile closed and desktop open views were visually inspected. Major stripe groups, timber rails and warm hardware are readable and the box is fully framed. The runner reads as a slightly thick decorative mat rather than soft draped cloth. Fine stripes compress into texture noise at mobile size; the default shallow camera shows less of the runner than the source poster. Dark posts/feet lose detail, and the source render retains sampling grain (denoising disabled). Open front view naturally hides the outside lid ornament; source hierarchy and runtime ancestry establish its attachment. Not photorealism, traditional-pattern fidelity or human art approval. Per-asset review was waived for the collection batch.

## Reproduce
From this directory, use Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge, and Node:

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. Optional rejection proof: Blender `--python verify_theme.py -- --negative-control` must exit nonzero.
8. `python package_delivery.py`

The supplied shared pilot node_modules lacked the actual esbuild entrypoint; identical pinned build dependencies were installed **only here** instead of populating a sibling directory. node_modules is excluded from Git/ZIP. `setup.py` records one-time scaffold provenance and needs sibling Japan files; ordinary regeneration uses the included mechanism and does not need setup.py. Build can use this folder's installed dependencies, falling back to sibling Iceland only if local dependencies are absent. Source regeneration overwrites art; preserve manual variants separately. Byte-preserving `.gitattributes` keeps the exact tested payload intact through Git.

## Scope
Only this new preview directory is added. No shared base-kit changes, blockchain node, keys, minting, broadcasts, chain queries, VPS, production edit, deployment, external messaging or merge. Branch backup only; collection integration is the downstream card.
