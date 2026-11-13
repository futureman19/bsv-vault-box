# Fiji v1 — Masi & Lagoon

Open **fiji-v1.html** directly in Edge/Chrome. All 3D runtime, maps, model and actual-source fallback poster are embedded. This is a cosmetic inner collectible, not an outer custody container, minted asset, public deployment or chain proof.

## Delivered
- Offline HTML: **2,662,852 bytes** (strict ceiling 5,000,000).
- Portable `fiji.glb`: **1,387,968 bytes**.
- Editable packed `fiji.blend`, inherited `mechanism.blend`, procedural `maps/`, reproducible author/build/verification scripts.
- Actual source `poster.png`/JPEG and desktop/mobile closed/open, rear-open and fallback browser captures.
- JSON acceptance reports, raw logs, exact SHA-256 inventory, read-back-verified source ZIP.

## What passed
Hermes ran the actual toolchain, not a delegated self-report. `python verify_all.py` rebuilds the embedded HTML and runs the motion, source, parity, theme, browser and extended checks without regenerating art.

- Actual GLTFLoader: 15,682 triangles, 63 meshes, 7 materials; zero nonfinite vertices or degenerate triangles. Base-color map ranges 41 and 181; glTF GREEN roughness range 58.
- Independently reopened source: 24 moving and 39 static meshes, 81 sampled staged poses, no unintended surface intersections. Latch versus moving lid is also sampled. Only original named hinge/hasp mating bearing contacts exempted. Ten hinge attachment pairs and hollow interior floor ray (z=0.265) pass. This is sampled surface intersection, not continuous collision or manufacturing certification.
- Saved source versus independently imported GLB: maximum nearest-vertex distance both ways **1.712013073529306e-7**, below 1e-5. Three packed images. Original pivot matrix maximum difference **0.0** against included mechanism.
- Lagoon vertices lie inside the actual pale rim polygon; all eight landscape parts belong to the lid. Three green islands are visibly separate. Deliberately detaching an island makes the theme assertion fail; restored parent passes. This negative control was written after modeling, not claimed as test-first history. Motion tests also reject missing lid/nonfinite/empty assets.
- Offline file:// Edge at desktop 1440x1080 and touch-emulated mobile 390x844: native controls, drag/touch rotation, open/close, reset mid-motion, reduced motion, full-open framing, no external HTTP requests, no runtime errors or horizontal overflow. Actual corrupted GLB input triggers parser error/poster fallback; JavaScript-disabled poster passes. Mobile is emulation on desktop NVIDIA RTX 4060, not physical-phone performance.
- Real poster pixel test rejects blank rendering. Visual inspection of source and normal mobile screenshot found the full silhouette, turquoise lagoon, all three islands, patterned body and controls readable and unclipped.

## Honest visual limits and brief deviation
This is a stylized procedural collectible, not photorealistic, a geographic scale model, a museum-pattern reproduction or an authentic masi craft object. The invented rectilinear decoration refers to material/color traditions, not sacred pattern ownership. Fibrous grain is subtle at mobile size; corners are visibly panelized, not seamless cloth. Island mounds are simplified and faceted, the opaque lagoon reads as enamel rather than deep water, the inherited latch is busy, and the actual source render has sampling grain. Rear/interior/hardware are family extrapolations.

The prewritten reef nominal X bound was +/-1.5. The deliberately irregular perimeter reaches **+1.51548**, an approximately .016-unit deviation; it remains inside the 3.72-wide lid. The explicit structural containment gate is +/-1.6, with actual bounds recorded, not a claim that the nominal brief was exact. No visual equivalence or human approval is implied. User waived per-asset human review for this collection batch.

## Failures retained
- Optional Codex lane failed with HTTP 401 refresh/auth errors and accepted no changes; Hermes implemented directly. `codex-lane.log` preserves the failure, without credentials.
- Initial shell `node --test` invocation returned `stdin is not a tty`; `initial-motion-shell-failure.txt` retained. Using the actual Windows Node executable fixed the shell-launch issue; no test was relaxed.
- Detached-island negative control and invalid-asset tests deliberately fail internally before checking restored/valid state. No art/collision failure occurred in the final authoring pass.

## Reproduce
Dependencies: Blender 5.2.1; Python with Pillow, numpy and Playwright; installed Edge; Node.js; pinned Three.js/esbuild package.json. Shared node_modules was empty, so dependencies were installed only in this folder. No dependency directory is archived.

```text
npm ci --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python verify_all.py
python package_delivery.py
```
Set BLENDER environment variable for another Blender executable. `verify_all.py` selects the native Windows Node binary to avoid the local shell shim. Regeneration overwrites source/model/poster: preserve manual edits separately. The saved source is packed; the source-build needs installed tools, but the shipped HTML has no external dependencies. Raw source render deliberately uses bounded threads/samples with denoising off.

## Provenance and rights
Research and pre-model targets are in design-brief.md. No external imagery is embedded. Procedural textures/geometry are authored here; mechanism, viewer and collision/parity harness lineage is the Japan Cedar v1 pilot at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8 (itself based on Iceland). Shared vault kit and other preview files unchanged. Three.js MIT license included. Hashes establish bytes, not ownership, issuer authenticity or storage availability. No chain/node/key/mint/custody code or VPS access. Only this new preview directory is delivered on its backup art branch; integration is a separate card.
