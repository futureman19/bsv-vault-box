# Public collection gallery

Static entry: `docs/gallery.html`; GitHub Pages serves `master:/docs`. This feature branch is **not a deployment**. Homepage layout, demos and asset loading are retained; only collection navigation and collection copy changed. Old three-design/chase/on-chain wording was replaced with accurate gallery language. The existing Morocco JPEG depicts a stone-like chest, not the ringed-planet scene described by the old caption; its bytes and filename are preserved.

## Sources and disclosure

201 exact identities from the supplied `boxsv-collection-review/manifest.json`: 195 countries, five oceans, `the-moon` (display name Moon). Country roster is 193 UN members plus Palestine and Vatican City. No new artwork, viewer bundles, models, minting, sales or chain functionality are included.

- Iceland, Japan and Moon: supplied `boxsv-marketing-pilot/{iceland,japan,moon}-final.png`. Read `source-manifest.json` and `generation-provenance.json`: xAI grok-imagine-image, actual-model image-to-image, corrected final sources. They are promotional illustrations, not screenshots.
- Morocco: unchanged existing `docs/assets/collection/saturn-over-the-atlas.jpg`, used as existing promotional collection imagery. No AI provenance is asserted for this file.
- Other 197: original JPEG/PNG posters extracted from the supplied standalone viewers. Both viewer SHA256 and embedded poster SHA256 are checked against the review manifest before conversion. No source HTML is published.

`docs/assets/gallery/manifest.json` records source hashes, model commits, output hashes/dimensions/bytes and image types. Marketing art is labeled on cards and in the dialog; model posters are labeled separately. Image conversion preserves aspect ratios and the complete composition. Cards use lazy-loaded, at-most-600px WebP; full-image dialogs load at-most-1400px WebP. There are 402 image files totaling 16,656,458 bytes; full images are loaded only when opened. Thumbnail and full-image encodings use quality 80/85 and method 6 respectively.

## Reproduce

Requires Python, `Pillow==13.0.0`, Python Playwright and installed Microsoft Edge. Source archives remain outside the repository. Supply their directories explicitly:

```sh
python scripts/build-gallery.py --review PATH_TO_COLLECTION_REVIEW --marketing PATH_TO_MARKETING_PILOT
python scripts/test-gallery.py --review PATH_TO_COLLECTION_REVIEW --output PATH_TO_QA_OUTPUT
```

Build fails on missing/duplicate roster identities, category mismatch, altered viewers or unmatched original posters. It writes only gallery assets and manifest. Tests start their own ephemeral loopback HTTP server and shut it down afterward; no persistent dev server or deployment is needed.

Tests assert exact source identity/name/category parity; all 402 hashes, dimensions and browser image decodes; category counts; combined filters, accent/case/hyphen-normalized searches and Moon aliases; empty/reset; native dialog Enter, Tab/Shift+Tab, Escape, close/backdrop and return focus; gallery/dialog overflow at 1440/1024/768/390/320; both homepage links and navigation; no browser exceptions or failed HTTP responses. Desktop/mobile screenshots and results JSON go only to the chosen output directory. Browser viewport emulation is not physical-phone or assistive-technology certification.

The native dialog has one actionable control (Close), with explicit Tab containment and native Escape dismissal. Loading errors and empty results are announced through a live status. JavaScript is required for the interactive gallery; a no-script link exposes the complete image manifest.
