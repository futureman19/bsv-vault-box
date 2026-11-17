# Jordan v1 — Wadi Rum / Rose & Ochre

Written before authoring. A landscape-inspired collectible, not a replica of a monument, geological survey or comprehensive representation of Jordan. No existing Jordan concept art was supplied. The primary reference is the documented landform vocabulary below; all geometry and maps are independently procedural, with no third-party image pixels embedded.

## Research
- UNESCO World Heritage Committee, decision 35 COM 8B.15: https://whc.unesco.org/en/decisions/4286 — Wadi Rum's sandstone mountains, valleys, natural arches, narrow gorges, towering cliffs and honeycomb weathering. Retrieved via web search for this brief.
- UNESCO nomination geology: https://whc.unesco.org/document/167435 — red-brown Umm Ishrin sandstone, vertical joints and water-widened siq gorges; rounded columns and varied sandstone summit silhouettes.
- IUCN/UNESCO geological supplement: https://whc.unesco.org/document/167436 — sandstone sequence above Precambrian granitoids, incision and isolated massifs. Research informs an imaginative miniature, not literal stratigraphic reconstruction.

## Frozen visual contract
- Wide keepsake silhouette: 3.72 X by 2.38 Y lid, 0.30 lid thickness, body exterior from z=0.10 to 1.56. Continuous hollow inherited five-sided interior. Four low stone feet. Front -Y, back +Y, right +X; glTF maps (X,Z,-Y).
- Rose/ochre sandstone body, restrained cream sediment wisps and fine grain: dominant map RGB around (166,88,57), ochre (194,126,69), cream (210,165,112). Compact 512x256 color/roughness maps, no photographs, scans or painted landmarks. Broad strata vary slowly and irregularly, with subordinate fine texture.
- A satin dark-red stone lid carries two irregular vertically fluted sandstone massifs separated by a visible open siq gap; a real raised stone arch spans a smaller gap toward the rear/right. Summit height <=0.90 above the lid. Mesh relief, not an image plane. Warm sandy lid inset under the terrain with a darker winding recessed-looking valley strip (stylized inlay, not a physically excavated canyon).
- Terrain within X +/-1.55, Y +/-0.95; every terrain mesh directly parented to Lid_Hinge. The sandstone arch has real open air below its bridge. No religious inscriptions, flags or invented historical claims. Interior and gold hardware are contemporary BoxSV family extrapolations.
- Thin dark umber seam below the lid; rear seam kept away from hinge sweep. Small warm brass corner protectors, inherited functional latch/pins/rear hinge attachment geometry and medallion.
- Exact inherited pivots: Lid_Hinge and child Latch_Pivot. First 25% of motion releases latch 80 degrees, remaining 75% opens lid 105 degrees. Collision-test all moving vs static meshes and latch vs lid at 81 poses. Only the explicit mating bearings may be excluded.

## Acceptance gates
- Reopen packed .blend independently; hollow floor ray, ten hinge attachment pairs, complete motion collision sampling, source/export world vertex parity within 0.00001.
- Actual GLTFLoader finite vertices, zero degenerate triangles, textured sandstone map variation, terrain lid ancestry, physically open arch and siq gap checked in source and normal-view captures.
- Native offline file:// desktop + 390x844 mobile touch controls: rotate, open/close, interrupted reset, reduced-motion, corrupt-model poster fallback, no-JS poster, no external network, errors or overflow. Mobile is emulation, not phone performance.
- Standalone HTML strictly <5,000,000 bytes with embedded runtime/GLB/actual-source poster. Inventory exact bytes and SHA-256; required deliverable set asserted.
- Failures retained if encountered, no blanket geometric exclusions or byte-budget relaxation. At most two bounded aesthetic corrections; technical defects corrected to pass.
- README separates technical acceptance from stylized appearance. No photoreal equivalence, custody, minting, hosting or on-chain storage claims. User waived per-asset review; finish this one asset only.
