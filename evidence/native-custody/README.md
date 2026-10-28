# Native wrapper research evidence — NOT external NFT custody

- `compile.txt`: native compiler produced two artifacts, zero compilation failures.
- `script-vm.txt`: 27 passing native-wrapper tests. Real compiled Script VM; malicious output tests regenerate owner signature/preimage. Names referring to assets/inventory are scoped to the **singleton native continuation**, not independent NFT custody.
- `existing-covenant.txt`: existing VAULT-0001 suite 8 passing using NETWORK=local/DummyProvider and disposable scalar 3. Its legacy “deployed” / faucet text does not mean anything was broadcast; do not fund that public test identity. A pre-existing Node module-type warning remains.
- `vectors.txt`: seven deterministic serialized lifecycle transitions and raw-byte replay. Full golden bytes: `vault/fixtures/native-vectors.json`.
- `browser.json`, `desktop.png`, `mobile.png`: local loopback lab lifecycle, wrong-owner rejection, funded deposit control disabled, no page exceptions, no mobile horizontal overflow. These are desktop Chromium viewport tests, not physical-phone tests.
- Existing root JS gates and Python parity outputs are captured separately when run.

Observed RED stages: the initial native-builder availability test failed before implementation; the principal-conservation regression failed with `1 !== 101` against the original fixed-100-satoshi deduction. The latter was fixed by preserving value in this zero-fee local-only prototype. This is **not** a solution for production fees, and no claim is made that every negative Script test was individually developed RED-first.

No production deployment, push, mainnet/testnet spend, mint, or external asset import occurred. The prior `evidence/deploy-9709a7a/` directory and all approved 3D models were left untouched.

## Outcome

BLOCKED for the requested custody product. Delivered executable native-wrapper research only. Read `BOX-NATIVE-1-DRAFT.md` for exact enforcement/validation boundaries and the external-custody construction, fee, node, lineage and independent-review gates still required.
