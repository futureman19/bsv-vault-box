# Namibia / Namib Dune Sea — v1

Open **namibia-v1.html** directly in Edge/Chrome. It embeds the model, runtime, maps and an actual Blender-rendered poster. Drag/touch to rotate, Open/Close lid, Reset view. No server or network is required. This is a local art asset, not a minted or hosted NFT; the lid action does not change custody.

## Delivered
- Standalone HTML: **2,922,315 bytes**, below the strict 5,000,000-byte cap.
- GLB: **1,649,960 bytes**; actual GLTFLoader: **21,800 triangles, 60 meshes, 8 materials**.
- `namibia.blend`: editable, packed Blender source; `mechanism.blend`: unchanged trimmed family mechanism copied from Japan v1 at repository base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`.
- `author.py`, `maps.py`, three 512×512 procedural maps and reproducible viewer/test scripts. No scans, borrowed photographs, AI promotional substitutes or claims of hand sculpture.
- `poster.png` / `poster.jpg`: actual source render. Desktop/mobile closed/open, rear-open, corrupt-input and no-JS screenshots: actual offline browser captures.
- `inventory.json`: exact byte/SHA-256 inventory. `delivery-check.json`: inventory and source ZIP readback verification. `namibia-v1-source.zip`: source, viewer, GLB, maps, license, evidence, explicit required files; excludes itself and inventory envelopes as documented below.

## Design and visual result
The brief was written before modeling, using UNESCO's [Namib Sand Sea description](https://whc.unesco.org/en/list/1430/). Three curved, asymmetric orange dune crests and an irregular pale playa travel on the lid. The body is an invented mineral keepsake-box interpretation, not an assertion of traditional Namibian box-making or a model of an exact location. The broad family silhouette, satin brass hardware, medallion, side ring and dark mineral feet are retained. No third-party imagery is embedded.

Final desktop/mobile inspection found the pale pan readable, three dune forms discernible and the whole closed/open silhouette in frame. **Stylized, not photorealistic:** smooth dunes are regular and simplified, body ripple texture can read as wood grain, the pale pan is a shallow inlay rather than a deep excavation, and the dark seam is conspicuous. The lowest dune is shorter to expose the pan. Dune feet blend into a thin lid sand field; fine relief joins are not natural geological reconstruction. The wide lid measures 3.72×2.38×0.30 units; body shell height is 1.46, with the closed main box spanning approximately 1.9 including the rim/lid (feet excluded). Render lighting changes the apparent palette; authored material colors are not promised as screenshot pixel values.

## Verified, with explicit limits
- Saved source independently reopened; both family pivot locations exactly retained. `Lid_Hinge` at `(0,1.32,1.668)`; `Latch_Pivot` local `(0,-2.61,0.22)`, a lid child. 80° latch release during first quarter, then 105° lid opening; reverse closes lid first.
- **81 sampled poses, all 21 moving and 39 static meshes, zero unintended surface intersections.** Also checks releasing latch against the lid and all new relief. Only matching moving-hinge-leaf/fixed-barrel and latch-knuckle/bridge/pin bearing pairs are exempt. Ten hinge attachment pairs intersect as intended. Interior floor ray hits z=0.2650000155. This is sampled surface-intersection evidence, not continuous collision, volume-containment proof or manufacturing certification.
- Source/export bidirectional nearest-vertex maximum error **1.712013073529306e-7 units**, below 1e-5. Geometry parity is not a claim of identical Blender/Three lighting or whole-file byte equality.
- Three raised ridge meshes have measured height approximately .240/.383/.518; curved crests span >.19 along Y. All ridges and the playa are lid children. Seven of seven source-hero rays see the pan. All three packed maps exist; actual GLTFLoader decodes color/normal/roughness maps with nonzero variation (46/14/32 channel range respectively), finite UVs, zero nonfinite vertices and zero degenerate triangles.
- Offline **file://** Edge: desktop 1440×1080 and 390×844 touch emulation. Native open/close, pointer/touch drag, reset during motion, reduced motion, no overflow, no external HTTP requests and no normal-run JS errors. Maximum opened projection |NDC| ≈ .8924. Actual corrupt bytes reach GLTFLoader, disable controls and display the poster; no-JS poster decodes. RTX 4060 desktop rendering, **not physical-phone or FPS/performance certification**.
- Motion unit tests reject missing lid, empty geometry and nonfinite bounds. A separate post-implementation negative control removes a real ridge from the reopened source in memory and must fail the theme test. It does not modify the source. This is regression evidence, not claimed test-first TDD.

## Actual failures and correction
1. Optional Codex lane returned HTTP 401 before editing. No Codex work accepted; Hermes authored and ran all tests directly. No credential store was read or changed.
2. First Blender export hit `MemoryError` on a host reporting 97% memory use. Original failure retained in `initial/author-memory-failure.txt`; bounded rerun with two Blender threads succeeded. No unrelated processes were killed.
3. First source render showed the pan only as an occluded sliver (`initial/pan-occluded-poster.png`). One visual correction shortened the foreground dune and moved/enlarged the playa into its exposed right-hand gap. Final source visibility: 7/7 sampled pan rays; mobile screenshot independently inspected.
4. First extended check incorrectly sampled the red channel of glTF's roughness texture and failed. Corrected it to the standard green channel; retained nonzero-variation assertion, no geometry or size gates weakened. Failure retained in `initial/roughness-channel-failure.txt`.

## Reproduce
Dependencies: Blender 5.2.1; Python with numpy/Pillow/Playwright; installed Edge; Node with pinned Three 0.180.0/esbuild 0.25.11. Runtime Three MIT license is included. Scripts are relative to this directory; the Blender executable defaults to the current Windows install and can be overridden via `BLENDER`. Build uses local `node_modules`, otherwise sibling `iceland-pilot/node_modules`; in an extracted source archive run `npm install` here. No dependency directory is embedded or committed.

From this directory:

```text
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --threads 2 --factory-startup --python-exit-code 1 --python author.py
python run_checks.py
python package_delivery.py
python package_delivery.py --verify
```

`run_checks.py` rebuilds the viewer but does not regenerate geometry; it reopens the saved source, runs motion/collision/theme/parity/browser checks and the missing-ridge negative control. Regenerating authoring overwrites the source, so preserve manual edits separately. Repack after any changes: inventory deliberately excludes itself, delivery-check and ZIP to avoid circular hashes. ZIP includes the inventory; readback compares every entry with original bytes and asserts required deliverables. The delivered HTML is the same in-folder file exercised by browser tests, not an untested external copy.

All additions are scoped to `preview/namibia-v1/`. No shared kit, other previews, production site, wallet, blockchain node, keys, funds, minting, chain queries, VPS or deployment were touched. Branch backup only; no merge. Collection direction remains 201 equally one-of-one designs, with storage/issuance independent of this local art deliverable. Human per-asset review is waived for this batch; technical acceptance does not imply user visual approval or launch readiness.
