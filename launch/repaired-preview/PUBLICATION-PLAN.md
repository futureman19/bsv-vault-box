# Scoped publication handoff — not deployed

Feature branch: `feature/repaired-collection-preview`.
Production base: `536af22c22f9f9edaf0fb53709e1a511184e87b4`. Fetch master again before publishing; do not reset or overwrite newer production work.

## Working deliverables

- Hostable folder: `preview/repaired-collection-v1/`.
- Main route: `/collection-preview/index.html` (also directory route `/collection-preview/`).
- Viewer routes: `/collection-preview/viewers/<canonical-id>.html`, **201** files, actual selected bytes.
- Assets: `/collection-preview/art/<id>.webp` (201 existing marketing images) and `/collection-preview/models/<id>.webp` (201 model-poster derivatives).
- Standalone attachment: `review.html`, **3,691,258 bytes**, self-contained poster-only comparison; no nonfunctional remote/local viewer links.
- Supporting routes: `manifest.json`, `inventory.json`, `README.md`; folder-local `.gitattributes` is delivery metadata, not a runtime dependency.
- Entire folder: **609 files / 612,433,189 bytes**.
- ZIP: **221,702,379 bytes**, SHA-256 `ffea9da367cb4bff25c7108e6256065ba4caba6177cfce6294276fa5ba7d456c`.
- ZIP readback: all 609 entries verified and recovered to `launch/repaired-preview/delivery/recovered/`.

The hostable ZIP is a viewer/media bundle, not a clean-source rebuild archive. Editable source and existing full source packages stay pinned in the manifest. Rebuilding this assembly requires the referenced Git objects, Python and Pillow; browser tests require Playwright and Edge.

## Exact additive publication plan

1. In the release-owned checkout, fetch current master and preserve its latest modern-web, six homepage selections, 201 marketing images and claw fixes.
2. Review this feature commit and publication plan. Copy only the complete `preview/repaired-collection-v1/` subtree to a new `docs/collection-preview/` route. Do not merge or replace old `docs/` from an art branch. No homepage, gallery, claw, wallet, custody, sale or manifest edits are required for this standalone preview route.
3. Existing `docs/` measures 19,167,445 bytes in the pinned checkout. New preview adds 612,433,189 bytes. Check current hosting/repository quotas again at publication time. Consider separate static hosting if desired; all links remain relative and complete.
4. Parent/release owner performs publication. This worker pushes FEATURE ONLY. No master push, deployment, funds, wallet permissions or sale activation.
5. After publishing, read back `/collection-preview/manifest.json`, entry HTML, all 201 viewer routes and image hashes against inventory; exercise desktop/mobile search, filters, compare, iframe model open/reset and focus restoration. Preserve existing homepage/gallery/claw behavior.

No navigation link is inserted into production by this card. The isolated preview URL is the bounded publication scope; any later homepage integration needs its own exact scoped change.

## Remaining substantive feature list

- **Cabo Verde**: Caldera opening remains only partly readable at mobile size.
- **Iceland**: Glacier still lacks convincing glassy depth; river and moss remain graphic. No demonstrated unsupported trim defect.
- **Indonesia**: Named copper openwork is not reliably legible in actual closed views.
- **Lithuania**: Pale corner blocks still differ from the requested/promotional black-corner treatment.
- **Malta**: Linear bastion miniature does not reproduce the branching reference silhouette.
- **Morocco**: Unresolved ceramic interlocking/corner fidelity in explicitly partial v6.
- **Mozambique**: Channel texture offsets remain visible; geological/water finish differs from the reference.
- **Pacific Ocean**: Broad pale lid field replaced by strongly blue-patterned coverage.
- **Saint Vincent and the Grenadines**: Crater depression remains difficult to read at mobile size.
- **São Tomé and Príncipe**: Dominant repetitive gray-green checks replace subdued pale-blue stone character.
- **United States**: USA stars continue across skirt/rim, not onto the main wall; explicit requested continuation remains unmet.

Ordinary finish choices are resolved for preview, not final art approval. Original records remain in `launch/repaired-preview/history/`. New packaging/geometry repairs are separately recorded rather than showing stale historical defects as still active. All collection/release, physical-device, preservation, rights and security gates remain separate. Real-wallet gate waits for the owner at their computer.
