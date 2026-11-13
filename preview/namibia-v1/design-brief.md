# Namibia / Namib Dune Sea — v1 design contract

Written before modeling. Landscape-led original collectible; no pre-existing Namibia concept image is asserted. Primary reference is the landform description, not copied photographic pixels.

## Research
UNESCO World Heritage Centre, [Namib Sand Sea](https://whc.unesco.org/en/list/1430/), describes extensive shifting coastal fog-desert dunes, ancient semi-consolidated and younger active dune systems, and associated playas. Retrieved through web search for this task. Its description supports a dune-and-pale-pan composition, not any claim of historic Namibian box-making. No third-party photos/textures are embedded. This is one landscape interpretation, not a representation of all Namibian cultures.

## Measurable visual contract
- Theme: **Namib Dune Sea**. Wide keepsake body, approximately 3.72 wide × 2.38 deep × 1.9 body height (family dimensions). Warm burnt-orange mineral body, satin dark reddish lid rim, low sculpted dune crests above lid, pale ivory playa inset. No cedar, moss, glacier, sacred motifs or national-symbol shortcuts.
- Procedural portable sand base-color and roughness/normal maps, maximum 1024 per dimension, fine ripples subordinate to broad ochre/red-orange color. Palette targets sRGB terracotta #AA542D, dune orange #CE773B, shaded rust #763B28, pale pan #DDD0AA. Source material colors within artistic tonal variation; lighting not asserted to preserve pixel swatches.
- At least three distinct curved asymmetric dune ridges; actual raised geometry, not a painted flat image. Lid relief height 0.15–0.65 above its top. One irregular pale basin between the ridges, clearly legible from the hero view. All relief parents to Lid_Hinge and moves with it. Avoid a rectangular raised terrain platform.
- Brushed aged brass family latch, medallion and compact corner fittings, low dark mineral feet; continuous hollow five-sided inner shell. Narrow dark umber seam no more than 0.10 high. Mechanical inheritance is documented, not a claim of manufactured operability.
- Coordinate convention: front -Y (latch), back +Y (hinges), right +X, up +Z; glTF (X,Z,-Y). Preserve source family Lid_Hinge and Latch_Pivot locations and staged 80-degree latch release before 105-degree lid opening; the latch remains a lid child.
- Sample 81 evenly spaced motion poses against every static mesh plus latch-vs-lid surfaces, including all new ornaments. Exempt only named intentional bearing mates. Require no unintended surface intersections, connected hinges and an interior floor ray.
- Actual saved .blend reopened independently; source/export world vertices within 1e-5. Actual GLTFLoader checks finite vertices, nondegenerate triangles and decoded maps; lid ancestry and relief geometry asserted.
- Actual source render supplies poster. Offline file:// desktop and emulated mobile: open/close, drag/touch rotation, interrupted reset, reduced motion, corrupt GLB and no-JS poster, zero external runtime requests/errors/overflow. Full opened silhouette fits the default viewport. Emulation is not phone performance.
- Complete standalone HTML strictly below 5,000,000 bytes with all GLB, runtime and poster embedded. Delivery inventory records exact bytes and SHA-256, excluding itself to avoid recursive hashing.

## Acceptance and limits
Machine checks must assert real geometry/behavior and fail on missing or invalid data. Preserve actual failures and document fixes; never invent a red run. Inspect actual desktop/mobile screenshots as a separate visual gate. No photoreal equivalence, geographic survey, real materials, physical engineering certification or chain functionality is promised. Maximum two focused visual corrections after first render. Per-asset human review waived by task; stop when gates pass.
