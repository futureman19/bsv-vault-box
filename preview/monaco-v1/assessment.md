# Execution history and bounded visual assessment

## Real failures and fixes
1. Optional Codex lane exited 1 with HTTP 401 / invalid_refresh_token before edits. `codex-lane.log` preserves its output. No credentials were accessed or changed; no Codex diff was accepted. Hermes implemented directly.
2. Initial `python preview/monaco-v1/build.py` exited 1 with `Cannot find module ...preview\\iceland-pilot\\node_modules\\esbuild\\bin\\esbuild`. The instructed baseline dependency directory existed but was empty. Installed the unchanged pinned package.json dependencies locally inside this new preview using `npm install --prefix preview/monaco-v1 --no-audit --no-fund`; build then passed. No baseline directory files changed. This failure was captured in tool output, not a saved raw build log; this is its contemporaneous summary.
3. A deliberately detached lid ornament was rejected by the ancestry assertion, then parent restored in memory. `theme-negative-control.json` records EXPECTED_FAIL. This is a post-implementation negative control, not test-first TDD and not a model defect. Three invalid runtime-asset controls also rejected.

4. First background `node tests.mjs` invocation hit the host shell shim (`stdin is not a tty`) and exited 1 before executing tests. Preserved as `initial/motion-shell-failure.txt`; invoking `C:/Program Files/nodejs/node.exe` directly fixed execution. All motion/build/browser checks then reran successfully.

5. Staged-inventory verification correctly failed because the repository ignores `*.log`, so the inventoried Codex failure log was absent from Git's index. Explicitly staging this one in-scope diagnostic log corrected the packaging/index mismatch; no hash check was relaxed.

## Actual image review
Actual Blender `poster.png`, offline mobile closed and desktop open screenshots were inspected. Body reads as pale mottled stone; red/ivory details, brass and terracotta/blue/green miniature are visible. Silhouette fits in closed and open tested views. Interior depth visible when open. No obvious major floating geometry was observed; independently sampled hinge attachment checks provide stronger evidence than the tiny fittings in the screenshot.

Limitations: stylized generic Mediterranean village rather than a recognizable exact Monaco landmark. Flat enamel sea, faceted cliff, sparse building detail and rounded garden clusters. Bright browser lighting makes sea lighter cyan and body nearly ivory. Fine render noise remains (24-sample source render with denoising disabled). Dark seam can suggest a slightly ajar box; it is a modeled decorative reveal. No photoreal equivalence, manufacturing suitability, physical-phone performance or geographic accuracy claimed. Browser assertions, not still-image inspection, establish actual offline interaction.
