# Brunei v1 — Tenunan Gold

Open **brunei-v1.html** directly in Edge/Chrome. Entire runtime, GLB, maps and actual-source poster embedded: **4,254,310 bytes**. Standalone GLB **2,584,812 bytes**. Local cosmetic collectible only; not minted, hosted, deployed or connected to a blockchain.

## Design and visual result
Research-backed kain-tenunan inspiration, with burgundy woven-map panels and fifteen raised brass diamond loops on the lid. The geometric motif is invented, not an authentic Jongsarat pattern or artisan work. The pre-model contract and two factual sources are in design-brief.md. No third-party images or AI promotional substitutes are embedded.

Actual source and mobile render inspection found the burgundy/gold treatment readable and the relief visible, with no obvious clipping or detached parts. At mobile size the fine weave reads more as a patterned finish than individual threads; the lid appears lighter/pinker in viewer lighting. Stone feet and long collection-family latch are stylized. Poster has some sampling noise (24 Cycles samples, denoising disabled). No photorealism, historic fidelity or human art approval claimed; user waived per-asset review for this collection batch.

## Verified evidence
- Saved Blender source independently reopened: 43 moving and 99 static meshes, **81 poses**, no unintended surface intersections. Includes all diamond ornaments; only explicitly named coaxial hinge/latch bearing contacts excluded. Ten hinge attachment overlaps and hollow floor ray z=0.2650000155 pass. Sampled surface checks, not continuous mechanical certification.
- Source/export bidirectional nearest-vertex maximum **1.712013073529306e-7**, below 1e-5. Four packed procedural maps.
- Actual Three GLTFLoader: **28,528 triangles, 142 meshes, 5 materials**, zero nonfinite vertices and degenerate triangles.
- Theme: exactly fifteen lid-owned loops within prescribed height envelope; fifteen centre rays pass through openwork to the solid lid. A deliberately detached ornament is rejected (negative regression control, not a historical implementation failure).
- Offline file:// Edge desktop 1440x1080 and touch emulation 390x844: native open/close, drag/touch rotation, interrupted reset, reduced motion, no overflow/external HTTP requests/JS errors. Full-open projection max absolute NDC 0.892365. Real corrupt GLB triggers parser failure and poster fallback. No-JS poster separately checked.
- Decoded base-color and actual GREEN-channel roughness maps vary; maximum map dimension 512. Motion unit tests exercise 101 progress values and reject invalid asset contracts.
- Exact SHA-256 inventory, ZIP membership/readback, and staged Git blob identities verified. No unexpected author/build acceptance failure occurred; corrupt-GLB, detached-parent and invalid-contract negatives prove tests reject bad inputs.

Browser uses desktop RTX 4060; mobile is emulation, not physical phone performance. Offline browser tests do not prove NFT-wallet compatibility or hosting durability.

## Contents and reproduction
Named editable brunei.blend, brunei.glb, mechanism.blend, maps/, poster.png/JPG, desktop/mobile screenshots, scripts, raw *-output.txt and JSON checks. Source ZIP excludes dependencies/backups. Mechanism and viewer derived from Japan pilot at base ff5d78f1e0d486af5c882c184fc08049996ebdc8; geometry authored with Blender Python, not manually sculpted. Legacy cedar map filenames are retained internal compatibility labels, but all pixels are newly generated textile maps.

Use Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node and npm. Main-checkout pilot node_modules was empty, so identical pinned build dependencies were installed locally inside this folder (ignored, never shipped). `npm ci --ignore-scripts --no-audit --no-fund` restores them. Three license included.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender similarly for verify_source.py, verify_parity.py, verify_theme.py.
5. `node --test --test-reporter=tap tests.mjs`
6. `python verify_browser.py` and `python verify_extended.py`
7. `python package_delivery.py`

Authoring overwrites generated assets; preserve manual edits separately. setup_author.py documents the initial adaptation and requires the sibling Japan author; the delivered author.py itself runs solely from included mechanism/maps and needs no sibling source. Regeneration changes source/render identities, so rerun all gates and packaging. No shared kit or previous preview modified. Branch backup only; integration belongs to the final collection task.
