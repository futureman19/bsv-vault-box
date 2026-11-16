# Public collection gallery

Static entry: `docs/gallery.html`; GitHub Pages serves `master:/docs`. This feature branch is **not a deployment**. The homepage collection section now features China, Canada, United States, Egypt and Moon in that order. Its five artwork links open the corresponding gallery dialogs through stable ID hashes. Hero, claw, Box demo and other sections are unchanged. The former Morocco spotlight is removed from the homepage; its gallery design and original JPEG remain unchanged.

## Sources and disclosure

201 exact identities from the supplied `boxsv-collection-review/manifest.json`: 195 countries, five oceans, `the-moon` (display name Moon). Country roster is 193 UN members plus Palestine and Vatican City. This release imports reviewed promotional artwork; no viewer bundles, model changes, minting, sales or chain functionality are included.

- Iceland, Japan and Moon: supplied `boxsv-marketing-pilot/{iceland,japan,moon}-final.png`. Read `source-manifest.json` and `generation-provenance.json`: xAI grok-imagine-image, actual-model image-to-image, corrected final sources. They are promotional illustrations, not screenshots.
- Morocco: unchanged existing `docs/assets/collection/saturn-over-the-atlas.jpg`, used as existing promotional collection imagery. No AI provenance is asserted for this file.
- The 197-design batch used each design's own model preview, including 11 explicitly accepted repairs replacing held candidates. Its prior rejection and repair history is retained. USA now intentionally supersedes that repaired image with the separately supplied, user-directed flag-and-fireworks redesign; this is not a fidelity repair. The canyon-inspired model is unchanged. Stars and stripes are stylized, not official flag counts; uppermost fireworks are naturally cropped in the supplied original. No additional crop or padding is applied. `evidence/marketing-gallery-release/usa-redesign.json` pins the native SHA-256, dimensions, provider URL, authorization and review notes. `supersededProvenance` retains the earlier USA repair and held candidate; no batch source manifests are rewritten.
- Native provider originals are used directly, never the square-padded batch delivery variants. No model or viewer changes are included. The four existing marketing designs and their image bytes remain unchanged.

`docs/assets/gallery/manifest.json` records source hashes, model commits, output hashes/dimensions/bytes and image types. All 201 cards and dialogs are labeled promotional art; there are zero model-preview images. Image conversion preserves aspect ratios and the complete composition. Cards use lazy-loaded, at-most-600px WebP; full-image dialogs load at-most-1400px WebP. There are 402 image files totaling 16,824,456 bytes; full images are loaded only when opened. Thumbnail and full-image encodings use quality 80/85 and method 6 respectively.

## Reproduce

Requires Python, `Pillow==13.0.0`, Python Playwright and installed Microsoft Edge. Source archives remain outside the repository. The native USA file remains untouched in `boxsv-usa-flag-fireworks/united-states-flag-fireworks.png`. Import/test default to that directory beside the batch archive; pass `--redesigns PATH_TO_NATIVE_USA_DIRECTORY` to relocate it. The override is mandatory and hash-checked before writes, so rerunning the importer cannot revert USA to its old repair. Supply archive directories explicitly:

```sh
python scripts/build-gallery.py --review PATH_TO_COLLECTION_REVIEW --marketing PATH_TO_MARKETING_PILOT
python scripts/import-gallery-promotions.py --batches PATH_TO_MARKETING_COMPLETE
python scripts/test-gallery-promotions.py --batches PATH_TO_MARKETING_COMPLETE
python scripts/test-gallery.py --review PATH_TO_COLLECTION_REVIEW --output PATH_TO_QA_OUTPUT
```

Build fails on missing/duplicate roster identities, category mismatch, altered viewers or unmatched original posters. It writes only gallery assets and manifest. Tests start their own ephemeral loopback HTTP server and shut it down afterward; no persistent dev server or deployment is needed.

Tests assert exact source identity/name/category parity; all 402 hashes, dimensions and browser image decodes; category counts; combined filters, accent/case/hyphen-normalized searches and Moon aliases; empty/reset; native dialog Enter, Tab/Shift+Tab, Escape, close/backdrop and return focus; gallery/dialog overflow at 1440/1024/768/390/320; both homepage links and navigation; no browser exceptions or failed HTTP responses. Desktop/mobile screenshots and results JSON go only to the chosen output directory. Browser viewport emulation is not physical-phone or assistive-technology certification.

The native dialog has one actionable control (Close), with explicit Tab containment and native Escape dismissal. Loading errors and empty results are announced through a live status. JavaScript is required for the interactive gallery; a no-script link exposes the complete image manifest.
