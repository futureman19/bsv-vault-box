# Paraguay v1 — Ñandutí Sunlace

Open **paraguay-v1.html** in Edge/Chrome directly from disk. All runtime code, GLB, maps and the actual-source poster are embedded. Drag/touch to rotate; Open/Close lid; Reset view. Cosmetic animation only, not an on-chain opening.

## Design and visual verdict
The prewritten `design-brief.md` cites Paraguayan ñandutí's radial needle-lace structure. Five invented ivory/ochre rosettes sit on wine-red timber. These are modeled openwork tubes with exposed backing between them, not printed lace or holes through the lid. No craft photographs or third-party pattern were copied. This is procedural Blender art, not artisan-made textile, scanned wood, or a historically faithful pattern.

Actual source and mobile/desktop screenshots were visually inspected. The radial motif and wine/brass palette are legible; the full open chest fits and its cavity and hinges remain visible. **Limitations:** the wine finish reads dusty pink in strong studio light, the fine loops crowd at mobile size, inherited clasp and stone feet are chunky, and the dark seam is prominent. The poster retains mild render noise (24 samples, denoising off). The small loops are rigid decoration, not simulated woven thread. Not photorealistic; no claim of visual equivalence to a supplied illustration (none was supplied). The open front view naturally hides the top ornament behind the lid.

The brief's approximate body height refers to the overall closed timber stack; inherited body walls are lower. The inherited body width and lid footprint remain about 3.72 × 2.38, with projecting hardware and side courses outside that footprint. Rear/interior/hardware details are family extrapolations. Ornament relief reaches about 0.053 above the slab; first ring threads intersect its surface slightly to avoid hovering.

## Verified
- `build-output.txt` records exact HTML_BYTES / GLB_BYTES; HTML is strictly below 5,000,000 bytes. `delivery-check.json` and `inventory.json` identify all final payloads by bytes and SHA-256.
- Actual Three.js GLTFLoader: **59,804 triangles, 279 meshes, 7 materials**, no nonfinite vertices or degenerate triangles.
- Independently reopened source: **81 motion samples**, 180 moving meshes against 99 static meshes plus latch against lid; zero unintended sampled surface intersections. Only named inherited bearing contacts exempt. Hollow floor ray z=0.265; ten hinge attachment intersections. Not a continuous collision or manufacturing proof.
- Saved source ↔ GLB nearest-vertex error **1.712013073529306e-7**, below 1e-5. Four packed images. Geometry parity is not a pixel-identical Blender/browser shading claim.
- Five rosettes, 152 ornament meshes, all under moving lid. Central rosette has 24 spokes, smaller ones 16 each. Independent rays through all five centers reach the backing; unchanged pivots compared to reopened trimmed mechanism. Detached-ornament negative control is rejected.
- Actual decoded portable maps: nonzero color variation; roughness is tested in glTF's green channel (range 53), not red. Largest map 512 × 512.
- Offline file:// Edge: desktop 1440×1080 and mobile 390×844 touch emulation; real open/close controls, drag/touch rotation, interrupted reset, reduced motion, full-open projection within view, no external requests, no runtime errors or horizontal overflow. Corrupt embedded bytes reach GLTFLoader and trigger poster fallback. No-JS poster also tested. This ran on an RTX 4060, **not physical phone hardware or an FPS benchmark**.
- Motion unit tests exercise staged 80° latch release before 105° lid lift, endpoints, and invalid-asset rejection. Packaging asserts required files and all archive entry hashes on readback. Folder-local Git attributes preserve payload bytes.

## Real failures and fixes
`initial-theme-output.txt` retains the failed source-height assertion: ornament lowest point was 1.995, above the slab. Lowering the base from 2.005 to 1.986 put the lowest thread at 1.976; the unchanged gate then passed. Source, GLB and poster were regenerated together. This is a real failure/fix, not fabricated TDD history.
The prescribed shared dependency directory existed but was empty; first build failed with missing esbuild. Dependencies were installed locally in this new directory using the inherited exact versions (Three 0.180.0 / esbuild 0.25.11). No shared directory was populated or edited. The optional Codex lane exited 1 with authentication failure; no Codex changes were accepted, credentials were not changed, and Hermes implemented and ran all gates directly. `lane-output.txt` retains this failure.

## Files and reproduce
`paraguay.blend` is editable packed source, `paraguay.glb` standalone model; `mechanism.blend` is the unchanged trimmed Japan mechanical starting point. `maps/` contains generated color/roughness/end-grain/stone images. `poster.png`/`.jpg` are real renders. Desktop/mobile PNGs are actual browser captures. `paraguay-v1-source.zip` includes source, model, viewer, evidence and inventory, excluding installed dependencies and backups. Three.js MIT license included.

From this folder with Python (Pillow, numpy, Playwright), Blender 5.2.1, Node.js and Edge installed:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. `python build.py` and `node --test tests.mjs`
5. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
6. `python verify_browser.py` and `python verify_extended.py`
7. `python package_delivery.py`

Canonical authoring needs only the included mechanism and maps; build uses local node_modules, falling back to sibling Iceland dependencies only if installed. Regeneration replaces art and poster; retain separate copies of manual edits. Exact inventories must be regenerated after any changes. The archive is self-contained source but needs the stated development dependencies to rebuild; the HTML needs no installation/server/network.

## Scope
Only `preview/paraguay-v1/` was added. No production site, shared kit, wallet, keys, blockchain node, broadcasts, minting, chain queries, VPS or deployment. Not hosted, minted, signed, on-chain or user visually approved. Branch backup is not publication to the production site. The explicit batch directive waives per-asset human review; integration and full-collection review remain downstream. Collection scope remains 201 equally one-of-one designs.
