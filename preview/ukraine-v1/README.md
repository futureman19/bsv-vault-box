# Ukraine v1 — Petrykivka Bloom

Original procedural floral collectible inspired by Ukrainian Petrykivka decorative painting. Open **ukraine-v1.html** directly in Edge/Chrome: all 3D, textures, runtime and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset; reduced-motion users get synchronous pose changes. This is cosmetic art only, not minted, hosted, on-chain, authenticated or a custody action.

## Delivered
- `ukraine-v1.html`: **3,833,953 bytes**, under 5,000,000.
- `ukraine.glb`: **2,284,784 bytes**, embedded portable maps.
- `ukraine.blend`: packed editable source; `mechanism.blend`: copied, unmodified Japan pilot mechanism used for reproduction.
- `maps/`: three independently procedural 1024×512 maps; `maps.py`, `author.py`, build/verification scripts.
- `poster.png` and JPEG: actual Blender render, not AI promotional art. Desktop/mobile closed/open and rear-open screenshots are actual offline browser captures.
- `ukraine-v1-source.zip`, `inventory.json`, `delivery-check.json`: required-artifact assertion, exact SHA-256/bytes and complete archive readback. No dependencies, caches or .blend1 backups included.

## Verified, with explicit limits
Saved source independently reopened: **150 moving and 39 static meshes**, **81 poses**, zero unintended sampled surface intersections including all floral ornaments and latch-versus-lid. Only named inherited concentric hinge/latch bearing contacts exempt. Ten attachment pairs intersect at their intended joints. Hollow floor ray hits z=0.2650000155. This is sampled surface clearance, not continuous collision or manufacturing certification.

Independent source/export world-vertex comparison: maximum bidirectional error **1.712013073529306e-7**, below 1e-5. Exact baseline pivot matrices retained. Actual Three GLTFLoader: **37,680 triangles, 193 mesh primitives, 9 materials, zero nonfinite vertices or degenerate triangles**. More runtime mesh primitives than source objects is expected from multi-material panels.

Theme checks confirm five flowers / 55 petals, eight tapered leaves and connecting leaf branches, five terminating flower stems, lid ancestry of every ornament, relief bounds and no inherited tree/moss. Deliberately detaching an ornament is rejected by the same ancestry validator. Three invalid geometry controls are rejected; the motion test samples all 81 staged states and exact 80°/105° endpoints. Decoded map variation is 213 for floral color, 9 for subtle wood color and 26 in the glTF roughness **green** channel.

Actual Edge **file://**, offline desktop 1440×1080 and mobile 390×844 touch emulation: native opening/closing, mouse/touch rotation, interrupted Reset, reduced motion, no horizontal overflow, no external requests and no runtime errors. Full open fits with maximum absolute projected NDC approximately 0.8924. Real corrupt GLB input reaches the parser and shows poster fallback; no-JS poster also passes. GPU reported RTX 4060; **not physical-phone performance testing**.

## Visual judgment / limitations
Readable dark floral box, bright original body friezes, sculptural red/coral lid flowers, warm brass fittings and hollow interior. Mobile/desktop screenshot inspection found no blocking framing/control defects. Raised petals are rounded and toy-like, foliage angular, grain regular and lacquer more satin than deep mirror gloss. Rim corner segmentation, long family hasp and dark interior remain visibly stylized. Opening hides the lid's floral face from the front; rear-open evidence shows it. No claim of photorealism, traditional pattern fidelity, botanical accuracy or artisan authorship. This is a deliberately invented relief translation of a planar painting tradition; research sources are in the prewritten brief, not copied image textures.

One bounded visual correction removed compressed decorative strips on thin panel-end faces and connected leaf roots to nearest flower stems. Initial source poster retained. No supplied or approved marketing reference exists; the sourced written brief was frozen before modeling. No material dimensional deviation was needed.

## Failure history and provenance
- Optional Codex lane exited with authentication 401 before editing; no changes accepted. Hermes authored and verified directly. No credential repair/access performed.
- First build genuinely failed because the requested shared dependency directory existed but was empty. `initial/build-output.txt` retained. Installed only pinned Three 0.180.0 / esbuild 0.25.11 locally in this new preview; lockfile included. Build now succeeds without changing the HTML cap.
- Background `node` shell shim returned `stdin is not a tty`; retained in `initial/motion-shell-failure.txt`. Using the native Node executable ran unchanged tests successfully.
- Source/motion/parity/geometry and theme gates were not weakened. Negative controls are explicit post-implementation regression checks, not a claim of test-first authoring.

Mechanism, viewer and general harness lineage: `preview/japan-cedar-v1/` at base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. Shared kit and prior preview files are unmodified. Three runtime is MIT; included license. Generated geometry and textures, no third-party artist work copied.

## Reproduce
Python with numpy, Pillow and Playwright; installed Edge; Blender 5.2.1; Node. In this folder:
1. `npm ci --no-audit --no-fund`
2. `python maps.py`
3. `blender --background --factory-startup --python-exit-code 1 --python author.py`
4. Same Blender invocation for `verify_source.py`, `verify_parity.py`, `test_theme_source.py`.
5. `node test_motion.mjs` (Windows background shell: use `C:/Program Files/nodejs/node.exe`).
6. `python build.py`, `python verify_browser.py`, `python test_theme.py`.
7. `python package_delivery.py`.

Authoring overwrites generated assets; keep manual edits separately. Windows tool paths in execution logs describe this host, not runtime dependencies. Dependency lookup prefers this folder then sibling Iceland; npm ci makes it self-contained for build. Packaging remains in this directory. After regeneration update reported counts/hashes rather than asserting old identities. Folder-local `* -text` preserves byte identities through Git. No public deployment, blockchain node, keys, mint or VPS access; branch backup only, with integration left to the collection's final card. Per-asset human review explicitly waived; not a claim of user visual approval.
