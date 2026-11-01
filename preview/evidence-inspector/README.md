# Recorded four-ordinal evidence inspector

Non-production, self-contained HTML attachment. Does not modify or publish `docs/`.

## Reproduce (repository root, installed dependencies)

```sh
node --test preview/evidence-inspector/export.test.js
node preview/evidence-inspector/export.js evidence/four-ordinal-sponsored/regtest-run-1
python preview/evidence-inspector/browser_test.py
```

The exporter defaults to that evidence directory and writes `preview/evidence-inspector/boxsv-evidence.html`. An optional second argument sets the HTML output path. On this Windows host, invoke Node through `subprocess.run([shutil.which('node'), ...])` if the shell shim fails. No installs, compiler, npm pretest/clean, node daemon, RPC requests or signing-key reads are needed. The browser test uses installed Python Playwright and Edge, opens `file://` with the context offline, and writes screenshots/download checks to the active telegram2 output directory.

From `vault/`, the independent existing replay is:

```sh
node scripts/four-ordinal-regtest-replay.js ../evidence/four-ordinal-sponsored/regtest-run-1
node node_modules/mocha/bin/mocha.js --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/four-ordinal.test.js tests/four-ordinal-sponsored.test.js
```

## Verification boundary

`export.js` computes transaction IDs and input/output amounts from bytes; matches submissions to exact captured RPC requests; checks accepted transactions against captured raw responses and block membership; checks mandatory Script rejections and contiguous before/after input UTXO probes; validates original inscriptions, canonical signed certificate commitment and signature under an explicit exporter fixture issuer policy; decodes covenant phases/owners; validates ordered ancestry, principal amounts and final Bob scripts; cross-checks final captured UTXOs and summary claims; and replays every submitted transaction in the local Script VM before generating HTML.

Counts and fees come from captured submissions and raw transactions, not the prose report. Original-to-final mappings follow the five ordered principals. The browser is only a reader: it does not run Script, start a node, validate a blockchain, or query current unspentness. Recorded RPC metadata remains evidence from the recorder, not independently re-executed node consensus. Self-consistently forged source evidence cannot be authenticated by a manifest generated from that same source; hashes identify bytes, not trust. This is not a production audit or a public-chain compatibility result.

The detached certificate is available in its card and as a download. Its inscription contains the hash only; issuer trust is external to the bundle. Cards are typographic representations of actual tiny text records, not invented NFT artwork.

## Safe download subset

The embedded JSON download contains 36 raw `.hex` files, `identity.json`, the cross-checked `result.json`, and `rpc-subset.jsonl` (39 files). The RPC subset retains exact selected line bytes for getrawtransaction, sendrawtransaction, getrawmempool, getblock, gettxout, getblockchaininfo and verifychain. It omits startup/network/process/config/shutdown records. The manifest hashes every exported file and also hashes the complete original RPC journal as provenance; that original journal is not included. No cookie, configuration, signing key, machine path, or node log is packaged.

Downloads are JSON containers with filename-to-UTF-8-content entries, not ZIP files. For full original replay use the repository's captured evidence and command above; the subset is not advertised as a standalone installation of the VM or full node. The generated HTML is ignored in git to avoid duplicating megabytes of committed source evidence, but remains available locally and copied to the attachment output directory.

## Executed acceptance

- Exporter: 7 tests passed. Original RED: all 7 failed against the empty implementation (`tdd-red.txt`). Checks cover derived output, missing/changed bytes, forged summary, changed final RPC value, string injection and missing rejection journal entries.
- Offline stored replay: 16 accepted / 20 rejected / 8500 total fee sats.
- Relevant existing suite: 129 passed, no contracts or artifacts changed.
- Real Edge `file://`, offline: desktop 1440×1100 and mobile 390×844; all five historical stages and four item dialogs; ordered-output disclosures; keyboard Enter, Tab containment, Escape and focus restoration; all three downloads; all 39 downloaded file hashes and sizes; zero external requests, JS errors or horizontal overflow.
- Desktop and mobile screenshots reviewed with vision. Mobile footer collision was found, reproduced by an additional failing browser assertion, fixed, and rerun. Larger note text and explicit control-sat/attack language improve mobile clarity. The certificate dialog deliberately scrolls to expose long signed data; screenshots are captured at its top rather than after the download control scrolled it down.

Real intermediate failures: initial RED 7/7; first GREEN pass 6/7 because the correct missing-evidence rejection used an insufficiently specific message (fixed message, not weakened test); initial browser test failed while generated artifact was absent; mobile footer regression test failed before CSS fix. All final commands passed. No pushes/deploys, live funds, wallet controls or node startups.
