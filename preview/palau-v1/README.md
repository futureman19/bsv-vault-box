# Palau v1 — Rock Islands & Lagoon

Open **palau-v1.html** directly in Edge/Chrome. This self-contained art preview embeds its real 3D model, textures, runtime and source-rendered poster. Drag/touch to rotate, Open/Close lid, Reset view. Reduced motion snaps immediately. No server or network is needed.

## Delivery
- Standalone HTML: **2,532,972 bytes**, strictly below 5,000,000.
- Standalone `palau.glb`: **1,322,992 bytes**.
- `palau.blend`: packed editable Blender source; `mechanism.blend`: included inherited family articulation/interior baseline.
- `maps/`: four original generated 384×384 images, not scans or copied photographs.
- `poster.png` / `poster.jpg`: actual source render, not AI promotional imagery.
- `desktop-closed.png`, `desktop-open.png`, `desktop-open-rear.png`, `mobile-closed.png`, `mobile-open.png`, fallback captures: actual offline browser screenshots.
- `palau-v1-source.zip`, `inventory.json`, `delivery-check.json`: explicit required-artifact inventory, exact bytes/SHA-256 and ZIP readback verification. No dependencies, backup .blend1 files, credentials or unrelated paths are archived.

## Design and visual result
The research-backed contract was written in `design-brief.md` before modeling. UNESCO's description of Palau's forested limestone islands and protected lagoon informs a pale coralline-limestone-inspired body, turquoise inset and six original island miniatures. This is not a map, a replica of a named island, traditional craft reproduction, sacred motif or geographic survey. No third-party photographs are embedded.

The family brass hardware and exact hinge/latch pivots are retained. The 80-degree latch release precedes the 105-degree lid opening. Water and all island geometry travel with the lid. A separate narrow teal reveal makes the seam legible; it can look like a slightly raised lid rather than a tight stone join. The hollow interior and hinge attachments remain visible when opened.

**Visual limitations:** intentionally stylized. Forests are mottled low green crowns rather than individual trees; limestone shores are simple pale undercut bands, not eroded photoreal cliffs. The water reads as turquoise enamel/resin, not simulated transparent ocean. Bright studio lighting shifts greens toward sage. The stone body is subtly mottled and could also read as ceramic. The inherited clasp is long and decorative; no manufacturing or real-lock certification is claimed. A low-sample source poster retains some render noise. One bounded correction exposed more pale shoreline; earlier screenshots remain in `initial/`. Actual mobile/open screenshots were inspected with vision, with no obvious detached islands, broken geometry, frame clipping or layout overflow. Passing technical gates does not establish photorealism or cultural/geographic completeness.

## Verification actually executed
- Saved `.blend` independently reopened: hollow floor ray at **z=0.26500001549720764**; ten explicit hinge attachment pairs intersect.
- **81 sampled staged poses**, all **23 moving and 39 static meshes**, no unintended surface intersections. All six islands and lagoon included. Only inherited mating bearing contacts are excluded. Sampling is not a continuous collision proof; intentional within-lid ornament/lagoon overlap is not mechanical interference.
- Source/export evaluated-vertex nearest-distance parity in both directions: **1.712013073529306e-7**, below the **1e-5** tolerance. Four packed source maps.
- Actual Three GLTFLoader: **16,056 triangles, 68 runtime meshes, five materials**, zero nonfinite vertices and zero degenerate triangles. Multi-material island meshes split into primitives in glTF; six source island assemblies retain lid ancestry.
- Independent theme assertions: six islands, original pivots unchanged, maximum terrain z **2.566999912261963**, island bases embedded in lagoon, footprint/height limits, sampled clear lagoon lanes. Detaching an island deliberately fails the ownership gate.
- Motion unit checks: 81 poses, staged endpoints and clamps; three invalid asset inputs deliberately rejected.
- Offline `file://` Edge at **1440×1080 desktop** and **390×844 mobile touch emulation**: native Open/Close, mouse/touch drag, interrupted Reset, reduced motion, no horizontal overflow, zero external HTTP requests and zero runtime errors. Full-open projected geometry fits; max absolute NDC approximately **0.912**.
- Actual corrupt-GLB parser error invokes visible poster and disables controls; no-JS poster loads. Portable color and roughness maps decoded in the browser, with roughness read from glTF GREEN. Poster checked nonblank/opaque.
- These browser tests ran on desktop NVIDIA RTX 4060 / Edge. **Not physical-phone performance testing**, an FPS benchmark or a mobile attachment-app compatibility promise.
- `acceptance-check.json` records canonical verifier exits; individual reports retain measured details. `initial/README.md` documents the actual missing-toolchain and shell-shim failures and fixes. No asserted acceptance threshold was relaxed. Optional Codex failed authentication before implementation; Hermes implemented and tested this asset directly.

## Reproduce
Dependencies: Blender 5.2.1; Python with numpy/Pillow/playwright; Edge; Node with the pinned `package.json` dependencies. The requested sibling dependency directory was empty, so this folder uses its own untracked `node_modules`. From this folder:

```text
npm ci --ignore-scripts --no-audit --no-fund
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python verify_all.py
python package_delivery.py
```

`BLENDER_EXE` can override the verifier's executable. `build.py` embeds all runtime data and prints HTML_BYTES and GLB_BYTES. Windows Node is invoked by explicit native executable in the test wrapper to avoid a non-TTY shell shim. Source generation needs only this folder's included mechanism and scripts. `setup_pipeline.py` is historical scaffolding that reads the sibling Japan pilot: **do not rerun it for normal reproduction**, as it resets copied sources. Regeneration overwrites the generated source/model/poster; preserve manual changes separately and refresh checks/inventory after rebuilding.

## Scope and provenance
Mechanism/viewer/test lineage: Japan Cedar v1 in repository base `ff5d78f1e0d486af5c882c184fc08049996ebdc8`; Three.js 0.180.0 MIT license included. Palau maps/geometry were procedurally authored in Blender, not hand sculpture or scans. The whole collectible is one cosmetic inner Box in the proposed 201 equally one-of-one collection, not the outer custody container. Cosmetic opening does not change any seal or custody state.

Local art plus authorized branch backup only. **Not minted, deployed, hosted, signed, chain-stored or production-certified.** No blockchain node, keys, wallets, chain queries, funds, vault code, shared art kit or other preview content was changed. Storage/pinning and token issuance remain separate unimplemented work. User waived per-asset human review; final collection integration/review belongs to its separate dependent card. Do not merge this branch as part of this asset delivery.
