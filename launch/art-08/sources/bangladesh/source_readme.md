# Bangladesh v1 — Jamdani & Tidal Delta

Open **bangladesh-v1.html** directly in Edge/Chrome. The complete 3D asset, runtime, four compact maps and actual-model poster are embedded. Drag/touch to rotate, open/close the lid, reset; reduced motion is supported. No server or network connection is required. Attachment apps may require saving the HTML and opening it in a full browser.

**HTML: 3,409,417 bytes. GLB: 1,975,836 bytes.** Strict standalone HTML limit: less than 5,000,000 bytes. The editable source and source archive are separate from that viewing payload.

## Design and provenance

An original composition combining a deep-teal, ivory-repeat **Jamdani-inspired textile inlay** with a shallow **tidal-delta lid**. UNESCO's description of Jamdani weaving around Dhaka and its Bangladesh Sundarbans entry inform the concept; exact citations and the measurable pre-model contract are in `design-brief.md`. No third-party photographs, texture scans or AI promotional substitutes are used. This is script-authored Blender geometry and independently generated maps, not hand sculpture or authentic woven cloth. The imaginary rigid finish is not a claim that textiles form a load-bearing box.

The wide hollow shell, brass articulation and pivot locations inherit the repository's trimmed Japan mechanism (local base commit `ff5d78f1e0d486af5c882c184fc08049996ebdc8`). The inherited mechanism's earlier lineage is Iceland v10. Japan's cedar, tree, moss and granite artwork are not reused. `mechanism.blend` is included so authoring does not read another preview. `art/vault-kit/` and all other preview directories are unchanged.

## Actually verified

- **Real Three.js GLTFLoader:** 21,472 triangles, 134 rendered meshes, 10 materials; zero nonfinite vertices, zero degenerate triangles, finite UVs. Four decoded 512×512 maps; actual color, green-channel roughness and normal variation checked. Ivory/teal motif populations are measured from the decoded map, not a label.
- **Saved-source reopening:** hollow interior floor ray at z=0.2650000155; ten explicit hinge attachment intersections. Original lid/latch pivot matrices match the independently opened included mechanism within 1e-8.
- **81 opening poses:** all 83 moving and 47 static source meshes sampled, including every new delta/border ornament; zero unintended surface intersections. Latch versus non-latch lid surfaces also tested. Only inherited mating hinge leaf/barrel and latch pin/knuckle/bridge bearing contacts are excluded. This is sampled surface collision evidence, not continuous collision freedom or mechanical certification.
- **Source/export parity:** independently reopened .blend compared bidirectionally with reimported GLB; maximum nearest-world-vertex error 1.712013073529306e-7 units, below the 1e-5 gate. All four maps are packed in source. This checks geometry positions, not byte-identical source serialization.
- **Theme:** four separate irregular islands, 67 lid ornament meshes under the lid, footprint/height bounds checked. Actual saved-source downward rays on a 101×61 interior grid find 1,517 visible water samples, all in one connected component reaching all four edges; water occupies 24.62% of that grid. This proves sampled visible connectivity, not geography or hydrology. A real loaded-island detachment is rejected by the runtime ancestry test, then restoration passes.
- **Offline desktop and touch-emulated mobile `file://`:** native click/tap open/close, mouse/touch drag, interrupted reset, reduced-motion snapping, no horizontal overflow, zero external HTTP(S) requests and zero successful-run console/runtime errors. Default full-open maximum absolute projected x/y NDC is 0.8923646517, within viewport.
- **Failure modes:** actual corrupt bytes reach GLTFLoader and produce the source poster with disabled controls; no uncaught page errors. No-JavaScript poster independently decoded and captured.
- **Delivery:** exact embedded GLB and poster bytes checked against standalone files; no external GLB buffers/images; required artifact set, SHA-256 inventory and every ZIP entry verified by readback. See `delivery-check.json` and `inventory.json`. No self-referential hashes.

Browser checks use installed Edge on an NVIDIA RTX 4060 with 390×844 mobile touch emulation and 1440×1080 desktop viewport. **No physical-phone performance, FPS, geographic accuracy, authentic craft replication or photoreal equivalence is claimed.** Source and browser lighting differ; source poster is not a pixel-equivalence reference.

## Bounded visual correction and real failures

The first version read as four isolated terrain tiles. One lid-only correction widened the landforms, lowered relief and made the banks irregular around narrower connected channels. `initial/poster.png` and `initial/mobile-closed.png` retain that earlier appearance; final actual-model desktop/mobile/lid-detail inspection found readable branching water and no severe defects. Remaining deliberate limits: angular miniature canopies, simplified enamel-like water, cropped edge motifs and substantial inherited family clasp. The open front view naturally hides the lid's exterior landscape. No water simulation or botanical species fidelity.

Two genuine **test-harness failures** are preserved, not represented as asset defects:
1. `initial/theme-channel-failure.txt`: the initial map test read red for every image. glTF packs roughness in **green**; correction samples the format's actual roughness channel (range 26), retaining a strict nonzero-variation gate.
2. `initial/pivot-harness-failure.txt`: an appended but unlinked Blender object's matrix was not evaluated. Correction independently opens and updates the baseline scene, copies its numeric matrices, then reopens the delivered source. The 1e-8 exact-pivot tolerance is unchanged.
The runtime detached-island negative control is an intentional post-implementation regression test, not test-first TDD. No collision or geometry gate was relaxed.

The optional Codex input lane exited with an authentication 401 before making any edits. No lane changes were accepted and no credentials were modified; Hermes authored and tested this deliverable directly.

## Files

- `bangladesh-v1.html`: standalone viewing artifact; `bangladesh.glb`: portable model.
- `bangladesh.blend`: named editable source; `mechanism.blend`: immutable mechanical seed.
- `maps/`, `maps.py`, `author.py`, `helpers.py`: reproducible procedural art.
- `poster.png` / `.jpg`: actual saved-source render, not promotional art.
- `desktop-closed.png`, `desktop-open.png`, `desktop-lid-detail.png`, `mobile-closed.png`, `mobile-open.png`, `mobile-fallback.png`, `mobile-nojs.png`: actual browser evidence.
- `*-check.json`, raw `*-output.txt`, `verification-output.txt`: executed gates and bounded evidence.
- `bangladesh-v1-source.zip`: explicit required files, source/maps/runtime, evidence and inventory. Excludes itself, delivery-check, aggregate transcript, caches and dependencies. `delivery-check.json` identifies the archive separately.

## Reproduce

Dependencies: Blender 5.2.1, Python with numpy/Pillow/Playwright and installed Edge; Node.js with Three 0.180.0 and esbuild 0.25.11. Build uses this folder's `node_modules` if installed, otherwise the read-only sibling Iceland pilot dependency link. For an extracted archive, run `npm install --no-audit --no-fund` here. All runtime dependencies are already embedded; this tooling is for rebuilding only. Three's MIT license is included.

From this directory:

```text
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python verify_all.py
```

`verify_all.py` independently runs build, motion tests, saved-source/collision, parity, source/runtime theme, browser/fallback and delivery gates. Set `BLENDER` to another executable path if needed. It does not regenerate the source; the author command does. Manual changes should be made in a separate source copy because authoring overwrites generated files. No dependency directory is archived.

## Scope

Local collectible art only. Cosmetic opening does not open an on-chain seal. Not minted, signed, hosted, deployed, chain-admitted or custody-verified. No blockchain nodes, keys, mint code, chain queries, transactions or VPS work. Only `preview/bangladesh-v1/` is added, committed and backed up on `art/bangladesh-v1`; no merge. Human per-asset review is waived for this batch, not evidence of user visual approval. Collection remains 201 equally one-of-one designs (195 countries, five oceans, Moon); accessories are deferred.
