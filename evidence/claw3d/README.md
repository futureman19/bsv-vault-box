# Claw scene verification — candidate, not release approval

Base: 2258bf5b7fb319c33e94112a5bedf00b71231f6f (origin/master).

## Passed
- `node --check docs/claw3d.js`.
- `python -m http.server 4179 --bind 127.0.0.1 --directory docs` and `python test/claw3d-browser.py`.
- Headed installed Chrome, hardware ANGLE / NVIDIA GeForce RTX 4060 / D3D11 (not SwiftShader), 1280x900 and 390x844 screenshots. These are viewport sizes, not physical phone evidence.
- Zero page errors (including unhandled rejections) and zero console errors on both page loads and WebGL-disabled load.
- Disabled WebGL: original CSS cabinet present. Reduced-motion cabinet screenshot byte-identical to baseline master rendered in the same browser.
- Reduced-motion canvas screenshots unchanged over time; switching preference enables visible idle changes.
- Idempotent dispose, remount, context-loss fallback.
- 761,874 net added bytes under docs, including vendor/license/provenance; below 1,500,000 bytes. No runtime CDN, no bloom.
- `docs/claw.js` identical to base; original markup and game/wallet/reveal/rules unchanged.
- `git diff --cached --check`; vendor upstream whitespace excluded by scoped attributes, bytes preserved.

## Not passed / limitations
- **BLOCKED: physical mid-range phone 60fps verification.** `adb devices` returned no connected devices. Desktop RAF sampling is approximately 17.6ms median / 18.2ms p95 (180 samples); it does not establish 60fps on a phone, nor GPU completion time. Do not call the mobile viewport a phone performance pass.
- General suite `node --test test/*.test.js`: 17 pass, 1 fail. The checker UI test still reads docs/index.html despite the checker having moved to docs/check.html. Reproduced the same `id="manifestTxid"` assertion failure on a temporary copy of base master; left this unrelated test untouched.
- Art is a procedural stylized cabinet, not photorealistic. Glass/metal and six prizes are recognizable; rear gifts overlap and small secondary labels remain small on mobile. Owner art approval remains advisable.
- Scene-only by design: PLAY still drives the hidden original CSS machine and original reveal. No 3D play animation until the child card.
- Optional Codex lane exited 1 with HTTP 401 token-refresh failure before editing; no Codex changes accepted. Implementation and tests were performed directly by Hermes.

## Evidence
- desktop.png / mobile.png: real headed GPU captures, reduced-motion deterministic pose.
- fallback.png: disabled-WebGL cabinet.
- report.json: actual renderer and lifecycle/motion/timing results.
- payload.json: staged Git-byte accounting.

No deployment or merge performed. Draft PR only; do not release the downstream animation task until the unresolved device gate is addressed or explicitly waived.
