# BoxSV production verification

Published https://boxsv.com/ from approved commit `9709a7a3fd1322a57cc090c97c03f733fed5ccb3`.

- Fetched origin: master `2940eb5` was already an ancestor, with no concurrent commits to integrate. Tracked working tree clean. Feature branch pushed and read back first; master fast-forwarded, pushed without force, and read back. No application changes made during publication.
- Pages source confirmed master:/docs; existing CNAME and HTTPS preserved. No DNS, wallet, payment or crypto changes.
- Pages build 1320659357 built exact approved SHA. Actions success: https://github.com/futureman19/bsv-vault-box/actions/runs/40637216342
- Local gates on exact published tree: 30/30 Node tests, 50 Python parity cases, git diff --check passed. Static docs deliverable has no bundler.
- hash-report.json: all 16 fetched HTML/CSS/JavaScript/GLB files returned 200 and SHA256 matched approved Git blobs. Four binary GLBs also match working-tree bytes exactly. Text working-tree CRLF normalization verified independently; original comparison failure preserved.
- runtime-report.json: live headed Chrome desktop 1440x1000 and mobile/touch emulation 390x844 (reduced motion) loaded all four GLBs, authored assets ready, keyboard/touch movement, drop/grab/carry/reveal/reset passed. No page errors, console errors, or HTTP errors.
- Renderer warnings retained: desktop D3D shader precision warning; both viewports Three PCFSoftShadowMap deprecation/fallback warning. These are not a warning-free result. Initial overly strict warning gate failure retained; only these explicit warning categories were separated from errors. No app/test-source rewrite.
- Screenshots: desktop/mobile idle, grab, carry, reveal and reveal-viewport. Desktop idle visually passed. Initial fullpage mobile modal screenshot suggested bounded backdrop; actual viewport screenshot visually confirmed full coverage and accessible prize/actions. DOM overlay coverage reports prove viewport coverage (clientWidth excludes scrollbar).
- This is not physical-phone verification or a new performance benchmark. Prior 55.78fps limitation remains; no strict 60fps claim. Demo only: no login, payment, mint or chain write exercised.

Evidence is local and uncommitted under evidence/deploy-9709a7a; approved application commit remains unchanged. verify-live.py reproduces bounded build polling, artifact hashes and live scenarios. Initial diagnostics retained in initial-*.log.
