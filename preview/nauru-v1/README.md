# Nauru v1 — Coral Pinnacles & Lagoon

Open **nauru-v1.html** directly in Edge/Chrome. Entire runtime, model, maps and actual-source poster are embedded. **HTML 2,484,194 bytes; GLB 1,281,980 bytes.** Drag/touch rotation, Open/Close lid and Reset view; reduced motion snaps to the endpoint. Cosmetic inner collectible only, not the custody vault or an on-chain action. No mint, keys, chain access, public hosting or deployment.

## Design and source
The prewritten `design-brief.md` cites the raised coral plateau, pinnacles and inland Buada Lagoon. This composition abstracts those landscape features, not a geographic model or traditional craft replica. Eight uneven pinnacles surround a visibly inset muted turquoise lagoon on a pale limestone terrace. The porous ivory stone body, brass family fittings, dark teal seam and hollow interior form a wide keepsake box. Maps are procedurally painted at 384×384, not scans or copied photographs.

`nauru.blend` is named editable Blender source; `nauru.glb` is the portable export. `mechanism.blend`, motion and viewer/test lineage are reused from repository Japan v1 / Iceland pilots at base ff5d78f. Shared base art and all other preview directories were left unchanged. `poster.png` is a real Cycles render of the delivered source, not promotional imagery. `poster.jpg` is its embedded compressed version. Three.js MIT license is included.

## Verified on the final bytes
- Actual GLTFLoader: 69 meshes, 14,092 triangles, 5 materials; zero nonfinite vertices or degenerate triangles. Decoded color/roughness/normal variation; roughness read from green channel. All eight pinnacles and terrain have lid ancestry.
- Independent saved-source reopen: hollow interior floor at z≈0.265; ten intersecting hinge attachment pairs. **81 sampled poses, all 30 moving and 39 static meshes, no unintended surface intersections.** Latch-vs-lid included. Only explicitly named concentric bearing contacts exempt. This is sampled surface-intersection testing, not continuous collision/manufacturing certification or a check of every co-moving decorative contact.
- Original lid/latch world pivot matrices independently compared against reopened mechanism.blend. 80° latch release precedes 105° lid opening; 101 unit-test samples and invalid-asset negative cases passed.
- Bidirectional saved-source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Three packed source maps. This does not assert byte-identical re-export.
- Theme tests: eight varied-height spires, actual roots intersect the terrace height, every lagoon vertex contained within the outer limestone polygon, source-camera center ray reaches lagoon, upper terrace normals face upward, all ornaments lid-owned.
- Edge offline `file://`: desktop 1440×1080 and touch-emulated 390×844. Native clicks/taps, drag/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Open silhouette max absolute projected NDC≈0.8924. Corrupted embedded bytes reach the real parser and show disabled controls/poster; no-JS poster separately checked.
- RTX 4060 desktop GPU; mobile **emulation**, not physical-phone performance, accessibility certification or frame-rate benchmarking.
- `inventory.json`: exact bytes/SHA-256; source ZIP inventory and every archived entry read back. Local Git attributes preserve bytes across Windows checkout. Package contains explicit required source, GLB, HTML and evidence, excluding dependencies/backups/caches.

## Failures, correction and visual limits
The first build could not find esbuild: the suggested main-checkout dependency directory was empty. Installed the existing package's pinned dependencies locally in this new folder (not an upgrade or runtime network dependency). Optional Codex lane failed with HTTP 401 and produced no edits; Hermes authored and verified this delivery directly.

A stricter comparison to the frozen brief rejected the first tallest pinnacle: actual perturbed cap **0.665035** exceeded the **0.65** limit. `initial/height-failure.txt` retains that real failure. Lowered its generator height by 0.02, rebuilt source/GLB/poster, and reran all gates without relaxing the bound. Terrace ring winding was also corrected during review and an upward-normal assertion added. A deliberately detached pinnacle was rejected in `initial/detached-negative-output.txt`; that negative-control mutation was never saved to delivered source. Browser timing checks wait for observed endpoint state rather than assuming a fixed short wall-clock interval contains a rendered frame.

Final poster/mobile and rear-open screenshot inspection found no obvious floating components or clipping. The lagoon is readable but foreshortened/subordinate at mobile size; peaks are simplified faceted spires, not photoreal weathered karst. Stone can read as chalk/plaster rather than unmistakable porous limestone. Brass is clean, the teal seam conspicuous, source render has some sampling grain, and right-side peaks overlap visually. These are honest v1 styling limits. No claim of reference equivalence or independent identification as Nauru without its label. User waived per-asset human review until collection assembly.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/Playwright, installed Edge, Node.js and the package's build dependencies. `npm ci --prefix preview/nauru-v1 --no-audit --no-fund` restores the local lockfile. Build also supports the sibling Iceland dependency folder if populated. Runtime HTML needs no install or server.

From repository root:
1. `python preview/nauru-v1/maps.py`
2. Blender `--background --factory-startup --python-exit-code 1 --python preview/nauru-v1/author.py`
3. Run Blender with each of `verify_source.py`, `verify_parity.py`, `verify_theme.py`, `verify_pivots.py` in this folder.
4. `node --test preview/nauru-v1/tests.mjs`
5. `python preview/nauru-v1/build.py`
6. `python preview/nauru-v1/verify_browser.py` then `python preview/nauru-v1/verify_extended.py`
7. `python preview/nauru-v1/package_delivery.py`

Authoring overwrites generated output; save manual edits separately. Refresh evidence/inventory after regeneration. Full archive is `nauru-v1-source.zip`. All changes are additive under `preview/nauru-v1/`; branch backup only, no merge. Final collection integration is handled by a separate dependent card.
