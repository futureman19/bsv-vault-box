# Belgium v1 / Petit Granit

Open **belgium-v1.html** directly in Edge/Chrome. Complete offline 3D runtime, GLB, textures and actual Blender poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. Reduced-motion preference snaps the articulated pose. This is an inner collectible art preview; no minting, custody action, chain connection, hosting or deployment.

## Delivery
- HTML: **4,095,204 bytes**, strictly below 5,000,000.
- GLB: **2,488,292 bytes**; 26,296 triangles, 124 meshes, five materials.
- `belgium.blend`: packed, named editable Blender source. `mechanism.blend`: reused trimmed collection mechanism from the Japan pilot.
- Three procedural 512×512 maps, actual `poster.png`/`poster.jpg`, desktop/mobile closed/open screenshots and fallback captures.
- `belgium-v1-source.zip`: complete required source/model/viewer/maps/scripts/evidence package, no dependencies or backups. `inventory.json` gives exact bytes and SHA-256 for payload files; `delivery-check.json` gives archive identity and actual ZIP readback validation. Manifest/packaging envelopes exclude themselves to avoid circular hashes.

## Design and visual verdict
The prewritten sourced `design-brief.md` is the primary reference. This represents the blue limestone of Soignies/Wallonia through a honed blue-grey body, darker polished lid and low pale fossil-inspired rosette. Eight segmented curved arms form a raised decorative relief, not an embedded scientifically accurate crinoid. Four continuous panels replace cedar finger courses; brass is inherited collection language, not a historical Belgian chest reconstruction.

Actual source and mobile screenshots were inspected. Box, ornament, brass and controls read clearly with no observed major floating or broken geometry. The uniform small fossil loops remain conspicuously procedural; mobile relief is angular/blocky and its central junction is crowded. This is stylized collectible art, **not photorealism, an authentic specimen, a scan or a human-crafted traditional object**. Rear/interior/hardware are extrapolations. No external source photos are used as textures.

## Verified evidence
- `source-check.json`: independently reopened saved source; hollow floor ray z=0.2650000155; all **85 moving / 39 static meshes** included in **81 poses**, zero unintended sampled surface intersections. Latch-vs-lid also sampled. Only moving hinge-leaf/fixed-barrel and latch knuckle-or-bridge/pin bearing contacts exempted. Ten connecting hinge attachment pairs tested separately. This is sampled surface evidence, not continuous collision or manufacturing certification.
- `parity-check.json`: saved-source versus independently imported GLB, bidirectional nearest-vertex maximum **1.712013073529306e-7** units, under 1e-5 tolerance; all three packed images present.
- `theme-check.json`: 69 ornament parts, eight open-gap rays, seated minimum z=1.978, highest z=2.0480000973; footprint bounds, nonoverlapping shell-panel volumes, exact original mechanical pivots and lid ancestry pass. Deliberately removing one ornament's lid parent produces **AssertionError: ornament ancestry**; restore returns the original design. This is a post-implementation negative control, not a test-first claim.
- `motion-output.txt`: two unit tests pass, zero fail; release to -80 degrees before lid moves to -105 degrees; clamped endpoints and rejected missing/empty/nonfinite geometry inputs.
- `browser-check.json`: actual GLTFLoader, zero nonfinite vertices/degenerate triangles; desktop 1440×1080 and touch-emulated mobile 390×844 under offline `file://`. Native controls, pointer/touch rotation, open/close, interrupted reset, reduced motion, no overflow, zero external HTTP requests and no successful-case JS errors. Full-open maximum absolute projected NDC 0.892364652 < 1. Real invalid GLB bytes reach the parser and produce the expected caught error plus poster fallback.
- `extended-check.json`: actual decoded base-color variation and roughness GREEN-channel range; blue-grey body means RGB 61.17/73.89/84.61. All 69 runtime ornament meshes have correct lid ancestry. No-JS poster and visible/accessibility country copy checks pass.
- `delivery-check.json`: explicit required-file set, nonblank source poster, HTML cap, exact ZIP entry bytes and CRC readback pass. Folder-local `* -text` preserves delivered bytes through Windows Git checkout; staged inventory verified independently before commit.

Browser used Edge/ANGLE NVIDIA RTX 4060. Mobile is desktop touch/viewport emulation, **not physical-phone performance**. No FPS or long-duration endurance claim. Named negative controls and real corrupt-parser failure establish tests can fail; no art-gate failure occurred in this bounded pass.

## Recovery and tooling notes
The optional Codex input lane failed immediately with authentication HTTP 401/token-refresh error, exit 1. No Codex edits or commits were accepted; Hermes authored and verified this asset directly. No credential repair was attempted. The prescribed main-checkout node_modules contained no esbuild entrypoint, so the unchanged pinned dependencies were installed only inside this new directory. No sibling toolchain was modified. The inherited Japan template contained a literal truncated media-query fragment; this was repaired before the first build rather than called a passing inherited stylesheet. Synchronous reduced-motion input snapping avoids dependence on a prompt next animation frame; render/camera updates remain in the frame loop.

## Reproduce
Dependencies: Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node.js. Run within this directory:

```text
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
node --test --test-reporter=tap tests.mjs
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

Capture motion stdout as `motion-output.txt` before packaging. Build tools use local dependencies first; standalone archives need `npm ci`. Generator uses the included mechanism, not sibling source paths. Authoring overwrites model/poster; preserve manual edits separately. Rendering bounded to two threads, 24 samples, 900×800 and denoising disabled; minor sampling noise remains. Three.js 0.180.0 MIT license included; esbuild 0.25.11 is build-only. All maps and new geometry are procedural. User waived per-asset human review until the full collection; branch backup only, no merge.
