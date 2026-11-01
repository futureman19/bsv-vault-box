# Iceland — Corner Ice v9 (local refinement candidate)

Open `iceland-corner-ice-v9.html` directly. Complete offline preview: **4,187,412 bytes**; GLB: **2,575,312 bytes**. No server, remote textures, wallet, minting, chain operations, deployment or funds. Source is scripted Blender art, not a photographic scan.

## Request-by-request result

1. **Far-right glacier: PASS.** Placement is defined in the actual hero-camera projection, not assumed from a world-space “back-right” label. The glacier center is at 0.914647 of the projected left-to-right corner span. This camera makes Blender +X/−Y the far-right corner. Glacier footprint is entirely on the lid, with minimum outer-edge clearance 0.137281 model units. The entire new continuous river joins its base and the original left-edge cascade; the original inset was removed by rebuilding only the slab to its previous outer dimensions/bevel. A ray verifies old-channel location is solid obsidian. All three motifs share the lid pivot.
2. **Glassy ice: TECHNICAL PASS / VISUAL PARTIAL.** Actual exported glTF and actual offline Three GLTFLoader decode transmission 0.97, roughness 0.035, IOR 1.31, volume thickness 0.18, pale-blue absorption (distance about 0.625). Closed ice volume, blue crevasses, smoothed facet normals and specular highlights improve its icy treatment. Nevertheless, independent screenshot inspection at desktop, mobile and macro still sees predominantly solid-looking ice with localized translucent edges, not unmistakable see-through glacial depth. This acceptance point is **not fully achieved**. Two focused correction rounds were used; no unbounded redesign followed.
3. **Darker basalt: PASS.** The retained shared grain map is multiplied by 0.28 in linear color. Geometry, chipped recesses, normal/roughness maps and green moss remain. Lighting, renderer exposure and black lid gloss are not darkened. Independent vision finds charcoal stone with readable fractures; very dark recesses and mobile fine grain remain less visible.
4. **Gold corner wraps: PASS at model/desktop scale; mobile fine detail partial.** All four existing shaped top caps grow inward, with correspondingly wider side wraps and eight added raised top fasteners. These are protective plates: the **front fittings are decorative guards, not extra pivots**. The original two real rear hinge assemblies retain their coaxial bearings, moving leaves and body attachment bridges. The visible plates are brass/gold, not orange blocks. Not all four corners can be visible simultaneously from one opaque-box view; rear screenshots expose the hidden pair.

Overall: a working, under-budget review candidate with **one unresolved visual acceptance item (convincing glass depth)**. Do not describe all four art requests as fully passed or photorealistic.

## Scope and portability

The wide body proportions, hollow liner, chipped basalt meshes, moss, latch choreography and original mechanical pivots remain. Native touch QA exposed Edge delivering touch pointer events without a synthesized button click; v9 adds movement-guarded touch activation and suppresses duplicate compatibility clicks, while retaining mouse/keyboard click behavior. `native-touch-first-failure.txt` retains the failed control; final native taps pass. `features-check.json` compares 109 named stone/moss/interior/hinge/latch raw source records exactly against packed v8. `motion.mjs` is byte-identical to the previous approved module. New work is confined to this directory; prior source/media are immutable.

Blender 5.2's exporter omitted the source's multiply factor and disconnected glTF thickness setting. The author script therefore serializes those **exact saved-source node inputs** into the exported material JSON, retaining the GLB binary geometry/image buffer. Independent source/export factor checks and GLTFLoader checks verify the result. They are not browser-only material substitutions. The Three viewer disables opaque shadow-map casting/receiving for the glacier specifically, because its ordinary shadow map does not model transparent ice. This rendering approximation is disclosed; all lights/camera/exposure match v8 comparisons.

## Evidence

- `contract-red.txt`: initial v8 fails new transmission/roughness/volume/darkening/rivet requirements. `contract-green.txt`: final portable-material contract passes.
- `features-check.json`: source material parity, connected river endpoints, one river component, old-channel closure, four top plus eight side wrap meshes, unchanged source records and edge clearance.
- `source-check.json`, `hinge-attachment-check.json`: independent saved-source reopen; **81 sampled poses, zero collisions**, same narrow intentional-bearing exclusions as v8, real mount overlaps and hollow-floor ray. This is sampled clearance, not continuous rigid-body simulation.
- `parity-check.json`: independent Blender GLB reimport; bidirectional world-vertex error below 1e-5 (observed approximately 1.72e-7).
- `browser-check.json`: actual **offline file:// Edge**, desktop and 390×844 touch emulation; loaded finite/nondegenerate geometry, native touch rotation/taps, open/close, reset during motion, reduced motion, no overflow, zero HTTP(S) requests or uncaught errors. Corrupt embedded GLB exercises real parser fallback. `no-js.png` verifies poster-only access. Mobile testing uses the desktop RTX 4060, **not physical-phone performance evidence**.
- `v9-runtime-check.json`: actual decoded material factors/volume, portable decoded maps and numerical projected-corner proof.
- `desktop-closed.png`, `desktop-open.png`, `mobile-closed.png`, `mobile-open.png`: unannotated real viewer captures.
- `v9-glacier-macro.png`: intentionally cropped macro of actual browser rendering; `v9-rear.png` exposes rear fittings.
- `before-after-matched.jpg`, `before-after-detail.jpg`, `before-after-rear.jpg`: same-camera, same-lighting v8/v9 comparisons. Only comparisons are annotated.
- `reference-comparison.jpg`: primary AI promotional art versus actual model at equal image-space object width; not a claim of photoreal parity. The user's far-right instruction supersedes the reference's more central glacier.
- `poster.png` / `poster.jpg`: Blender-rendered fallback, not evidence of browser glass quality.
- `initial-correction.png`, `correction1.png`: retained earlier attempts; final screenshots are named desktop/mobile/v9.

## Source and regeneration

`iceland.blend` is packed and editable. `approved-v8.blend` is its immutable packed input. `iceland.glb` is the final portable asset. The source ZIP includes these, generator, viewer, tests, local evidence and Three license; excludes node_modules, secrets and Blender backup files. Exact SHA-256/byte inventory and ZIP/delivery readback appear in `inventory.json` / `delivery-check.json` (inventory excludes itself to avoid self-reference).

Requirements: Blender 5.2.1; Node dependencies from `npm ci`; Python with Pillow/Playwright and installed Edge. Run Blender with `--background --factory-startup --python-exit-code 1 --python author.py`; then `python build.py`, `python test_contract.py`, Blender `verify_features.py`, `verify_source.py`, `verify_parity.py`, and Python `verify_browser.py`, `verify_views.py`. Source generation overwrites this candidate's artifacts. Comparison/preservation tests additionally require sibling v8 and the primary reference at their documented workspace paths. Do not regenerate earlier versions. Packaging uses `python package_delivery.py` after final evidence/README.
