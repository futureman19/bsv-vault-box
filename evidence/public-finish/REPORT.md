# Public claims and claw prize overlay — scoped completion

Base: db4760ddcb33108da563b1df84a7e308205de3ec. Branch: feature/public-claims-overlay-finish. No production deployment or master push.

## Delivered

The prize reveal is a native modal dialog with opaque backing, inert pending actions, keyboard containment, background scroll lock, Escape dismissal and focus restoration. Replay and dismissal invalidate pending reveal callbacks. Try the Box focuses the separate demo section; returning to the claw remains playable. Six showcase designs, collection gallery, authored assets and unrelated evidence are unchanged.

### Changed-copy evidence

| Surface | Before | Now |
|---|---|---|
| checker metadata/introduction | No trust in seller, issuer or page operator | Historical VAULT-0001, WhatsOnChain-backed; not full-node/SPV verification |
| checker explanation | proves exact UTXO unspent | reports indexer transaction/confirmation/unspent data; commitment is not NFT custody |
| README | impossible contents substitution | immutable hash does not enforce custody of referenced NFTs |
| README | chosen trustless/provably fair packs | historical deterministic research; production randomness/order/fairness unproven |
| homepage provenance | signed record documents provenance | production plan; unsigned collection candidates versus separate signed Iceland fixture |
| prize result | real product can reuse | separate fictional simulation; repacking not proven on-chain reuse |

201 one-of-ones remain 195 countries, five oceans and one Moon. Planned package remains one inner collectible NFT and detached signed record, not accessory/certificate NFTs. Demo has no paid prize, checkout or mint.

## Reproduce the local visual preview

From this feature checkout, run:

```sh
python -m http.server 8794 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:8794/ and choose **Play demo without a wallet**. Stop with Ctrl-C. No server is left running by this delivery. This is a loopback preview, not a remotely hosted release. Settled desktop and mobile preview PNGs are attached separately.

## Verification

- `BOXSV_EVIDENCE_DIR=evidence/public-finish/browser-final python test/claw-launch-browser.py`: **14/14** grouped checks, zero uncaught page errors. Headed Chrome, authored assets, desktop keyboard, mobile CDP touch, portrait/landscape, background focus/tap isolation, reduced motion, replay/reset, Escape before/after reveal, real timeout, delayed/failed modules and GLBs, late asset latch, context loss and genuine no-WebGL fallback.
- `BOXSV_EVIDENCE_DIR=evidence/public-finish/web python test/web-launch-browser.py`: **10/10** grouped checks. Edge gallery errors/retry/search, embedded/standalone Box keyboard, two simulated reuse cycles, history, reset, normal/reduced motion, widths 320–1440.
- `node --test test/claw-interactive.test.js`: **4/4**; independently rerun by reviewer.
- `git diff --check`: pass. No contract, custody, wallet or production-chain suite rerun claimed for this presentation-only patch.
- Independent read-only review `deleg_8545ef41`: **PASS, no scoped blockers**. Reviewed actual diff, browser report/captures; reran four unit tests and whitespace gate. No review correction passes needed. Final harness-only change waits for full prize opacity and retains viewport-only settled captures; final full browser rerun passed afterward.
- Parent inspected final desktop/mobile PNGs: readable, no background interference or overflow. Small explanatory text and stylized exposed ribbon remain aesthetic limitations, not physical-phone accessibility certification.

## Retained iteration evidence

`red/report.json` records the original missing modal isolation. `public-finish-focused.txt` retains an intermediate malformed script tag failure; corrected before subsequent runs. `browser-01` records focus trapping and a mistaken light-DOM Box-button focus target; fixed with explicit two-action Tab containment and section-title focus. `browser-02` passes. Final capture waits for actual opacity 1; phase/race captures use separate filenames and cannot overwrite settled desktop evidence. Logs and earlier captures are preserved. No failed result is counted as acceptance.

## Scope and remaining boundaries

Read the exact final-QA report, collection decisions at f0a54d9b3e80338fbe34c869987a45d6d23ae25c, and continuous local implementation report at d02b279d8ea41871c4f4af6760576a3926617fb6. The latter closes local fixture binding only and remains a separate feature branch, not merged or deployed by this task.

No physical phone/Safari or deployed-site verification; no new nodes, funds, production keys, wallet permission approvals, public broadcast, paid generation or economic/legal choices. Unchanged holds include final art/package approvals, rights, real-wallet/payment integration, commercial miner/indexer compatibility, independent security review, external storage/checkpoints/monitoring, key recovery, economics/legal decisions, funding/mainnet and exact release authorization. Reusable covenant support remains unproven. Existing owner/release cards stay blocked.

Recommendation: review the local visual preview and request an explicitly scoped presentation release only after included-asset rights and release approval; do not activate a sale.
