# Slovakia v1 — Čičmany / Lime & Timber

Open `slovakia-v1.html` offline in Edge/Chrome. Complete embedded runtime, GLB, textures and actual-source poster; drag/touch rotation, Open/Close and Reset. Cosmetic collectible only, not minted, hosted or connected to custody.

HTML **4,138,711 bytes** (see build-output.txt for authoritative rebuilt bytes); GLB **2,485,936 bytes**. Source is `slovakia.blend`; procedural maps and scripts included. The frozen sourced design brief precedes modeling. This is original geometric abstraction of Čičmany white-on-dark timber craft, not a copy of a particular house or documented embroidery design.

## Verified
Saved source reopened independently: 81 poses, all 88 moving and 207 static meshes, zero unintended intersections; explicit inherited mating bearings only exempt. Hollow floor ray and ten hinge attachment pairs pass. Pivots match included mechanism within 1e-7. Source/export maximum vertex error 1.712013073529306e-7 (<1e-5). Fifteen lid diamonds/60 strokes seated on the lid, 108 facade strokes, five packed maps. Detached ornament mutation is rejected. Actual GLTFLoader: 21,244 triangles, 295 meshes, 6 materials, zero degenerate/nonfinite vertices. Decoded color, roughness (green) and normal (green) variation checked.

Offline file:// Edge desktop and 390x844 touch emulation: native open/close, drag, interrupted reset, reduced motion, no overflow, no external requests or errors. Full-open silhouette fits (max NDC ~0.8924). Actual corrupt GLB parser fallback and no-JS poster pass. RTX4060 desktop GPU; NOT real-phone performance. Motion endpoint tests and three malformed geometry negative controls pass. SHA-256 inventory and ZIP contents are independently read back; exact bytes preserved in Git via folder-local attributes.

## Visual verdict and limitations
Actual source poster plus desktop-open and mobile-closed browser images inspected. Readable timber/white geometric motifs and brass, full silhouette, hollow interior and clear controls. Timber appears medium-brown under studio lighting despite dark base maps. Lid diamonds look like applied raised square frames in perspective, not subtle inlay. Seam is conspicuous; stone feet and hardware are stylized. Source render retains sampling noise. These are disclosed stylistic limits, not photoreal equivalence, ethnographic accuracy, continuous collision proof or manufacturing certification.

## Real failures retained
`initial/build-missing-deps.txt`: prescribed main-checkout dependencies were empty; installed pinned dependencies locally in this new directory. `initial/size-failure.txt`: first HTML 7,360,692 bytes failed strict cap. Changed authored cube microbevels from three segments to one, retaining all motifs; final full gates rerun. `initial/normal-channel-failure.txt`: initial normal probe sampled constant red; corrected to varying green, retaining nonzero threshold. Codex optional lane failed 401 refresh before edits; no accepted Codex changes. Direct Hermes implementation and verification.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/playwright, installed Edge, Node.js and npm. From this folder: `npm ci --no-audit --no-fund`; `python maps.py`; Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`; Node `tests.mjs`; Blender same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`; `python verify_browser.py`; `python verify_extended.py`; `python package_delivery.py`. Use native node.exe on Windows if shell shim reports non-TTY. Regeneration overwrites source, export, poster and checks: rerun all before repackaging. No sibling source required; build falls back to sibling compiler dependencies only if local dependencies absent.

Mechanism/viewer/test lineage is repository Japan pilot at base ff5d78f1e0d486af5c882c184fc08049996ebdc8; no Japan tree/terrain retained. Read-only shared vault kit unchanged. Three 0.180.0 MIT license included. Maps and geometry procedural, no photographic scans or third-party images embedded. All work additive in this folder. Branch backup only; integration is separate.
