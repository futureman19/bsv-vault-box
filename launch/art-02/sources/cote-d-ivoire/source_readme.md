# Cote d'Ivoire v1 — Indigo Stripweave

Open `cote-d-ivoire-v1.html` directly in Edge/Chrome, offline. Drag/touch rotates; Open/Close lid and Reset are functional. HTML **3,148,250 bytes**, GLB **1,732,976 bytes**. All runtime assets are embedded. This is cosmetic collectible art, not minted, hosted or a custody transaction.

## Design and provenance
The pre-model design brief cites UNESCO's Ivorian narrow-strip weaving entry (01949). Nine raised lid strips and eight physical joining seams reinterpret that construction in invented indigo/cream/ochre rhythms. No community-specific sacred/status motifs or third-party textile photographs were copied. Walnut-colored shell and warm brass use the Japan pilot's reusable mechanism, retaining its exact pivots. Geometry and 256px maps are procedurally authored, not handwoven textile, scans, ivory or hand sculpture. The brief is the design reference; no prior approved illustration is claimed.

## Verified evidence
- `source-check.json`: independently reopened packed source; hollow floor at z=0.265; 81 poses, all 72 moving meshes versus 191 static meshes and latch versus lid; no unintended surface collisions. Only explicit mating bearings excluded. Ten hinge attachment pairs checked. This is sampled surface evidence, not continuous manufacturing certification.
- `parity-check.json`: source/export bidirectional maximum vertex error 1.712013073529306e-7, below 1e-5.
- `theme-check.json`: nine strips, eight joins, lid ownership, measured relief below 0.20 above lid, original pivot positions, packed-image variation. Detaching a strip was actually rejected as a negative control and restored without saving the mutation.
- `browser-check.json`: actual GLTFLoader, 18,732 triangles, 263 meshes, six materials, zero nonfinite vertices or degenerate triangles. Desktop 1440x1080 and touch-emulated 390x844 mobile over offline file://: rotation, native controls, open/close, interrupted reset, reduced motion, no overflow, no external requests/errors. Full-open projection maximum about 0.8924. Real corrupt GLB parser failure shows poster. Mobile is desktop RTX 4060 emulation, not physical-phone performance.
- `extended-check.json`: runtime strip ancestry, decoded base-color and green-channel roughness variation; real no-JavaScript poster fallback and nonblack source poster.
- `motion-output.txt`: endpoint/clamping and staged release tests, plus invalid-asset rejection.
- `inventory.json` and `delivery-check.json`: exact payload SHA-256/bytes, explicit required artifacts and ZIP readback.

## Real failure and fix
Initial three-segment bevels produced HTML **6,031,439 bytes**, GLB **3,896,600 bytes**, failing the unchanged 5,000,000-byte assertion (`initial/size-failure.txt`). Single-segment microbevels on box/panel prisms retained the silhouette and reduced the final payload; all source/export/browser gates were then rerun. Optional Codex lane failed with HTTP 401 before edits; Hermes implemented and verified directly. Its diagnostic log is retained; credentials were not modified. Shared pilot dependencies were absent, so the unchanged pinned package manifest was installed locally inside this folder only.

## Visual limits
Actual source and mobile renders were inspected. The wide chest and indigo/cream stripes read clearly; ochre is restrained. Cloth panels remain rigid, slat-like relief rather than soft cloth simulation; fine lid lines alias at mobile scale. Indigo looks somewhat denim-like under studio lighting. Dark seam is conspicuous, and inherited hardware is stylized. No photorealism, cultural-authenticity certification, exact traditional-pattern reproduction or physical-phone performance is claimed. User waived individual review until the collection exists; no visual approval is implied.

## Files / reproduce
Editable `cote-d-ivoire.blend`, exported `cote-d-ivoire.glb`, compact `maps/`, actual source-render `poster.png`/JPEG, standalone HTML, desktop/mobile captures and safe source ZIP. `mechanism.blend` is the included read-only lineage copy. Three.js MIT license included.

Requires Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node.js and pinned npm dependencies. Build-time dependencies are not viewer dependencies. Run in this folder:
1. `npm ci --ignore-scripts --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
5. `node --test tests.mjs`; `python build.py`
6. `python verify_browser.py`; `python verify_extended.py`
7. `python package_delivery.py`

Authoring overwrites source/export/poster; save manual edits separately. No sibling preview, shared base kit, production, chain or server changed. Branch backup only; integration belongs to the separate final collection card.
