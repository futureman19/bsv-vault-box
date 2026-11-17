# Micronesia v1 — Basalt & Tidal Canals

Open **micronesia-v1.html** directly in Edge/Chrome. Fully embedded offline interactive art: drag/touch rotate, Open/Close lid, Reset, reduced motion and actual-render fallback. No server, wallet, chain or external assets. This is cosmetic movement of an inner collectible, not a custody operation.

## Delivered
- HTML **2,738,484 bytes**, strictly below 5,000,000.
- GLB **1,461,776 bytes**; editable packed `micronesia.blend` and inherited trimmed `mechanism.blend`.
- Three generated 256×256 maps, reproducible author/build/check scripts, actual source-render PNG/JPEG, desktop/mobile closed/open and rear-open captures.
- `inventory.json`: SHA-256 and exact bytes for every packaged payload. `delivery-check.json`: archive readback and explicit required artifact checks. ZIP is source/art/evidence, not runtime.

## Design and limits
The sourced written brief was frozen before modeling. Pohnpei-inspired stacked basalt, six pale constructed islets separated by a teal channel network, and a small open stone enclosure. This invented miniature is not a surveyed Nan Madol reconstruction, sacred structure reproduction, historical artifact, endorsement, or a representation of all FSM cultures. Geometry and maps are procedural, not scans or hand sculpture. No third-party images are used.

Actual source and browser visual review: wide stone-block chest, clear gold hardware and teal inlay. Stylized rather than photoreal: basalt remains smooth and regular, water is a shallow opaque inlay rather than simulated water, feet are rounded/rough, and the low enclosure reads somewhat like a small well. At mobile size the motif is readable but counting all six platforms is not immediate. Source Cycles render has visible sampling noise (24 samples, no denoising); it is real source evidence, not promotional art. Front-open view naturally hides outward lid relief; rear-open capture documents it. No supplied approved illustration or visual-equivalence claim.

## Verified here
- Build succeeded: `HTML_BYTES 2738484 GLB_BYTES 1461776`.
- Independent saved-source reopening: **81 poses**, **56 moving / 147 static meshes**, **zero unintended surface intersections**; latch vs lid included. Only original named hinge/latch mating-bearing surfaces excluded. Ten hinge attachment intersections pass. Interior floor ray z=0.2650000155. These are sampled surface checks, not continuous collision/manufacturing certification.
- Original lid/latch pivot world matrices match trimmed mechanism. Motion unit tests exercise release-before-opening, 80° latch, 105° lid, clamping and invalid asset rejection.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. All three images packed in source.
- Actual Three GLTFLoader: **203 meshes, 17,196 triangles, 5 materials**, zero nonfinite/degenerate triangles. Every one of 40 relief meshes has lid ancestry. Three decoded map ranges 51,109,54; roughness sampled from its actual GREEN channel.
- Theme: six platforms, 112 real basalt course blocks, relief height 0.383; exposed connected canal cross sampled with downward saved-source geometry rays; enclosure center open. A deliberately detached platform is rejected by the SAME ownership gate before restoration (negative control, not an implementation failure).
- Edge offline `file://`: 1440×1080 desktop and 390×844 touch emulation, native open/close, drag, interrupted reset, reduced-motion endpoints, no HTTP(S) requests/errors/overflow. Open projection max absolute NDC 0.892365. Genuine corrupted GLB reaches parser and produces poster fallback; JS-disabled poster also checked. RTX 4060 desktop GPU, **not physical-phone performance testing**. No FPS claim.
- Poster decoded nonblack coverage >72%, alpha opaque coverage 100%.

## Failure history
The optional Codex implementation lane exited on authentication failure and contributed no edits. Hermes implemented and tested directly; no credential changes were attempted. `codex-lane.log` preserves the failure (no tokens).
The first build genuinely failed because the requested sibling node_modules source was empty. `initial-build-failure.txt` preserves it. Fixed by installing the exact already-pinned Three 0.180.0 / esbuild 0.25.11 dependencies locally within this preview, then rebuilding successfully; no gate relaxed. No geometry collision or source-parity failure occurred.

## Reproduce
Requirements: Blender 5.2.1; Python with numpy, Pillow and Playwright; installed Edge; Node/npm. In this directory:

```text
npm ci --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme.py
node --test tests.mjs
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

Regeneration overwrites output; retain manually edited source separately. `setup.py` is the original adaptation recipe and requires sibling Japan v1; it is NOT needed for normal standalone reproduction, whose author script loads the included mechanism. Build uses local modules or the sibling installed toolchain. Node modules/caches/backups are not packaged. Windows exact payload bytes preserved with folder-local `* -text`; inventory validated against staged Git blobs before commit.

Three.js MIT license included. Shared kit and all other previews remain untouched. Local branch-backed art only: not hosted, minted, signed, sold or stored on-chain. Proposed collection remains 201 equally one-of-one designs. Integration/gallery review belongs to the separate final card; per-asset review was explicitly waived.
