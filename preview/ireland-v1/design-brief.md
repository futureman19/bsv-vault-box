# Ireland — Connemara & Burren

Written before authoring. Primary reference is this sourced visual contract, not an existing approved illustration. This combines two distinct western Irish geologies; it does not claim that Burren limestone pavement sits on Connemara marble in nature.

## Research
- Geological Survey Ireland, Derryclare Marble Quarry: green serpentine marbles interbedded with white diopsidic/dolomitic marble; green-yellow-fawn-white ornamental coloration. https://gsi.geodata.gov.ie/downloads/Geoheritage/Reports/GY050_Derryclare_Marble_Quarry.pdf
- GSI, Streamstown Bay Marble Quarry: green, pale brown, grey and white varieties, often banded and folded; decorative objects. https://gsi.geodata.gov.ie/downloads/Geoheritage/Reports/GY125_Streamstown_Bay_Marble_Quarry.pdf
- Burren and Cliffs of Moher UNESCO Global Geopark, Limestone pavement: dissolution fissures (grikes) divide limestone blocks (clints). https://www.burrengeopark.ie/wp-content/uploads/2013/04/Geology-Sheet-11-Limestone-Pavement.pdf
Sources retrieved in research search. No third-party images or textures copied. Procedural material, miniature and brass fittings are invented interpretations, not authentic artisan objects or a geographic scale model.

## Measurable visual contract
- Wide body: 3.72 X by 2.48 Y, exterior z .10–1.56. Continuous hollow liner from inherited trimmed mechanism. Front -Y, rear +Y, up +Z; glTF (X,Z,-Y).
- Four continuous green marble exterior panels, no timber joints. Dominant muted green (target map mean G > R and B), folded pale cream/fawn veins and dark streaks. Compact 512px color/roughness maps, separate 256px limestone map; no scans. Polished satin marble rather than neon plastic.
- Lid 3.72 by 2.38 by .30 centered at z1.828. Dark green seam <=.108 high, interrupted at fittings. Satin brass corners, clasp, side ring and four pale limestone feet.
- Lid carries a low Burren-inspired pavement: 20 irregular pale clints in five columns/four rows, separated by real open grikes. Relief top z2.07–2.24, footprint within |X|1.55, |Y|.85, base seated at z1.97. Dark muted green underlay is visible through fissures; no tree, temple or sacred symbol.
- Every clint and underlay is parented to Lid_Hinge. Ray checks must hit a clint at its center and the underlying bed in fissures. Pale low relief must be readable in normal mobile view; not a literal landscape reconstruction.
- Inherited pivots unchanged: latch releases 80 degrees during first quarter, lid subsequently opens 105 degrees. Independently reopen source and sample 81 poses across all moving/static and latch/lid meshes, exempt only inherited explicit mating bearings. Hollow-floor and connected-hinge probes retained.
- Actual GLTFLoader: finite vertices/bounds, zero degenerate triangles, correct ancestry, visible map variation. Saved-source/export world vertex error <1e-5.
- Offline file:// desktop + touch-emulated mobile: rotation, open/close, interrupted Reset, reduced motion, no overflow/network requests, corrupt GLB and no-JS poster fallback. Poster is an actual source render. Emulation is not phone performance.
- Full embedded HTML strictly <5,000,000 bytes. Exact SHA-256 inventory and archive readback. Only this new folder added, branch backed up without merge. Technical success is not photorealism or human visual approval.
