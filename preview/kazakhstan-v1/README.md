# Kazakhstan v1 / Steppe Felt & Brass

Open **kazakhstan-v1.html** directly in Edge/Chrome. Entire runtime, model, maps and actual-source poster are embedded. Drag/touch to rotate, open/close the lid, and reset. This is cosmetic movement of an inner collectible, not an outer custody container or a transaction.

- **HTML_BYTES 3196697** (strictly below 5,000,000)
- **GLB_BYTES 1840508**
- Editable `kazakhstan.blend`, frozen `mechanism.blend`, procedural maps, reproduction scripts, original source poster and actual browser screenshots included.
- Exact file sizes and SHA-256 hashes: `inventory.json`. Archive inventory and readback: `delivery-check.json`. The inventory intentionally excludes itself and packaging envelopes to avoid circular hashes.

## Design and provenance

Original brief-driven interpretation of Kazakh felt and ornamental craft: cream wool-like panels, oxblood paired curling appliques, wood frame and low circular lattice on the lid, satin brass hardware. The research-backed `design-brief.md` was written before modeling. No third-party photo pixels, AI promotional substitute, flag, sacred symbol or claim of authentic historic artifact. Shared yurt craft is not presented as exclusive to Kazakhstan. Original procedural geometry/maps, not scans or hand-sculpted work.

Mechanical source and viewer/test lineage: `preview/japan-cedar-v1` at base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; Japan's frozen mechanism descends from the Iceland pilot. No cedar tree, moss, glacier or Morocco terrain is retained. `mechanism.blend` is copied, not edited in the prior folder. Shared `art/vault-kit` remains read-only. Six portable materials and three generated 512px maps, no runtime downloads. Three.js license is included.

## Verification actually run

- Saved Blender source independently reopened; hollow floor ray hits z=0.2650000155. Ten intersecting hinge attachment pairs confirm actual source connection, not merely proximity.
- **81 sampled poses, 32 moving and 67 static meshes, zero unintended surface intersections**, including all new moving decorations and latch-vs-lid surfaces. Only the named coaxial hinge/latch bearing contacts are exempted. This is sampled surface intersection evidence, not continuous collision/solid-containment or manufacturing certification.
- Source/export world-vertex nearest-neighbor maximum error **1.712013073529306e-7** (<1e-5), in both directions. Packed source maps confirmed. This is geometry parity, not pixel-identical shading between Blender and browser.
- Actual Three GLTFLoader: **36,176 triangles, 99 meshes, six materials; zero nonfinite vertices and zero degenerate triangles**.
- Contract check independently verifies 3.72×2.38×0.30 lid slab, narrow seam, low ornament relief and both pivot transforms/parents exactly equal to frozen mechanism. Motion tests verify latch 80° before lid 105°.
- Theme check: eight lid curls, eight front/rear curls, eight side curls, six lattice bars and one rim; all lid ornaments attached to the lid. Decoded felt color/roughness ranges 31, wood range 23; 512px maps. Removing a real loaded lid curl causes rejection. Invalid/empty/nonfinite asset fixtures are rejected by motion tests.
- Actual Edge **offline file://**, desktop 1440×1080 and 390×844 touch-emulated mobile: native open/close, drag/touch rotation, interrupted reset, reduced-motion snap, no horizontal overflow, no external HTTP requests, no JS errors. Entire open silhouette fits (max absolute projected coordinate 0.892365).
- Genuine corrupt embedded GLB reaches the real loader and yields poster fallback with disabled controls. No-JS poster tested separately. Tests used the desktop RTX 4060; **no physical-phone performance, FPS or accessibility certification** is claimed.

## Real failures and bounded correction

`initial/` retains actual output, not fabricated red tests:
1. A shell Node shim failed with `stdin is not a tty`; direct `C:/Program Files/nodejs/node.exe` runs both tests successfully.
2. A Blender export process crashed with a Microsoft C++ exception. Re-running with `--threads 2` completed authoring/export/render; root cause is unproven. Final source/export checks ran with two threads.
3. The initial texture test incorrectly sampled roughness from red. Standard glTF stores roughness in **green**. The failure showed range 0; correcting the sampled channel yields range 31 without changing/relaxing the >10 variation assertion or asset.
4. Initial source visual review noted an overly exposed dark lid seam. Restored the inherited wood rim-corner geometry and added side scrolls; final screenshots show the revised candidate. Previous source poster is retained. No claim of eliminating every visual gap.

## Honest visual verdict

Actual mobile review confirms a wide, fully framed chest with readable cream/red/wood/brass and low lattice; desktop open review confirms the hollow interior. This is a **stylized craft collectible**, not photorealism or an exact ethnographic reconstruction. Felt reads as fine-grained fabric rather than individually resolved fibers; wood is regular and medium warm brown despite the darker design target. Curls are rounded, with blunt ends; the grille is a contemporary geometric allusion. The inherited long latch and dark seam are conspicuous. Source geometry proves connected rear mounts, but from the front-open camera their dark gap can still look floating. No engineering certification is implied. These are disclosed v1 visual limitations, not hidden technical test waivers.

Per task directive, per-asset human review is waived until the complete collection exists. This card delivers only Kazakhstan v1; no batch integration, merge or publication.

## Reproduce

Use Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1 and Node/Three/esbuild. From this directory:

```text
python maps.py
blender --background --threads 2 --factory-startup --python-exit-code 1 --python author.py
python build.py
node --test tests.mjs
blender --background --threads 2 --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --threads 2 --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --threads 2 --factory-startup --python-exit-code 1 --python verify_contract.py
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

On this host use the full executable paths documented above and `C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe`. Build uses local node_modules if available, otherwise sibling `iceland-pilot/node_modules` (worktree junction to main checkout). Source extraction needs `npm install` using the included package.json. Dependencies/junction are not archived. Source authoring is relative-path/self-contained; rerunning overwrites generated artwork, source/render hashes and evidence, so repackage after regeneration. `build.py` prints exact bytes; scripts assert and return nonzero on gate failures. Raw logs are preserved unedited.

Local art only: no keys, blockchain node, minting, signing, chain queries, broadcasts, custody proof, VPS access or website deployment. Off-chain content-addressed storage remains a proposal, not implemented by this asset. The branch push is a Git backup only. The future launch direction is 201 equally one-of-one designs; no launch accessories.
