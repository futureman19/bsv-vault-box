# El Salvador v1 — Añil & Volcanic Lagoon

Open **el-salvador-v1.html** directly in Edge/Chrome. It embeds the model, Three.js runtime, procedural maps and an actual Blender-rendered poster; no server/network is needed. Drag/touch to rotate, Open/Close lid, Reset view. Reduced-motion preference is honored. This is cosmetic art, not custody, minting or a blockchain operation.

## Delivery
- Standalone HTML: **2,264,441 bytes**, strictly below 5,000,000.
- GLB: **1,077,848 bytes**; 12,808 triangles, 57 runtime meshes, six materials.
- Named editable `el-salvador.blend`, packed maps; trimmed inherited `mechanism.blend`; author/map/build/test scripts; source-rendered PNG/JPEG poster and actual offline screenshots.
- `inventory.json`: exact per-file byte counts and SHA-256. `delivery-check.json`: explicit required-file set, ZIP inventory and byte-for-byte readback. ZIP excludes dependencies, caches and Blender backups. Folder-local Git attributes preserve exact bytes.

## Verified
Saved source independently reopened; 18 moving meshes versus 38 fixed meshes through **81 opening poses**, plus latch against lid: zero unintended sampled surface intersections. Only named inherited mating hinge barrels and latch bearings are exempt. Ten hinge attachment intersections verified. Hollow floor ray z=0.2650000155. Inherited pivot matrices compared to separately opened mechanism source. Not continuous collision detection or mechanical certification.

Source/export nearest-vertex distance 1.712013073529306e-7 units, below 1e-5. Actual GLTFLoader reports zero nonfinite vertices and zero degenerate triangles. Three compact portable 256px maps verified; color ranges 78/79 and roughness green-channel range 153. Crater and water ancestry, bounds, root height and five downward lagoon rays pass. Detached-parent and wrong-color negative controls are actually rejected; invalid runtime geometry and real corrupted GLB are rejected too.

Actual offline file:// Edge desktop 1440×1080 and mobile 390×844 with native touch emulation pass rotation, native open/close controls, interrupted reset, reduced motion and no overflow. No external HTTP requests or unexpected runtime errors. Full-open maximum absolute projected NDC ~0.9673 (<1). Actual invalid embedded bytes hit the parser and display the poster/disable controls; JavaScript-disabled poster also passes. Emulated mobile runs on desktop RTX 4060, not physical-phone performance evidence.

## Art verdict and limits
A stylized indigo-blue keepsake box with refined brass fittings, dark stone lid, uneven crater and a small visible turquoise lagoon. Source and mobile/desktop screenshots inspected; no serious clipping or presentation defects. Body appears brighter/cobalt under studio lighting than a deep textile indigo; the pale marks are invented resist-inspired accents, not a claimed Salvadoran historical pattern. Stone is faceted, crater compact, water an opaque satin inlay rather than realistic fluid. The front rim partly hides the lagoon. No photorealism or precise Santa Ana topography is claimed. Suchitoto dye craft and Ilamatepec lagoon sources are cited in the prewritten design brief; no third-party photos or AI promotional substitute is embedded.

One bounded visual correction lowered the front crater rim by up to .22 units and darkened the ash band; the original source poster is retained in `initial/`. This keeps the overall prewritten bounds and opens the lagoon at normal mobile scale. Back/interior and fitting details are collection-family extrapolations.

## Real failures and corrections
- Optional Codex lane failed authentication before implementation; no Codex edits accepted. `codex-lane.txt` retains the failure. Hermes authored and tested directly, without touching credentials.
- Initial build failed `MODULE_NOT_FOUND`: the prescribed main-checkout dependency directory was empty. Retained `initial/build-output.txt`; installed pinned Three 0.180.0/esbuild 0.25.11 locally in this preview, no shared dependency modifications. Final build succeeds.
- Background shell `node` shim failed `stdin is not a tty`; retained `initial/motion-shim-failure.txt`. Canonical verification invokes the actual Node executable. No assertion was weakened.

## Reproduce
Build-time tools: Blender 5.2.1, Python with numpy/Pillow/Playwright, Edge, Node. Run from this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` — rebuilds HTML and independently runs motion, reopened source/collisions, parity, theme, desktop/mobile/fallback/map checks. Native Blender/Node paths are explicit in this wrapper; adjust on another machine. It does not regenerate the model.
5. `python package_delivery.py` — regenerate inventory/ZIP after any artifact changes.

Rendering uses bounded CPU threads and no denoising; residual source-render grain is disclosed. Generation overwrites output; save manual edits separately. Viewer itself needs none of these build tools. Mechanism/viewer lineage is repository Japan Cedar v1 from base ff5d78f; Three.js MIT license included.

Only this new preview directory is delivered. No shared base kit changes, hosting, production changes, chain queries, signing, minting, deployment or claims of on-chain storage. Branch backup only; integration into the 201-design collection is separate.
