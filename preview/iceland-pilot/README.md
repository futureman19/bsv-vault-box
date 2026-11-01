# Iceland / Basalt — local 3D collectible pilot

Open **iceland-pilot.html** directly in Edge/Chrome. No server, installation, CDN, wallet or internet connection is needed. JavaScript and WebGL are required for 3D; the actual-model poster remains available if loading fails. Mobile attachment apps may require saving the HTML and choosing a browser rather than their restricted preview pane.

This is **one inner collectible, not the outer BoxSV custody container**. Open lid is a reversible cosmetic demonstration, not opening a seal or making a transaction. Not minted, signed, hosted, chain-admitted or production ready. No keys, nodes, wallets or sale systems were accessed.

## Delivered visual

- `iceland.blend`: independently reopened editable Blender 5.2.1 source; named wall, basalt, lid, mineral and hardware meshes. Studio lights/camera/floor are source-only.
- `iceland.glb`: actual mesh geometry, hollow continuous inner shell, floor, lid inner face, brass hardware and mineral lines. No texture downloads or image planes.
- `poster.png`: 1500 × 1200 render of this source model, not the AI reference.
- `reference-original-basalt.png`: separate, unchanged approved original AI concept. Inspiration, not a texture or exact reconstruction. The unseen interior and mechanism are authored interpretations.
- `iceland-pilot.html`: self-contained bundled Three.js viewer, GLB and poster embedded; drag/touch rotation, zoom, lid toggle, reset and reduced-motion behavior.
- `desktop-closed.png`, `desktop-open.png`, `mobile-closed.png`, `mobile-open.png`, `mobile-fallback.png`: final actual browser screenshots.
- `manifest.json`, `asset-identity-proposal.json`: exact SHA256/byte identities, actual-loader geometry metrics and storage proposal.
- `iceland-pilot-source.zip`: source, assets, offline viewer, references and evidence. Excludes node_modules, secrets, caches and .blend1.

The asset is procedurally authored editable geometry, not hand-sculpted or exact image-to-3D reconstruction. Wide, low rectangular proportions replace the rejected tall-cube direction. Faceted basalt is intentionally stylized; final mineral microdetail, optimized material batching and real phone performance remain future art/engineering work.

## Mechanism and checks

`Lid_Hinge` rotates about its rear local X axis, 0 to −105°. `Latch_Pivot`, a lid child, rotates 0 to −80° during the first quarter of progress; only then does the lid move. Reverse motion closes the lid before lowering the hasp. The camera gently reframes the opened silhouette. Reset cancels motion and restores camera and closed pose. Reduced motion snaps immediately.

- `tests.mjs`: tests authored before `motion.mjs`. `test-red.txt` records the genuine missing-module failure; `test-negative-zero-red.txt` records a subsequent endpoint failure, corrected without relaxing the test; `test-green.txt` records the pass.
- `source-check.json`: independent saved-.blend reopen; named pivot hierarchy, floor ray, and 81 sampled poses checked with evaluated mesh BVH intersections. Moving parts checked against static body and latch against lid. Explicit mating bearing contacts excluded. This is a bounded sampled collision test, not continuous mechanical/manufacturing certification.
- `browser-check.json`: actual GLTFLoader parse, finite bounds/vertices, triangle/material counts and no zero-area triangles. Offline file:// desktop and mobile emulation, pointer/touch rotation, open/close, interrupted reset, reduced motion, zero external HTTP requests, zero JS errors and no horizontal overflow. Full open silhouette projection tested within viewport at reset camera.
- Corrupted embedded GLB bytes were supplied to the actual parser; its caught failure showed the poster and disabled model controls. The error is expected and recorded separately from unhandled JS errors.
- Initial visual QA found clipped open-lid framing. `initial-open-clipped.png` and `framing-debug.png` retain earlier imperfect views. Final screenshots and projection checks supersede them. The full open silhouette now fits. User-directed extreme zoom/rotation may intentionally crop the model; Reset restores tested framing.
- Tests ran in Edge on an NVIDIA RTX 4060. Mobile viewport/touch emulation is **not a physical-device performance result**. No FPS, production readiness, wallet compatibility or chain support is claimed.

## Identity / storage decision

Proposal: identify the immutable model version by `sha256:<GLB bytes hash>` and bind the poster and source archive separately by their exact hashes. Keep logical collectible identity distinct from an asset-version hash, which changes when art bytes change. Hashes prove byte integrity, not issuer identity, authenticity, availability or ownership.

**Storage choice NOT YET IMPLEMENTED:** content-addressed off-chain model and poster (IPFS with separately funded independent pinning, plus HTTPS archival mirrors); retain editable source and source ZIP off-chain. A future issuance record could commit to these exact hashes/URIs after real art admission and retrieval/recovery tests. There are currently no CIDs, uploads, persistence guarantees or on-chain art bytes: all supplied media are local only. No certificate was signed. Future certificates are signed records, not additional NFTs.

Approved launch direction remains 201 one-of-one Boxes: 195 countries, five oceans and the Moon, all identical edition scarcity. Accessories belong to a later separate collection. This pilot is not a launch allocation, sale or custody proof.

## Rebuild / recheck

Commands from this directory (Windows native paths; Python is `python`):

```text
npm ci --no-audit --no-fund
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python verify_source.py
node --test tests.mjs
python build.py
python verify_browser.py
python package_delivery.py
```

`build.py` currently uses the Windows x64 esbuild binary. Browser checks need Python Playwright and installed Edge. These are build/test dependencies only; the delivered HTML needs none of them. `npm ci` restores the exact lockfile dependency graph; Three.js MIT license is included. Regenerating `author.py` outputs overwrites manual edits to the .blend, GLB and poster; save edited variants separately.

`manifest.json` hashes payload files except itself and packaging envelopes (to avoid circular hashes). ZIP inventory is exactly the payload plus manifest; `delivery-check.json` records verified archive inventory and ZIP/manifest hashes. The ZIP and copied output files are read back and compared byte-for-byte. No public website files were modified or deployed.
