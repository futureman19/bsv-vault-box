# Consolidated collection candidates — NOT approved for release

Eight independent QA ledgers cover exactly 201 designs: 195 countries, five oceans, Moon. 128 are candidates with limitations; 73 retain user/package decision holds. Zero final approvals, zero changed artwork, no minting or production publication.

## Review

Open `index.html` in the full extracted archive for searchable comparisons and links to all unchanged interactive models. Open `review.html` separately for a self-contained comparison overview (3,625,186 bytes); this smaller file intentionally has no interactive viewer links. Promotional images are illustrations, not model captures. Boards are inherited pinned review evidence, not fresh renders or calibrated comparisons. Original-resolution capture sets remain on the eight exact Git refs in `ledger.json`.

There is no changed-art before/after to show: all eight batches and this consolidation preserved the selected model bytes. Each record keeps its complete independent findings, package history and candidate/last-approved distinction. Morocco's preserved approved-v5 baseline source/export remains distinct from its partial finish-v6 candidate. Null baseline fields mean these records do not establish a prior approved version; they do not erase historical user preferences. USA v9 remains unapproved with full star-to-body continuation unresolved. Bosnia and Herzegovina retains the reviewer-added copper-readability hold.

## Remaining decisions

All 73 held IDs can be selected with the Needs user review filter; full reasons and inherited gate history are preserved per ID in `ledger.json`. The other 128 are not approved. Every design still needs explicit final art approval, rights clearance, storage/preservation policy and release authorization. Historical exact-byte source ZIP discrepancies remain for Iceland, Morocco and Rwanda. Historical full inner inventories remain unchecked for Iceland, Morocco, Namibia, New Zealand and Paraguay. New outer packaging/recovery verification does not clear these inner-archive issues.

Some inherited missing-gate strings still mention independent review even though the QA record documents it; these original records are preserved verbatim rather than silently rewritten. Review completion is not complete fresh Blender/source parity, sampled collision, corrupt-GLB/no-JS fallback or physical-device certification. Fresh runtime scope varies by batch and remains labeled in the original records. This consolidation tests gallery/packaging, not new model mechanics.

## Offline integrity and recovery

`payload-inventory.json` maps all 1,407 original file-role references. Canonical viewer/model/source/promotional/notice bytes are unchanged from the pinned upstream manifest. Historical ZIPs are preserved unchanged. Detached certificate fixtures in upstream metadata remain unsigned and non-NFT; no issuer authentication, on-chain origin or custody is established.

Authenticate this checker or the whole archive hash through a separately trusted channel. A manifest cannot authenticate its own verifier. Given the trusted inventory hash from `package-report.json`, run:

```
python check_package.py boxsv-201-reviewed-candidates.zip --expected-sha256 <trusted-inventory-sha256> --output <new-empty-recovery-directory>
```

Recovery uses only the local ZIP and standard library, checks exact member set, safe unique paths, sizes and SHA-256, and reads back recovered bytes. No website, Git, network, signing or external storage is needed. This demonstrates local recoverability while files remain available, not permanent preservation.

## Reproduction and evidence

The feature branch contains `launch/collection/`: builder, checker, tests, original eight QA ledger snapshots, upstream manifest/tools, browser captures/reports, package report and exact-byte inventories. `consolidate.py` requires Python/Pillow and the pinned Git objects plus the hash-pinned existing parent archive; paths are machine-local and need explicit adaptation elsewhere. `check_package.py` is standalone. `package_delivery.py` rebuilds the ZIP twice with fixed timestamps/order and compares hashes, then recovers it with socket and subprocess creation prohibited. The final output gallery is tested in offline Edge at desktop/mobile emulation sizes; this is not physical-phone performance evidence.

No changes to production docs, old previews, custody code, funds, keys, prices, allocation or release settings. Next: consume the consolidated immutable candidate ledger in the pre-created rehearsal, retaining all art/package/release holds.
