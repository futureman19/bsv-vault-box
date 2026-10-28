# Arcade material and presentation polish

Local production files in `docs/`, served without a build step. Headed Chrome on Windows / NVIDIA RTX 4060. Mobile sizes are viewport emulation, not phone certification.

## Scope

- Beveled cabinet shell, plinth, marquee and prize packaging; matte wrapping, satin/brass trim, moderated chrome and interior lighting; lighter cast shadow.
- Responsive two-column desktop composition and stacked mobile presentation, clearer typography, seal-checker entry point and demo disclosure adjacent to PLAY.
- Launch rules explicitly labeled as future behavior; draw-at-open identified as draft. Wallet code, motion mechanics, checker, covenant and cryptographic implementation unchanged.
- No payment, mint, broadcast, deployment or default-branch push.

## Executed checks

- `node --test test/*.test.js`: 30 passed, 0 failed.
- `python test/python-parity.py`: 50 differential cases passed.
- `python test/hardening.py`: encoding/input/cap tests and 5 independent exact permutation odds oracles passed.
- `python test/arcade-visual-browser.py`: desktop 1440×1000, mobile 390×844, narrow 320×740, tablet 768×1024; no horizontal overflow, static reduced-motion backing-store pixels, normal idle movement, keyboard PLAY, cancel, seal-checker navigation; disabled-WebGL fallback.
- `python test/claw3d-browser.py`: hardware renderer, reduced motion, normal idle, dispose/remount/context loss and fallback drop/reveal passed.
- `python test/claw-interactive-browser.py`: keyboard/pointer/touch aiming, bounds, duplicate drop protection, actual thirty-second timeout, grab/carry/drop/reveal, replay, synthetic wallet call contract, reduced motion, fallback and context-loss checks passed. Final input response: 8 ms.
- `git diff --check`: passed.

## Evidence and limitations

`desktop.png`, `mobile.png`, `narrow.png`, `tablet.png`, `fallback.png` are full-page captures. `desktop-armed.png` and `mobile-reveal.png` cover active play. Desktop/mobile/fallback screenshots were reviewed with vision.

`visual-report.json`, `renderer-report.json`, and `interaction-report.json` preserve actual measurements. Landing console errors: none. The unchanged checker requests a missing `/favicon.ico` on first navigation, recorded separately in the visual report.

Strict 60 FPS was **not achieved**: final interaction sample ~56.37 FPS; 4× CPU-throttled desktop proxy ~54.95 FPS. No physical phone performance claim. Wallet testing is a synthetic API-contract test, not a real extension login.

Browser tests were adapted for the new layout: touch targets scroll into view before viewport-coordinate injection; motion equality uses backing-store pixels rather than fractional element screenshot crops. The old historical CSS-cabinet screenshot parity assertion was replaced by fallback play/reveal and overflow checks because layout/background changes are intentional. Historical evidence directories were restored; new reports live here.

Deployment discovered via GitHub Pages API: legacy Pages build from `master:/docs`, custom domain `https://boxsv.com/`. Merge to master would publish; no deployment was performed.
