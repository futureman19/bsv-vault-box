# Saint Vincent and the Grenadines v1 — Soufrière & Cays

Open **saint-vincent-and-the-grenadines-v1.html** directly in Edge/Chrome. Entire viewer, model, textures and actual-source poster are embedded: **2,017,290 bytes**, strictly below 5,000,000. Standalone GLB: **952,272 bytes**. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion snaps to endpoints.

## Design and provenance
A charcoal volcanic-stone keepsake box with a turquoise enamel sea inset, five separate sand-edged green cays, a schematic reef arc and a raised asymmetric crater. The frozen `design-brief.md` preceded modeling and cites the government's descriptions of La Soufrière and Tobago Cays. This is an invented compressed landscape composition, **not a geographical map**: the volcano is not in the Tobago Cays. No third-party photographs or textures were copied. Procedurally authored Blender meshes and generated maps, not scans or human hand-sculpture.

Source: `saint-vincent-and-the-grenadines.blend`; portable model: matching `.glb`. `mechanism.blend` is the repository's trimmed Japan pilot mechanism, retaining the family pivots, hollow liner, brass latch and hinges, but not the cedar/tree artwork. `author.py`, `geometry_helpers.py` and `maps.py` reproduce the asset. `poster.png` is a 900×720 Cycles source render, with `poster.jpg` embedded in the viewer. Desktop/mobile screenshots are actual offline browser captures, not promotional artwork. Three.js 0.180.0 is MIT; see `THREE-LICENSE.txt`.

## Gates actually passed
- **Source:** independent saved .blend reopen. 24 moving meshes and 35 static meshes, **81 full-motion samples**, no unintended BVH surface intersections. Latch-versus-lid included, ornaments included. Only named coaxial hinge-leaf/barrel and latch-knuckle/bridge/pin bearing contacts exempt. Ten hinge attachment pairs overlap. Hollow floor ray hits Interior floor at z=0.2650000155.
- **Mechanics:** original pivot matrices preserved; 80° latch release over first quarter, then 105° lid opening. Two Node tests passed, with 81 numeric samples and rejected invalid geometry fixtures.
- **Parity:** 5,904 source vertices versus 19,716 exported split vertices; bidirectional maximum nearest-vertex error **1.712013073529306e-7**, below 1e-5. All three maps packed in saved source.
- **Theme:** five cays, all terrain/sea/reef on lid, sampled source crater depth **0.31999921798706055**; raised rim height within brief. Deliberately detached cay fails the ancestry assertion, restored without saving the broken fixture.
- **Actual GLTFLoader:** 11,320 triangles, 65 meshes, seven materials; zero nonfinite vertices or degenerate triangles. Three 256×256 portable maps decode with nonzero variation (base-color red range 38, roughness **green** range 75, normal red range 60). Export splits multi-material cays into group plus two primitives: 15 matching runtime nodes represent five source cays, not fifteen islands.
- **Offline browser:** Edge file://, 1440×1080 desktop and 390×844 touch-emulated mobile. Real clicks/taps, drag/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP(S) requests or runtime errors. Open silhouette maximum absolute NDC 0.93410935 (<1). Actual corrupted GLB reaches parser and shows poster/disabled controls; no-JS poster also loads. RTX 4060 browser; **not physical-phone performance testing**.
- **Delivery:** `inventory.json` records exact byte counts and SHA-256 per artifact. `delivery-check.json` verifies the required artifact set and every ZIP entry on readback. Local `* -text` preserves bytes through Git. Packaging envelopes are excluded from their own recursive hashes.

## Visual verdict and limits
The final source and actual mobile/rear-open screenshots were inspected. Five cays are distinguishable in the final higher view; the stone's initial patterned appearance was reduced using irregular multiscale grain. The turquoise panel is intentionally enamel-like, islands are faceted reliefs, and the reef arc looks like fine decorative wire rather than a living reef. The crater has measured depth and reads clearly in the source render, but its small opening can still read as an uneven summit at mobile size. Brass hardware remains simplified. In open rear views the small hinge joints and projecting volcano root can look under-explained despite tested attachment geometry. Source render retains mild sampling grain. No photorealism, reference equivalence, continuous collision proof or engineering/manufacturing certification claimed.

One bounded presentation correction was made (higher camera plus nonperiodic stone texture); `initial/` retains first-pass source/mobile images. No further art polish is implied by technical PASS.

## Actual failures and fixes
- Optional isolated Codex lane exited on authentication HTTP 401, made no changes, and was not used. Hermes authored/reviewed/executed everything directly; `codex-lane.log` retains the failure, without credentials.
- The requested shared `node_modules` target existed but was empty, so the initial build failed `MODULE_NOT_FOUND` for esbuild. Dependencies were installed **only in this new folder**, pinned by package-lock.json. A subsequent browser launch from the initial shell lacked `set -e` and failed because no HTML existed; `initial/browser-output.txt` retains that real failure. Final verification runs use fail-fast sequencing. The original build-error log was inadvertently replaced by a first-success checkpoint; this note reports that limitation rather than claiming it is preserved.
- Background `node` shell shim returned `stdin is not a tty`; retained as `initial/motion-node-shim-failure.txt`. The same tests passed using the explicit native Node executable. No test threshold was weakened.

## Reproduce
Prerequisites: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node.js. From this folder:

1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly for `verify_theme.py`, `verify_parity.py`, `verify_source.py`.
5. `python build.py`
6. `python verify_browser.py` and `python verify_extended.py`
7. `"C:/Program Files/nodejs/node.exe" --test tests.mjs` (or native Node on another OS).
8. `python package_delivery.py`

Source builds use local dependencies first; build.py can fall back to a populated sibling pilot. `setup.py` is the historical template bootstrap, **not a rebuild step**: it reads the sibling Japan pilot and would overwrite local customized files. Normal author/build/check scripts use included local source assets. Authoring overwrites generated .blend/GLB/poster, so save manual edits separately; regeneration requires refreshed evidence/inventory. Source ZIP excludes dependencies/cache/backups. Inventory excludes its own envelopes and active packaging log.

## Scope
Local art asset with backed-up branch only; not minted, hosted, deployed, sold or chain-verified. Cosmetic lid movement has no custody effect. No node service, keys, wallets, blockchain queries, transactions, VPS or production changes. The collection remains 201 equally one-of-one designs. Next step is the separately gated collection integration/review package; no merge performed here.
