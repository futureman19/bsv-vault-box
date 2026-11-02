# Israel / Negev Erosion — pre-model visual contract

Written before authoring the asset. A landscape/material interpretation of Israel's Negev, not a map, territorial statement, architectural replica or claim to represent every community. No sacred symbols, inscriptions or flags. No supplied Israel concept artwork exists; the references below are factual design inputs, not copied images.

## Research and rights
- Israel Nature and Parks Authority, Makhtesh Ramon Visitors Center: https://en.parks.org.il/reserve-park/makhtesh-ramon-nature-reserve-and-visitors-center/ describes the 40-km makhtesh and exposed colorful sands, fossils and volcanic rocks.
- USGS EROS CalVal, Makhtesh Ramon: https://calval.cr.usgs.gov/apps/makhtesh-ramon describes a flat-bottomed drainage basin enclosed by steep rock walls in Israel's Negev, with sparse vegetation and diverse minerals.
- DarkSky International, Ramon Crater Nature Reserve: https://darksky.org/places/ramon-crater-nature-reserve-dark-sky-park/ explains erosion rather than meteor impact: softer chalk/sandstone below more durable dolomite/limestone layers.
Sources retrieved via web-search excerpts during this task; direct extraction backend was unavailable. No source photographs or text are embedded in the collectible. All maps and relief are generated independently. This is an abstract elongated erosional basin, not survey-accurate terrain.

## Geometry and materials
- Preserve wide keepsake silhouette: body width 3.72, depth 2.38, exterior z=.10 to 1.56; lid 3.72 x 2.38 x .30 centered at z=1.828. Hollow five-sided liner and four mineral feet.
- Body: warm pale limestone with compact procedural cream/ochre irregular beds, not cedar courses. Main albedo target approximately sRGB (193,170,129), bounded fine granular variation and thin darker bedding. Roughness .7–.9. Three portable 512x512 maps: color, roughness and normal; no scans.
- Dark umber reveal/seam under .12 tall, rear width limited to preserve hinge clearance. Gold/brass hardware, compact corner caps, existing staged latch, solid medallion and side ring. These are collection extrapolations, not historical craft claims.
- Lid relief: a single continuous irregular elongated basin, roughly 2.9 x 1.65; floor z about 2.02–2.08, asymmetric scalloped rim z 2.22–2.50. Elliptical/noncircular contour and visibly recessed center distinguish erosion basin from volcano. Warm ochre interior contrasting cream rim; no tree, glacier or blue river. Relief is closed on sides and sits in the lid. Lid terrain is a child of Lid_Hinge.
- Retain original coordinate conventions: front -Y, back +Y, right +X, up +Z; glTF (X,Z,-Y). Original lid pivot y=1.32 z=1.668; original latch pivot retained from included trimmed mechanism.
- Mechanism: 80-degree latch release in first quarter, then 105-degree lid lift. Include all moving geometry in 81 evaluated collision samples; exempt only documented mating bearing pairs. Hollow floor ray and hinge attachment intersections required.

## Acceptance gates
1. Saved .blend reopens, three packed generated maps, finite geometry and actual GLTFLoader zero degenerate triangles; source/export vertices agree bidirectionally within 1e-5.
2. Basin has at least .14 vertical floor-to-rim relief, aspect ratio >1.5, minimum lid seating overlap; actual loaded terrain parent is Lid_Hinge. Body contains no cedar/tree resource names. Textures decoded with nonzero variation and max 512px dimension.
3. Actual-source poster and offline file:// HTML <5,000,000 bytes, all assets embedded. Desktop and touch-emulated mobile: rotate, open/close, interrupted reset, reduced motion, projected full-open fit, no overflow/errors/external requests. Corrupt GLB and no-JS poster fallback.
4. Inventory records exact bytes and SHA-256. All required assets exist and source ZIP entries/hashes are read back. All tests assert failures, not merely write PASS flags. Preserve any genuine failing run before fixing it.
5. Inspect actual closed/open desktop/mobile images and report stylization honestly. No physical-phone, continuous collision, geological accuracy, photorealism, minting, storage availability or on-chain verification claims.

Bounded first version: at most two focused correction passes if acceptance exposes defects. Human review waived for this asset by task directive. No deployment or merge; scoped branch backup only.
