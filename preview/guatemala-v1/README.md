# Guatemala / Atitlán & Woven Indigo — v1

Open **guatemala-v1.html** directly in Edge/Chrome. Complete offline interactive collectible, **1,957,093 bytes**; standalone GLB **869,496 bytes**. Drag/touch rotates, Open/Close stages the latch then lid, Reset restores pose/view, reduced motion snaps. No hosting, minting, wallets, blockchain queries or custody actions occurred.

## Design and provenance
The researched `design-brief.md` was written before modeling. Museo Ixchel's discussion of living Maya weaving traditions and Britannica's Lake Atitlán description informed original indigo/ochre/crimson stripe panels and a blue-green lake with three unequal volcanic reliefs. No research photography, garment pattern, sacred motif or external texture is embedded. This is not an authentic huipil, indigenous endorsement, geographic replica or representation of all Guatemala.

Editable `guatemala.blend` and procedural `author.py`/`maps.py` are included, with portable packed maps. Source is Blender-script-authored, not human hand sculpting or photogrammetry. `mechanism.blend`, viewer and mechanics originate from repository Japan/Iceland pilots at base ff5d78f1e0d486af5c882c184fc08049996ebdc8. Shared originals were not changed. Three.js runtime is MIT; license included.

## Actual verification
- Build: `HTML_BYTES 1957093 GLB_BYTES 869496`; strict HTML cap <5,000,000.
- Actual GLTFLoader: **10,890 triangles, 57 meshes, 7 materials**, zero nonfinite vertices or degenerate triangles.
- Independently reopened source: **20 moving and 35 static meshes**, **81 sampled poses**, zero unintended intersections. All four landscape meshes included. Only original explicitly named hinge/latch mating bearings excluded. Ten hinge attachment contacts and hollow floor ray z=0.2650000155 pass. This is sampled surface-intersection evidence, not continuous mechanical certification.
- Original lid/latch world matrices match independently reopened mechanism exactly. 80° latch release precedes 105° opening. Motion unit tests include rejecting bad asset contracts.
- Source/export world nearest-vertex error **1.712013073529306e-7** both directions (<1e-5). All four source images packed.
- Theme checks: three unequal rear-half peaks, lake bounds exceeding 1.3 × 0.6, five exposed-water surface rays, all four terrain meshes on lid. A deliberately detached volcano fails ownership, then is restored without saving mutation.
- Runtime map checks decode base color/normal and actual glTF roughness GREEN channel: respective ranges 206/14/40 for textile and 61 for stone; maps at most 512×256 or 256×256.
- Offline `file://` Edge at 1440×1080 and 390×844 touch emulation: native click/tap controls, drag/touch rotation, open/close, mid-motion reset, reduced motion, no horizontal overflow, zero external HTTP requests and zero runtime errors. Full-open max absolute projected NDC 0.91113 (<1). Real corrupt GLB reaches loader and shows poster; no-JS poster tested separately. RTX 4060 emulation is not a physical-phone performance test.
- Actual saved-source render `poster.png` (1000×800) is nonblack and opaque; PNG/JPEG and actual desktop/mobile closed/open/rear screenshots are included. No AI promotional image substituted.
- `inventory.json` lists exact byte counts/SHA-256; `delivery-check.json` records archive readback. Inventory excludes itself, archive and delivery envelope to avoid recursive hashes.

## Visual outcome and limits
Actual poster/mobile/rear-open images were visually inspected: three peaks, lake and indigo stripe panels are visible; no obvious floating parts or clipped model. The lake reads as a raised blue-green enamel plaque rather than recessed natural water. Peaks are stylized faceted miniatures, not an accurate geographic arrangement. Woven texture is subtle on rigid panels; no cloth simulation. Source render has slight sampling grain. Rear/interior/hardware are family extrapolations; latch is intentionally long. Fine hinge contacts are supported by source tests, not fully visible in every screenshot.

**Brief clarification:** 1.9-tall body target describes the body-plus-lid silhouette (lid top 1.978); actual textile wall height is 1.46 above the short feet, retaining the proven mechanism. The lake is inset within the stone outline but its surface rises 0.037 above the lid, an enamel interpretation, not a recessed water cavity. These are disclosed design interpretations, not claims of exact realism.

## Failures and corrections
Optional Codex implementation lane exited with authentication 401 before editing; `codex-lane.log` preserves it. Hermes performed implementation and verification directly without accessing credential files. The first inherited build failed because both prescribed sibling node_modules locations were empty (`Cannot find module ... esbuild/bin/esbuild`); installing this preview's declared dependencies locally fixed build resolution. No source/mechanism/visual gates were relaxed. The deliberate detached-landscape and malformed-asset negatives are post-implementation regression controls, not claimed test-first history. `failure-notes.md` records the tooling issue.

## Reproduce
Python with numpy/Pillow/Playwright, installed Edge, Blender 5.2.1, Node, and `npm ci` inside this directory are required for building/tests. Runtime HTML needs no dependency installation or network. `node_modules`, cache and Blender backup files are excluded from Git/archive.

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background -t 2 --factory-startup --python-exit-code 1 --python author.py`
4. `python verify_all.py` — rebuild + motion/source/theme/parity/browser/extended gates; optional BLENDER environment variable overrides executable path.
5. `python package_delivery.py` — verifies/hash-inventories and archive readback.

Regeneration overwrites source/export/poster; save manual edits separately and regenerate evidence/counts. Source archive is self-contained apart from the documented installed toolchain. Build can use local dependencies or the historical sibling fallback. This branch is backup only; integration into the 201-design gallery is a separate card. No merge or deployment is included.
