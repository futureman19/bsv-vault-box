# Cabo Verde / Fogo — Atlantic Caldera

Contract written before modeling. A wide collectible made of dark, warm volcanic stone, a sea-blue inset seam and a miniature dry Fogo-inspired caldera on the lid. Not a geographical scale model, not an erupting lava fantasy, and not a claim to represent every island or culture of Cabo Verde.

## Research and provenance
- UNESCO Man and the Biosphere, **Fogo**, https://www.unesco.org/en/mab/fogo (retrieved HTTP 200; research-notes.md records the retrieval; raw site HTML omitted from delivery): Fogo is the archipelago's youngest and only volcanically active island, rising to 2,829 m; the reserve includes surrounding Atlantic marine space; volcanic soils support artisanal Chã wine. This supports volcanic stone, a dry crater and restrained cultivated-green accents, with Atlantic-blue as an artistic edge treatment.
- UNESCO World Heritage Centre **Tentative List** entry, *Parc Naturel de Fogo – Chã das Caldeiras*, https://whc.unesco.org/en/tentativelists/6100 (search retrieved): describes an approximately 8 km caldera open toward the east. This is a tentative nomination, NOT a claim of World Heritage inscription. Its open caldera informs an asymmetric horseshoe ridge around a smaller cratered cone.
No photographs, third-party textures or UNESCO artwork are copied into the collectible. Procedural maps and script-authored Blender geometry; no scans or hand-sculpture claim. The design brief itself is the primary art direction; there is no user-supplied Cabo Verde concept image to match.

## Measurable visual contract
- Family proportions: body approximately 3.72 wide × 2.38 deep, body/lid together approximately 2.1 high (excluding feet and terrain). Preserve the inherited hollow liner and rear/latch mechanism. Front = Blender -Y, rear = +Y, right = +X, up = +Z; glTF (X,Z,-Y).
- Body: charcoal/brown volcanic stone, generated mottled basalt/scoria maps <=512px per dimension. Color targets sRGB charcoal #373431, warm scoria #695345, restrained ash #928574; roughness 0.65–0.95. Irregular pores/fissures, not cedar grain, glacier, or Morocco's cream bands.
- Lid: dark stone slab, narrow blue Atlantic-inspired inset/reveal (height <=0.10). Deep muted blue #245966, not luminous cyan. Keep a visible segmented seam and brass clearance at hinges.
- Lid ornament: genuinely modeled asymmetric horseshoe caldera ridge, visibly broken/open on its +X/east side; footprint <=2.9 ×1.65. An off-center cratered cone approximately 0.55–0.85 high above lid, with a real depressed summit rather than a solid pointed cone. Restrained rust/ash material bands and small muted green cultivated patches on the caldera floor, not a forest. No glowing lava, flag, lettering or imported sacred imagery.
- Hardware: compact gold/brass family corners and front clasp; metal target #b78b48, roughness 0.25–0.45. Preserve actual connection to body/lid, feet and inner floor. Hidden rear/interior styling is an authored extrapolation.
- Retain precisely the approved pivots and staged **80° latch release, then 105° lid opening**. Every lid ornament is under Lid_Hinge. Include ALL moving and static meshes in 81-pose surface collision sampling, with only explicitly named mating bearing exclusions inherited and documented.
- Closed and full-open silhouette must fit default desktop and mobile camera. Reduced-motion preference snaps, Reset interrupts movement and restores closed camera; drag/touch rotation and real native buttons work.
- Offline standalone HTML <5,000,000 bytes including embedded GLB, runtime and actual-source-render poster. No runtime network requests. Editable .blend, maps and source remain separate.

## Acceptance gates established before authoring
1. Reopen saved .blend independently; assert names, dimensions, hollow interior, exact pivots, parentage, actual terrain shape/crater/ridge gap, seam height, nonflat generated maps and hinge attachments.
2. Actual GLTFLoader checks finite geometry, zero degenerate triangles, material/maps and theme ancestry. Independently compare source/export world vertices at <=1e-5 units.
3. 81 motion poses, all moving/static meshes and latch-versus-lid; zero unintended surface intersections. Sampled test, not continuous or manufacturing certification.
4. Actual offline file:// desktop + mobile touch emulation: closed/open, native taps, drag, interrupted reset, reduced motion, corrupt-GLB poster fallback, no-JS poster, no overflow/errors/external requests, full-open bounds.
5. Review actual source render and desktop/mobile browser screenshots. Technical checks do not prove photorealism or cultural completeness. Up to two focused correction passes, then disclose visual limitations.
6. Build byte cap, explicit required-file inventory with SHA-256 and source ZIP readback, negative-control test proving meaningful gates reject a changed payload. Preserve genuine failures if encountered.

Only preview/cabo-verde-v1/ is writable. No shared kit changes, blockchain, keys, network infrastructure, production site, mint or deploy. Per-asset human review is waived; this is autonomous v1 delivery, not human art approval.
