# ASSETS — candidate metadata and offline recovery

This is a reusable **candidate-only packaging pipeline**, not a final art freeze, signed issuer certificate, NFT issuance, storage purchase or release. It preserves the exact 201-design roster: 195 country-inspired designs, five named oceans and Moon, each edition supply one. No accessories or certificate NFTs. The inner collectible is not the outer BoxSV custody container.

## Delivered and verified

- 201 stable slug-based IDs in `urn:boxsv:collection:impossible-places:v1:<slug>`. These are application IDs, not minted origins. Updating candidate bytes changes the manifest commitment without changing these IDs.
- 1,407 content-addressed payloads, **2,423,487,786 bytes**. Separate roles for viewer, standalone model, editable Blender source, promotional illustration, source notices, optional research briefs and unchanged historical source archives.
- Canonical manifest: **948,915 bytes**, SHA-256 `307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb`.
- Recovery ZIP: **2,425,588,308 bytes**, 1,411 entries, SHA-256 `28c47ef3f985c4af68f1929045586e0c58cd9a1e93988e9a28fb93dc4f479947`.
- All 1,407 payload references read back from the ZIP and hashed. All 201 recovered item folders created and all 1,407 copied payloads hashed with network and subprocess/Git creation disabled. Recovery metadata and detached unsigned fixture records accompany each item.
- Eight regression tests pass, including full synthetic 201-item recovery, reproducible ZIP bytes, missing/tampered payload, missing/duplicate/substituted roster, wrong category/supply, duplicate archive, missing source notice, false final approval, root-hash tamper and stable identity under candidate change.
- Four **actual recovered** viewers (Iceland, Morocco, Rwanda, USA) passed offline Edge mobile-emulation readiness, native open/close/reset, no overflow, no external requests and no page exceptions. These are recovery smoke tests, not renewed full geometry/mechanics/art acceptance or physical-phone testing. Other 197 viewers were byte-verified, not freshly browser-tested here.

`acceptance-report.json`, `build-final.json`, `recovered-browser-report.json`, `tests-final.txt` and the four PNGs preserve execution evidence. `build-report.json` and `bundle/` identify the earlier intermediate package, NOT the final delivery. Final package is `bundle-v2/`; old files remain untouched.

## Trust and authenticity boundary

Every item has a detached `boxsv-detached-authenticity-fixture-v1` record with deterministic public fixture issuer label, subject ID and files commitment. **signature=null; UNSIGNED-FIXTURE-NOT-AUTHENTICATED.** These records demonstrate packaging only. No real/private keys are generated or loaded. Real issuer authentication, key policy, signing and chain-origin binding are explicitly downstream requirements. Hashes do not establish copyright, issuer identity, ownership, custody or availability.

The expected manifest hash must arrive through an independently trusted channel; do not read it only from the same untrusted download. Similarly, **verify the checker before running it**, using trusted Git/reviewed source or the separately recorded hash:

- `packaging.py`: `b5f9b995d34c5d08d187a90fce640df7d3b65cf37b88233f6a0673b6a3082110`
- `roster.json`: `f71c916d0814f9b707f7563c9310f2fe302487f0d246e5f67442966c26a4b59d`

The manifest commits content and ledger semantics, not its checker executable. The ZIP hash commits the complete archive including checker. A malicious checker can lie about its own verification; the expected hashes must not be taken as self-authentication. Use a trusted SHA-256 utility before extracting/running a received archive.

Canonical encoding v1 is sorted-key, compact ASCII-escaped JSON with no newline, finite JSON values; it is explicitly **not** a claim of RFC 8785 compliance. Arrays are retained except sorted item selection; input entries are order-normalized for their semantic commitment. `sha256:` URIs resolve to `blobs/<64-lowercase-hex>` locally, not a website or IPFS gateway. They are not IPFS CIDs. Full original ledger bytes remain in Git; the packaged ledger is canonicalized.

## Reproduce / recover without boxsv.com

Python standard library only. Use a trusted copy of the checker and roster. All output destinations must be new: the tools refuse to overwrite a prior package, recovery folder or ZIP.

```sh
python launch/assets/test_packaging.py
# Build from immutable Git blobs and the ledger's read-only local archive paths:
python launch/assets/packaging.py build launch/assets/input-ledger.json NEW-PACKAGE
# After copying/extracting the package, no repository/website is needed:
python packaging.py verify PACKAGE --expected-sha256 307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb
python packaging.py recover PACKAGE NEW-RECOVERY --expected-sha256 307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb
python packaging.py archive PACKAGE NEW-ARCHIVE.zip --expected-sha256 307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb
```

Open the recovered `<slug>/viewer-<index>.html` directly via `file://`; filenames and hashes are in `recovery-inventory.json`. GLB and Blender sources are separate files. Source build scripts/maps remain within unchanged historical source archives; original absolute-path build dependencies are not promised portable. Recovery of bytes is proven, regeneration of every Blender scene is not.

Build uses local Git object availability and the original local archive paths; **recovery does not**. All selected viewer/model/notice bytes come from pinned commits, not moving branches. Parent input is commit `6db6388d04fee0da8e0324a640d5880a5813a39c`, original raw ledger SHA `28e032084f6bddf80143fd3bfd0e5b06cbdf84dc2343937e7b9bc71734ac3c9c`. Regenerating with a new ledger is an explicit new candidate package. The current strict candidate pipeline refuses final-approval assertions; final freeze/signing requires the downstream lane, not a flag on this tool.

## Historical discrepancies and artistic holds

Iceland, Morocco and Rwanda's old ZIP HTML has newline-only differences from selected Git/delivered bytes. **No old archive was rewritten.** The new package supplies selected canonical HTML separately and retains each original archive plus its original hash and failure report. Exact selected-byte recovery is now proven without pretending the old mismatches disappeared.

Five historical full inner inventories remain unchecked in the inherited evidence: Iceland, Morocco, Namibia, New Zealand, Paraguay. All archive bytes themselves are hashed and recoverable here, but this does not retroactively validate their embedded inventories. These holds remain in metadata. All final art, fresh full technical acceptance, storage and release holds remain. USA v9 remains unapproved, with full star-to-fixed-body continuation unresolved. No artwork was changed, no promotional illustration replaced a model, and no final approval inferred.

Source notices are included for all 201; research briefs exist for 197 and are optional. The package preserves those notices and promotional provider provenance, **not blanket rights clearance**. Review licenses/source permissions before publication/mint. Existing generated illustrations remain different from actual models; recovered USA screenshot shows the closed chest and fireworks but does not settle its unresolved requested continuation.

## Storage proposal, not purchase

`storage-proposal.json` gives measured role bytes and a reproducible calculation. Runtime viewers total **592,749,853 bytes**; standalone GLBs total **326,810,140 bytes** but are already embedded in viewers, so do not sum them as mandatory viewer transfer size. Historical ZIPs dominate preservation storage.

Recommendation: retain two independently held offline copies now; decide hosted preservation only after candidate consolidation. One whole 2.425588308 GB ZIP stored for a full month on R2 Standard would round to 3 GB-month, **$0.045 storage-only before free tier** at $0.015/GB-month; $0 storage if its 10 GB allowance is entirely available. Requests are separately billed/rounded, account usage/taxes are unknown. No account was inspected or purchased, and nothing was uploaded. Official pricing source: https://developers.cloudflare.com/r2/pricing/index.md (indexed search retrieval; direct page returned HTTP403). IPFS pinning and on-chain bytes are unquoted alternatives, not approved decisions or availability guarantees.

## Independent review and bounded finish

A read-only reviewer inspected the actual scripts, manifest, all blob hashes, three original mismatch archives and parent comparison image. It found stale bundled code and incomplete input guards. The initial review is retained in `independent-review.md`; actual five failing guard subcases were preserved in `tests-review-red.txt`, then fixed. Final bundled code matches reviewed source and is separately hash-pinned. Full recovery/archive execution and additional regression coverage were added; final outcomes above are independently measurable. Initial `tests-red.txt` was a missing-implementation assertion, not behavioral TDD; the ordering, archive-role and review-guard failures are real later behavioral negatives.

Only `launch/assets/` is changed. No production docs, old preview, other worktree, key, node, mint, funds, storage or sale operations were performed. Next: downstream collection consolidation consumes this pipeline against reviewed candidates; it must retain unresolved holds and separately authorize a final freeze/signing/storage/release.
