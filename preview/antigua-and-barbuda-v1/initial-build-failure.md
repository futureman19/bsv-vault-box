# Observed initial toolchain failure

Build process exited 1 after source, parity and theme verification succeeded.

Observed error:
```
Error: Cannot find module 'C:\Users\futur\Desktop\bsv-vault-box\.worktrees\t_334fd501\preview\iceland-pilot\node_modules\esbuild\bin\esbuild'
code: 'MODULE_NOT_FOUND'
Node.js v24.13.0
```

This is a concise transcription of tool output, not the complete raw stderr. Inspection showed the shared `node_modules` existed but had no entries. Correction: `npm install --prefix preview/antigua-and-barbuda-v1 --no-audit --no-fund` installed the pinned local dependencies; temporary symlink was removed. Unchanged build script then succeeded (build-output.txt). No tests or byte thresholds relaxed.
