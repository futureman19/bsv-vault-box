# Burkina Faso v1 — Earthen Courtyard

Open **burkina-faso-v1.html** directly in Edge/Chrome. Everything needed at runtime is embedded: model, maps, Three.js and actual-source poster. Drag/touch to rotate; Open/Close lid; Reset view. Cosmetic movement only, not a custody or blockchain operation.

## Delivered
- Offline HTML: **2,905,568 bytes** (strictly below 5,000,000).
- `burkina-faso.glb`: **1,622,452 bytes**.
- `burkina-faso.blend`: packed editable Blender source; `mechanism.blend`: included inherited mechanics baseline.
- Three original 256×256 earth color/roughness/normal maps; source-render PNG/JPEG poster; desktop/mobile closed/open, rear-open and fallback screenshots.
- Reproducible author/build/check scripts, exact SHA-256 inventory and source ZIP with verified inventory/readback.

## Design and provenance
Research and measurable contract were written before modeling in `design-brief.md`. UNESCO/ICOMOS accounts of Tiébélé inform warm earth, low buildings and enclosed courtyards. Three low architectural volumes and connected enclosure sit on the moving lid. Decorative lines are newly invented framing, **not copied or authenticated Kasena symbols**. This is not a Royal Court replica, culturally endorsed artifact, or representation of every Burkina Faso tradition. No third-party photographs, scans or AI promotional substitutes are used.

Mechanics, hollow liner, viewer and verification lineage: Japan pilot from repository base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`, ultimately Iceland. Japan's tree, granite/moss terrain, cedar skins and finger joints are not carried into this design. Three.js 0.180.0 MIT license included; esbuild 0.25.11 is build-only.

## Verified gates
- Independent saved-source reopening; hollow interior floor at z=0.2650000155; ten intersecting hinge-attachment pairs.
- **81 poses**, all **36 moving / 63 static meshes**, including the entire courtyard; moving-vs-static and latch-vs-lid BVH surface-intersection sampling: **zero unintended intersections**. Only explicitly documented mating bearings exempt. Not continuous collision or engineering certification.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. This is geometry parity, not byte-identical re-export or complete shader equivalence.
- Source theme: exact retained lid pivot, 3 architectural volumes, 20 lid-parented ornament parts, bounded footprint/heights, narrow seam, packed portable maps, no foreign-theme meshes.
- Actual GLTFLoader checks finite vertices, triangle areas, bounds; decoded maps have real variation. Offline `file://` Edge at 1440×1080 desktop and 390×844 touch-emulated mobile: native controls, drag/touch rotation, open/close, interrupted reset, reduced motion, full-open framing, no horizontal overflow, external HTTP requests or runtime errors.
- Corrupt actual embedded GLB input reaches the parser and activates poster fallback; no-JS poster also verified. Invalid-asset unit controls throw. Assertions are enforced, not placeholders. No model/build acceptance failure occurred in the initial positive runs; deliberate invalid-input rejection is negative-control evidence, not a fabricated failure-and-fix story. A repeat aggregate command exceeded a 180-second harness timeout; unchanged browser assertions subsequently passed with a larger bounded budget after source checks finished (see `verification-timeout.txt`).
- Optional Codex implementation lane failed authentication before editing (exit 1); no credential changes or accepted Codex code. Hermes authored and independently exercised this delivery.

## Visual verdict and limits
Actual desktop-closed and mobile-open screenshots were visually inspected. The warm-earth courtyard identity, wide box silhouette and small brass fittings are readable, with no obvious silhouette clipping. This remains stylized: regular trim and stretched fine grain can read somewhat wood-like; flat doorway panels do not imply usable interiors; the dark seam is conspicuous; hinge connections are small/ambiguous at mobile size despite geometric attachment checks. No photoreal equivalence or user visual approval is claimed. Mobile is desktop-GPU emulation, **not physical-phone performance**. Ornament naturally hides behind the raised lid from the front; rear-open capture shows it.

## Reproduce
Requires Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge and Node.js. Run from repository root:

```text
python preview/burkina-faso-v1/maps.py
blender --background --factory-startup --python-exit-code 1 --python preview/burkina-faso-v1/author.py
python preview/burkina-faso-v1/build.py
node --test preview/burkina-faso-v1/tests.mjs
blender --background --factory-startup --python-exit-code 1 --python preview/burkina-faso-v1/verify_source.py
blender --background --factory-startup --python-exit-code 1 --python preview/burkina-faso-v1/verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python preview/burkina-faso-v1/verify_theme.py
python preview/burkina-faso-v1/verify_browser.py
python preview/burkina-faso-v1/verify_extended.py
python preview/burkina-faso-v1/package_delivery.py
```

Build uses local `node_modules`, falling back to sibling `iceland-pilot/node_modules`. For standalone extraction install package.json dependencies locally first. Authoring uses included mechanism/maps only. Regeneration overwrites generated artifacts; preserve manual edits separately. Packaging excludes caches, backups and lane diagnostics; inventory excludes itself and packaging envelopes to avoid recursive hashes. The ZIP includes the explicit required file set and each member is read back and hashed.

All changes are additive under this preview directory. No production deployment, website edit, mint, keys, chain queries, funds or VPS access. Feature branch backup only; integration is separate. The planned collection remains 201 equally one-of-one designs; this file is neither minted nor hosted.
