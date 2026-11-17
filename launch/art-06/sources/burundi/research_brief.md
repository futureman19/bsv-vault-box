# Burundi / Sisal & Sweetgrass — v1 design contract

Written before model authoring. An original craft-inspired collectible, not a replica of a historic basket, not a commissioned artisan object, and not a claim that one tradition represents everyone in Burundi.

## Research and interpretation
- MADE51 (UNHCR initiative), [Preserving Burundian heritage skills](https://made51.org/news/preserving-burundian-heritage/), describes Burundian artisans wrapping sweetgrass bundles with dyed sisal and building the wrapped coils into spirals and basket walls. It documents skills passed between generations and contemporary refugee/returnee livelihoods. This informs the visibly coiled lid and bound-fibre body.
- [MADE51 Burundi](https://made51.org/burundi/) describes coiling, plaiting and braiding, papyrus/banana-bark cores and sisal/sweetgrass wrapping. This supports a fibre rather than generic wood/stone identity.
- The Metropolitan Museum of Art, [Tutsi Basketry](https://www.metmuseum.org/essays/tutsi-basketry), discusses traditions shared across Rwanda and Burundi, natural pale-gold fibre with black/red dyes, geometric bands, miniature precious-object receptacles and woven architectural panels. This informs the straw/charcoal/brick palette, not an exclusive national attribution.
Sources retrieved as search excerpts during this task. No source photograph, text, named traditional motif or culturally specific symbol is copied into the asset. The geometric diamonds are an original visual interpretation, not a claim of traditional motif meaning. No artisan endorsement or heritage certification is asserted.

## Measurable visual contract
- Wide keepsake silhouette: body exterior 3.72 X by 2.48 Y, z .10–1.56; lid 3.72 by 2.38, thickness .30 centred at z 1.828. Hollow continuous inner liner and floor inherited from the functional pilot mechanism.
- Pale straw/gold woven panels with charcoal and subdued brick-red diamond bands; dark brown narrow frame and feet; satin brass hardware. Target map sRGB swatches: straw approximately #c7a46b, charcoal #352b25, brick #904a35, with subordinate fibre variation. These are design colors, not measured natural dyes.
- Four real inset panel surfaces, portable 512px color/roughness/normal maps with visible cross-fibre microdetail. Frame edges must not become giant metal corner wraps. No geological landscape or tree borrowed from other countries.
- Lid ornament: low, shallow, oval coiled sweetgrass-inspired medallion, approximately 2.7 by 1.6, centred on lid. At least 12 nested raised coil paths, maximum z below 2.30; alternating natural/dark/brick bands. This is a geometric coil study, not a literal museum basket. Every coil is parented to Lid_Hinge; real geometry, not only a flat printed spiral.
- A narrow dark reveal around z 1.618 (height <=.108), rear strip narrowed to protect hinge sweep. Brass corner caps, solid front medallion, left hanging ring and physically connected rear hinges.
- Blender front -Y, rear +Y, right +X, up +Z; glTF (X,Z,-Y). Preserve Lid_Hinge and Latch_Pivot transforms from included mechanism.blend. Latch releases 80 degrees during first quarter, lid opens 105 degrees over remainder; reverse closes in reverse order.
- Sample 81 poses against every static and moving mesh; only documented concentric bearings excluded. Test hollow floor, ten physical hinge attachment pairs and source/export bidirectional vertex parity <1e-5.
- Offline file:// desktop and 390x844 touch emulation: drag, native open/close, reset interruption, reduced motion, corrupt-model fallback, no-JS poster, no external HTTP(S), no console/page errors on normal path, no overflow, full-open silhouette fits.
- Runtime GLTFLoader must find finite vertices, zero degenerate triangles, real varied maps and correct coil parentage. Strict final HTML <5,000,000 bytes, actual source-render poster, exact SHA-256 inventory.

## Boundaries
Script-authored stylized art and procedural maps, not hand weaving, fibre simulation, scanned materials or photoreal-equivalence. Mobile emulation is not phone performance. Cosmetic preview only; no chain access, mint, deployment or custody behavior. The user waived per-asset human review for the collection; technical completion does not imply personal aesthetic approval.
