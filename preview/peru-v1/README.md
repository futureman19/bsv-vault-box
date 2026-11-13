# Peru v1 / Andean Stone & Terraces

Open **peru-v1.html** directly in Edge/Chrome: complete offline collectible, 2,243,764 bytes. GLB: 1,097,392 bytes. All runtime assets embedded; no server, wallet, mint, blockchain node, public deployment or remote request. Cosmetic opening is not custody release.

## Art and files
Warm-grey staggered masonry, five green stone terraces and two asymmetric rear crags, brass latch/ring/corners. Research-backed frozen design-brief.md cites UNESCO. This is an invented miniature inspired by Andean terraces, not a scale reconstruction of Machu Picchu or a representation of all Peru. Materials are procedural 256px color/roughness maps, not scans. The source poster is a genuine Blender render, not promotional AI imagery.

`peru.blend` is packed editable source; `peru.glb` is the portable model. `mechanism.blend` is the copied Japan mechanical baseline. Maps, authoring/viewer/test scripts, actual desktop/mobile captures, JSON evidence and exact inventory accompany the source ZIP. Three.js 0.180.0 license included. Reproduction uses local installed packages, not online runtime dependencies.

## Verified
- Real GLTFLoader: 14,100 triangles, 131 meshes, four materials; zero nonfinite vertices and zero degenerate triangles.
- Independent saved-source reopen: 81 poses, all 28 moving meshes versus 103 static meshes, plus latch-versus-lid tests; zero unintended intersections. Only explicitly named concentric bearings exempt. Ten hinge attachment overlaps and hollow floor ray at z=0.265 verified. Sampled surface clearance is not continuous physical certification.
- Both original pivots independently compared to the included mechanism. Staged 80° release, then 105° opening. All 12 landscape meshes lid-owned, five treads and landscape bounds verified. Deliberately detaching an ornament makes the ownership predicate fail; this is a post-implementation negative control, not test-first development.
- Independent source/GLB world vertex parity maximum error 1.712013073529306e-7 (<1e-5). Three packed source images. Actual runtime map variation: 43 color levels, 77 roughness levels measured in glTF GREEN channel.
- Offline file:// Edge desktop 1440×1080 and mobile touch emulation 390×844: rotation, native Open/Close, interrupted Reset, reduced motion, no overflow, zero external requests and runtime errors. Open silhouette maximum absolute projected coordinate 0.892365. Genuine corrupt GLB parser fallback and no-JS poster pass.
- Automated visual inspection of actual mobile closed and desktop open images: readable stone/terraces/brass, no obvious cropping, floating geometry or clipping. Technical gates are not a photorealism claim. Emulation runs on RTX 4060, not a physical phone performance test.

## Limits and failures
The rectangular masonry is simpler than fitted polygonal Inca stonework; terraces are regular, rocks rounded/low-poly and vegetation represented by muted green surfaces. No archaeological accuracy or prior user art approval is asserted. The rear terrain is naturally obscured behind the opened lid from the front.
Optional Codex lane failed authentication before making edits; all implementation/verification was performed directly by Hermes. Initial build failed because the authorized shared node_modules directory existed but was empty. Fixed by installing the exact pinned Three/esbuild dependencies only inside this new folder; no dependency upgrade or other preview edit. No geometry acceptance failure occurred. Setup junction command initially had a Windows Python escaping error; corrected before creating the junction. No credentials were inspected or altered.

## Reproduce
Python with Pillow/numpy/playwright, installed Edge, Blender 5.2.1, Node.js build tools. `npm ci` here restores pinned dependencies; no node_modules included in source archive.
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python run_checks.py` (set BLENDER environment variable if not at documented Windows path).
4. `python package_delivery.py`

Authoring overwrites generated assets. `setup.py` documents initial pilot adaptation and depends on sibling Japan source; it is NOT required to rebuild this self-contained folder and should not be rerun over edits. Archive inventory excludes itself and packaging envelope to avoid recursive hashes; delivery-check records archive readback. Folder-local .gitattributes preserves exact bytes across Git checkout. Only preview/peru-v1 additions are committed; branch is backed up without merge. Final collection integration is a separate card.
