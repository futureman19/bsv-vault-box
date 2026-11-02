# Sudan v1 — Meroë / Desert Gold

Open **sudan-v1.html** directly in Edge/Chrome. The complete model, runtime, procedural maps and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced motion snaps to the target. No network or server is needed. This is a local inner collectible art asset, not a custody container, mint, sale, blockchain seal opening or deployment.

## Deliverables
- **Standalone HTML: 3,274,491 bytes**, strictly below 5,000,000.
- **GLB: 1,909,528 bytes**; 15,156 triangles, 75 meshes, four materials through actual Three GLTFLoader.
- `sudan.blend`: packed, named editable Blender source; `mechanism.blend`: inherited trimmed mechanical baseline.
- `maps/`: three independently generated 512×512 sandstone base-color, roughness and normal maps. No external image textures or scans.
- `poster.png` / `poster.jpg`: actual source render, not AI promotional imagery.
- Desktop/mobile closed/open, rear-open, corrupt-input and no-JS screenshots. `visual-review.jpg` is a labeled montage of actual captures.
- `sudan-v1-source.zip`: source, maps, GLB, HTML, scripts, license and evidence. `inventory.json` has exact byte/SHA-256 identities. `delivery-check.json` records ZIP readback and extracted-HTML offline verification, outside the ZIP to avoid recursive hashes.

## Theme and provenance
The brief was written before authoring. UNESCO's Meroë site and inscription decision inform the semi-desert setting, reddish/ochre palette and Kushite pyramid-inspired forms; citations are in `design-brief.md`. This is a contemporary stylized interpretation, not a measured monument reconstruction or representation of every Sudanese tradition. Sandstone-like surface and brass fittings are artistic choices. No ancient inscriptions, burial contents or sacred symbols are reproduced. No third-party source pixels are used.

The body is approximately 3.72×2.38 units, with regular masonry-like courses, four stone feet, a dark umber seam and warm hollow interior. Three steep square pyramid ornaments have real stepped-course geometry and heights 0.55, 1.05 and 0.80. Each intersects the shallow dune field and belongs to the lid. The mechanism/viewer/test lineage is Japan's trimmed mechanism and the Iceland articulation, read-only from base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. The shared vault kit and every earlier preview remain unchanged. Three.js runtime license included; no dependency upgrades.

## Verified acceptance
- Independent saved-source reopen: original rear pivot at y=1.32, z=1.668; latch parent; slab dimensions; three seated pyramids with twelve courses each; four feet; seam height 0.108; no cedar/moss geometry.
- Source-to-GLB and GLB-to-source maximum nearest-vertex discrepancy **1.712013073529306e-7 units**, below 1e-5. Three packed maps present. This is geometry parity, not an assertion of byte-identical re-export or identical Blender/browser shading.
- **81 sampled motion poses**, all 20 moving meshes versus 55 static meshes, plus latch versus moving lid. Zero unintended surface intersections. Only explicit inherited mating bearings exempt. Ten hinge attachment pairs intersect, and the hollow floor ray hits at z=0.26500001549720764. This is discrete BVH surface testing, not continuous clearance, solid-volume or mechanical engineering certification.
- Staged latch releases 80° before lid opens 105°. Node motion/asset-contract tests pass, including invalid input rejection.
- Actual GLTFLoader: zero nonfinite vertices and degenerate triangles. All three pyramids and dune mesh have correct exported lid ancestry. Decoded base-color/normal/roughness variation verified; roughness is sampled from glTF's green channel, not its constant red channel.
- Edge offline **file://** desktop 1440×1080 and mobile 390×844 touch emulation: native clicks/taps, drag/touch rotation, open/close, reset during motion, reduced motion, no horizontal overflow, no external HTTP requests and no JS errors. Open silhouette maximum absolute NDC approximately 0.8924. Corrupt GLB bytes actually reach the loader and trigger poster fallback. No-JS decoded poster verified.
- Mobile emulation ran on NVIDIA RTX 4060 desktop hardware. No physical-phone performance, FPS or broad browser compatibility claim.
- Negative controls reject a missing pyramid, detached pyramid, green palette, invalid model contract and genuinely corrupt GLB.

### Real failure and fix
`initial-roughness-channel-failure.txt` retains the initial extended-test assertion failure. The harness inspected red-channel variation for every map; glTF packs roughness in green and leaves red constant. Fixed the harness to inspect green for roughness, retaining the nonzero-variation requirement and original size ceiling. The corrected observed roughness range is 68. No model acceptance limit was weakened. Optional Codex implementation was rejected after authentication failed; all authoring and verification were performed directly by Hermes, without credential changes.

## Visual verdict and limits
Actual source poster, desktop closed/open, mobile closed and rear-open views were inspected. No obvious clipping or detached ornament; all three pyramids remain on the raised lid; cavity and lid underside are visible. Normal/mobile size reads as a stylized sandy architectural collectible, not cedar forest. This is **not photorealism or archaeological fidelity**. The long regular horizontal courses retain some generic chest/plank character, pores are subtle at mobile scale, and the dune field is shallow. The dark seam is deliberately pronounced; its passing mechanical checks do not make it a realistic seal. Hardware and feet are family extrapolations; the inherited hasp is conspicuous when fully opened. Supporting mobile copy is small. No human per-asset review is claimed; this card explicitly waived it until collection completion.

## Reproduce
Dependencies: Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with Three.js/esbuild from package.json. `build.py` resolves local node_modules or read-only sibling `iceland-pilot/node_modules`. The installed sibling dependency directory was linked into this worktree; it is not tracked or archived. A standalone source extraction must install package.json dependencies locally. Authoring uses only the included mechanism source/maps, not external art directories.

```text
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python verify_all.py
```

`verify_all.py` builds the HTML, runs motion tests, reopens source for mechanism/theme/parity checks, runs both browser suites, then creates/verifies the archive. Override Blender executable with `BLENDER` if needed. Individual scripts may be run independently; all paths resolve from their own directory. Regeneration overwrites generated model/source/poster: save manual variants separately. Packaging never includes node_modules, caches or .blend1 backups.

Folder-local `.gitattributes` disables newline conversion so Git checkout preserves inventory bytes. The optional broad `git diff --check` flags original Three shader-string whitespace and preserved raw-log terminal blank lines; these generated/raw bytes were not rewritten to manufacture a clean whitespace result. Authored-source whitespace is checked separately.

No keys, blockchain nodes, chain queries, minting, VPS, funds, production directories, external messaging, uploads or public-site changes were involved. Authorized Git branch backup only; integration is a separate card. The collection remains 201 equally one-of-one designs; no authenticity, chain storage or asset availability guarantee is implied by local hashes.
