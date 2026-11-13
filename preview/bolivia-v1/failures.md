# Observed failures and fixes

The optional Codex lane exited 1 before producing edits: `ERROR: Your access token could not be refreshed. Please log out and sign in again.` Raw lane output is retained separately. No credentials were read or modified; direct Hermes implementation followed.

First build exited 1:
```
Error: Cannot find module 'C:\Users\futur\Desktop\bsv-vault-box\.worktrees\t_662ce9e8\preview\iceland-pilot\node_modules\esbuild\bin\esbuild'
code: 'MODULE_NOT_FOUND'
```
Inspection showed both referenced node_modules directories existed but were empty. `npm install --no-audit --no-fund` in the NEW Bolivia directory returned `added 3 packages in 12s`; local pinned dependencies fixed the build. No other preview source was changed.

Theme negative control actually removes the mountain's lid parent in memory and receives `Detached lid ornament`; restores it and rechecks. Motion negative control rejects missing lid/empty triangles. These are explicit post-implementation regression controls, not a claimed TDD red phase.
