# saint-vincent-and-the-grenadines — bounded camera trial, still held

Open `saint-vincent-and-the-grenadines-view-v2.html` offline. Camera-only successor: camera (-5,7.5,7), target (0,.95,0), maximum distance 12.5 so opening reframing is not clamped. No geometry, textures, source Blender or motion bytes changed; `launch/collection-repairs/recovery-browser.json` independently proves exact source/model/motion identity against the pinned original.

Actual before/after mobile captures are `camera-comparison.jpg`. The higher angle exposes more of the summit, but the small crater remains weak at normal mobile size. This is **partial**, not a resolved art hold or a recommendation to replace the approved baseline. Stop after this one trial: a larger or contrasting crater would be a substantive new art decision. The unchanged fallback poster intentionally retains the original source camera.

Fresh `browser-check.json`, `extended-check.json` and `fresh-motion.txt` cover offline Edge desktop/mobile emulation, mouse/touch rotation and buttons, open/close, interrupted reset, reduced motion, full-open framing, corrupt-GLB and no-JS fallback, no network/errors/overflow. No fresh Blender collision/parity run was necessary for byte-identical model/source; those historical results are under `historical-v1/` and are not new certification. Not physical-phone testing.

Build with the pinned package dependencies (`npm install --ignore-scripts --no-audit --no-fund` on initial recovery, then `npm ci` using this new lockfile) and `python build.py`. Run `verify_browser.py`, `verify_extended.py`, and `node --test --test-reporter=tap tests.mjs`. First attempted npm ci failed because the original had no lockfile; the pinned install generated one only here.

Cosmetic inner collectible only, not a custody container operation. Preserve final-art, rights, storage, signing, sale and release gates. No deployment/minting.
