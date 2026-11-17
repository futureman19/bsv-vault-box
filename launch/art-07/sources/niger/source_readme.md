# Niger v1 — Aïr & Ténéré

Open `niger-v1.html` directly in Edge/Chrome. Complete embedded runtime, GLB, maps and actual-source poster: **2,828,600 bytes**. Standalone GLB: **1,514,928 bytes**. No server or network is required. Drag/touch to rotate; Open/Close lid; Reset view; reduced-motion preference is honored.

## Design and provenance
The pre-model `design-brief.md` uses UNESCO’s Aïr and Ténéré Natural Reserves description (https://whc.unesco.org/en/list/573): Niger’s volcanic Aïr massifs contrast with the surrounding Saharan desert. The warm mineral body, low dune relief and dark rear-right outcrops are a stylized interpretation, not a surveyed miniature or representation of all Nigerien cultures. No reference photos, sacred symbols, flags or third-party textures were copied. Brass is a collection-family invention. Geometry and portable maps are procedurally authored, not scans or hand sculpture.

The included `mechanism.blend` comes from the Japan pilot; the hollow liner, pivots and brass articulation are retained, not the cedar/tree artwork. Shared `art/vault-kit` and all other previews remain unchanged. Three.js 0.180.0 is MIT; license included. Node.js is used only as build tooling, never as a blockchain node.

## Verified results
- Independent reopening of `niger.blend`: hollow floor ray z=0.2650000155; ten hinge attachment surface-overlap pairs; exact baseline pivot matrices.
- **81 sampled poses**, every one of the **20 moving and 39 static meshes** considered: zero unintended surface intersections. Includes dunes/outcrops and latch-versus-lid checks. Only explicit inherited mating bearings excluded. This is sampled surface evidence, not continuous clearance or engineering certification.
- 80-degree latch release precedes 105-degree lid opening. Two motion/invalid-asset tests pass. Deliberately detaching an outcrop makes the ancestry assertion fail; it is restored without saving.
- Saved source versus independently imported GLB: maximum bidirectional nearest-world-vertex distance **1.712013073529306e-7**, below 1e-5. Four packed source maps; actual loader: **17,284 triangles, 59 meshes, four materials**, zero nonfinite vertices and zero degenerate triangles.
- Theme checks: four lid-owned terrain meshes; three outcrops in +X/+Y; relief maximum **0.41767852** above lid, below 0.65. Sand base color/normal/roughness and rock maps decode with nonzero variation, at most 512 pixels per dimension. Roughness is tested in glTF’s green channel.
- Actual Edge offline `file://`: desktop and 390×844 touch emulation, native open/close, pointer/touch rotation, interrupted reset, reduced motion, full-open projection, no overflow, no external HTTP requests or errors. Genuine corrupt-GLB parsing triggers the embedded poster; JavaScript-disabled poster also verified. Mobile emulation uses the desktop RTX 4060, not a physical phone performance test.
- Poster is an actual Blender source render, with nonempty decoded pixels. Screenshots are actual browser captures. Inventory records exact bytes/SHA-256; archive entries are read back and verified. Folder-local `* -text` preserves bytes in Git.

## Visual verdict and bounded corrections
This is a finished first-version **stylized** desert collectible, not photoreal equivalence or a user-approved reference match. Dunes are shallow but visible from the raised final camera; the faceted dark outcrop reads as rock, not diagnostically volcanic lava. Broad chest panels can still suggest wood despite their generated mineral color/normal maps. Initial stronger ripple bands looked too wood-like; `initial/woodlike-poster.png` retains that rejected source render, and the final texture reduces directional banding and warms/darkens the mineral palette. The final viewer camera was raised to expose the low landscape. No extra polish loop is implied.

The source poster retains low-sample render grain. The dark lid seam is conspicuous. At full opening, the released latch and rear fittings can appear visually separated in projection; independent attachment pairs and source collision samples pass, but no manufacturing/physical mechanism claim is made. Opening naturally hides the lid-top relief from the front; `desktop-open-rear.png` shows its reverse view.

## Failures and recovery
The optional Codex implementation lane exited with an authentication refresh 401 before making edits; Hermes authored and tested the asset directly. No credentials were read or changed. Initial copy setup referenced nonexistent Japan `tests.mjs`; corrected by using the Iceland motion test source. Shared build dependencies were absent, so unchanged pinned packages were installed only in this new folder. No source/collision/parity/browser gate was relaxed. Negative tests are intentionally post-implementation regression controls, not a claim of test-first TDD.

## Reproduce
Requirements: Blender 5.2.1, Python with numpy/Pillow/playwright, installed Edge, Node.js and npm. All scripts resolve their asset paths relative to this folder. `npm ci --ignore-scripts --no-audit --no-fund` restores local build dependencies. No node_modules is delivered.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `node --test tests.mjs`; `python build.py`
4. Run Blender with the same flags for `verify_source.py`, `verify_parity.py`, `verify_theme.py`.
5. `python verify_browser.py`; `python verify_extended.py`
6. `python package_delivery.py`

Authoring overwrites generated source/model/poster; preserve manual edits separately. Build uses local dependencies (with inherited sibling fallback only if absent). Reproduction is not promised byte-identical across Blender versions. `inventory.json` excludes itself and archive/delivery envelopes to avoid circular hashes; source ZIP excludes backups, dependencies and optional lane diagnostic logs.

Local art only: not minted, signed, hosted, chain-admitted or deployed. No keys, wallets, chain queries, broadcasts, VPS, custody code, production site, or shared kit changed. Branch backup is not a merge or deployment. Next step: collection integration on its separate gated card.
