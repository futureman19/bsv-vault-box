# Preserved failure record

1. Optional Codex CLI input lane exited 1 before implementation: HTTP 401 invalid_refresh_token / invalid_jwt. No Codex patch or commit was accepted. Hermes authored and verified the asset directly; credentials were not modified.
2. First `python preview/serbia-v1/build.py` failed with MODULE_NOT_FOUND for `preview/iceland-pilot/node_modules/esbuild/bin/esbuild`. Both the prescribed worktree dependency path and main-checkout dependency directory existed but were empty. Fix: `npm install --prefix preview/serbia-v1 --no-audit --no-fund` installed the already pinned Three 0.180.0 and esbuild 0.25.11 locally (3 packages); no dependency upgrade or sibling edits. Subsequent build: `HTML_BYTES 2303237 GLB_BYTES 1140356`.
3. Deliberately removing ivory relief 0 from the theme validator's object list raises AssertionError; restoring the original six objects passes. This is a postimplementation negative control, not test-first TDD. See theme-check.json. Corrupt GLB and invalid motion-asset controls separately exercise rejecting paths.

No geometry, collision, parity or browser acceptance failure occurred in the first completed acceptance run. None of those thresholds were relaxed.
