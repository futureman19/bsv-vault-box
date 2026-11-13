# Austria v1 — Adnet & Alpine Crown

Open **austria-v1.html** directly in Edge/Chrome. All runtime code, GLB, maps and actual-model poster are embedded. Drag/touch rotate, Open/Close lid, Reset, and reduced-motion support are included. No server or network required.

- HTML: **3,009,593 bytes**, strictly below 5,000,000.
- GLB: **1,643,776 bytes**.
- Editable source: `austria.blend`; frozen inherited articulation: `mechanism.blend`.
- Source render: `poster.png` and its JPEG derivative. Browser captures: desktop/mobile closed/open plus corrupt-input and no-JS fallback. No AI promotional substitute.

## Design and honest visual verdict
The sourced brief was written before authoring. Austria is represented by red Adnet decorative limestone and an invented snow-capped Alpine crown, not by a surveyed model of Grossglockner. Adnet is commercially named marble but geologically limestone. No third-party photographs were copied into maps.

The final model is deliberately stylized: wine/pink-red stone with large angular pale calcite networks, three unequal snowy summits, cool exposed rock, green foothills, satin brass family fittings and a hollow interior. Stone veins remain graphic and oversized rather than a geological scan. The terrain is a low-poly miniature, not photorealism. The render is slightly grainy (24 samples, denoising disabled); the interior stone pattern can obscure floor/wall boundaries. Hardware is a family extrapolation, not historical Austrian chest reconstruction. No user-specific visual approval is claimed; this card explicitly waives per-asset human review.

One bounded visual correction replaced stretched side UVs with dominant-plane stone UVs, reduced the rounded cellular distortion into more angular clasts, and rounded the rectangular terrain footprint. `initial/poster-before-polish.png` preserves the earlier source render. Final desktop/mobile screenshots were inspected: all three peaks readable when closed, no clipped silhouette or obvious floating parts, legible controls. At full opening the lid naturally hides the crown from the front; source and runtime ancestry tests establish its continued presence.

## Verification actually run
- Independent reopening of saved Blender source: **81 sampled poses**, **17 moving / 39 static meshes**, zero unintended BVH surface intersections. All crown surfaces included. Latch-vs-lid checks included. Only explicitly named concentric bearing contacts excluded. Ten hinge attachment overlaps and hollow-floor downward ray at z **0.2650000155** pass. Sampled surface tests are not continuous analytical collision proof, containment proof, or mechanical certification.
- Independent source/GLB nearest-world-vertex parity: maximum error **1.712013073529306e-7**, below 1e-5; three packed map images. Source pivot matrices equal frozen mechanism with **0.0** maximum error.
- Crown bounds z **1.9700000286–2.9201612473**; three independent summit rays hit crown geometry; snow/rock/foothill polygon counts pass. Red map median **[152,61,59]**, ivory fraction **0.0782241821**. Actual decoded runtime map ranges: base color **109**, roughness green channel **44**, foot map **99**.
- Actual Three GLTFLoader: **16,870 triangles**, **58 rendered mesh primitives**, **7 materials**, zero nonfinite vertices or degenerate triangles. Multi-material crown becomes multiple primitives; source object count is not runtime primitive count.
- Actual offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, mouse/touch rotation, interrupted Reset, reduced motion, no horizontal overflow, no external HTTP requests and no JS errors. Full-open projection maximum absolute NDC **0.9101578753**. NVIDIA RTX 4060 desktop renderer; no physical-phone, FPS or long-duration performance claim.
- Actual corrupt GLB bytes sent into GLTFLoader produce caught parser error, poster and disabled controls. JavaScript-disabled context shows decoded poster.
- Motion tests: **2 passed / 0 failed**, including rejection of missing articulation, nonfinite bounds and empty geometry. The detached-crown negative control genuinely exits 1 with `AssertionError: Crown must travel with the lid`; it mutates an in-memory test copy only. This is post-implementation negative-control evidence, not an invented test-first history. No unintended acceptance-test failure occurred.
- `acceptance-check.json` consolidates assertions. `inventory.json` contains exact byte counts/SHA-256; `delivery-check.json` verifies complete ZIP membership/readback. Folder-local `* -text` prevents Git newline rewriting; indexed/committed inventory verification performed before delivery.

## Reproduce
Blender 5.2.1; Python with numpy, Pillow, Playwright; installed Edge; Node with Three 0.180.0 and esbuild 0.25.11. The mandated shared pilot node_modules directory existed without its compiler, so unchanged pinned dependencies were installed **inside this new folder only**. No sibling dependency tree was populated. Build dependencies are excluded from the archive and are not runtime dependencies.

1. `npm ci --ignore-scripts --no-audit --no-fund` inside this directory.
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `verify_theme.py -- --negative` must fail with the recorded ancestry assertion.
6. `node --test --test-reporter=tap tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
7. `python package_delivery.py`.

Authoring overwrites generated assets; preserve manual edits separately. The standalone folder includes its frozen mechanical source, so generation does not need sibling previews. Mechanism/viewer/test lineage: repository Japan Cedar pilot at base ff5d78f, originally Iceland staging. Three.js MIT notice included. `adnet-edge.png` is a generated but currently unused map, retained as source output.

## Scope
Additive `preview/austria-v1/` only. No shared kit, production site, wallet, keys, blockchain node, chain query, mint, transaction, VPS, deployment or public messaging. Branch backup only on `art/austria-v1`, not merged. This is one inner collectible in the 201 one-of-one collection, not the outer custody container. Lid motion is cosmetic. SHA-256 proves bytes, not authenticity, availability or on-chain storage. Next: final collection integration/review under its separate dependent card.
