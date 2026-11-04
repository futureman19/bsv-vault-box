# Moldova v1 — Woven Garden

Open `moldova-v1.html` directly in Edge/Chrome. Standalone offline preview: **3,476,054 bytes**; embedded standalone `moldova.glb`: **2,016,624 bytes**. No server or network required. Drag/touch rotates; Open/Close lid and Reset operate the model; reduced-motion preference is honored. Cosmetic movement only, not a custody operation.

## Design and provenance
Research-backed brief written before modeling: Moldova's shared wall-carpet tradition with Romania, documented by UNESCO (citation in design-brief.md). Dark woven-inspired wall and lid inserts, walnut-colored frame, burgundy/ivory geometric borders and three raised eight-petal garden medallions. These motifs are invented contemporary designs, not authenticated historic patterns, fabric scans or a comprehensive representation of Moldova. No third-party reference images are embedded. Named Blender geometry and four 512px procedural maps are authored by scripts.

Mechanism lineage: included trimmed `mechanism.blend`, viewer and test framework reused from repository Japan v1 at base ff5d78f. Existing kit and other previews unchanged. Three.js MIT license included. No mint, wallet, keys, chain queries, external messaging, VPS or production deployment. This is one inner collectible in the proposed 201 equally one-of-one collection, not its outer custody box.

## Verified final files
- Independent saved-source reopen: hollow floor ray z=0.26500001549720764; ten intersecting hinge attachment pairs. Original lid and latch world pivot matrices unchanged.
- **81 sampled motion poses**, all **50 moving / 47 static meshes**, zero unintended surface intersections. Latch-versus-lid surfaces included. Only named mating hinge barrels and latch-pin bearings excluded. This is sampled surface collision evidence, not continuous collision or manufacturing certification.
- Original choreography: latch releases 80 degrees first; lid then opens 105 degrees. Two Node tests passed, including rejecting missing/nonfinite/empty asset records.
- Saved-source/export maximum nearest-vertex error **1.712013073529306e-7**, below 1e-5. Four packed images. Real GLTFLoader: **15,412 triangles, 97 meshes, 7 materials**, no nonfinite vertices or degenerate triangles.
- Theme tests: five woven panels; three eight-petal flowers (33 total flower/leaf/heart meshes) all owned by lid; petal span and relief bounds; no inherited tree/terrain theme; original pivots. Deliberately detached ornament was rejected by ancestry oracle and restored without saving.
- Actual Edge offline file:// desktop 1440×1080 and mobile 390×844 touch emulation: native open/close, drag, interrupted reset, reduced motion, no overflow, no external HTTP requests or runtime errors. Open-pose maximum absolute projected NDC ~0.8924 (inside viewport). Actual corrupted embedded GLB parser failure shows poster and disables controls; no-JS poster also tested.
- Runtime maps decoded with nonzero variation, roughness from the green channel. Poster rendered from final authored source, nonblack pixel check. Exact file-byte/SHA-256 inventory and archive readback in delivery-check.json. Git bytes separately compared to inventory.

## Visual verdict and limits
All three angular flowers, patterned dark wall panels, body and controls are visible in final mobile captures. Open desktop shows hollow interior, released latch and no obvious major clipping. The craft-inspired design is stylized, **not photorealistic or a faithful traditional weave**. Thread bundles were enlarged in one bounded refinement after initial source inspection found the weave too smooth; initial poster and screenshots are preserved in `initial/`. At mobile scale individual over/under threads still do not resolve clearly. Borders read graphically; wood grain is regular; the inherited clasp is visually large, and the seam/hinge gap is conspicuous. Numeric attachment checks establish contact that the hero camera cannot clearly show. Small noise remains in the non-denoised source render. Mobile emulation used an RTX 4060 desktop, not physical phone hardware; no FPS or universal device claim.

## Reproduction
Dependencies: Blender 5.2.1; Python with numpy/Pillow/playwright, installed Edge; Node with pinned package dependencies (`npm ci --ignore-scripts --no-audit --no-fund`). Local dependencies are build-only, never embedded as external runtime requests. The initially specified sibling dependency directory was empty, so dependencies were installed in this preview instead; initial build failed with MODULE_NOT_FOUND before that correction. Optional Codex CLI failed with HTTP 401 and authored nothing; Hermes performed the implementation and all tests directly. Neither credential repair nor secrets access was attempted.

From repository root:
1. `python preview/moldova-v1/maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python preview/moldova-v1/author.py`
3. Run Blender the same way on `verify_source.py`, `verify_parity.py`, `test_theme.py`.
4. `python preview/moldova-v1/build.py`; `node --test preview/moldova-v1/tests.mjs`
5. `python preview/moldova-v1/verify_browser.py`; `python preview/moldova-v1/verify_extended.py`
6. `python preview/moldova-v1/package_delivery.py`

Scripts resolve their inputs in this folder. `prepare_author.py` is retained as implementation provenance and requires the sibling Japan author script; it is NOT needed for normal regeneration. Authoring overwrites source/export/poster. No .blend1 backups, node_modules or Python caches are archived. Source ZIP includes the explicitly required GLB, editable source, offline HTML, maps and tests. Inventory excludes itself and packaging envelopes to avoid recursive hashing; delivery-check is outside the ZIP. No hosted URL or art approval is implied. Per-asset review was explicitly waived; full-collection integration/review remains a separate card.
