# United States flag v4 — lid-only canton

V3 was visually rejected despite connected topology. V4 removes ALL navy/star body panels. All four sides, clasp seat, exterior seams and feet use horizontal red/ivory stripes. Only the lid retains the original navy/star design, including its narrow vertical lid edge. Interior velvet and brass hardware remain unchanged.

Intentional design deviation: unlike the marketing illustration there is NO upper blue body band. This explicitly eliminates duplicated-looking fields, not an exact marketing match. Feet show red over ivory. V3, original model and site remain untouched; art branch only. Nothing minted or deployed.

## Verification
- body-material-check.json: 17 body/feet/seam meshes use stripe-only material; every atlas row constant and every pixel red or ivory, so no stars; sole star material belongs to lid, whose map is byte-identical to v3.
- canton-check.json: 496 perimeter positions x 40 heights sampled through actual saved mesh UVs; zero navy and zero missed samples. Rejected v3 is negative control. All 57 collectible geometries/transforms/parents unchanged. Mechanism, viewer, motion, fireworks and tests byte-identical.
- export-identity-check.json: 165 non-UV accessor views exact v3; UV/material edits only; exported map pixels exact.
- source-check.json: 81 sampled poses, zero nonbearing collisions; hollow-floor and hinge attachment checks pass. Sampled tests are not continuous proof.
- parity-check.json: reopened packed source/export geometry within 1e-5.
- browser-check.json: offline desktop/mobile-emulated touch rotation, open/close, interrupted reset, reduced motion, framing, no external requests/errors/overflow, genuine corrupt-GLB fallback.
- extended-check.json: decoded map variation, unchanged separate animated/frozen fireworks, framing and no-JS poster. motion-output.txt passes 81 poses and three invalid-asset negatives.
- Normal comparison and opposite-corner rotated actual-model images visually inspected: no navy/star body panels. Four corner views captured. Navy on lid thickness is the original lid design, not a body patch. User approval pending; mobile is browser emulation, not physical-device testing.

## Deliverables and reproduction
Open united-states-flag-v4.html offline; strict cap 5,000,000 bytes. GLB: united-states.glb. Editable packed source: united-states.blend. poster.png/jpg freshly rendered from the exact source. reference-comparison.jpg compares marketing / rejected v3 / v4.

Run Python maps.py; Blender 5.2.1 background author.py; Python build.py (frozen viewer bundle). Blender checks: verify_source.py, verify_mechanism.py, verify_parity.py, verify_canton.py. Python checks: verify_export_identity.py, verify_body_materials.py, verify_browser.py, verify_extended.py, capture_views.py. Node: --test --test-reporter=tap tests.mjs. Python dependencies: Pillow, NumPy, Playwright/Edge. Identity checks require sibling v3; comparison requires the explicit local marketing reference path. Historical reference files are not duplicated into ZIP. Build itself is self-contained apart from installed tools.

package_delivery.py validates required ZIP members, entry hashes, copied output and delivered HTML offline. inventory.json records exact bytes; archives, backups and post-package envelopes excluded. Folder-local Git attributes preserve bytes. Only art/united-states-flag-v4 is pushed.

