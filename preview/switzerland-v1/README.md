# Switzerland v1 — Alpine Walnut & Matterhorn

Open **switzerland-v1.html** directly in Edge/Chrome. Complete offline interactive model, textures, runtime and actual-source poster are embedded. HTML **3,950,712 bytes**; GLB **2,391,704 bytes**. No wallet, chain, mint, node service, deployment or custody action. The reversible lid animation is cosmetic.

## Design and visual outcome
Research-backed brief was written before modeling. This original interpretation combines dark walnut-colored joinery, quiet brass and a faceted snow/rock horn on the lid. It is not a mountain survey, traditional Swiss walnut craft attribution, photoreal reconstruction or user-approved art. Wood geometry and mechanics inherit the Japan pilot; its tree/foliage were removed and an original Alpine terrain mesh added. The mountain peak is offset +X/+Y and rises to z=2.9400; the lid top is approximately z=1.978. Base/normal/roughness maps are procedural, not scanned or copied third-party imagery.

Actual mobile screenshot inspection found legible snow/rock separation, fully framed box and mountain, and no major defect. Limitations: deliberately low-poly horn, rounded foothills, regular fine grain, lighter lid than body, long inherited latch and small secondary copy. Source poster uses 24 Cycles samples without denoising and retains some noise. The mountain is naturally hidden behind the open lid in the front view; `desktop-open-rear.png` documents its reverse side. No claim of exact Matterhorn profile.

Brief dimensions were approximate: inherited wooden wall courses run z=.10–1.56, with lid z≈1.678–1.978 and feet extending below zero. Thus the stated approximate 1.9 height is the box/lid envelope rather than the wood wall alone; retained side finger ends extend depth to approximately 2.49. No mechanical pivot was moved.

## Verified
- `run_checks.py`: all seven commands exit 0, including two motion/invalid-asset tests. Real missing/empty/nonfinite asset negative controls reject invalid input.
- `source-check.json`: independent saved-source reopen, **81** sampled staged poses, **32 moving / 99 static meshes**, **zero unintended intersections**. Ten hinge attachment pairs intersect; hollow floor ray z=0.26500001549720764. Only named mating hinge/latch bearing contacts excluded. This is sampled surface checking, not continuous or manufacturing certification.
- `parity-check.json`: bidirectional source/export nearest-vertex error **1.712013073529306e-7**, below 1e-5. Five packed source images. Not a byte-identical re-export claim.
- `theme-check.json`: all four terrain meshes descend from lid, two mountain face materials, contained footprint/height, exact inherited pivot matrices.
- Real GLTFLoader: **27,818 triangles**, **132 meshes**, **7 materials**, zero nonfinite vertices or degenerate triangles.
- Offline `file://` Edge: 1440×1080 desktop and 390×844 touch emulation, real drag/touch rotation, open/close, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests, no runtime errors. Full-open max absolute projected NDC ≈0.892365. Actual corrupt GLB reaches parser and shows poster; no-JS poster also verified.
- Decoded maps: base-color range up to 143, roughness GREEN range 53, normal RED range 25; dimensions at most 512. Map variation is not a realism metric.
- `delivery-check.json` and `inventory.json`: exact bytes/SHA-256 and ZIP readback of explicit required deliverables. Local `* -text` preserves Windows checkout bytes.

Mobile evidence is desktop RTX 4060 emulation, **not physical-phone performance**. Technical gates do not constitute human art approval.

## Real failures and bounded correction
Optional Codex lane failed immediately with expired-auth 401, accepted no changes; Hermes authored and verified directly. `codex-lane.log` preserves it. Initial build failed because the requested inherited node_modules location was empty; `initial/verification-log.txt` retains MODULE_NOT_FOUND. Installing the exact existing versions (Three 0.180.0/esbuild 0.25.11) locally in this folder fixed it without changing any other preview. Initial poster was too pale; `initial/poster.png` retains it. One material correction darkened walnut albedo and rock, then regenerated source/render/GLB and reran all checks. No thresholds were relaxed.

## Files / reproduction
Editable `switzerland.blend`; `mechanism.blend` trimmed inherited mechanical baseline; standalone `switzerland.glb`; `maps/`; actual `poster.png`/JPEG; desktop/mobile closed/open/fallback/no-JS evidence; scripts, checks, raw logs and source ZIP. Three MIT license included. `lane-prompt.txt` is historical failed-lane input, not a runtime dependency.

From this directory with Python (Pillow/numpy/playwright), Blender 5.2.1, Node and installed Edge:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_checks.py` (Blender executable is the explicit local Windows path; change it for another host)
5. `python render_review.py`
6. `python package_delivery.py`

Regeneration overwrites authored outputs; retain manual edits separately. Local source needs the included mechanism, not sibling art; build checks local node_modules first and the inherited dependency location second. The offline HTML itself requires no build dependencies or network. ZIP excludes dependencies/backups. No merge or hosting is performed; the asset branch is backed up for the separate final collection integration card.
