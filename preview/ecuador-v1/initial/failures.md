# Actual tooling failures

1. Optional Codex lane exited 1 with `invalid_refresh_token` / HTTP 401 before implementation. Raw output is retained in lane-log.txt outside the deliverable ZIP. No credential modification, accepted diff or Codex test run.
2. Bootstrap failed with FileNotFoundError for `preview/japan-cedar-v1/tests.mjs`. Japan does not carry that file; reusable unit tests were obtained from read-only `preview/iceland-pilot/tests.mjs` instead. Bootstrap completed after that correction.
3. First build failed `Error: Cannot find module ... preview/iceland-pilot/node_modules/esbuild/bin/esbuild`, `MODULE_NOT_FOUND`, exit 1. Direct directory inspection found the main shared node_modules directory empty. `npm install --prefix preview/ecuador-v1 --no-audit --no-fund` installed the exact existing package.json pins locally; no dependency upgrade. Subsequent build output: `HTML_BYTES 3118630 GLB_BYTES 1722744`.

These are real failed commands, not deliberate RED tests. Geometry/theme tests were authored after implementation. The deliberate detached-islet negative control and invalid-asset unit tests prove their corresponding assertions reject malformed state, not that every assertion was individually mutation-tested.
