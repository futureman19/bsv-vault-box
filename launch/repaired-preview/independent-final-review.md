# Independent bounded final delivery review

## Verdict

**APPROVED FOR PREVIEW DELIVERY ONLY. No blocking delivery defect found.**

This approves the delivered gallery bundle and poster-only review attachment as usable previews. It does not approve final artwork, resolve the retained substantive feature holds, authorize publication/deployment, or approve minting, sale or launch. No implementation, art, production or lifecycle changes were made.

## Independently executed integrity checks

Evidence: `independent-review/check.py`, `integrity.json`, `results.json` and screenshots. The check script completed successfully with real local Python Playwright / Microsoft Edge execution.

- Compared manifest roster IDs against the preserved original baseline as Counters: exactly 201 unique IDs, with 195 Country, five Ocean and one Moon records.
- Compared each selected viewer hash with its baseline viewer hash: exactly 17 changed, 184 retained. Selected versions include `united-states-flag-v10` and `bangladesh-finish-v2`; the complete changed-version mapping is recorded in `results.json`.
- The selection comprises USA V10, Bangladesh renderer/presentation v2, 13 structural repair successors (including Panama's additional camera change), and two camera-only trials (Cabo Verde and Saint Vincent and the Grenadines). Raw manifest classifications count USA among 13 `geometry` entries, plus one `geometry+camera`, one `presentation`, two `camera` and 184 `unchanged` entries; these are consistent, not competing totals.
- Independently fetched all 201 selected viewer blobs using `git show <commit>:<path>` and SHA-256 matched every blob against the selected manifest entry. This was a separate successful terminal check, not reliance on `selection-check.json`.
- Independently hashed all 603 manifest URL payloads (201 viewers, 201 marketing images, 201 model posters) and checked both sizes and hashes.
- Opened the actual hostable ZIP and read every entry. All 609 entries byte-match BOTH recovered copies and the source delivery subtree. All 608 inventory entries pass size/SHA-256 checks; `inventory.json` is the sole intentionally non-self-inventoried entry. No duplicate ZIP entries or traversal paths were found.
- Delivered standalone attachment byte-matches recovered `review.html`.
- Independently calculated ZIP SHA-256: `ffea9da367cb4bff25c7108e6256065ba4caba6177cfce6294276fa5ba7d456c`.
- Independently calculated attachment SHA-256: `38e8ca18ff1c1f871b9f4ebfcea5a522fca885b3a1deb0bea69bc53553a5e48e`.

## Actual delivered-file browser checks

Opened `delivery/recovered/index.html` and `delivery/boxsv-repaired-collection-review.html` via `file://`, in headless Microsoft Edge with networking offline. Desktop was 1440×1000; touch-emulated mobile was 390×844. Local-file iframe access was explicitly enabled with `--allow-file-access-from-files`.

All four delivered-file cases passed:

- 201 rendered cards and successful decoding of all 402 images per case.
- Country/Ocean/Moon filters; changed-viewer filter returns 17; substantive-hold filter returns 11.
- Moon alias search, USA/Bangladesh search, empty search result and reset.
- Native mobile tap and desktop click into detail; initial Close focus, repeated Tab/Shift+Tab navigation, blocked background-input focus, Close and Escape dismissal, restored card focus, keyboard Enter reopening.
- No document horizontal overflow, uncaught page errors or attempted HTTP(S) requests in these runs.
- From the recovered gallery itself, actual USA and Bangladesh iframes loaded and reached `pilot.ready`; native Open reached `progress===1`, native Reset reached `progress===0`, and hiding the model removed the iframe. Verified on desktop and mobile, not merely through standalone model pages.
- The review attachment correctly hides interactive/standalone-viewer actions; it is intentionally poster-only, not a broken interactive package.

The first independent test had one **harness false positive**, not an application fix: an over-strict Tab assertion rejected Edge's native modal focus cycle when `document.activeElement` temporarily becomes BODY. A focused probe confirmed the cycle returns to the dialog and its controls; an explicit attempt to focus the background search was blocked. Corrected the oracle to permit the browser-owned BODY boundary while still rejecting any background control. No product bytes changed.

## Visual inspection and focused follow-up

Inspected fresh recovered desktop/mobile gallery screenshots, fresh USA mobile detail, delivered standalone mobile attachment, recovered Bangladesh mobile open iframe, and the authoritative `browser-final/hosted-desktop-usa-detail.png`.

No blocking overlap, horizontal clipping, missing visible image or inaccessible Close/control was found. Actual-model and promotional imagery are explicitly distinguished. USA's main-wall hold and preview-only approval boundaries are plainly disclosed. Softer model thumbnails and the mobile Reset label wrapping are ordinary preview presentation limitations, not new blockers.

A screenshot showed the bottom of Bangladesh's iframe note outside the current viewport. A focused live probe found a 758px iframe viewport and 914px scrollable document; scrolling reached `scrollY=156`. This is reachable vertical content, not inaccessible clipping. Follow-up capture: `independent-review/bangladesh-scroll-check.png`.

## Substantive holds preserved

The manifest and hold filter preserve exactly these 11 IDs:

- Cabo Verde: partial mobile caldera readability.
- Iceland: glassy ice/material fidelity; clean dependency-pinned rebuild remains separately unestablished.
- Indonesia: named copper openwork legibility.
- Lithuania: pale versus requested black corners.
- Malta: linear versus branching bastion silhouette.
- Morocco: partial-v6 ceramic interlocking/corner fidelity.
- Mozambique: channel texture offsets and geological/water fidelity.
- Pacific Ocean: blue-patterned coverage versus broad pale field.
- Saint Vincent and the Grenadines: mobile crater readability.
- São Tomé and Príncipe: repetitive checks versus subdued pale-blue stone.
- United States: stars on skirt/rim do not satisfy requested main-wall continuation.

All 201 records retain false final-user-approval and launch-ready flags. Read `CURRENT-DISPOSITIONS.md` and `PUBLICATION-PLAN.md`: repaired mechanical/static-support issues and superseded package-envelope defects are not represented as new unresolved delivery blockers. Historical records remain historical; ordinary presentation acceptance does not waive the feature list.

## Scope and limitations

This is delivery QA, not a new all-201 geometry or art audit. No fresh Blender source reopening, collision sweep, source rebuild, full inner-source-package audit, rights/security review, physical-phone testing or production-host deployment was performed. Source GLB/editable files and source archives are pinned references rather than payloads inside this viewer/media ZIP; this review independently hashed the delivered URL payloads, not every external source artifact. Existing `browser-final/results.json` was read as prior evidence, not relabeled as independently rerun coverage. Native devices, other browser engines, file-origin behavior without the stated Edge flag, public hosting quotas and final publication readback remain outside this approval.

Only this report and own evidence under `independent-review/` were created. Parent owns Git push and lifecycle. No broad polish or new audit work is requested.
