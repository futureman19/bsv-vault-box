# Authored vault asset acceptance — local static site

Built on `5b438c89ef4ccfb1557ed7635a32f488d7124baa`, retaining the earlier material/UI polish. **Not deployed or pushed.** `docs/` is the actual static deliverable; no bundler differs from this tested artifact.

## Review first

- `desktop-model.png`: actual authored game canvas, not a Blender beauty render.
- `desktop-carry.png`, `mobile-reduced-carry.png`: actual selected vault attached during carry.
- `desktop-rejected-idle.png`, `fallback-cabinet-idle.png`: real GLB-request rejection returns to original primitive art.
- `gameplay-desktop.webm`: 1440×1000, 11.28-second actual keyboard/drop/grab/carry/reveal/reset capture; 25fps recording, **not a 60fps benchmark**. Chrome played it to end without decoder error (286 reported frames, 3 dropped; see `video-report.json`).

Screenshots were visually inspected: reinforced cabinet, engineered claw joints/hooks and lock-front vaults show tangible geometry changes; no obvious gross detached pieces or cropped cabinet. The static grab contact is crowded and partly occluded. Carry reads as attached/elevated but the pile overlaps in projection. This remains the original nonphysical arcade motion, not a realistic gripping simulation. Mobile fine lock/pivot detail is less legible than desktop.

## Verified

- `source-report.json`: Blender 5.2.1 independently reopened the saved editable `.blend`; evaluated every part, checked nondegenerate triangles, bounds and Y-up anchor contract.
- `browser-report.json`: actual pinned GLTFLoader parsed all four assets over HTTP 200, measured triangles/bounds, checked finite vertices and nonzero triangle areas, compared source/export triangle counts and bounds within 0.00001 units, and matched HTTP SHA256 to disk.
- Seven headed-browser scenarios: authored desktop, authored mobile/reduced motion, desktop rejected vault request, and each of four GLBs independently rejected on mobile. Keyboard or native CDP touch moved the claw; each scenario completed drop/grab/carry/reveal/reset; all three finger groups and six prize groups retained their anchors/animation responsibilities. All page-error arrays empty.
- 30 Node tests passed; 50 Python differential cases passed (`node-tests.log`, `parity.log`, archived in `logs.zip`). Game/DOM/control/draw files match parent Git blobs (`unchanged-contracts.json`; normalized by Git's existing Windows line-ending rules).
- Existing gates passed: `existing-visual/visual-report.json` (desktop/mobile/320px/tablet, keyboard cancel, checker navigation, ordinary versus reduced motion, CSS fallback); `existing-claw3d/report.json` (hardware WebGL, resize, dispose/remount/context loss); `existing-interactive/report.json` (real 30-second timeout, duplicate-drop protection, bounds, joystick, reveal/reset, reduced-motion mock-wallet call contract and WebGL-disabled gameplay).
- Asset-specific loader budget is separately reported: 684,372 GLB bytes; 853,053 optional bytes including loader/addons/adapter. Original core payload guard remains ≤5% over its historical reference (measured 2.25%); optional kit is capped at 1,000,000 bytes. This is an explicit new asset budget, not a claim that the entire new experience stays within the old 5% envelope.

## Honest limits / retained failures

- RTX4060/D3D11 measured 55.78fps, p95 18.2ms in the existing 180-frame interactive probe. **Strict 60fps is not met.** Mobile is a desktop-browser viewport/touch emulation, not physical-phone certification. Authored idle renderer reports 151 calls/46,562 triangles including render passes, versus fallback 233 calls/14,882 triangles: fewer calls, more triangles, no claimed speedup.
- Initial grab assertion sampled the exact phase boundary where close=0. The harness now waits for actual closure >.2. Original failure retained in `logs.zip`.
- Two strict reduced-motion PNG-equality probes failed on primitive fallback. Diagnostic PNGs and `static-difference.json` show **one pixel differing by one 8-bit channel step**, with unchanged transforms. The authored mobile case remains byte-identical. The new acceptance explicitly allows at most that one-pixel/one-LSB raster variance, still requiring identical pose snapshots; larger differences fail. Final report records which cases used it. Original failure/diagnostic logs and partial report are retained, not discarded.
- Existing checker navigation requests a missing `/favicon.ico` (404), recorded in the old visual gate's console array. Game landing and asset loads have no such errors; checker code was untouched.
- Playwright's bundled FFmpeg lacks the null output muxer, so that probe failed; the actual WebM was instead verified by full Chrome playback. Failed FFmpeg output retained in `logs.zip`.
- Original primitives remain allocated for fallback until disposal. Rigid finger compression is unchanged; no new IK, collision physics, wallet authentication, payment, mint, chain write or odds behavior is claimed.

## Re-run

From repository root:

```sh
python test/vault-assets-browser.py
python test/vault-video-browser.py
BOXSV_EVIDENCE_DIR=evidence/vault-assets/existing-visual python test/arcade-visual-browser.py
BOXSV_EVIDENCE_DIR=evidence/vault-assets/existing-interactive python test/claw-interactive-browser.py
# For the old renderer gate, serve docs/ at localhost:4179 first:
BOXSV_EVIDENCE_DIR=evidence/vault-assets/existing-claw3d python test/claw3d-browser.py
```

Source/rebuild instructions and asset inventory: `art/vault-kit/README.md`. Raw terminal logs are byte-preserved in `logs.zip`; duplicate temporary recorder files and Blender backup files are not shipped.
