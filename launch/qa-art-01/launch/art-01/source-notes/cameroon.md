# Cameroon v1 — Fako / Basalt & Rainforest

Open **cameroon-v1.html** directly in Edge/Chrome. Self-contained actual 3D collectible: **3,832,994 bytes**, with **2,342,852-byte GLB** embedded alongside the runtime and actual-source poster. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion preference snaps the pose. No server or network downloads.

## Design and files
A wide volcanic-stone keepsake box carries an elongated Fako-inspired massif, two subsidiary shoulders, muted green lower slopes and clustered rainforest canopy. Aged-brass family hardware surrounds a hollow interior. Research and the pre-model measurable contract are in `design-brief.md`; this is one landscape interpretation, not all of Cameroon's cultural identity or measured topography.

- `cameroon.blend`: named editable, packed Blender source. `cameroon.glb`: portable model and embedded maps.
- `mechanism.blend`: unchanged trimmed mechanical baseline copied from the Japan pilot, not its tree/wood artwork.
- `maps/`: three generated 512×512 basalt color, roughness and normal maps; not photographs or scans.
- `poster.png` / `poster.jpg`: real source render. Desktop/mobile closed/open, rear-open, fallback and no-JS PNGs are real offline browser captures.
- Reproducible author/build/test scripts, machine-generated JSON checks, raw text outputs, retained `initial/` failures, exact SHA-256 `inventory.json`, and readback-verified `cameroon-v1-source.zip`.

## Verified, with boundaries
- Saved source independently reopened; original lid/latch pivot locations and rotations compared with trimmed baseline. Slab 3.72 × 2.38 × .30 units; body stone panels 1.46 high, overall closed body/lid approximately 1.9 above feet. Relief spans over 1.7 X units and less than .85 Z units. Actual green material polygons, two shoulders beneath main crest, 100 lower-flank canopy meshes, and lid ancestry checked.
- **81 opening poses**, **117 moving / 39 static source meshes**, zero unintended sampled surface intersections. Every moving landscape part is included. Latch-versus-lid checked separately. Only named mating hinge leaf/barrel and latch knuckle/bridge/pin contacts excluded. Ten hinge attachment overlaps and hollow-floor ray at z=0.2650000155 verified. Not a continuous collision proof or manufacturing/engineering certification.
- Exact choreography: first-quarter **80° latch release**, then **105° lid opening**, tested endpoints and 81 motion samples. Closing reverses the order.
- Source/export nearest-vertex error **1.712013073529306e-7 units**, below 1e-5. Three packed source images. This is geometry parity, not byte-identical re-export or identical Blender/browser lighting.
- Actual Three GLTFLoader: **24,092 triangles**, **157 meshes**, **7 materials**, zero nonfinite vertices and zero degenerate triangles. Export splits the two-material relief into two mesh primitives; both inherit the lid through the named Fako group. Actual decoded map variation checked, including glTF roughness's green channel.
- Offline `file://` Edge desktop and 390×844 touch emulation: real native open/close controls, mouse/touch rotation, interrupted reset, reduced motion, no horizontal overflow, no external HTTP requests or runtime errors. Open projected vertices fit (maximum absolute NDC approximately .892365). Genuine corrupted GLB reaches the parser and displays poster fallback; no-JS poster also checked. NVIDIA RTX 4060 desktop GPU; **not physical-phone performance**.
- Missing-Fako mutation is rejected by the theme test. This is post-implementation negative-control evidence, not test-first TDD. Other assertions fail on dimensions, hierarchy, map variation, intersections, invalid geometry, parity, interaction or byte limits; packaging requires passing evidence and explicit mandatory files.

## Honest visual verdict
The actual desktop/mobile model shows an elongated rocky massif, green foothills, stone body and brass hardware without major clipping. It remains deliberately stylized: faceted mountain, rounded overlapping canopy clusters, soft/procedural stone texture that can read as concrete, a visible thin relief perimeter, brighter studio-lit stone/greens than dark albedo targets, clean simplified brass, long inherited hasp and separate decorative front medallion. No photorealism, exact Fako recognition without its label, botanical specificity, physical mechanism certification or human art approval is claimed. Rear/interior construction is family extrapolation. No source images were copied into textures.

## Real failures retained
`initial/` records a browser material-split assertion failure and a roughness-channel assertion failure, corrected to match actual glTF representation without weakening geometry/size gates. Raw GLB names retain spaces, while loader names are sanitized; the theme harness was corrected accordingly. The first 180-second browser run timed out; a longer bounded run completed the suite. Optional Codex failed HTTP 401 before making changes; Hermes implemented and ran all verification directly. No credential files were accessed or modified.

## Reproduce
Dependencies: Blender 5.2.1; Python with Pillow/numpy/playwright; installed Edge; Node.js build tooling with Three 0.180.0/esbuild. No blockchain node is used. `build.py` finds local node_modules or the sibling Iceland pilot toolchain. For a standalone source extraction, install the included package.json dependencies in this folder. The final HTML has no such runtime dependencies. Three's MIT license is included.

From this directory:
1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python build.py`
4. Run Blender with the same flags on `verify_source.py`, `verify_parity.py`, `verify_contract.py`.
5. `node --test tests.mjs`; `python test_theme.py`
6. `python verify_browser.py`; `python verify_extended.py` (allow several minutes for Edge teardown on this host).
7. `python package_delivery.py`

Regeneration overwrites generated source/render files; save manual variants separately. Inventory excludes itself, ZIP and delivery envelope to avoid recursive hashes. Package script reads back every ZIP entry and verifies an explicit required file set. The tested HTML is the delivered HTML in this folder, not an untested copy.

## Scope
Additive local art under `preview/cameroon-v1/` only, backed up on `art/cameroon-v1`; no merge/deploy. Inner collectible cosmetic motion is not an outer custody-container seal change. Not minted, hosted, signed or stored on-chain. No blockchain queries, keys, wallets, funds, nodes or VPS. Launch direction: 201 equally one-of-one designs; accessories remain deferred. Per-asset review waived for collection production; integration belongs to a separate final card.
