# Lesotho v1 — Maloti Basalt & Woven Indigo

Open **lesotho-v1.html** directly in Edge/Chrome. All model, textures, runtime and poster bytes are embedded: no server or internet is needed. Drag/touch to rotate, Open/Close lid, Reset view. This is a cosmetic inner collectible study, not an outer custody container or transaction interface.

## Delivered

| Artifact | Exact bytes |
|---|---:|
| Standalone HTML | **3,136,261** |
| Portable GLB | **1,802,704** |

The complete HTML is strictly below 5,000,000 bytes. `inventory.json` records exact SHA-256 and byte counts for the source, maps, viewer, images and evidence. `delivery-check.json` records archive/readback checks and the separate source ZIP size/hash. The source archive is not part of the viewer payload.

- `lesotho.blend`: packed, editable, named Blender source.
- `lesotho.glb`: exported articulated geometry and embedded maps.
- `mechanism.blend`: unchanged trimmed family mechanical source from the Japan pilot; not Japan's art.
- `maps/`: three independently generated 512×512 mineral color/roughness and indigo stripe/weave maps; no scans or borrowed artwork.
- `poster.png` / `poster.jpg`: actual Cycles source render, never AI promotional imagery.
- `desktop-closed.png`, `desktop-open.png`, `desktop-open-rear.png`, `mobile-closed.png`, `mobile-open.png`, `mobile-fallback.png`, `mobile-nojs.png`: real offline browser captures.
- `design-brief.md`: research-backed contract written before modeling. No preexisting Lesotho concept image was supplied; the written brief is the design reference.
- `lesotho-v1-source.zip`: source, scripts, maps, viewer and evidence; no dependencies, secrets or Blender backups.

## Theme and visual verdict

Lesotho's basalt highlands supply the primary landscape/material identity: a wide blue-charcoal mineral box, three unequal connected miniature summits and muted olive grass accents. A broad ivory/rust stripe panel on indigo refers generally to textile craft. **The stripe design is invented, not a reproduction of a named Basotho blanket or ceremonial motif.** The mountain is not a surveyed named summit. Official tourism sources and retrieval limitations are cited in the brief.

Final actual mobile review found the three summits and broader stripes readable, with no severe visible defect. This remains stylized procedural art, not photorealistic or user aesthetic approval. The stone can still read as weathered painted material, the pale facets can suggest snow, and the micro-weave is not strongly legible at mobile scale. The open pose is fully framed and the hollow shell is readable. Rear hinge connections are geometrically attached but visually subtle; the dark closed seam can appear slightly ajar. No physically engineered closure claim is made.

One bounded correction darkened the mineral surface, broke up plank-like ledges, clarified peak separation and broadened the stripes after actual screenshot review. `initial/` preserves the superseded render/mobile image and early source/theme evidence. No further optional art iteration is implied.

## Verified on the final files

- **Actual Three GLTFLoader:** 17,958 triangles, 102 mesh primitives, 10 materials; zero nonfinite vertices and zero degenerate triangles. All three maps decoded with nonzero pixel variation and finite UVs. The multi-material ridge loads as one named group containing four primitive meshes, not a single named mesh. `features.ridge: 0` in extended evidence counts directly named meshes only; `ridge_group` proves its actual four-child hierarchy.
- **Saved source independently reopened:** 37 moving meshes and 62 static meshes. Ten hinge attachment pairs intersect as intended. Hollow interior ray reaches the floor at z=0.2650000155.
- **Motion:** 81 evaluated BVH surface-intersection samples, every moving mesh against static surfaces and latch against lid. Zero unintended intersections; only explicit mating hinge-leaf/barrel and latch-knuckle/bridge/pin bearings excluded. Exact inherited pivot matrices retained. Staged 80° latch release precedes 105° lid opening; reverse closure, endpoints and clamping tested.
- **Source/export geometry parity:** maximum nearest-world-vertex error in either direction **1.712013073529306e-7**, below the 1e-5 tolerance. This is geometric parity, not Blender/browser lighting equivalence.
- **Theme:** three real unequal peaks, bounded footprint/height, lid ancestry for all 21 ornaments, seam <=0.09, wide lid dimensions, three packed compact maps. A real in-memory detached-ridge negative control is rejected. It does not modify the saved source.
- **Offline browser:** Edge file:// at 1440×1080 desktop and 390×844 touch-emulated mobile. Native Open/Close, drag rotation, interrupted Reset, reduced-motion snapping, actual corrupt-GLB parser failure/poster and no-JavaScript poster. No external HTTP requests, runtime errors or horizontal overflow. Full-open projected geometry max absolute NDC about 0.8924 (<1). Tested on RTX 4060 desktop; **not physical-phone performance or FPS certification**.
- **Delivery:** exact required-artifact inventory, ZIP entry/hash readback, byte-identical copied HTML reopened offline with native mobile Open/Reset. Hashes identify bytes, not authorship, ownership or availability.

Sampling is not continuous collision proof, watertight solid-volume certification or manufacturability. Surface intersection tests cannot establish all possible containment contacts. Decorative static relief overlaps and terrain/grass attachments are intentional.

## Real failures and fixes

1. The first extended runtime test assumed the multi-material ridge would be one mesh named after its Blender object. It failed with zero directly named ridge meshes. The retained `initial/extended-output.txt` shows that failure. The corrected test requires the actual named ridge group, four mesh children and `Lid_Hinge` parent; it does not waive ancestry.
2. One Cycles rerender failed allocation (`Calloc/Malloc returns null`), retained in `initial/render-memory-failure.txt`. A bounded retry with `--threads 2` completed; source export, final render and every acceptance gate were rerun afterward. An old poster was not shipped against a new GLB.
3. Optional Codex input lane exited 1 with HTTP 401 refresh failure and made no edits. Hermes implemented and verified everything directly; no credentials were inspected or changed. Lane transcript is provenance only, not acceptance evidence.

## Reproduce

Blender 5.2.1, Python with numpy/Pillow/Playwright, installed Edge, Node with Three 0.180.0 and esbuild. Build resolves local node_modules or the read-only linked `../iceland-pilot/node_modules`; an extracted archive can run `npm install` from its included package.json. These are build-time dependencies, not viewer network dependencies. Windows defaults for Blender/Node are explicit in `run_verification.py`, overridable with `BLENDER_EXE` / `NODE_EXE`.

From the repo root:

```text
python preview/lesotho-v1/maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --threads 2 --python-exit-code 1 --python preview/lesotho-v1/author.py
python preview/lesotho-v1/run_verification.py
python preview/lesotho-v1/package_delivery.py
```

Generation overwrites the authored files; preserve manual edits in a separate copy. The packager writes only inside this new directory. Inventory and ZIP/delivery envelopes exclude self-hashes to avoid recursion. Rebuilding requires refreshed hashes and size documentation; do not reuse old evidence against modified bytes.

## Scope and provenance

Mechanism/viewer/test lineage: `preview/japan-cedar-v1/` at base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`. No shared source, prior preview or production files modified. Three.js runtime is MIT (`THREE-LICENSE.txt`). Source/map geometry is script-authored, not hand sculpture, photogrammetry or copied reference imagery.

No blockchain nodes, keys, wallets, queries, minting, broadcasts, site deployment, Hetzner VPS or messaging used. Branch backup only; no merge. Media remains local/off-chain with no persistence or custody guarantee. Collection scope remains 201 equally one-of-one designs; this folder delivers Lesotho only. Next: include this branch in the separate collection integration pass.
