# Final independent review — ordinary finish 20 / Bangladesh finish-v2

**Verdict: accept-for-candidate-delivery.**

**Art approval: false. Launch readiness: false.** This accepts the bounded correction and disposition evidence for candidate packaging and owner review, not final art, collection completion, mint/sale, custody, or production release. Source packaging, staged-byte verification, feature-branch push and remote readback remain subsequent work; none is claimed complete here.

## Scope and preservation

Reviewed workspace branch `feature/ordinary-finish-20` against parent `3952a4eb1c57ca921c21d0aa774ab8b8752e3df7`. The tracked diff against that parent is empty; the candidate additions are untracked pending delivery. All 437 nonignored untracked files at the scope check were under the two authorized directories, `preview/bangladesh-finish-v2/` and `launch/ordinary-finish-20/`. An empty tracked diff alone was not treated as proof of candidate correctness: the new files were inspected directly.

- All **96** entries in `review-freeze.json` match their SHA-256 values, including the source, generated viewer, historical files and candidate captures. Rechecked after the read-only browser rerun.
- All **61** historical-manifest files match their original Git blobs, declared sizes and hashes.
- Root Blender source, GLB, template, motion module, tests, posters and Three license match their historical counterparts byte for byte.
- The whole parent disposition ledger remains byte-identical to its committed parent, with **201** records and SHA-256 `92b18001a867fa643d801b7ca46724cb5e2bb29eb6ee78c3594e7ff4524941db`.
- No frozen captures, source reports, original assets or parent ledger were rewritten by this review. The only review-created repository file is this document.

## Independent visual inspection

Used vision on the eight original native screenshots, not just a board or written summaries:

- Before: `launch/ordinary-finish-20/captures/bangladesh/{desktop,mobile}-{closed,open}.png`.
- After: `preview/bangladesh-finish-v2/{desktop,mobile}-{closed,open}.png`.
- Also inspected `preview/bangladesh-finish-v2/comparison-mobile.png` directly.

The before views show pixel-scale stepping/softness on fine ivory motifs and narrow diagonal brass/pattern borders, especially at mobile size and on the oblique side. The candidate retains the same silhouette, teal/ivory/brass palette, delta relief, camera composition and fully framed closed/open states. The side-by-side mobile view supports a localized improvement in motif separation and thin-edge continuity, not a major finish transformation. Small oblique motifs remain limited; the stills do not establish freedom from motion shimmer.

The pronounced closed seam and segmented corner trim remain. Neither those design choices nor the simplified delta are newly repaired or newly approved. Open views retain the visible cavity and paired rear hinges without obvious new gross displacement or clipping. Still-image inspection is not new collision/attachment proof. The baseline mobile-open button has a different interaction highlight from the candidate capture; the exact source comparison below establishes unchanged CSS/UI behavior, so this is not evidence of a UI restyle.

For the other nineteen IDs, this final review audits the preserved individual reviewer findings and adjudications; it does **not** claim a new independent visual inspection of all their screenshots. Their prior reviewer-a/b findings cover the exact twenty-ID roster and are retained separately from owner approval.

## Code, build and runtime evidence

`viewer.js` has exactly one runtime expression substitution: `renderer.setPixelRatio(Math.min(devicePixelRatio,2))` becomes `renderer.setPixelRatio(2)`. Independently replayed `build.py`'s deterministic replacement in memory against the historical source, compiled bundle and standalone HTML; all three outputs match the delivered candidate bytes exactly. No compilation, geometry regeneration or output overwrite was needed.

The standalone HTML measures **3,409,390 bytes**, below the strict 5,000,000-byte cap. Its SHA-256 is `26a3beaf1d2da147274c118d29cea0c34dd5856cf8c63a94f439e82bcf6cf325`. Exact model identity and exact single-expression HTML/bundle substitution support preservation of materials, UVs, texture filtering, lights, camera, motion, CSS and embedded payloads.

Fresh independent executions:

- `node --test --test-reporter=tap preview/bangladesh-finish-v2/tests.mjs`: **2 passed, 0 failed**. These are the original pose/asset-contract unit assertions, not new mesh collision sampling.
- Re-executed the candidate Playwright/Edge browser harness in memory with only screenshot and report writes removed. **Desktop DPR1; mobile DPR1, DPR2 and DPR3; corrupt-GLB; and no-JS cases all passed.** Drawing ratio was 2 in each rendering case; controls, drag/touch, interrupted reset, reduced-motion endpoints, no overflow, full-open projection, and no external requests/page errors passed. Maximum projected extent was approximately 0.8924, within the viewport.
- Frame-interval medians on this host were approximately 17.85, 17.75, 17.60 and 17.65 ms respectively. These are not physical-phone GPU, battery or thermal benchmarks. The reduced-motion harness checks endpoint completion, not a frame-by-frame proof of instantaneous snapping.
- Reran original source archive verification read-only, suppressing report writes: **20 archives / 1,099 members**, exact hash/size, safe unique paths, CRC, supported inner inventories and selected HTML/GLB/Blender payload checks passed. The regenerated in-memory result equals `source-package-check.json` exactly.
- Checked all twenty selected baseline viewer hashes and parsed the saved **40 desktop/mobile results plus 40 fallback results**; their recorded gates pass. This is an audit of the saved all-ID browser rerun, not a second fresh all-ID browser execution by this reviewer.

The retained Blender parity report records maximum bidirectional error `1.712013073529306e-07`, below `1e-5`. I inspected it and independently verified unchanged source/export bytes; I did not launch Blender again. No fresh collision sampling is inferred. The original no-JS selector failure remains preserved, and the corrected harness uses the existing `#fallback` image without changing fallback code.

## Twenty-ID disposition audit

Programmatically verified twenty unique, matching IDs across baseline, dispositions and prior independent findings:

`argentina`, `bangladesh`, `cambodia`, `comoros`, `djibouti`, `eritrea`, `gambia`, `guinea-bissau`, `lebanon`, `malawi`, `mexico`, `myanmar`, `nigeria`, `palestine`, `qatar`, `samoa`, `southern-ocean`, `tajikistan`, `tunisia`, `zambia`.

There are **19 unchanged-with-explicit-limitations** and **1 presentation-correction-candidate** entries. Every entry has final approval and launch readiness false, and no geometry change. All twenty complete `original_review` objects in `baseline.json` equal the corresponding parent records. Per-ID unresolved and inherited hold arrays remain exact. The report distinguishes optional sampling investigations and subjective promotional differences from demonstrated defects rather than converting those differences into unauthorized redesigns.

## Remaining conditions / nonblocking limitations

- At DPR1, ratio 2 has **4× the drawing-buffer pixel area** of ratio 1. This is not a measured 4× GPU-time cost. Physical-device suitability remains unverified and must not be implied by candidate acceptance. At DPR ≥2 the effective ratio is unchanged.
- No final aesthetic, rights, preservation/storage, authentic issuer/origin/key, wallet/payment/chain, security, economics/legal, mint/sale or release hold is cleared. Preserve 201 equal-supply one-of-ones, one inner NFT plus detached signed record; no accessory/certificate NFT or reuse-support claim.
- The preview README's future-facing reference to a new root inventory must be fulfilled during packaging; this review does not certify a not-yet-produced successor ZIP/inventory. Verify the required files, archive readback and exact staged/committed bytes before reporting delivery complete, then verify the exact remote branch SHA after the authorized push.
- No actionable correction blocker found within this candidate-only boundary. Do not turn acceptance into final art approval or another blanket polish pass.

## Reviewed report identities

SHA-256 values at review time (this review is not itself part of the existing freeze):

| File under `launch/ordinary-finish-20/` | SHA-256 |
|---|---|
| `baseline.json` | `9cebc86f11cf3624769acfc42c7b1e27219edb9cd3cff5d1b44e2b24467fc222` |
| `dispositions.json` | `fb8c3ce43614876b756a18b9a5cf90f016595bc950c8ed546b0babee32966423` |
| `README.md` | `e790b76dd3a733af97f72987eb345f1487b847c39149c12fbf7d6af1923a4fdc` |
| `source-package-check.json` | `edda014bcf824d233ba746778bc83706277d1c88c3921970fe00062d8b5c339b` |
| `runtime-summary.json` | `731184a89a4beedb61b9eda6e54881bf236da070ed5837737552d47ab21d328e` |
| `review-freeze.json` | `444cf5f3e68a17d346fd5f7037caee10ff640101f395db6f9cebb1754da0470d` |
