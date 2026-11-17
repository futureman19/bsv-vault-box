# United States / Flag & Fireworks — V9 review candidate

## Outcome
Restored the substantial **0.30-unit lid**, replacing V8's 0.06-unit slab. This is the exact V7 source geometry, UV layout, original hardware seating and pivots, not a stretched V8 reconstruction. No homepage, older preview, publication, minting or custody changes.

Requested base-color pigments: **red #B50018 (181,0,24)** and **navy #021F41 (2,31,65)**. PNG solid regions store exact sRGB bytes. Constant foot/navy material factors use the sRGB-to-linear transfer once; texture multipliers are identity. All four feet use the same exact red material. Gold material and white pigment (239,235,218) are unchanged. Render lighting, tone mapping, gloss and antialiased boundary texels naturally differ from the base-color values.

## Honest visual result
The actual browser comparison shows a visibly substantial lid again, but this is not reference-equivalent marketing photography. The model has a more layered navy rim, simpler/angular hardware, brighter lit ivory and sparse viewer-only fireworks without cinematic smoke. Four left and five front same-size stars genuinely fold across the top/bevel/vertical lid, with no detached extra small-star rows or lower-bevel echoes. The 14 main top stars remain the same large size.

**Stars do not continue onto the fixed body in V9.** The 0.25-unit glyph diameter is smaller than the restored 0.30-unit lid thickness, before accounting for its bevels and the body gap. Enlarging all stars enough to span that path conflicts with the current 0.27-unit front-row pitch and five separated stars within the existing canton. We retain genuine undistorted lid-side wrap instead of thinning again, stretching stars or duplicating motifs. Navy alone continues below the lid. Edge glyph fragments can read as pointed slivers from the normal camera. Latest explicit lid proportions take precedence.

One authored candidate; no visual correction iterations were needed after restoration (bounded maximum: two). This is a review candidate, not user-approved art.

## Verified
- Independent packed-source reopening; all 57 collectible mesh/empty source records, vertices, polygons, UVs, matrices and parents exactly match V7. Actual exported V8/V9 thickness measured, not assumed.
- Packed images exactly equal source PNG files; decoded GLB base-color image pixels equal those files. Both requested solid pigments verified; exported constant factors invert to exact requested bytes; four foot material assignments verified.
- White solid interiors and gold unchanged. Initial overstrict exact-white-mask oracle failed on 156 antialiased boundary pixels because neighboring pigment changed; preserved `palette-output.txt`. Corrected oracle tests solid white cores while independent wrap rays verify the same stencil scale/placement. No art was altered to pass it.
- Saved/export geometry bidirectional maximum difference 1.713e-7 units (<1e-5 tolerance); actual loader: 55 meshes, 13,324 triangles, no degenerate or nonfinite geometry.
- Full 81 sampled poses: zero unapproved moving/static or latch/lid collisions; only named intentional bearings excluded. Ten hinge attachment intersections; hollow-floor ray. Sampled, not continuous collision proof.
- Export triangle UV ray sampling: four left/five front continuous components, top-to-bevel-to-side connection, same 0.125 radius as top stars, no lower-bevel duplicates.
- Real Edge offline file:// desktop 1440x1080 and emulated touch mobile 390x844: drag, native buttons, open/close, interrupted reset, reduced motion, no overflow, no external requests or uncaught errors. Full-open collectible bounds inside viewport.
- Reduced-motion fireworks frozen; normal particles move. Full-cycle projected bounds plus 52 rendered phase checks against fireworks-hidden controls. Corrupt actual GLB fallback and no-JS poster verified.
- Browser-generated fireworks hero is also the embedded fallback; Blender no-effects source render is separately labeled.
- `primary-v8-v9-comparison.jpg` uses primary marketing illustration and actual-browser captures at equal chest width with original aspect ratios. Camera perspective is not calibrated to the illustration.

## Files and reproducibility
Open `united-states-flag-v9.html` locally. `united-states.blend` is editable and packs all three images; `united-states.glb` is the standalone collectible without viewer-only fireworks. Source archive contains scripts, maps, baselines, runtime, screenshots, evidence and inventory; excludes dependencies, backups and the ZIP itself.

Generate: `python maps.py`, then Blender `--background --factory-startup --python-exit-code 1 --python author_v9.py`. Build dependencies pinned in package-lock.json; install locally with `npm ci` if absent, then `python build.py`. Runtime has no network dependency. Blender 5.2.1, Pillow/NumPy and Playwright with Edge were used. `build.py` includes the verified local Windows Node path; adapt for another machine. Comparison capture scripts reference preserved local older viewers and marketing artwork; those absolute reference paths must be supplied on another machine. Geometry/palette/UV checks use included baselines. Rebuilding source overwrites manual Blender edits.

Full interaction verification is rerun on the copied delivery HTML. ZIP readback verifies required files and every inventoried SHA-256; final byte counts live in delivery-check.json. Branch-only backup: `art/united-states-flag-v9`; no deployment.
