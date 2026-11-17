# Afghanistan v1 — Lapis & Hindu Kush

Open **afghanistan-v1.html** directly in Edge/Chrome: **3,127,732 bytes** including model, runtime, maps and actual-source poster. Standalone GLB: **1,758,768 bytes**. No runtime network dependency. Cosmetic inner-collectible movement only; not minted, hosted, signed or on-chain.

## Design and visual result
Research-backed pre-model `design-brief.md` references GIA and IUGS on Sar-e-Sang lapis in northeastern Afghanistan. Deep blue mineral body, cream calcite-inspired veining and sparse gold flecks, satin brass fittings, dark-blue seam, and an invented three-peak pale mountain relief. Original procedural maps and script-authored Blender meshes; no scans, copied research imagery, sacred motifs or claim of traditional artisan manufacture.

Actual source poster and final desktop/mobile closed/open screenshots were visually inspected. The mobile view shows three peaks, blue body and distinct controls without clipping. This is a stylized collectible, not photorealistic lapis or surveyed Hindu Kush terrain. Long cream veins can read as blue marble; pyrite flecks are subtle. The mountain's seated rectangular footprint reads as a miniature terrain panel, not naturally continuous bedrock. Pale feet are stylized, source poster has modest render grain, and small secondary UI text is less readable than headings/buttons. Open front view hides the ornament behind the lid naturally; hierarchy and motion checks establish it travels with the lid. Hardware is inherited family extrapolation, not manufacturing certification.

## Actual verification
- `source-check.json`: independently reopened saved source, hollow interior ray at z=0.2650000155; 81 sampled poses, every 17 moving and 39 static meshes, zero unintended surface intersections. Named concentric hinge and latch bearing pairs alone exempted. Ten hinge mounting attachment pairs checked separately. Sampled surface tests are not continuous collision proof or solid-volume engineering analysis.
- `parity-check.json`: source/export bidirectional maximum vertex error 1.712013073529306e-7 (<1e-5), four packed images.
- `theme-check.json`: exact inherited world pivot positions, terrain owned by lid, three separated peak neighborhoods, height 0.688875124 above lid and seated underside. Deliberate detached-parent negative control was rejected.
- `browser-check.json`: actual Three GLTFLoader: 56 meshes, 16,586 triangles, four materials, zero nonfinite vertices and degenerate triangles. Desktop 1440x1080 and 390x844 touch emulation, offline file://, native open/close, mouse/touch drag, interrupted reset, reduced motion, full-open projection <1, zero external HTTP requests, runtime errors or horizontal overflow. Actual corrupted GLB triggers caught parser failure and visible poster; no-JS poster also checked.
- `extended-check.json`: decoded actual base-color, roughness GREEN channel and normal maps vary, maximum 512 pixels; terrain ancestry, visible country copy and accessible canvas label; nonblack source poster pixels.
- `motion-output.txt`: two passing tests covering latch-first 80-degree release, then 105-degree lid opening, clamping and malformed-asset rejection.
- `delivery-check.json` and `inventory.json`: exact bytes/SHA-256 and ZIP readback, explicitly required HTML, GLB, blend, maps, source/evidence. Packaging envelopes exclude themselves to avoid circular hashes. Folder-local `.gitattributes` preserves bytes; staged Git blobs independently compared to inventory before commit.

Browser used Edge on RTX 4060. Touch emulation is not physical-phone performance or accessibility certification. Visual limitations remain separate from passing technical gates.

## Real failure and correction
`initial/theme-height-failure.txt` preserves the actual failed <=0.70 terrain-height assertion; the first relief reached about 0.7085 above lid. Reduced central Gaussian amplitude from .66 to .64, without changing the gate; regenerated source, GLB, poster and reran all source/theme/parity/browser checks. The previous source poster is preserved under `initial/`. No gate was waived.

Optional Codex implementation attempt failed immediately with HTTP 401 and produced no code. Hermes authored and verified the asset directly; no credential store was read or changed. Shared pilot node_modules had no esbuild compiler; identical pinned dependencies were installed locally in this new folder only. No sibling preview or shared kit changed.

## Files and reproduction
`afghanistan.blend` is the editable packed source; `mechanism.blend` is the copied trimmed Japan articulation baseline. `afghanistan.glb` is the exported runtime model. `poster.png/jpg` are actual Blender renders, not AI promotional images. The source ZIP includes standalone runtime, source, maps, scripts, license and checks; excludes node_modules, backups and lane diagnostics. Three.js 0.180.0 MIT license is included; esbuild 0.25.11 is build-only.

Requirements: Blender 5.2.1, Python with Pillow/numpy/playwright, Node and installed Edge. From this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python build.py`; `node --test --test-reporter=tap tests.mjs > motion-output.txt`
6. `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`

`build.py` names this host's native Node executable; adjust that path on another OS. `setup.py` is an adaptation-history helper depending on the sibling Japan source; normal regeneration uses the already included scripts and mechanism, not setup.py. Regeneration overwrites source/render outputs; preserve manual variants separately and regenerate inventory afterward. Delivery remains in-folder; there is no separate hosted or copied product. Branch backup only, no merge, blockchain activity or deployment. Final collection integration is a separate dependent task.
