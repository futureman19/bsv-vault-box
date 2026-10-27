# Interactive claw verification

Status: functional gates pass; **strict 60fps gate is NOT passed**. Draft PR only; do not merge on the strength of the functional test exit code.

## Implementation

Shared deterministic `ClawMotion` mechanics drive both renderers. Connect/demo arms a real 30-second deadline. Pointer/touch joystick, cabinet drag and arrow keys move with eased velocity within pit bounds. DROP/Space/Enter/timeout lock input and retrieve the nearest equally-sized wrapped prize; aiming never determines contents. Descend, close, lift, carry, release/squash and chute flash lead into the unchanged demo reveal. PLAY AGAIN resets the round. Reduced motion shortens retrieval, not aiming time. Late mounting/remounting and WebGL context loss preserve the same round.

No wallet payment, mint, draw or covenant code changed. Demo remains illustrative, not an actual VAULT-0003 draw.

## Reproduce

From repository root (Python with Playwright and installed Chrome):

```
node --test test/*.test.js
python test/claw-interactive-browser.py
python test/claw-interactive-perf.py
node --check docs/claw.js
node --check docs/claw-motion.js
node --check docs/claw3d.js
```

Browser scripts start/stop their own loopback server and headed Chrome. Functional script exits nonzero for functional failures; performance is recorded separately as `strict_60fps_pass` and must not be inferred from exit status.

## Gates

1. **PASS functional:** synthesized keyboard, mouse joystick drag, CDP native touch, DROP button. Headed Chrome RTX 4060 D3D11. Captures: [armed](armed.png), [moving](moving.png), [descend](descend.png), [grab](grab.png), [carry](carry.png), [drop](drop.png), [reveal](reveal.png). Zero console errors, page errors, unhandled rejections in desktop, reduced/mobile and fallback contexts.
2. **PASS:** real 30-second wait, no clock acceleration; [timeout](timeout.png) has phase descend, remaining 0, reason timeout, drops 1.
3. **PASS:** held input reaches x=.9,z=.5 and cannot exceed bounds; unit test additionally drives negative depth; repeated Space/drop calls during retrieval ignored; exactly one callback. PLAY AGAIN resets timer, selection and inputs.
4. **PASS:** separate headed browser with `--disable-webgl`, keyboard + cabinet drag + Enter + replay. [Fallback moving](fallback-moving.png), [grab](fallback-grab.png), [carry](fallback-carry.png), [reveal](fallback-reveal.png). CSS attachment bounding-box assertion and visual inspection confirm prize follows claw. Remount and actual `WEBGL_lose_context` also tested.
5. **PARTIAL / BLOCKED:** input state response 5.7ms; raw runtime payload 793,880 vs parent scene 783,759 bytes (+1.291%, including vendored JS; unchanged external font/CSS references not included). Desktop input 56.80fps, median 17.6ms, p95 18.2ms. 4x CPU proxy 56.75fps, median 17.6ms, p95 18.2ms. **Not 60fps and not phone proof.** Separate comparison found blank page 56.13fps, parent scene 55.90fps, interactive 56.58fps, consistent with a host/browser scheduling ceiling. At 4x CPU, mechanics step p95 0.20ms/max 0.40ms. Need a genuine 60Hz+ headed environment rerun or explicit owner acceptance of environment-limited proxy; no waived gate assumed.
6. **PASS API-flow regression, not live extension authentication:** cancel leaves idle; demo arms; synthetic CWI fixture verifies unchanged `waitForAuthentication({})` then `getPublicKey({identityKey:true})`, followed by identity-bearing demo reveal. No credentials or transaction signing used.

20 Node test entries passed. Exact measurements: [report.json](report.json), [perf-comparison.json](perf-comparison.json).

## Recovery / QA notes

Recovered uncommitted prior-run implementation, reviewed it directly, added independent tests. Fixed a CSS vertical-scale mismatch that detached carried prizes, moved the timer clear of the rail, reset stale reason/travel state, and shared mechanics across late/remounted renderers. No new Codex subprocess used. One perf-harness defect was corrected: Playwright supplies route plus request, so a default-valued second lambda parameter was incorrectly overwritten by Request. This was a harness error, not a product error.
