# Maldives v1 — Faro / Lagoon & Sand

Open `maldives-v1.html` directly in Edge/Chrome. Complete embedded runtime/model/poster; no server or network required. Drag or touch to rotate, Open/Close lid, Reset view. Cosmetic movement only: not a custody seal, minted NFT or chain operation.

## Delivery
- HTML: **2,245,553 bytes**, strictly below 5,000,000.
- GLB: **1,102,092 bytes**, embedded procedural maps; 15,656 triangles, 60 meshes, 6 materials.
- `maldives.blend`: packed editable source; `mechanism.blend`: inherited trimmed mechanical base.
- `poster.png` / `.jpg`: real 900×820 source render, not AI promotional artwork.
- Desktop/mobile closed/open, rear-open and fallback PNGs: actual offline browser captures.
- `inventory.json`, source ZIP and `delivery-check.json`: exact bytes/SHA-256 and archive readback; no build dependencies or Blender backups archived.

## Design and visual limits
Research-backed brief was written before model authoring. This is an invented low oval faro, with a raised sand-colored reef, turquoise lagoon, an open channel and three green cays. It is not a named atoll or geographically scaled reconstruction. No traditional pattern or sacred symbol is claimed. Geometry/maps are script-authored, not scans, real coral or artisan hand sculpture.

Source and mobile image review found all three cays, the ring and lagoon readable, without model/UI clipping. Deliberate stylization remains: smooth green cays resemble pebbles, reef break has geometric edges, lagoon is opaque enamel rather than simulated water, brass is simplified, and low-sample source render has visible grain. No photorealism or reference equivalence claimed. This bounded first version is complete under the collection's no-per-asset-review instruction.

## Verified evidence
- `source-check.json`: independent saved-source reopening, hollow floor ray z=0.2650000155, 21 moving meshes versus 39 static meshes across **81 poses** plus releasing latch versus lid. Zero unintended surface intersections. Only named mating hinge/latch bearings excluded. Ten hinge attachment pairs overlap; all ornaments included. Sampled, not continuous collision or manufacturing certification.
- `parity-check.json`: source/export nearest world-vertex error in both directions **1.712013073529306e-7**, below 1e-5; three packed source maps.
- `theme-check.json`: five lid-owned ornament objects, three cays, 80 upward-facing reef top quads, actual rays hit lagoon/reef/channel/ocean, z limits, and independent inherited pivot matrix equality. A deliberately detached cay is rejected by the ancestry predicate, then restored in memory.
- `browser-check.json`: actual GLTFLoader, zero nonfinite/degenerate vertices. Edge file:// offline desktop 1440×1080 and 390×844 touch emulation; native open/close, drag/touch rotation, mid-motion reset, reduced motion, no overflow/errors/external HTTP requests. Full-open maximum absolute NDC 0.926991. Corrupt actual GLB bytes reach the parser and activate poster/disabled controls.
- `extended-check.json`: source-poster pixel sanity, all three actual decoded portable map slots vary (roughness GREEN channel), correct visible/accessibility country copy, no-JS poster, rear-open capture.
- `motion-output.txt`: staged 80-degree latch before 105-degree lid, endpoint clamps and invalid geometry rejection tests.
- Mobile emulation used a desktop NVIDIA RTX 4060, not a physical phone or performance/FPS benchmark.

## Real failure and fix
`build-initial-output.txt` preserves MODULE_NOT_FOUND for the requested inherited esbuild path: its shared node_modules directory was empty. Installed the exact existing pins locally in this new preview only (Three 0.180.0, esbuild 0.25.11); successful build is in `build-output.txt`. No shared preview was repaired or modified. No geometry/collision assertion failed in this run. The first packaging assertion also failed because it expected TAP `# fail 0` while Node defaulted to the spec reporter (`ℹ fail 0`). Preserved that successful spec test output in `motion-initial-spec-output.txt`, then explicitly reran with `--test-reporter=tap`; no test threshold changed. Negative controls are regression checks, not claimed test-first failures.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, and Node.js. Run from this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender similarly for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test tests.mjs`; `python build.py`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`

`author.py` is the self-contained generated author script. `setup.py` documents initial helper/viewer adaptation from the sibling Japan pilot and is not needed for normal reproduction; rerunning setup overwrites adapted scripts and needs that sibling. Regeneration overwrites artifacts; preserve manual edits separately. Build can use local pinned dependencies or the sibling installation, neither required by the delivered HTML. Three MIT license included. Brief cites factual inspiration only; no third-party image pixels are embedded.

## Scope
Only new `preview/maldives-v1/` files, on `art/maldives-v1`. Branch backup is not public hosting. No production docs, vault, mint, shared art kit, VPS, keys, chain queries or transactions touched. Proposed collection remains 201 equally one-of-one designs; storage, issuance and custody are outside this art task. Next: integrate this backed-up branch through the collection's final integration card.
