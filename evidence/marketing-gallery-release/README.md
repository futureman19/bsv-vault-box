# Complete marketing integration — feature branch only

Baseline: `fd5cf2aa5d84655fecf361fff5b0b00b0c36c05e` (fetched origin/master). Branch: `feature/marketing-gallery-release`.

197 reviewed native originals imported, including 11 explicitly approved repairs. Total: 201 promotional art, zero model previews. Existing Iceland/Japan/Morocco/Moon entries and eight image files unchanged. No generation, model edits or minting. Feature branch only; no master push or deployment.

## Normalization schema

`normalized-manifest.json`, schema `boxsv-marketing-release-v2`:
- `baselineCommit`, `sourceManifests[{path,sha256}]`, `counts`, `policy`, `entries`.
- Every entry: `id`, `batch`, `releaseStatus`, original `reviewStatus`, optional `acceptance`, original review `notes`, `source{src,sha256}`, `original{path,sha256,dimensions}`, `provider`, `model`, `providerUrl`, `exactModelEquivalenceClaimed:false`.
- Repaired entries retain `priorProvenance` (held status, original hash, provider URL and review notes) and `repair` (selected attempt, prior rejection notes and all attempt hashes/statuses/verdicts). United States selects accepted attempt 2, retaining rejected attempt 1 as history. Six archive manifest hashes are pinned.
- Accepted entries additionally have `outputs{thumbnail,image}` containing public relative paths, dimensions, byte lengths and hashes.
- Archive image paths are relative to the supplied batch root. Provider URLs are retained only in this non-site evidence, not the public manifest. Historical review-note paths may remain in this non-site ledger. Raw originals remain in the archive; only optimized WebP derivatives are published by a future release.
- `accepted-with-documented-limitations` means authorized promotional use, not literal model fidelity. Batch 4 material limitations and other per-design notes remain intact.

Native schema mapping: batch 0 generated_output_path/output_sha256; batch 1 provider_original; batch 2 generated_path/generated_sha256; batch 3 native_generated; batch 4 provider_original_path/provider_original_sha256. The 197 unique IDs exactly match baseline Model preview entries, with source and native hashes checked before writes. No padded delivery image is selected.

## Verification executed

- `test-gallery-promotions.py`: PASS exact 201 roster, all 197 source/native hash pairs, independently re-encoded 394 no-padding/no-crop derivatives, eight unchanged images (four frozen marketing designs), no tracked model changes or public local paths.
- `test-gallery.py`: PASS 402 disk hashes/dimensions and browser decodes, exact category roster, search/filter/reset, keyboard/dialog/backdrop/focus behavior, widths 1440/1024/768/390/320, homepage navigation, zero browser exceptions or failed HTTP requests.
- `git diff --check`: PASS with Windows CR-at-EOL handling.
- Existing square image-element assertion passed unchanged; CSS/layout needed no modifications.
- Screenshots saved externally in active-profile `output/boxsv-marketing-release-final-qa/`, with machine report `results.json`. Desktop cards and mobile gallery screenshots inspected. Subjects are contained and undistorted; visible letterboxing is the existing CSS object-fit contain area around unequal native aspect ratios, not baked-in square padding. Mobile two-column labels fit; long names wrap. This is browser viewport emulation, not physical-device certification.

## Release boundary

All eleven repairs accepted and imported. Each repair must be inspected and explicitly approved, match its selected accepted attempt, source hash and native bytes. No padded delivery is imported. Minor visual differences remain disclosed.

Commit and push only feature/marketing-gallery-release. Parent owns merge and deployment. Public image bytes total 16,766,742. Source archives and screenshots remain outside the repository. Browser viewport emulation does not certify physical devices or measured accessibility contrast.
