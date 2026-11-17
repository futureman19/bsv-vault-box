# Samoa / Siapo & Lava — pre-model visual contract

This written brief is the primary design reference; no supplied or approved illustration exists for Samoa. Written before authoring. One stylized collectible, not a replica of an heirloom or an ethnographic claim.

## Research and interpretation
- Te Papa, *Siapo (tapa cloth)*: https://collections.tepapa.govt.nz/object/531809 — identifies Samoan siapo as paper-mulberry barkcloth, assembled sheets, freehand or relief-board decoration and plant/earth dyes. This Samoa-specific museum record grounds the craft connection.
- US National Park Service, *Siapo: The Traditional Fabric of the Samoan Islands*: https://nps.gov/npsa/learn/education/siapo-the-traditional-fabric-of-the-samoan-islands.htm — describes brown o'a, black lama, red loa and yellow ago dyes. This is a regional Samoan-islands source published in American Samoa, not a claim that the two jurisdictions are identical.
- Samoa Tourism Authority, *Saleaula Lava Field*: https://www.samoa.travel/plan-book/activities/saleaula-lava-field — describes Savai'i lava rocks/mounds from the 1905–1911 Matavanu eruption. Geological inspiration only; no miniature ruined church, grave, inscription or sacred/tattoo imagery.
Sources retrieved as search text; direct extractor unavailable. No source photographs or artwork copied. All textures and geometry independently procedural. Invented leaf/diagonal lozenge repeats are contemporary craft-inspired ornament, NOT authenticated traditional motifs or licensed reproductions of museum objects.

## Measurable visual contract
- Wide family keepsake proportions: body width 3.72, depth approximately 2.48, wall z .10–1.56; lid 3.72 × 2.38 × .30, centred z 1.828. Blender front -Y, hinge rear +Y, up +Z; glTF (X,Z,-Y).
- Charcoal lava-like outer shell, with warm ochre/ivory siapo-inspired inset front/rear and side panels. Palette targets: cloth ivory #dac39a, brown #6f422a, soot #30241f, rust #a75936; basalt charcoal #343a37. Portable 512px procedural colour/roughness maps, no scans.
- Narrow dark brown reveal below lid, maximum .108 high, interrupted at fittings; five-sided hollow liner. Four irregular dark stone feet. Family brass hasp, round medallion, left ring and small lid corner caps.
- Main lid ornament is a shallow, gently rippled cloth-inspired rectangle, width 3.16, depth 1.88, top height 2.01–2.07, over a dark slab. Three-dimensional waved edge, not a poster plane. Its alternating leaf/lozenge repeat remains readable at whole-box scale. No miniature cedar tree, moss or Iceland glacier.
- Small irregular lava forms along rear-left lid, within x [-1.45,-.30], y [.38,.88], max z 2.40. They form a restrained geological accent, not a geographic model of Saleaula. All lid ornaments parent to Lid_Hinge and travel with it.
- Preserve original mechanism pivots: Lid_Hinge and Latch_Pivot from included trimmed mechanism.blend. 80-degree latch release during first quarter, then lid to 105 degrees. Every moving mesh collision-sampled at 81 poses against static and latch/lid surfaces; only original named bearing interfaces exempt.

## Gates written before model
1. Independently reopen source; check hollow floor, ten connected hinge/body/lid contacts, 81-pose collision list empty, and geometric dimensions/cloth range/ancestry.
2. Compare saved source and imported GLB world vertices within 1e-5 units; packed textures present. Actual GLTFLoader finite geometry, zero degenerate triangles, decoded colour and roughness variation (green channel).
3. Assert cloth and lava ornament counts/ownership and intended palette; fail a deliberately detached ornament negative control. Test actual motion endpoints and staging.
4. Offline file:// desktop 1440×1080 and touch-emulated mobile 390×844: drag, native open/close, interrupted reset, reduced motion, full-open fit, no overflow/network/runtime errors. Corrupt-GLB and no-JS poster fallback. Mobile emulation is not phone-performance testing.
5. Poster rendered from actual final source; inspect actual desktop/mobile renders. No photorealistic-equivalence claim. Up to two focused visual corrections, then disclose limits.
6. Standalone HTML strictly <5,000,000 bytes; source, GLB, maps, evidence and hash inventory in this new directory only. Archive readback and staged Git bytes agree. No chain, mint, production edit, deployment or merge.
