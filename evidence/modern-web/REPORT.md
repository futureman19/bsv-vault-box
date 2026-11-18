# BoxSV modern platform update — feature publication candidate

## Source and scope
- Base: origin/master `606147d6a1521adf635d79a70785ba7f82dbbf77` (six-item showcase).
- Reviewed site source: `feature/public-claims-overlay-finish@55b0a48c5c53abb37b8897f35958c39029866376`.
- Imported only that source's `docs/` changes and three site regression tests; did NOT merge its backend, mint, custody, collection-production or evidence history. Compared the resulting docs against the source: only gallery.js, gallery.html, gallery.css and claw.js differ for modernization.
- Gallery assets/manifest are byte-identical to origin/master. No wallet API, sale activation, funds, keys or protocol changes. No production publication.

## Implemented
1. Gallery uses `closedby="any"` with a feature-detected pointer-safe light-dismiss fallback. Clicking dialog padding or dragging from inside to outside does not dismiss. The fallback closes on the completed click, after touch compatibility events, preserving native focus return.
2. Native modal owns focus containment/restoration; URL-opened cards are focused before showModal so Escape returns to a meaningful invoker. Close uses a native `form method="dialog"` rather than a click listener.
3. Gallery modal/backdrop contain scroll gestures without body overflow locking; root scrollbar and grid position stay stable. Scroll containment remains progressive enhancement where the browser does not implement it (notably Safari per the retrieved guide).
4. Claw loot reset uses `replaceChildren()` rather than parsing an empty HTML string.
5. Preserved reviewed opaque prize modal, pending-action isolation, reveal cancellation, cross-section focus, honest public custody claims, gallery recovery behavior, all 201 designs and the six showcase links.

## Guidance provenance
Read the supplied qwen-profile SKILL.md read-only. Executed `npx.cmd -y modern-web-guidance@latest legacy-scan docs --json` before editing: two verified findings (`dialog`, `js`). Retrieved both complete guides; saved retrieval in `guides.md`. Final scan: zero deterministic findings across 38 guides / 52 rules, approximately 20% of corpus. This is not a claim of full-site compliance.

### Modern Web Guidance
- **`dialog`**: I adopted declarative light dismiss, native focus and native close form while keeping a feature-detected fallback. The guide says “Require the press and the release outside, so a text-selection drag that ends on the backdrop does not dismiss”; touch testing additionally required deferring fallback closure to click. I replaced gallery body locking with modal/backdrop containment: “Do not fall back to `overflow: hidden` or `position: fixed` on `html` or `body`”.
- **`js`**: I clear claw loot with `replaceChildren()` to avoid unnecessary parsing and compatibility with Trusted Types sinks: “call `container.replaceChildren()` with no arguments to remove all `childNodes` instead of `container.innerHTML = ''`”. This does not claim site-wide Trusted Types support.

## Verification
- `node --test test/claw-interactive.test.js`: 4/4 pass.
- `python scripts/test-gallery.py --review C:/Users/futur/Desktop/bsv-vault-box-featured-six/docs/assets/gallery --output evidence/modern-web/gallery-verified`: PASS. Independent production-source roster; 201 unique designs (195 countries, 5 oceans, Moon); all 402 images hashed, dimension-checked and browser-decoded. All category/search/deep links and six ordered showcase images pass; no overflow at 320/390/768/1024/1440; no page errors.
- `python test/modern-web-browser.py`: four combinations PASS (desktop/mobile, native/forced fallback), Edge 157.0.4341.60. Native modal, inert background, Tab/Shift+Tab, Escape, form close, click/touch dismiss, padding/drag safety, restored focus, unchanged page width/grid x. Backdrop wheel scroll delta zero in every combination.
- `BOXSV_EVIDENCE_DIR=evidence/modern-web/claw-final python test/claw-launch-browser.py`: all checks PASS in headed Chrome. Authored 11-part kit, keyboard isolation, duplicate drop, real 30-second timeout, pending-reveal cancellation, opaque prize focus isolation, Try Box/return/replay; native CDP touch, portrait/landscape, reduced motion, WebGL loss, delayed/failed modules/GLBs, late timeout latching and genuine no-WebGL fallback. No uncaught errors.
- `BOXSV_EVIDENCE_DIR=evidence/modern-web/web-final python test/web-launch-browser.py`: 10 checks PASS: gallery reload/retry/full-image and thumbnail failure; mobile initial load only 10 lazy thumbnails (no full art or GLB); standalone/embedded Box with normal/reduced motion, transfer, two reuse cycles, history, persistent lid, interrupted reset and responsive layout.
- Final legacy-scan zero; `git diff --check` clean. Screenshots inspected through vision: desktop/mobile prize overlays, desktop gallery, mobile forced fallback, six-item mobile showcase and actual mobile homepage viewport. No clipping/overlap observed; preserved charcoal/gold identity. Small disclosure text remains an existing limitation.

## Corrections and limits
One implementation correction: pointerup-based fallback lost focus on mobile compatibility mouse events; click-based completion fixed it and all four cases pass. Two existing harness assertions assumed hash cleanup happened synchronously after native focus return; changed them to wait for the actual close-event effect. First parallel claw run missed the authored-ready deadline under concurrent browser load; all other checks passed, and the complete serial rerun passed without changing production readiness behavior. Retained initial failure logs.

Forced fallback in Edge is not actual Safari certification. No physical-device, Firefox or Safari run. Scroll containment intentionally degrades in older engines as prescribed by the guide. Existing prize modal focus/scroll implementation was preserved from the reviewed source rather than broadened into another refactor. No performance improvement percentage or full accessibility certification is claimed. Parent owns scoped publication and live verification.

## Evidence
Reports: `gallery-verified/results.json`, `platform/results.json`, `claw-final/report.json`, `web-final/report.json`; execution logs adjacent to this report. Representative screenshots are committed from those directories. Earlier local captures may remain untracked and are not the publication payload.
