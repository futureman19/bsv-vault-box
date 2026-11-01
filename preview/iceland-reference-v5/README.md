# Iceland reference v5 — structural reconstruction, not exact photoreal match

Open `iceland-reference-v5.html` directly. It contains the runtime, GLB, PBR images and actual-model JPEG fallback, with no remote assets. Do not confuse the promotional reference with the interactive model.

## Visual acceptance / remaining gaps

| Requested correction | Final status |
|---|---|
| Rich black glossy obsidian lid | Black PBR material and polished response present; promotional reflection quality not reproduced exactly. |
| Organic blue river integrated into lid | Actual boolean-cut shallow channel and inset blue mesh plus short left-edge cascade. Broader than prior scratch; still simplified regular banks. |
| Raised glacier at rear, moving with lid | Asymmetric low triangulated ice ridge, 0.267 above lid, glTF transmission 0.36, attached to Lid_Hinge. Reads as stylized ice, not photoreal crystals. |
| Broken basalt and recessed moss | 72 separately fractured blocks with irregular width/strata/recesses; 212 smooth-shaded moss clumps tucked into ledges. Major breaks are geometry, not painted noise. Moss still clumpy and rock weathering much coarser than reference. |
| Wrapped brass corners and hardware | 24 shaped top/side sheet pieces, fasteners, lower guards, original staged clasp, plain medallion and side rings. Categories match; clasp/guard profiles and ring shape are not exact. |
| Proportions and camera | Original wide baseline retained; left-front camera instead of prior opposite side. Actual model remains shorter/squatter than promo. Comparison equalizes object WIDTH without warping proportions; camera is a comparable estimate, not calibrated exact recovery. |
| Articulation and hollow interior | Original motion module unchanged; physical rear wall-to-bearing mounting bridges and stems added. Hollow floor ray and sampled clearance pass. |

**Final visual audit: recognizable substantial structural reconstruction; NOT exact-match or photoreal-reference complete.** Back/interior are authored extrapolations. No third art iteration after two focused corrections. First render retained in initial-review; first correction in review-one. Second correction adds subtle compact stone PBR maps, smooth growth shading, and lower browser environment intensity so the lid reads black. Subsequent rear mounting support work is mechanical verification, not another art iteration. Studio/browser lighting differs, explicitly; surfaces are the same portable exported materials and geometry.

## Verified

- Initial missing-source RED gate retained; final independently reopened source feature test passes.
- 27,289 triangles, zero degenerate/nonfinite triangles through actual browser GLTFLoader; 378 meshes, 15 materials.
- Source vs imported GLB bidirectional nearest world-vertex deviation: 0.0000001713 maximum. This is evaluated geometry-position parity, not byte-identical mesh topology or UV-corner proof.
- Packed source 128px color JPEG, roughness JPEG, normal PNG; real loader decodes color/normal/roughness maps and ice transmission. No photographic scans or large blurry maps.
- 81 staged-motion BVH surface-intersection samples, all moving parts including glacier/river/straps tested; zero unintended intersections. Exclusions only original explicit mating hinge leaf/barrel and latch bearing pairs. Sampling is not continuous collision/solid-volume proof.
- Ten explicit BVH intersections prove wall→bridge→fixed mount→bearing stem→barrel attachment and moving leaf→lid connection for both rear hinges.
- Offline file:// Edge desktop and 390×844 mobile-emulation: rotate/touch-drag, reset, open/close, interrupted reset, reduced motion, full-open framing, no overflow, no remote requests or console errors.
- Real corrupt embedded GLB causes poster fallback; no-JavaScript retains poster/disabled controls. Mobile test runs on desktop RTX 4060, not a physical phone; no performance claim.
- Old v1–v4 files and primary reference SHA-256 snapshot checked unchanged. Nothing deployed, pushed, minted or connected to funds.

## Reproduce

Dependencies: Blender 5.2.1, Node with `npm ci` here (or existing ../iceland-pilot/node_modules), Python with Pillow and Playwright, installed Edge.

1. `python textures.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. Same Blender invocation for `test_features.py`, `verify_source.py`, `verify_parity.py`.
4. `python build.py`
5. `python verify_browser.py` and `python verify_extra.py` (the latter uses primary reference at its recorded active-profile path).
6. `python package_delivery.py`

Regeneration overwrites v5 outputs and manual edits in its source. Baseline helper source is bundled as `baseline_author.py`, not fetched from prior files. Source ZIP excludes backups, caches, dependencies, and itself. `inventory.json` gives bytes/SHA-256; `delivery-check.json` verifies ZIP and delivered bytes without self-referential hashes. Full offline HTML is the budgeted artifact; blend/source archive are separate downloads.
