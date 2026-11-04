# Pakistan v1 — Multan Blue

Open **pakistan-v1.html** directly in Edge/Chrome. All model/runtime/poster assets are embedded. Drag or touch to rotate, Open/Close lid, Reset; reduced motion supported. Cosmetic animation only, not custody or an on-chain seal.

- HTML: **2,990,885 bytes**, strictly below 5,000,000.
- GLB: **1,552,160 bytes**.
- `pakistan.blend`: packed editable, script-authored Blender source.
- `mechanism.blend`: inherited trimmed Japan mechanical source; not country art.
- `poster.png`/`.jpg`: actual source render, not generated promotional imagery.
- `pakistan-v1-source.zip`: reproducible scripts, maps, source, model, viewer and evidence; excludes dependencies/backups.

## Visual interpretation and limits
Ivory ceramic-inspired panels with cobalt/turquoise repeated floral decoration; deep blue lid with three raised eight-petal rosettes and satin brass hardware. This is an invented contemporary interpretation of Multan's kashikari palette, not an artisan-made object, traditional-pattern facsimile, shrine replica or representation of every Pakistani culture. Research citations and frozen contract are in `design-brief.md`; no research photographs are embedded.

Actual source and mobile screenshots were visually inspected: three flowers read clearly, body motifs and hardware are present, no gross broken or detached geometry visible. The pattern repeats mechanically and cuts at panel corners. Surface glaze is stylized, not photoreal ceramic. Feet are intentionally speckled and rough; small fittings/flower details soften on mobile. The source render has some sampling grain. Subtitle/disclaimer are small. Technical acceptance is not human art approval; per-asset human review was explicitly waived for this batch.

## Verified evidence
- Independently reopened saved source: 43 moving and 39 static meshes; **81 poses, zero unintended surface intersections**, latch-vs-lid also checked. Narrow named bearing exclusions only. Rear hinge mounting overlaps and hollow floor ray at z 0.265 verified. This is sampled, not continuous mechanical certification.
- Both original pivot matrices match the included mechanical baseline. 27 rosette objects are lid-parented; relief z 1.983–2.080. An intentionally detached petal is rejected by the actual theme validator (negative control).
- Independent source/export nearest-vertex maximum error **1.712013073529306e-7**, under 1e-5; all four packed maps retained.
- Actual browser GLTFLoader verifies finite geometry and no degenerate triangles. Decoded color and roughness map variation checked (roughness green channel), maximum map dimension 512.
- Offline file:// desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, drag/touch rotation, interrupted Reset, reduced motion, full-open framing, no overflow, no HTTP requests or JS errors. Corrupt bytes actually reach GLTFLoader and trigger poster fallback; JavaScript-disabled poster separately passes. Mobile emulation is not physical-phone performance evidence.
- Node motion tests exercise staged 80° latch and 105° lid motion and reject invalid geometry contracts.
- `delivery-check.json` verifies exact-byte SHA-256 inventory and ZIP readback. `.gitattributes` preserves original bytes across Git checkout.

## Actual failure and fix
`build-initial-output.txt` preserves the failed initial build: the promised shared compiler directory did not contain esbuild. Installed the existing exact package pins (Three 0.180.0, esbuild 0.25.11) locally within this new folder; build then passed. No sibling/shared directory was populated. No geometry failures were observed; the detached-petal negative is a deliberate regression control, not a claim of test-first development.

## Reproduce
Requirements: Blender 5.2.1, Python with Pillow/numpy/Playwright and installed Edge, Node and npm. `npm ci --prefix preview/pakistan-v1 --ignore-scripts --no-audit --no-fund` restores build-time dependencies. From this directory:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node --test --test-reporter=tap tests.mjs`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Regeneration overwrites source/export/poster: preserve manual edits separately. `setup.py` is a one-time scaffold provenance script requiring the sibling Japan pilot; it is NOT needed to reproduce the finished artifact. The other build/test scripts use this folder and installed toolchain only. Three MIT license included.

Local art asset and authorized branch backup only. No production website, blockchain, node, keys, minting, external messaging, VPS or shared kit changes. Storage remains an unimplemented off-chain content-addressing proposal, not a persistence guarantee. Next: full collection integration and collective visual review, not another per-asset approval gate.
