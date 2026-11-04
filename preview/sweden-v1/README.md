# Sweden v1 — Falun Red & Kurbits

Open **sweden-v1.html** directly in Edge/Chrome. Entire offline viewer: **3,709,575 bytes**. Embedded GLB: **2,202,964 bytes**. Drag/touch rotates; Open/Close runs the staged latch/lid; Reset cancels movement; reduced motion snaps. No runtime network dependencies. Not minted, hosted, deployed, or a custody proof.

## Design and visible limits
A wide red painted-wood keepsake box with pale finger joints, blue inset, three newly invented floral rosettes, cream/green low relief, dark wooden feet and satin brass. Sweden's Falun-associated red wooden buildings and Dalarna kurbits painting informed the sourced pre-model `design-brief.md`. No reference photographs or copied historical motifs are embedded; no claim of branded pigment use, historical authenticity, hand-painted craftsmanship or representation of every Swedish tradition.

Actual browser screenshot inspection: clear chest silhouette, visually attached brass hardware, hollow interior and connected open lid; the entire open model fits mobile. Floral composition reads clearly from the elevated `lid-detail.png`. At default mobile scale the flowers read as decoration rather than resolved craft detail; blue becomes pale under studio light. Clean uniform grain, simplified brass and sparse angular relief remain deliberately stylized. Closed dark seam is prominent; no photoreal-equivalence or physical-manufacturing claim. Ornament is shallow relief, not freestanding terrain. Front and unseen interior/hardware construction are authored interpretations.

## Verified evidence
- `source-check.json`: independently reopened packed Blender source; **81 motion samples, 79 moving and 99 static meshes**, zero unintended intersections; explicit inherited mating bearings only exempt. All new lid ornaments participate. Hollow floor ray z=0.2650000155 and ten hinge attachment pairs. Sampled surface intersections, not continuous collision certification.
- `parity-check.json`: saved-source and imported export vertex sets within **1.712013073529306e-7 units**, below 1e-5; three packed procedural maps.
- `theme-check.json`: original mechanism pivot matrices unchanged, 51 lid-owned decorative meshes, three rosettes/24 petals/20 leaves, declared slab dimensions and relief bounds. Deliberately detaching an ornament triggers a rejection; restored candidate passes. This negative control is post-model regression proof, not TDD.
- `browser-check.json`: real Three GLTFLoader, **28,180 triangles / 178 meshes / 9 materials**, no nonfinite vertices or degenerate triangles. Offline file:// desktop 1440×1080 and mobile touch emulation 390×844: native open/close, drag, interrupted reset, reduced motion, full-open fit, no overflow, no HTTP(S) requests or JS errors. Corrupted embedded GLB hits the real parser and falls back to the poster. Browser was Edge on RTX 4060; no physical-phone or FPS claim.
- `extended-check.json`: actual decoded red color, pale wood and GREEN-channel roughness ranges 49/41/47; maximum texture axis 512. Nonblank actual-source poster and no-JavaScript fallback passed. No inherited Japan visible copy.
- `motion-output.txt`: two motion/invalid-input tests pass, including staged release and invalid-asset rejection.
- `delivery-check.json` / `inventory.json`: exact bytes and SHA-256 for payload files, ZIP entry-set and hash readback; envelopes excluded from their own inventories to avoid circular hashes.

## Real failure and correction
`initial/theme-relief-height-failure.txt` preserves the genuine failed source assertion: initial round stems extended below the intended relief height. Raised stems from center z=2.04 to 2.054 and thickened the blue carrier to keep relief seated, then regenerated source/export/poster and reran all source, parity, theme and browser gates. Final relief z=2.026–2.099. The original dimensions/height assertion was not relaxed. The approximate brief's lower relief target 2.03 admits the 0.004 seating overlap of leaves.

The main checkout's promised node_modules directory existed but was empty. First build failed with MODULE_NOT_FOUND for esbuild. Installing the pinned package.json dependencies inside this new directory repaired the build without modifying another preview. Node here is only the JavaScript build/test runtime; no blockchain node was used.

## Files / reproduction
`sweden.blend` is named editable source; `sweden.glb` standalone mesh; `poster.png`/`.jpg` are actual source renders, not promotional substitutes. Desktop/mobile screenshots are actual browser output. `mechanism.blend` is the unchanged trimmed Japan pilot mechanism, not its country art. Three.js MIT license is included. `sweden-v1-source.zip` excludes node_modules, backups and caches.

Tools: Blender 5.2.1, Python with Pillow/numpy/Playwright, Node with pinned Three 0.180.0 and esbuild 0.25.11, installed Edge. From this directory:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py`
5. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
6. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

`author.py` rebuilds independently using the included mechanism and maps. Optional `setup_author.py` records scaffold derivation and depends on sibling Japan source; it is not needed for standalone reproduction. Regeneration overwrites source/export/poster, so preserve manual edits separately. Update README measurements and regenerate inventory after changes. Build can use local dependencies or sibling pilot dependencies; neither is a runtime dependency.

Scope is additive `preview/sweden-v1/` only. Shared vault kit, other previews, chain, keys, mint, VPS and production site untouched. Branch backup is not deployment. Per-asset human review was waived for the batch; final integration/review is a separate card.
