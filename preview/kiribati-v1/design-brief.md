# Kiribati / Pandanus & Lagoon — v1 visual contract

Written before authoring. Primary design reference is this researched brief, not an existing approved illustration. A stylized collectible interpretation, not a map, traditional chest, or reproduction of a named community's weaving motif.

## Research
- Tourism Authority of Kiribati, People, Culture & Heritage: https://kiribatitourism.gov.ki/people-culture-heritage describes 32 low-lying atolls and one raised coral island; weaving mats, roof thatch, pandanus and coconut-husk cord are part of local material life.
- Tourism Authority of Kiribati, Gilbert Islands: https://kiribatitourism.gov.ki/gilbert-islands describes Abemama's lagoon and community activities including mat weaving.
- Supplemental firsthand travel description: https://www.travel-tour-guide.com/kiribati/09_north_tarawa.htm describes pandanus-leaf mats and roofs, lagoon sand flats and passages in North Tarawa.
These support the choice of woven warm-fibre panels and a low coral-sand atoll encircling turquoise water. No source photography, traditional pattern, text or sacred symbol is copied into the asset. Generic alternating over/under weave is invented here; metal fittings and teal enamel are collection fantasy, not ethnographic claims.

## Dimensions and palette
- Retain wide family silhouette: body width 3.72, depth 2.38, exterior z .10–1.56; lid centre z 1.828, thickness .30. Hollow inherited five-sided liner. Front is -Y; hinge rear +Y; right +X; glTF axes (X,Z,-Y).
- Four continuous framed woven panels: warm ochre/flax base sRGB approximately #B58C50 to #D4B77B, darker strand gaps. Portable 512x256 procedural colour/roughness/normal maps, subtle physically small emboss. No wood-grain reskin.
- Dark coconut-brown frame/liner and small cream coral-inspired feet. Narrow dark teal seam under .11 high, with rear clearance beside inherited hinges.
- Satin turquoise/teal lid, four restrained brass corner fittings; retain satin brass front latch, solid emblem, side ring and connected rear hinges.
- Lid miniature: one irregular elongated C-shaped sand/reef rim, outer radii about 1.40 x .79 and inner radii about 1.08 x .48; 35-degree opening towards front-left. Height .06–.18 above lid. Lagoon is real inset opaque turquoise geometry at z~2.00, not an image; low green vegetation patches sit on the back/right rim, under z2.30. Entire ornament parented to Lid_Hinge. No tall mountain, temple or imported cedar.
- Land/water palette: pale coral sand #DCCB9A, turquoise lagoon #26AFAF, dark teal lid, muted green low shrub cover. Fantasy compressed terrain, not geographic/hydrological accuracy, glass simulation or living coral detail.

## Mechanical and delivery contract
- Preserve original pivot transforms, 80-degree latch release first, followed by 105-degree lid opening. Reverse order on closing. All ornament follows lid. 81 evaluated motion samples include ALL moving parts against static geometry and latch versus lid, exempting only explicit original mating bearings. Verify hollow floor and physical hinge attachment.
- Saved .blend independently reopened; compare exported world-space vertices within 1e-5. Actual GLTFLoader must find finite bounds/vertices and zero degenerate triangles. Decode PBR maps in correct channels. Independent theme gates check woven-map variation, reef geometry and opening, low relief and full lid ownership. Negative controls must demonstrate rejection.
- Offline file:// browser desktop 1440x1080 and touch-emulated 390x844: rotation, open/close, interrupted reset, reduced motion, uncropped default open pose, no overflow, no HTTP requests/errors, corrupt-GLB and no-JS real-source poster fallbacks.
- Source-render poster and real browser screenshots are the visual evidence, no AI substitutes. Inspect closed/open desktop/mobile. Maximum two targeted art corrections, honest limitations rather than photorealism claims.
- Standalone embedded HTML strictly <5,000,000 bytes. Deliver source, GLB, maps, reproducible scripts, evidence, SHA-256/byte inventory and readback-verified source ZIP. Scoped byte-preserving attributes. Additive-only in preview/kiribati-v1; no chains, keys, nodes, production edits or deployment. Branch backup only.
