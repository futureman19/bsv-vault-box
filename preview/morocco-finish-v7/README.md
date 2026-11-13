# Morocco finish v7 — partial fidelity candidate, not approval

Open `morocco-finish-v7.html` offline. No mint, custody, deployment, gallery integration or merge. V5 remains the user-approved baseline; v5/v6 are read-only.

## Finish changes
- Same continuous v6 ceramic carriers: every v6 geometry index and UV array unchanged. Dark-first primary-patch classification and median-3 cleanup increase repeat near-black coverage **13.5982% → 42.9955%**, mean RGB luminance **119.1038 → 86.8739**. Pigments: [8,12,10], [12,64,39], [202,193,160]. These are texture measurements, not rendered equivalence scores.
- Six/four long/short-edge repeats, mirrored endpoints and inset-contour sampling: 404 analytic miter samples, maximum phase mismatch **1.7763568394002505e-15**. Phase continuity is not aesthetically resolved corner composition. Hidden regions are extrapolations from the illustration, not scans.
- Vertical wood mean RGB **[115.5930,68.5861,34.6241] → [90.5150,64.5186,45.4811]**; mean channel spread **80.9688 → 45.0339**; detail gain 1.8 → 1.1. Same 3px directional test **1.9637168799254763** (>1.5), within-row variation **7.0547724508769125** (>3). Top/interior untouched.
- Body retains exact v5 image payloads and UV registration, **0.90 linear-light** multiplier; non-dark sRGB ratios **0.9283646217581908–0.9541809689978538**, zero newly clipped channels. No body regeneration or added noise.
- Hardware, ridge, pivots, viewer, controls, camera, lighting and animation unchanged. JS/bundle/template/motion bytes match checked-out v6 exactly. Checked-out v5 text has different line endings (normalized content identical); v5 text byte identity is not claimed.

## Visual result — mixed, still a candidate
`reference-comparison.jpg` and `lid-comparison.jpg` show primary/v6/v7. The actual v6/v7 pair uses identical camera/lighting, proportional resizing only.

**Border value and less-orange vertical wood improve, but angular interlocking and corner composition are NOT convincingly resolved.** The macro border is no longer pale mint; instead the darker repeat can read as noisy olive/brown fragments rather than clean emerald/cream polygons. **At whole-box/mobile scale the border still reads pale/cream-heavy with weak green motif readability despite darker texture measurements.** Wood grain remains more conspicuous than the primary. Unchanged central wood is too light/golden; changing it is outside scope. Existing hardware/ridge differences remain. One bounded integrated finish pass, no additional art iteration; this is not reference equivalence or user approval.

## Executed verification
- HTML **4,017,780 bytes**, GLB **2,419,636 bytes**; HTML strictly below 5,000,000.
- Offline Edge file:// desktop **1440×900**, touch-emulated mobile **390×844**: native controls, drag/touch rotation, open/close, interrupted reset, reduced motion, zero external requests/unhandled errors/overflow.
- Actual corrupt-GLB parser input and no-JS decoded/visible poster fallback at both sizes. Mobile is desktop-GPU emulation, not physical-phone performance.
- Independent packed-source reopening: **81** motion/contact/attachment poses, **zero unexpected collisions**, original narrow bearing exceptions retained; hollow-floor z **0.26500001549720764**.
- Source/export maximum distance **1.712013073529306e-07** both directions. V5 nonceramic geometry, original images/body UVs and all parent transforms preserved. Separate v6 comparison proves all geometry/indices/UV exact.
- **193 tracked v5/v6 files** hash-readback checked unchanged. Old v6 ledger included absent machine-local pycache; current ledger uses tracked baseline files. Git scope separately verifies additive-only changes.
- Full actual outputs: source-check, parity-check, finish-check, delta-check, browser-check, extended-check, fallback-check JSON and corresponding output text. Delivery/inventory generated AFTER final HTML and evidence; staged Git blobs checked independently.

## Tooling caveats and retained failures
Initial adaptation moved template.html along with historical HTML; restored exact copied v6 bytes. Initial finish oracle compared v5 line endings and an old missing-pycache ledger; corrected to exact v6 runtime plus current immutable tracked baselines. Python 3.14 browser review exited 139; unchanged browser scripts passed under Python 3.12 via uv. Review labels initially called both models V7; fixed and regenerated. No viewer behavior or acceptance threshold relaxed.

`pre-correction/` is inherited historical v6 evidence, not v7 tests. `inherited-v6/` is local historical evidence excluded from delivery/Git. Shared node_modules was empty; no sibling toolchain was modified. build.py embeds the exact inherited compiled runtime instead of recompiling it.

## Rebuild and delivery
Python numpy/Pillow/Playwright; Blender 5.2.1 LTS. Run materials.py; Blender --background --factory-startup --threads 4 --python-exit-code 1 --python author.py; finalize_glb.py; build.py; verify_finish.py; verify_delta.py; verify_browser.py; verify_extended.py; verify_fallbacks.py; review.py. Run verify_source.py, verify_parity.py and verify_source_preservation.py through Blender. Finally package_delivery.py and verify_inventory.py; after Git staging use verify_inventory.py --staged. Do not rerun adapt_v7.py (one-time bootstrap).

History comparisons require sibling v5/v6, not runtime network resources. Regeneration overwrites v7 outputs and requires new inventory. Source ZIP includes packed v5 baseline, final packed blend/GLB, offline HTML, poster, maps/references, scripts and fresh evidence. Excludes caches/dependencies/backups/intermediate export. Inventory and ZIP are unhashed outer envelopes to avoid recursive self-hashes; every payload including delivery-check.json is inventoried. No source ZIP portability claim for optional sibling-history comparisons.
