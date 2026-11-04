# Observed tooling failures

- Optional Codex exec returned exit 1 with HTTP 401 invalid-refresh-token before edits. Raw log retained. No accepted Codex changes or commits. No credentials were inspected or changed.
- First `python preview/guatemala-v1/build.py` exited 1: Node could not resolve `preview/iceland-pilot/node_modules/esbuild/bin/esbuild`. Python inspection found both the worktree and main checkout's prescribed node_modules directory empty. Fixed by `npm install --prefix preview/guatemala-v1 --no-audit --no-fund` (3 packages installed), then reran the unchanged build successfully. The local lockfile captures dependencies; no other preview modified. This note is a contemporaneous summary of terminal output, not a reconstructed raw log.
- Research URL extraction tool was search-only; fetched Museo Ixchel with Python urllib instead. First text parser attempted bs4 (not installed); switched to standard-library tag removal, without changing packages.

- First staged-Git inventory check failed: repository-wide `*.log` ignore rules omitted `author.log` and other raw logs from the index even though they were in the source ZIP. Fixed by explicitly force-adding only this preview's log files, then rerunning every staged blob hash check; no byte/hash gate relaxed.

Art acceptance passed on its first run. Deliberate detached-terrain, corrupt-GLB and invalid asset-contract tests are separately labeled negative controls, not accidental art failures.
