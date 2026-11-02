# Guinea-Bissau v1 — Bijagós Tidal Mangrove

Open `guinea-bissau-v1.html` directly in Edge/Chrome: complete embedded 3D model, runtime, procedural maps and actual-source poster. Drag/touch to rotate; Open/Close lid; Reset view. This is a cosmetic inner collectible, not the custody container. Nothing minted, broadcast, deployed or merged.

## Design and visual outcome
The pre-model `design-brief.md` cites UNESCO's Bijagós landscape descriptions. Four asymmetric sandy islands, teal tidal channels, three mangrove trunks and fifteen exposed prop roots form a miniature lid landscape. Every landscape part travels with the lid. Brown ripple-textured shell, small satin brass fittings and a dark teal seam retain the wide family silhouette. No third-party photographs, sacred motifs or invented traditional box-making claims.

Actual Blender poster, desktop/mobile closed/open captures and rear-open capture were visually inspected. The collectible is coherent and mobile-readable with no obvious clipping. **It is stylized, not photorealistic or geographically exact.** The brown sediment-inspired material reads more like wood grain than mud; water reads like decorative resin, islands are simplified, and foliage is rounded/flattened rather than botanically detailed. The roots convey mangroves, especially with the title. Those are disclosed art limitations, not claims of reference equivalence. No original country concept image was supplied; this is a brief-led interpretation. Human per-asset art review was waived for the collection batch, not silently claimed.

## Verified
- Build output and exact byte/hash inventory are recorded in `gate-0.txt`, `inventory.json` and `delivery-check.json`; HTML is strictly below 5,000,000 bytes.
- Actual GLTFLoader: 17,780 triangles, 108 meshes, 11 materials; zero nonfinite vertices and degenerate triangles. Three portable decoded maps are 512×256 with nonzero variation.
- Independently reopened `.blend`: hollow floor ray z=0.2650000155; ten hinge attachment contact pairs. **81 poses, all 69 moving meshes and 39 static meshes, zero unintended sampled surface intersections.** Releasing latch is also checked against lid ornaments. Only named mating bearing contacts exempted. Sampled surface intersections are not continuous collision, volume-containment or manufacturing certification.
- Source/export world-vertex nearest-distance parity maximum 1.712013073529306e-7 (<1e-5), both directions. Three packed source images. This is geometric parity, not byte-identical independent re-export certification.
- Four islands, three trunks, fifteen prop roots, all 53 terrain/vegetation meshes parented to lid; rear/right trunk positions and height checked. Roots penetrate island surface by measured 0.021–0.058 units. Deliberately detaching an island is correctly rejected by the same validator; not a fabricated historical failure.
- Motion unit tests enforce latch first (80°), lid second (105°), endpoint clamping and malformed-asset rejection.
- Edge offline `file://`: desktop 1440×1080 and touch-emulated mobile 390×844; real buttons, drag/touch rotation, opening/closing, interrupted reset, reduced motion, no horizontal overflow, no HTTP requests or successful-run JS errors. Full-open projected maximum absolute NDC about 0.892365. Actual corrupt GLB triggers parser fallback; no-JS poster tested.
- Mobile is emulated on desktop NVIDIA RTX 4060, not physical-phone or FPS validation.

## Reproduce
Blender 5.2.1; Python with numpy, Pillow, Playwright; installed Edge; Node and the existing Three/esbuild dependencies. Build resolves local `node_modules`, otherwise sibling `iceland-pilot/node_modules`. A standalone source extraction requires installing the included package dependencies. No runtime network dependencies. `BLENDER` and `NODE` override test executable paths on other hosts; build's Node invocation must be available on PATH.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python check_all.py` — rebuilds HTML and reruns every acceptance check, logs exact commands/exit codes.
4. `python package_delivery.py` — explicit artifact inventory, source ZIP readback and offline archived HTML check.

Source regeneration overwrites authored outputs. `mechanism.blend` is the included trimmed Japan-family mechanism, not a full previous country model; the shared vault kit and all sibling pilots remain untouched. Viewer/mechanism/check lineage is the local base commit ff5d78f1e0d486af5c882c184fc08049996ebdc8. Three runtime license is included. Editable source remains named and packed.

## Failure honesty and scope
Optional Codex lane failed token refresh (401) before producing edits; Hermes authored and verified this asset directly. No credential repair was attempted. An initial motion-test command hit the Windows Node shell shim and then a missing copied test file; fixed by using native Node and copying the existing Iceland tests. A subsequent browser run failed a 60ms fixed sleep after Reset; its raw failure is retained in `initial-browser-frame-wait-failure.txt`. The harness now waits for the actual reset state with a bounded one-second timeout rather than assuming frame scheduling. No viewer behavior, geometry, collision or byte gate was weakened. The detached-island and corrupt-GLB negative controls are explicit regression probes, not test-first historical failures.

Local files/branch backup only. Source/hash identities do not imply authenticity, hosting, availability, on-chain storage, ownership or custody verification. The 201 one-of-one collection scope is unchanged. Integration is a separate final card; this branch must not be merged by this task.
