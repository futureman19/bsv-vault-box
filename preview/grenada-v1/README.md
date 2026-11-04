# Grenada v1 — Nutmeg & Mace

Open **grenada-v1.html** directly in Edge/Chrome. The model, procedural maps, runtime and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view; reduced-motion snaps to endpoints. No server or network is required.

## Design and honest visual limits
A wide warm-brown wooden collectible with satin brass, a dark-red seam and a sculptural nutmeg still-life: brown seed, nine raised scarlet mace strands, two golden fruit cheeks, four green leaves and a branch. Grenada Tourism Authority's nutmeg-processing and spice-garden descriptions inform the concept; see the pre-model `design-brief.md`. The wood is an invented spice-colored finish, not a claim about a particular timber species or traditional Grenadian box craft. No research images are used as textures.

This is procedural stylized art, not a scan, hand-sculpted work, botanical reconstruction, or photorealism. Mace strands are thick and cord-like; fruit cheeks are simplified rounded forms rather than anatomically cut shells; leaves are partly obscured from the front. Grain is regular, the red seam prominent, and inherited stone feet intentionally contrast with the wood. The actual Cycles poster retains sampling noise (24 samples, denoising off). Hidden interior/rear hardware are family extrapolations. No supplied concept illustration or prior art approval is claimed.

## Files and verification
- `grenada.blend`: independently reopened, packed editable Blender source. `mechanism.blend`: included reusable Japan-family articulation/interior baseline, unchanged. `author.py` generates new theme geometry; `maps.py` generates portable color/normal/roughness maps.
- `grenada.glb`: 35,854 triangles, 148 meshes, 10 materials through actual Three GLTFLoader; zero nonfinite vertices or degenerate triangles. Exact current bytes are reported in `delivery-check.json` and `build-output.txt`.
- `grenada-v1.html`: strictly below 5,000,000 bytes including all assets. `poster.png/jpg` are actual source renders, not AI substitutes. Desktop/mobile closed/open and rear-open PNGs are actual file:// browser captures.
- `source-check.json`: 81 opening samples, all 49 moving and 99 static meshes; zero unintended intersections. Latch versus lid checked separately. Only inherited explicit mating bearings excluded. Hollow interior floor ray z=0.265; ten hinge attachment pairs verified. This is sampled surface intersection evidence, not continuous collision or mechanical engineering certification.
- `parity-check.json`: source/export nearest-vertex geometry agreement below 1e-5 world units. `theme-check.json`: ornament count, lid ancestry, bounds, palette, mace clearance above lid, independent baseline pivot comparison and actual detached-seed negative control.
- `browser-check.json`: offline desktop 1440×1080 and touch-emulated 390×844; native open/close, rotation, interrupted reset, reduced motion, no external HTTP requests, JS errors or horizontal overflow. Full-open viewport projection checked. Actual corrupt GLB reaches the parser and triggers poster fallback. `extended-check.json` verifies no-JS poster and decoded map variation, including roughness's GREEN channel. Mobile is desktop RTX 4060 emulation, not physical-phone performance.
- `tests.mjs`: exact staged 80-degree latch / 105-degree lid endpoints and 81 progress samples; invalid geometry negative controls. Acceptance checks use assertions and exit nonzero on failure.
- `inventory.json`: SHA-256 and byte identity of payload files. `grenada-v1-source.zip`: explicit required assets, source, maps, scripts and evidence, independently read back. `delivery-check.json` hashes the ZIP outside its own envelope. `.gitattributes` preserves exact bytes across Git checkout.

## Real failures retained
`initial/` preserves the initial missing-build browser error and dependency explanation: sibling dependencies were empty, fixed by installing build dependencies in this new folder only. The theme counter initially included leaf-vein meshes as leaves; corrected the prefix selector while retaining the four-leaf requirement. A subsequent **real geometry failure** found a mace strand at z=1.929 penetrating the lid. Raised the lower rib path to z>=2.02, rebuilt the source/GLB/poster, and added an even stricter mace vertex clearance gate above z=1.978. No acceptance threshold was relaxed. The negative-control seed detachment is memory-only and never saved to the delivered source.

## Reproduce
Build/test dependencies: Blender 5.2.1, Python with Pillow/numpy/playwright, Node.js, installed Edge. From this folder:

1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py`
4. `python run_verify.py`

`BLENDER_EXE` can override the verifier path. The build prefers local node_modules, with sibling Iceland dependencies as a fallback; no runtime network dependency exists. Authoring overwrites generated source/model/poster; preserve manual edits separately. Regeneration changes hashes, so rerun verification/packaging. The bundled Three runtime is MIT (`THREE-LICENSE.txt`). Dependencies, caches and .blend1 backups are not in the source ZIP.

Local art asset only: not minted, hosted, signed, deployed or admitted to chain custody. Cosmetic lid movement does not change a seal. No keys, wallets, blockchain nodes, chain queries, production paths or shared base kit were accessed/modified. Collection direction is 201 equally one-of-one boxes. This branch is backup-only; integration and full-set review are separate tasks.
