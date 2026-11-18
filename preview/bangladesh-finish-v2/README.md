# Bangladesh finish V2 — presentation-only candidate

One correction pass. On low-DPR screens, fine ivory textile motifs and diagonal trim showed pixel-scale breakup. The new viewer uses a 2× drawing buffer instead of `min(devicePixelRatio, 2)`. At DPR ≥2 the existing effective ratio is unchanged. Camera, lighting, texture filtering, materials, geometry, pivots, motion, poster and CSS remain unchanged. This is not a model redesign or final art approval.

The same-camera native-mobile comparison shows clearer individual motifs and more consistent thin edging. It does not repair intentionally segmented trim, make the landscape realistic, or establish absence of motion shimmer. Tiny oblique motifs still lose detail. Low-DPR fill work increases; physical-phone thermal, battery and performance testing remains unperformed. Desktop/mobile emulation passed; the 30-frame interval samples in browser-check.json are observations on this host, not device benchmarks.

## Files and reproduction
- `bangladesh-finish-v2.html`: self-contained offline viewer, **3,409,390 bytes**, below 5,000,000.
- `bangladesh.blend`, `bangladesh.glb`: exact original selected source/export bytes.
- `historical-v1/`: original committed files (excluding the redundant old ZIP), original tests and failure evidence unchanged. Its original inventory does not cover this successor; use the new root inventory.
- `historical-manifest.json`: original Git SHA and exact per-file hashes.
- `build.py`: deterministic one-expression patch to frozen original source, compiled bundle and HTML. No compiler/network needed for this viewer-only correction. Full geometry regeneration remains the original historical workflow and dependencies; no claim that it was freshly regenerated.
- `verify_parity.py`: freshly reopens the saved Blender file and imports the GLB; bidirectional geometry tolerance <1e-5.
- `verify_browser.py`: desktop and mobile native controls, drag, open/close, interrupted reset, reduced motion, open projection, DPR 1/2/3, genuine corrupt-GLB and no-JS fallback, offline/no external requests. An initial incorrect `noscript img` harness assumption failed; `browser-initial-failure.txt` is retained. The actual fallback is the persistent `#fallback` image; no viewer code was changed for this harness fix.
- `tests.mjs`: two original motion/asset contract tests freshly passed. No fresh collision sampling: every geometry, material and pivot byte is unchanged.

Run `python build.py`, `node --test --test-reporter=tap tests.mjs`, Blender background/factory-startup with `--python-exit-code 1 --python verify_parity.py`, then `python verify_browser.py` in an environment with Playwright/Edge. A whole-archive hash must be trusted separately; inventories prove byte consistency, not publisher authenticity.

## Holds
All original final-user-art, preservation/storage, mint/release and other owner holds remain. Bangladesh is one of 201 equal-supply one-of-one inner collectibles; the launch boundary is one inner NFT plus a detached signed record, not an accessory/certificate NFT. No reuse support, mint, sale, production deployment or collection-wide completion is claimed.
