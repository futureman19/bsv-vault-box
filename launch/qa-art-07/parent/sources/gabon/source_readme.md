# Gabon v1 — Okoume & Loango

Open `gabon-v1.html` directly in Edge/Chrome. Complete embedded runtime, GLB, maps and actual-source poster; no server or network needed. Drag/touch, Open/Close, Reset and reduced motion are verified. This is cosmetic collectible artwork, not a minted token or custody operation.

HTML **2,658,948 bytes**; GLB **1,433,992 bytes**. Editable `gabon.blend`, included `mechanism.blend`, procedural maps and authoring/verification scripts are provided. The brief predates the recovered model; research informed timber palette and coastal-forest/lagoon identity, not geographic reconstruction. No third-party photographic pixels are embedded.

## Verified
- Fresh independent Blender source reopen: 54 moving meshes versus 39 static meshes across 81 poses; zero unintended surface intersections. Latch-vs-lid checked; only named mating bearings excluded. Ten hinge attachment pairs and hollow interior floor ray pass.
- Source/export nearest vertex error in both directions: 1.712013073529306e-7 units (<1e-5).
- Actual browser GLTFLoader: 15,962 triangles, zero nonfinite vertices/degenerate triangles. Decoded color/roughness map ranges 143/96/53; roughness measured in green channel.
- Theme: 15 canopy meshes in three groups; 38 lid-owned ornament meshes; connected 82-vertex lagoon with 40 unobstructed downward face-center rays; measured ornament bounds, .08 seam height and original mechanism pivots pass.
- Offline file:// Edge desktop 1440x1080 and touch-emulated mobile 390x844: native controls, rotation, interrupted reset, reduced-motion endpoints, open silhouette, no errors/external HTTP requests/overflow. Genuine corrupt embedded GLB fallback and no-JS poster tested.
- Motion test independently asserts all 81 staged poses and rejects three invalid-asset negative controls. All acceptance scripts assert and exit nonzero on violations.
- SHA-256 payload inventory and ZIP readback in delivery-check.json; Git index byte verification separately performed before commit.

## Corrections and limitations
Recovered unfinished prior work after infrastructure crashes. Optional Codex lane failed authentication (401); no Codex changes accepted, no credential-store edits. Hermes completed and independently reran checks.
Visual QA caught inherited “Yakushima okoume” subtitle and a wrong concept-origin description. Both corrected; extended acceptance now checks country copy and accessible canvas label. Higher presentation camera makes the winding lagoon readable on mobile. Geometry was not changed during recovery. Final actual mobile screenshot was visually inspected and passed the brief-led appearance check.

Stylized broadleaf diorama, not photorealism, botanical accuracy, exact Loango geography, artisan-made craft or sustainably sourced physical timber. Water is a shallow ribbon/inlay, trees have simplified crowns, wood is regular procedural grain, and family hardware is prominent. Stone feet and unseen interior are design extrapolations. Sampled surface intersections are not continuous mechanical certification; emulated mobile is not real-phone performance. No supplied primary concept illustration or per-asset human approval is claimed.

## Reproduce
Python with Pillow/numpy/playwright, installed Edge, Blender 5.2.1 and Node.js build tooling (not a blockchain node). `npm install` locally restores exact versions declared in package.json; current build used existing sibling pilot node_modules. Viewer itself requires no dependencies/network. Run from this folder:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Blender command above with `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `node tests.mjs`; `python verify_browser.py`; `python verify_extended.py`.
6. `python package_delivery.py`.
Authoring overwrites generated source/model/poster; preserve manual edits separately. Setup.py records initial extraction lineage and is not required for standalone regeneration. No shared kit or other preview is modified. Three.js license included. Final branch backup only; integration remains a separate task.
