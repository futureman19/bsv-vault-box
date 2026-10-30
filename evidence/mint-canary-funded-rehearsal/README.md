# Funded adapter build evidence — no mainnet execution

Verified on 2026-10-30. Base: `c745986`; branch: `codex/mint-funded-adapter`.

- `mint-tests-final.txt`: **90 passed, 0 failed**, including unchanged broadcast-locked paths, forged/wrong-chain capability refusal, absent/noninteractive/wrong-challenge gates, staged funding checks, mock-only adapter/publisher tests, and offline buyer checks. `mint-tests.txt` is the earlier 89-test pass before adding the wrong-challenge regression.
- `vault-tests.txt`: **90 passed** (`node node_modules/mocha/bin/mocha.js --no-config 'tests/*.test.js'` from vault).
- `official-sale/`: official guarded v1.2.3 sale lifecycle, old-owner rejection and clean node shutdown.
- `rehearsal/`: shared funded runner through prep, inscription, empty box, deposit, seal, durable commitment/reservation, payment and confirmed three-input transfer; then a **separate offline buyer process** signs open/withdraw and the local harness publishes them. Final two one-sat outputs verified buyer-owned; complete history verified; service, journals and node closed.
- `rehearsal/owner-gate-refusal.json`: no network calls before absent-gate refusal.
- `rehearsal/funding-gate-refusal.json`: runner refuses a wrong report shape before creating run evidence.
- `rehearsal/onchain-funding-refusal.json`: actual guarded-chain 50500-sat sponsor sources rejected by startup preflight; only the disposable harness corrects these fixtures, never the runner.
- `live-preflight.json`: fresh live public-fixture **inspect** PASS with all roles UNFUNDED. This is deliberately NOT funded startup readiness.
- `live-complete-utxo.json`: live GET-only address/script `/unspent/all` shape checks.
- `audit.json`: 10 live mainnet GETs, zero mainnet writes; 33 guarded local broadcast attempts across both node journals; no serialized keys/credentials found; both nodes and runner closed.

## Reproduce

From the repository root, on Linux/WSL using native absolute paths:

```sh
npm test --prefix mint
(cd vault && node node_modules/mocha/bin/mocha.js --no-config 'tests/*.test.js')
node mint/scripts/regtest-sale.js /ABS/NEW/official-sale
node mint/scripts/canary-run.js --owner-authorized --regtest-rehearsal /ABS/NEW/rehearsal
node mint/test/preflight-live-readonly.js /ABS/NEW/live-preflight.json
node mint/test/funded-live-readonly.js /ABS/NEW/live-complete-utxo.json
node mint/test/audit-funded-evidence.js evidence/mint-canary-funded-rehearsal
```

The original Windows invocation supplied a Git Bash `/c/Users/...` path to native Node, which resolved the evidence destination under `C:/c/Users/...`. After successful execution, the two complete evidence directories were moved to this repository directory without editing their bytes. Historical stdout therefore retains the original `/mnt/c/c/Users/...` destination. Node datadirs were separate fresh POSIX cache directories; this path issue did not change chain/network isolation. Future Windows invocations must use `C:/Users/...` native paths, or invoke directly inside WSL with `/mnt/c/Users/...` paths. The pre-existing unrelated node was not touched.

## Review boundary

All POST behavior exercised by unit tests is **mocked HTTP**, not live mainnet traffic. Real broadcast journals are guarded local regtest only. No real random keys were generated; disposable deterministic fixture WIFs were removed by the harness and are not in this pack. Pool held/dispensed totals are not fees. Local seal commitment is not a new on-chain root protocol transaction.

Owner-approved staged interpretation: startup requires exact inventory/sponsor funding and UNFUNDED payment; exact confirmed payment is required only after durable reservation. Buyer keys never enter runner/service; runner ends at transfer-confirmed. Buyer fee funding is two 1500-sat outputs (each 500 prep + 1000 transition). A funded mainnet execution, commercial miner acceptance, independent security approval, deployment and merge remain outside this delivery.
