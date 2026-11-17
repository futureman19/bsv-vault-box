# LAUNCH-03 — claw reliability handoff

Base: `606147d` (origin/master at start). Candidate branch: `feature/launch-03-claw-reliability`. No production deployment, wallet connection, funds, mint, or art changes.

## Changes
- Claw keyboard shortcuts only own the machine/aim controls. Navigation, Box controls and other page controls keep their Space/Enter/arrows; focus departure clears held inputs.
- Returning from a completed round via Try Box restores Play and disarms the old round. Previously returning to the claw left no visible Play button.
- Reveal continuations are fenced by round generation; interrupted replay cannot reopen an old prize card.
- Reveal timing follows changes to the OS reduced-motion preference (existing waits are not rescheduled). Mechanics continue to sample preference on arm.

## Executed evidence
- `BOXSV_EVIDENCE_DIR=evidence/launch-03/verified python test/claw-launch-browser.py`: **13/13 checks pass**, no uncaught page errors. Headed local Chrome; real authored GLBs; loopback server; desktop and mobile viewport/CDP-touch emulation.
- `node --test test/claw-interactive.test.js`: **4/4 pass**; `unit.txt` retains output.
- `node --check docs/claw.js`, `git diff --check`: pass (Git reports normal LF/CRLF warnings).
- `red/report.json`: both navigation Space stealing the drop and the Try Box return dead-end reproduced before changes.
- `acceptance/report.json`: initial full-matrix attempt retained, including **four harness-assumption failures**. Existing reduced-motion-at-load behavior intentionally selects CSS, so those tests could not assume authored GLBs. Corrected tests load normal motion first and change preference afterward.
- `final/report.json`: corrected matrix 13/13. Independent reviewer inspected diff, tests, report and actual mobile/carry screenshots; approved for downstream integration, not release. Reviewer identified no-WebGL test conflation with initial reduced motion and incomplete global error check. Both harness gaps were corrected; `verified/report.json` is the final independently isolated WebGL-unavailable run plus whole-matrix error gate.
- `verified/*.png`: actual captures, including authored grab/carry/reveal, mobile controls/orientation, delayed loading, late timeout arrivals, module/GLB failures and no-WebGL fallback. Full-page screenshots include unrelated lazy gallery images which were not scrolled into view; blank lower-page slots are not established image failures.
- `logs/*.txt`: raw browser runner HTTP/check output, including initial RED and harness correction attempts.

## Acceptance boundaries and remaining limitations
- The existing demo **always retrieves the nearest wrapping** even from off-target positions. No miss/lose state exists; off-target unit regression explicitly verifies that behavior. No payout, odds, random mint or real prize integration was added.
- Real thirty-second deadline, duplicate drops, replay during pending reveal, Box keyboard isolation, return/replay, native CDP touch, viewport rotation, reduced motion, authored loading, GLB/module failures, 12-second timeout with late delivery, and context loss were exercised.
- Final desktop sample: 120 frames, median 17.6 ms, p95 18.2 ms, approximately **56.86 fps**, 151 draw calls and 46,562 triangles. This is a measurement, not a strict 60-fps pass or evidence of physical-phone performance. No baseline attribution or performance optimization claim.
- Mobile is desktop Chrome emulation, not Safari/iOS/Android hardware. No video was recorded. Existing small marquee softness, compact secondary text, and ambiguous small-scale claw/prize contact remain; approved art was preserved.
- GLB failure/timeout retains the existing primitive 3D fallback; module/no-WebGL uses CSS. Late assets do not replace the settled presentation. Initial reduced-motion preference intentionally uses CSS; live preference changes suppress renderer flourishes and shorten subsequent reveal waits.
- This card does not audit wallet authentication, accessibility of every modal, gallery loading, custody, or production readiness.

## Next step
`t_f12005a1` owns isolated integration/review and broader website/mobile polish. Integrate the exact pushed feature SHA from the board handoff; inspect these actual images and rerun the bounded harness after integration. Production release remains separately held.
