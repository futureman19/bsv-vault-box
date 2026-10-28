# Offline verification report

Base: `68be07458a025220b6a543400c7db789dfa0bd56`.
Branch: `feat/ordinal-sponsored-bounded`.

## Observed red/green

Before implementation, `npx mocha --no-config tests/ordinal-sponsored.test.js` produced **0 passing, 2 failing**: sponsor input count was 2 rather than 3; repeated-transfer transaction was 84469 bytes against the 30000-byte bound.

Before replacing empty synthetic funding-parent input scripts with signed P2PKH preparations, the targeted `--grep 'genuinely signed'` test produced **0 passing, 1 failing** on the nonempty scriptSig assertion. It passes with preparation-input VM verification now.

## Final execution

From `vault/`, with command exit failures chained by `&&`:

- `npx scrypt-cli compile -i 'src/contracts/ordinalPair.ts'`: exit 0; **1 passing, 0 failing**. Saved `compile.txt`.
- `npx tsc --noEmit`: exit 0; no diagnostic output (`typecheck.txt` is intentionally empty).
- `npx mocha --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/native-custody.test.js`: exit 0; **90 passing (7s)**. Saved complete output `tests.txt`.
- `npm run vectors:ordinal`: exit 0; byte-exact deterministic fixture check. Saved `legacy-vectors.txt`.
- `npm run vectors:ordinal-sponsored`: exit 0; byte-exact deterministic fixture check and anchored replay. Saved `vector-check.txt`.
- `git diff --check`: exit 0; Windows LF/CRLF informational warnings only.

Measurements in **`sizes.json`** are emitted by the executed vector generator, not manually fabricated. The vector has 16 custody transitions: deposit, seal, 12 alternating ownership transfers, open, withdraw. Each spends a separately signed bounded funding parent. Transfer sizes are 15853–15856 bytes, parent digest is 32 bytes per covenant, and final withdrawal is 8810 bytes. Full custody history remains 242495 bytes; funding-parent history is another 3061 bytes. The golden fixture includes all raw transactions and assumed funding-root bytes.

## Security scope

Both requested local targets implemented. Sponsor mode enforces 1–10000 sat fee, exact preserved principal outputs, sponsor-only optional change, exact third P2PKH funding outpoint/value/script via bounded parent reconstruction, and owner plus sponsor SIGHASH_ALL|FORKID authorization. No sibling introspection or outsourced trust. Original admission/ancestry and actual UTXO boundaries remain required.

Not production ready. Funding-parent grammar is deliberately restricted to one input/one output and at most 108 scriptSig bytes; arbitrary wallet UTXOs need a preparation transaction and fee. No full-node/miner/indexer/production-wallet acceptance, audit, chain inclusion or independent complete implementation was demonstrated. No real funds, broadcasts, deployments, pushes, public UI changes, or funded secrets. Pre-existing untracked `evidence/deploy-9709a7a/` preserved and excluded from commit.

One diagnostic read of the old large vector exceeded Node execFileSync's default buffer; rerun with a 10000000-byte buffer succeeded and confirmed historical sizes. This did not affect compilation, VM tests or vector validation.
