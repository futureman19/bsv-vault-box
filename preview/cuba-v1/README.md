# Cuba v1 — Viñales Karst

Open **cuba-v1.html** directly in Edge/Chrome. Complete offline viewer: **1,822,582 bytes**. Embedded standalone GLB: **765,548 bytes**. Drag/touch rotation, staged Open/Close and Reset; reduced-motion support. Cosmetic inner collectible only, not custody or seal operation. Not minted, hosted or chain-verified.

## Design and provenance
A pale limestone keepsake box holds a red-earth miniature with three green-crowned mogotes. `design-brief.md` was written before authoring and cites UNESCO's Viñales landscape description and a red-earth reference. All geometry and maps are procedurally authored, not scans, sourced photographs or hand sculpture. No supplied concept illustration existed. The inherited Japan mechanism supplies articulation, liner and family brass fittings; its geometry/pivots remain in `mechanism.blend`. The shared vault kit was read only and not changed. Three.js MIT license included.

## Verified results
- Saved `cuba.blend` independently reopened. Hollow floor ray z=0.2650000155. Ten hinge attachment overlap pairs. All 20 moving and 35 static meshes considered at **81 poses**, with **zero unintended sampled surface intersections**; only specifically named concentric hinge/latch bearings excluded. This is not continuous collision proof or manufacturing certification.
- Three hills seated at z=2.023 on the valley plain, parented to lid, heights inside the frozen .45–.83 gate, rock and green crown materials. Pivot matrix difference from independently opened mechanism: **0.0**. Deliberately detaching one hill caused `mogote detached from lid`; restoration passed. This is a postimplementation negative control, not test-first development. No actual modeling/test failure needed correction in this run.
- Source/export nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. All three source maps packed.
- Actual GLTFLoader: **9,044 triangles**, **58 runtime meshes**, **5 materials**, no nonfinite vertices or degenerate triangles. Multi-material hills split into primitive children. Real decoded map ranges: limestone 68, earth 52, roughness green channel 37; all 256×256.
- Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native open/close, drag/touch rotation, interrupted reset, reduced motion, no overflow, no external HTTP(S) requests, no JS errors. Open-view maximum absolute projected coordinate 0.892365 <1. Actual corrupt GLB parser fallback and no-JS poster verified. Mobile emulation is not physical-phone performance.
- `poster.png` rendered from the saved/exported source; alpha and nonblack content checked. Desktop/mobile closed/open and rear-open screenshots are actual browser output. Visual inspection found intact silhouette and attached landscape without obvious clipping. Technical checks do not establish photorealism.
- `delivery-check.json` and `inventory.json`: exact byte/SHA-256 identities and ZIP readback. Directory-local Git attributes preserve bytes through Windows checkout.

## Visual limits
Stylized faceted mogotes, simple olive crowns instead of individually modeled vegetation. The procedural stone has conspicuous diagonal waviness rather than photoreal limestone microstructure. The straight rectangular earth bed and clean brass emphasize collectible design, not a geographic diorama. Green seam is pronounced and the inherited clasp is blocky. Unseen interior/hardware are family extrapolations. No photoreal-equivalence, traditional Cuban craft, surveyed geography or full-device-performance claims.

## Files and reproduction
`cuba.blend` editable packed source; `cuba.glb` portable asset; `maps/` generated images; `author.py`, `maps.py`, `build.py` reproducible author/build steps; `verify_*.py` acceptance; `*-check.json` and `*-output.txt` evidence. `cuba-v1-source.zip` contains explicit required deliverables, scripts, screenshots and inventory, excluding dependencies and Blender backups.

Dependencies: Blender 5.2.1, Python with Pillow/numpy/Playwright and installed Edge; Node with pinned package.json dependencies. Install with `npm install` inside this folder. Build prefers local node_modules and otherwise sibling Iceland toolchain; runtime has no dependencies outside the HTML. The attempted prescribed sibling link found an empty main dependency directory, so dependencies were installed only in this new asset folder.

Run `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Blender on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`. Regeneration overwrites authored outputs; retain manual edits separately. No blockchain nodes, keys, broadcasts, VPS, production directories or shared art were touched. Branch backup only; integration remains a separate task.
