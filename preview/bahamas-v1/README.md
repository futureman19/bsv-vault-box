# Bahamas v1 — Pink Sands & Blue Hole

Open **bahamas-v1.html** directly in Edge/Chrome. Entire runtime, model, maps and actual-source poster are embedded: **2,240,611 HTML bytes**, **1,114,028 GLB bytes**. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion is supported. No server/network/wallet required.

## Design and provenance
A wide pale limestone-inspired box with satin brass hardware, pink shell-sand banks, turquoise enamel-like shallows and a dark blue-hole inset. Two different Bahamian landscapes are combined, not mapped: Harbour Island pink sands and Long Island's Dean's Blue Hole. Sources and pre-model visual contract are in `design-brief.md`. All geometry/maps are procedural; no third-party photographs, scans, cultural patterns or AI posters are embedded. This is one inner collectible, not an outer custody container.

`bahamas.blend` is the packed editable Blender source; `bahamas.glb` is the portable export. `mechanism.blend`, viewer and mechanical checks derive from the existing Japan pilot; the shared vault kit and other previews were not modified. `poster.png` and its embedded JPEG are actual Blender renders. Three.js MIT license included. `setup.py` is the one-time scaffold history (requires sibling Japan); ordinary regeneration uses the self-contained `author.py` instead and must not rerun setup over subsequent edits.

## Verified gates
- Source independently reopened: 21 moving and 39 static meshes, **81 staged motion poses**, zero unintended surface intersections. Every new lid ornament included; latch-versus-lid checked. Only explicit mating hinge leaf/barrel and latch bearing contacts excluded. Ten rear attachment overlaps and hollow floor ray z=0.2650000155 pass. Sampled surface tests are not continuous collision/manufacturing certification.
- Unchanged mechanical pivot matrices against the included baseline; 80-degree latch release before 105-degree lid opening. Unit tests also reject missing lid/nonfinite/empty geometry.
- Saved-source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. Three packed source maps verified.
- Actual browser GLTFLoader: **15,172 triangles, 60 meshes, 7 materials**, zero degenerate or nonfinite geometry. Decoded base-color ranges 50/50 and roughness green-channel range 83; maps 256×256.
- Five lid-borne landscape meshes, two sand banks and two blue-hole components. Downward rays hit pink shore, turquoise lagoon and dark center separately. Intentional in-memory detached-ornament negative control is rejected, then restored; this is post-implementation regression evidence, not test-first TDD.
- Edge offline `file://`: 1440×1080 desktop and 390×844 touch-emulated mobile. Native controls, pointer/touch drag, open/close, reset during movement, reduced motion, no horizontal overflow, no external HTTP requests or JS errors. Full-open maximum absolute projected NDC 0.892365. Actual corrupt GLB parser failure shows poster and disables controls; no-JS poster separately tested.
- Actual source/poster and mobile closed/desktop open screenshots visually inspected. Open interior/latch/hinges readable and no obvious clipping. Emulation ran on RTX 4060; **not physical-phone performance testing**.
- `inventory.json` gives exact byte lengths/SHA-256; `delivery-check.json` verifies explicit archive requirements and every archived file on ZIP readback. `.gitattributes` preserves bytes across Git checkout. No self-referential ZIP/inventory hashing.

## Honest visual limits / brief deviations
Water is stylized opaque enamel, not optical depth or a water simulation. The blue center reads as a small dark patch on mobile and is lighter in the Blender poster because of lighting; not a photoreal sinkhole. Pink sand is pale raised relief, not individual grains, and the cream body has restrained procedural speckle rather than scanned limestone. The planned long beach crescent became an irregular elongated bank; the smaller cay is retained. The prominent teal seam and inherited long clasp are family mechanical language, not geographic details. Rear/interior are invented. Source Cycles poster has some sampling noise; no claim of photographic equivalence or per-asset human art approval.

## Real failure and recovery
The supplied shared node_modules directory was empty, so the first compiler invocation failed with MODULE_NOT_FOUND for esbuild; an early browser attempt consequently failed because HTML did not yet exist (`initial/missing-html-browser-output.txt`). Installed the declared dependencies locally in this new directory, then reran build and all acceptance gates successfully. No acceptance thresholds were weakened. Missing-tool setup recovery is distinct from an art defect. Negative controls (detached ornament, corrupt GLB, invalid asset contracts) prove rejection behavior.

## Reproduce
Python with Pillow/numpy/Playwright, installed Edge, Blender 5.2.1, Node with package dependencies. No blockchain software needed. `npm ci --ignore-scripts --no-audit --no-fund` in this folder restores local dependencies; only build-time dependencies, never runtime requests.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
5. `node --test tests.mjs`; `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Regeneration overwrites generated source/export/poster. Recompute evidence and inventory after any change. Source ZIP excludes node_modules, caches and .blend1. No production edits, deployment, mint, funds, chain query, key access or merge. Branch backup only; final collection integration is a separate card.
