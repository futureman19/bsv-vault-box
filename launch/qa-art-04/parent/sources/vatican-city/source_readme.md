# Vatican City v1 — Travertine & Mosaic

Open **vatican-city-v1.html** directly in Edge/Chrome. The complete 3D model, textures, runtime and actual-source poster are embedded. Drag/touch to rotate, Open/Close lid, Reset view. Reduced-motion preference is honored. No server or external runtime download is needed.

## Delivery

- Offline HTML: **2,742,907 bytes**, strictly below 5,000,000 bytes.
- `vatican-city.glb`: **1,516,044 bytes**; 20,108 triangles, 235 meshes, 6 materials through actual Three GLTFLoader.
- `vatican-city.blend`: packed editable Blender source; `mechanism.blend`: copied read-only Japan mechanism lineage.
- `maps/`: three independently generated 256×256 stone color/roughness/foot maps. No scans or copied artwork.
- `poster.png` and `poster.jpg`: actual Blender source render, not AI promotional art.
- `desktop-closed.png`, `desktop-open.png`, `desktop-open-rear.png`, `mobile-closed.png`, `mobile-open.png`: final offline browser captures. Fallback/no-JS captures are separate.
- `inventory.json`: byte counts and SHA-256 identities. `delivery-check.json`: full source-ZIP readback and size checks. Packaging envelopes exclude their own hashes to avoid recursion.

## Design and visual limits

The research-backed **design-brief.md was written before modeling**. Pale travertine-inspired stone and an invented blue/ivory/gold enamel border surround a miniature oval piazza: two opposing curved arcades with 24 individual columns. No sacred images, papal arms, inscriptions or actual mosaic patterns are reproduced. The arcade is an original abstraction, not a measured replica of Saint Peter's Square. Research sources inform material/craft associations only.

The final higher camera makes the open central space legible on emulated mobile; the earlier lower view remains in `initial/`. Render sampling increased from 24 to 64, without denoising, to reduce poster grain. Final desktop-open review found a coherent hollow chest and no obvious clipping/floating parts. The lid ornament naturally sits behind the raised lid from the front; the rear-open capture shows it.

**Stylized, not photorealistic or architecturally exact.** Stone reads as generalized cream mineral/plaster at mobile scale, not a geological sample. Pale columns can blend with the lid; the continuous cornice is deliberately chunky. Mosaic chips are raised, regular decorative geometry rather than historical fitted mosaic technique. Rounded stone feet and simplified brass fittings retain the collectible family language. The dark bronze seam can appear slightly open even in the closed pose. No physical-device performance or mechanical/manufacturing certification is claimed.

## Executed verification

- `source-check.json`: independent saved-source reopening; hollow interior floor ray z=0.2650000155; **81 motion samples, 196 moving and 39 static meshes, zero unintended sampled intersections**. Latch-vs-lid tests include the entire ornament. Only named concentric hinge leaf/barrel and latch knuckle/bridge/pin bearings excluded. Sampling is not continuous collision proof; static-static and every co-moving contact are not blanket-certified.
- `hinge-attachment-check.json`: ten actual intersecting source attachment pairs link rear hinge body mounts and lid leaves.
- `theme-check.json`: exact inherited pivot matrices, 24 columns with seated shaft endpoints, 180 lid-owned ornament meshes, 21 downward rays through the open center, 22 sampled column gaps. A deliberately detached column fails the ownership assertion and is restored without saving.
- `parity-check.json`: independently reopened source vs imported exported GLB nearest-world-vertex maximum error **1.712013073529306e-7**, below 1e-5. Three packed maps present. This is geometry tolerance evidence, not a byte-identical Blender re-export claim.
- `motion-output.txt`: two Node tests PASS, including staged 80° latch/105° lid endpoints and rejected missing/empty/nonfinite geometry.
- `browser-check.json`: actual GLTFLoader zero degenerate/nonfinite geometry; desktop 1440×1080 and mobile 390×844 touch emulation over offline file://; native open/close, drag/touch rotation, interrupted Reset and reduced motion. Zero external HTTP(S) requests, runtime errors or horizontal overflow. Full-open projected vertex absolute NDC maximum 0.911882 (<1). Real corrupted embedded GLB reaches the parser and shows poster fallback with disabled controls.
- `extended-check.json`: actual decoded texture ranges 41/56 for color and 77 for roughness (correct GREEN channel); all 256px. Nonblack/alpha poster checks, visible country-copy regression, and no-JS poster pass.
- `delivery-check.json`: strict size boundary rejects 5,000,000 bytes; explicit required artifact set, exact inventory and every ZIP member hash verified on readback. Preview-local `.gitattributes` preserves exact bytes on Windows.

Checks use real assertions and negative controls, not hand-written success reports. Browser evidence uses Edge on desktop RTX 4060, **not physical-phone testing**.

## Failures retained

1. Optional Codex lane failed authentication (401) before producing edits. `lane-output.txt` retains the failure; all implementation and verification were performed directly by Hermes. Credentials were not altered.
2. The expected sibling dependency directory was empty. First build failed with missing esbuild; a browser attempt before a successful build failed with missing HTML. Both raw failures are in `initial/`. Installed the declared packages locally in this new preview, then rebuilt and retested successfully; no dependency tree is shipped.
3. The background shell's `node` shim failed with `stdin is not a tty`. Retained in `initial/node-shim-failure.txt`; invoking the native Node executable passed both motion tests.
4. Earlier lower-camera and 24-sample poster images are retained as presentation history, not final evidence. No geometry collision or parity failure occurred.

## Reproduce

Requirements: Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge, Node.js with package-lock dependencies. Commands from this directory:

```text
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
blender --background --factory-startup --python-exit-code 1 --python author.py
python build.py
blender --background --factory-startup --python-exit-code 1 --python verify_source.py
blender --background --factory-startup --python-exit-code 1 --python verify_parity.py
blender --background --factory-startup --python-exit-code 1 --python verify_theme.py
node --test tests.mjs
python verify_browser.py
python verify_extended.py
python package_delivery.py
```

On this Windows host Blender is `C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe`; use native `C:/Program Files/nodejs/node.exe` if the shell shim requires a TTY. `build.py` uses local node_modules, otherwise the sibling Iceland dependency directory. These are build-time dependencies only. `initial/setup-lineage.py` is historical scaffolding, NOT a rebuild entry point; current author/viewer scripts are authoritative. Regeneration overwrites authored assets; copy manual edits elsewhere first. Packaging writes only in this folder and excludes node_modules, backups and caches. Source ZIP includes the standalone GLB, viewer and all required evidence.

## Scope

Local cosmetic inner collectible only. No chain node, key, wallet, mint, broadcast, deployment, VPS or production-site changes. Cosmetic opening does not change custody or break an on-chain seal. Not hosted, signed, minted or stored on-chain. The collection direction remains 201 equally one-of-one designs; no accessories or additional certificate NFTs. User waived individual art review for the batch. Branch backup is separate from integration; no merge is authorized here.

Lineage: Japan mechanism/viewer/test patterns and Iceland motion tests from local base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; Three.js license included. Research links are informational, not licenses to source imagery. Exact final bytes/hashes are recorded in the machine-generated inventory.
