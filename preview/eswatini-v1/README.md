# Eswatini v1 — Lutindzi Coil

Open **eswatini-v1.html** directly in Edge/Chrome. The complete interactive model, renderer, maps and actual-source poster are embedded. Drag/touch to rotate; Open/Close lid; Reset view. No server or connection is needed. This is a cosmetic inner collectible, not a custody operation or minted NFT.

## Delivered
- Standalone HTML: **3,669,950 bytes**, below the strict 5,000,000-byte cap.
- `eswatini.glb`: **2,166,720 bytes**, 81 meshes, 50,564 triangles, five materials.
- `eswatini.blend`: packed, editable, named Blender source; `mechanism.blend`: included inherited mechanical baseline.
- Original procedural weave, roughness and binding maps; reproducible authoring/build/test scripts.
- `poster.png` / `poster.jpg`: actual source render, not AI promotional imagery.
- Desktop/mobile closed/open, rear-open and fallback screenshots: actual offline Edge captures.
- `inventory.json` and `delivery-check.json`: exact bytes/SHA-256 identities and archive readback verification. `eswatini-v1-source.zip` includes the explicitly required standalone model, source, maps, viewer and evidence; no dependencies, credentials or Blender backups.

## Concept and visual limits
Research and the pre-model contract are in `design-brief.md`. Eswatini producer Gone Rural describes indigenous lutindzi grass harvested in rocky mountainous areas and dyed at Malkerns. This inspired warm woven panels, twelve raised body courses and twelve concentric lid coils with restrained rust accents. No third-party imagery, exact basket design, royal/sacred symbol or claim of artisan endorsement is used.

This is a **stylized craft-inspired chest**, not photorealism, botanical verification or a replica of a hand-woven basket. Fine weave is a procedural map; larger coils are geometry. The brown edges read as rigid umber framing rather than wrapped grass bindings. Lid coils are nested closed loops, not one continuous spiral; hidden ties and artisan fastening are not modeled. Hardware is an inherited BoxSV family interpretation, not an ethnographic claim. Visual inspection of source/mobile/rear-open renders found the intended palette, woven identity and full silhouette readable with no obvious major detached geometry; visual checks do not replace geometric tests. Small supporting UI text remains compact on mobile. No human per-asset review was required for this batch.

## Verification actually run
- Independent saved-source reopening; all inherited pivot positions preserved exactly; hollow floor ray z=0.2650000155; ten hinge attachment pairs intersect as designed.
- **81 motion poses**, all 30 moving meshes against 51 static meshes, plus latch-versus-lid geometry. Zero unintended surface intersections. Only named mating hinge leaf/barrel and latch knuckle/bridge/pin bearings exempt. All new lid coils are included. This is sampled surface-intersection evidence, not continuous collision, containment or mechanical certification.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7**, below 1e-5. Three packed source images. Real Three GLTFLoader: zero nonfinite vertices, zero degenerate triangles.
- Theme tests check real coil counts, lid ancestry, seam height, ornament height, pivot identity, decoded map dimensions/variation and straw color ordering. Detaching a real saved-source lid coil in memory causes the ancestry assertion to fail; restoring it passes. This is a post-implementation negative control, not test-first TDD.
- Motion tests independently sample 81 staged poses, clamp endpoints and reject invalid asset records: 80-degree latch release, followed by 105-degree lid opening.
- Offline file:// Edge desktop 1440×1080 and touch-emulated mobile 390×844: native controls, drag/touch rotation, open/close, interrupted reset, reduced motion, zero external HTTP requests/errors, no overflow. Open silhouette max absolute projected NDC about 0.892365 (<1). Genuine corrupt embedded GLB reaches parser and displays poster; no-JS poster also checked.
- Tests ran on desktop NVIDIA RTX 4060. Mobile is emulation, **not physical-phone performance**. No FPS, accessibility audit or wallet compatibility claim.

## Real failure and fix
The initial extended test rejected the binding map's red-channel range of 18 against the declared >20 gate (`initial/texture-range-failure.txt`). Doubled binding-only weave contrast, regenerated maps/source/export/poster, and reran the unchanged gate: range **34**; straw range **79**. All source/parity/browser gates then passed. A chained author/build/browser shell command exceeded its 180-second wrapper limit after the extended check; the final browser gate was rerun independently and passed. The optional Codex input lane failed HTTP 401 before edits; Hermes authored and verified all work directly. No credentials were read or changed.

## Reproduce
Prerequisites: Blender 5.2.1; Python with numpy, Pillow and Playwright; installed Edge; Node.js with pinned Three 0.180.0/esbuild 0.25.11. `build.py` uses local node_modules or the sibling Iceland pilot's installed dependencies. An extracted archive can `npm install --no-audit --no-fund` here. Node.js is build tooling only; no blockchain node is used. Three MIT license included.

From this directory:
```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
node tests.mjs
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme_source.py
python verify_browser.py
python verify_extended.py
python package_delivery.py
```
Regeneration overwrites source/render outputs: preserve manual edits separately. Build source and baseline are local to this folder; baseline/viewer/test lineage is Japan/Iceland from base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. Research URLs supply factual inspiration only. No claims of exact byte-identical Blender rebuilds. Inventory excludes itself, delivery-check and ZIP to avoid recursive hashing; ZIP includes inventory and readback checks every member.

Only `preview/eswatini-v1/` is added. No shared kit, existing preview, production docs, mint/vault logic, chain queries, keys, nodes, broadcasts, VPS or deployments touched. Branch backup is not publication or collection integration. Recommended next step: include this asset in the separate final collection-integration card; retain these exact bytes and hashes.
