# United States flag v5 — larger stars, shallow wrap, visible fireworks

Targeted art-only successor to v4 (e3a224093be57d8ffdf4dc5cddd5d8e680408108). No website, main/master, minting or custody changes.

## Visible changes
- 14 lid stars instead of 27; decoded average silhouette width 50.14px versus 26.56px in the same map. Star radius .125 versus .065 source units. Ivory remains RGB 239/235/218, not bleached white.
- Five broad lid/body stripes instead of seven; red map RGB 235/8/20 instead of 183/23/43.
- The SAME navy lid field continues down the upper body as a single perimeter band, 12.89% of body height. Boundaries match x=-.15 on front/rear and wrap left corner; no body stars, lower navy patch or navy feet. Existing articulation seam remains visible.
- Brighter bounded 324-point, 1296-trail-segment fireworks outside the GLB, staggered at 1.2 seconds in a 3.6-second cycle; nonzero opacity floor. Reduced motion has visible fixed bursts.
- poster.jpg / poster.png and hero-fireworks.png are actual browser captures INCLUDING fireworks. blender-source-no-fx.png is the separately labelled genuine Cycles source render, not the user-facing poster.

## Verification
features-check.json: decoded star components/widths, stripe count, red channels, unchanged ivory, shallow single solid navy interval and lid/body boundary registration.
canton-check.json: saved-source 496x40 barycentric wall UV rays, one connected navy run, zero lower navy and zero missed samples; feet UV excluded from navy; all 57 geometry/transforms/parents exact v4.
export-identity-check.json: 165 non-UV accessor views and nodes exact v4; authored image pixels match exported GLB.
source-check.json: independently reopened source, 81 sampled opening poses, zero nonbearing collisions, hollow interior and hinge contact checks. This is sampled, not continuous collision proof.
parity-check.json: saved-source/export geometry within 1e-5 tolerance.
browser-check.json: actual offline Edge desktop/mobile-emulated rotation, native touch, open/close, interrupted reset, reduced motion, framing, no overflow/errors/external requests, genuine corrupt embedded GLB fallback.
extended-check.json: full 3.6-second fireworks expansion cycle sampled every .05s closed/open desktop/mobile, all NDC under 1; frozen reduced particle arrays, normal motion and no-JS fallback.
fireworks-pixels-check.json: 52 actual rendered phase comparisons against fireworks-hidden control, >100 changed pixels per phase at channel delta >35. Captures initial and expanded phases; no blank phase in sampled cycle.
motion-output.txt: actual Node motion tests.

One corrective iteration after initial visual review: brighter warm red fireworks, more ivory cores, higher minimum opacity. Initial snapshots/checks retained in initial-check. No geometry changes. Final hero and mobile-open captures visually inspected.

## Honest visual limits
Decorative flag adaptation, not exact national flag counts. Stars remain softly filtered at mobile scale. The stepped physical lid/seam makes the shallow band look layered; there is no second star panel. The body red is vivid, while lit lid highlights read lighter/coral. Fireworks are stylized fine trails, not cinematic smoke/bloom or the marketing illustration; some lower rays overlap/are naturally occluded by the raised lid. Mobile checks are desktop browser emulation, not phone hardware benchmarks. Visual approval remains the user's decision.

## Files and reproduction
Open united-states-flag-v5.html offline. Standalone GLB united-states.glb; editable packed united-states.blend; source ZIP and SHA-256 inventory included in delivery. GLB intentionally excludes viewer-only fireworks.
Install pinned dependencies with npm ci. Run Python maps.py; Blender 5.2.1 --background --factory-startup --python-exit-code 1 --python author.py; Python build.py; Python capture_fireworks.py; Python build.py again to embed actual browser poster. Run verify_source.py, verify_mechanism.py, verify_parity.py, verify_canton.py with Blender; run other verify scripts with Python; node --test --test-reporter=tap tests.mjs. Python uses Pillow, NumPy and Playwright/Edge. Source identity/comparison checks require sibling v4 from the baseline commit. Blender and Node paths are local Windows paths, not a portable installer.

package_delivery.py asserts required artifact subset, ZIP readback, SHA-256 copied output and opens the delivered HTML itself offline. Archives/node_modules/backups excluded from inventory self-reference. Only art/united-states-flag-v5 is authorized for remote backup.
