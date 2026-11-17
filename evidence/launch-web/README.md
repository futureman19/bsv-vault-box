# WEB launch-preparation handoff

Scope: local integration and verification only. No production publication, art replacement, mint, purchase, real funds, key handling or chain broadcasts.

## Candidate and integration

- Branch: `feature/launch-web-polish`.
- Production baseline fetched: `606147d6a1521adf635d79a70785ba7f82dbbf77`.
- Claw parent integrated by fast-forward: `080f1ec2643451cc04741077c60aba15dd2ca140`; no conflict or manual resolution required. No claw source edits beyond that reviewed parent.
- Ledger parent reference: `6db6388d04fee0da8e0324a640d5880a5813a39c`, `launch/launch-01/launch-candidates.json` (not imported into this WEB branch). This card preserves the production gallery artwork; it does not promote model/art candidates from the ledger.

## Changed

- `docs/gallery.js`, `gallery.html`, `gallery.css`: shareable query/category state with image hashes, restore on reload, accessible loading/failure statuses, manifest retry, named thumbnail fallback and full-image recovery without removing promotional provenance. Retains lazy thumbnails and on-demand full images.
- `docs/index.html`: narrows historical VAULT-0001 claims; marks reuse as simulated, removes unsupported arbitrary-package/secrecy/atomic-resale implications, distinguishes inner collectible/outer container and signed record; clearly separates fictional claw and Box. Social descriptions agree. No checkout activation.
- `docs/box-demo.html`, `box-inspector.js`: revealed guidance names the actual current fictional item and explicitly says it remains inside until withdrawal.
- `test/web-launch-browser.py`: reproducible bounded local browser regression with explicit overall result/failure.

## Executed acceptance

1. `python scripts/test-gallery.py --review C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-collection-review --output evidence/launch-web/gallery`: PASS. Exact 201-design roster, 195 countries/5 oceans/Moon; 402 hashes/dimensions and 402 real-browser image decodes. Category/search aliases, empty/reset, keyboard dialog/focus/backdrop, 320/390/768/1024/1440 widths, six ordered showcase deep links. `gallery/results.json`, `gallery.txt`.
2. `python test/web-launch-browser.py`: PASS, 10 grouped checks. Query reload and selection, full-image/thumbnail/manifest failure recovery, initial mobile 10 thumbnails with no full art/models, two reuse cycles with transfer and interrupted reset on BOTH standalone/embedded surfaces in normal/reduced motion, persistent opened lid and correct history, narrow widths. Final authoritative `interaction/report.json` and `interactions-final-verified.txt`; process exit 0.
3. `BOXSV_EVIDENCE_DIR=evidence/launch-web/claw python test/claw-launch-browser.py`: 13/13 PASS on integrated candidate in headed Chrome. Authored-kit readiness, key isolation, return/replay, stale callback fencing, native CDP touch, viewport rotation, reduced motion/context loss, delayed/failed/late assets/modules and genuine no-WebGL fallback. `claw/report.json`; no uncaught page errors.
4. `node --test test/claw-interactive.test.js`: 4/4 PASS (`unit.txt`). `node --check docs/gallery.js`, `node --check docs/box-inspector.js`, `git diff --check`: PASS.

Gallery server log includes connection-aborted exceptions when navigating away from pending lazy requests; browser report has no HTTP/page errors and all 402 images separately decoded. Initial custom-test failures are retained: reused decoded image bypassed injected abort, standalone DOM incorrectly selected as a custom element, collapsed history read using visible text. These were harness assumptions; corrected before the authoritative complete rerun.

## Independent review

Read-only reviewer `deleg_caf107dd` approved scoped downstream WEB integration after reading all six changed source files, both test harnesses and three reports, inspecting seven actual desktop/mobile screenshots, and independently checking 201 IDs/402 image hashes and unchanged assets. Reviewer did not rerun browser suites. Its nonblocking recommendation for an explicit test-report overall result was implemented and the full custom suite rerun. No art approval or independent security certification is claimed.

## Preserved and held

- China, Canada, United States, Egypt, Moon, Iceland showcase unchanged; gallery assets and manifest unchanged from production baseline.
- USA v9 remains unapproved; full star/body continuation unresolved upstream. No art generation or candidate swap.
- Local Edge/Chrome and emulated mobile are not physical-phone/Safari or deployed-site evidence. Claw measured about 56.56 fps in this run, not a 60 fps guarantee. Existing nearest-wrap no-miss demo remains.
- Small embedded poster captions on Moon/Iceland remain hard to read at thumbnail size; enlargement is available. Box's static introductory seal-tap instruction persists after opening; state-specific status/withdrawal guidance remains correct. These are nonblocking visual limitations, not redesigned art.
- Repacking still alternates fixed fictional examples; no arbitrary NFT admission or chain-supported reuse claim. No live unspent-state validation performed.
- Production release, storage/funding choices, sale/allocation rules, independent custody review and physical-device acceptance remain held.

Next: downstream `t_35cdff45` should integrate this exact feature commit for its bounded launch rehearsal, not publish it. Git commit/remote SHA is supplied on the task lifecycle handoff. `sha256.json` identifies the saved evidence bytes, not recorder authenticity.
