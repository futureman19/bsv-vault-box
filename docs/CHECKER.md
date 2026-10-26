# VAULT-0003 checker

`vaultcheck.js` remains a single browser/Node file, with no packages or bundler.
Use a modern browser with Web Crypto (HTTPS/localhost), or Node 22+.

```js
const result = await VaultCheck.checkBox(holdingTxid, 3, {
  manifestTxid, // transaction containing OP_FALSE OP_RETURN <VAULT3-MANIFEST> <JSON>
  mintTxid,     // optional transaction containing <VAULT3-MINT> <JSON>
});
```

Node: `const VaultCheck = require('./docs/vaultcheck')`.

## Resolution and evidence

The covenant stores a **canonical manifest hash**, not its transaction id.
Supply the manifest txid as a locator; the checker fetches the OP_RETURN and
verifies its canonical SHA-256 against `contentRef`. There is no fabricated
root-to-txid resolver or indexer. Without a locator, legacy seal verdicts stay
unchanged and opened boxes explicitly say `packStatus: NOT-CHECKED`. A mint
cannot be verified without the manifest locator.

For opened outputs the checker follows input outpoints backwards to the
SEALED→OPENED transition, including the compiler's initial-state marker. It
matches both box identity and manifest commitment. It does not use a later
opened-transfer height as the opening height. It reads `blockheight` and
`blockhash` from that opening transaction, obtains height + 1 from WoC, checks
its previous hash, and runs the inline library draw port. Hashes are display
hex text; the seed is not byte-reversed. D is fixed at 1.

Each output may contain `manifestTxid`, `openingTxid`, `drawHeight`, `drawHash`,
`packStatus`, `pack: {designs, retries, trace}`, and `mintStatus`.
The evidence list also includes the ordered design ids. The UI links the
manifest transaction, including while a draw is pending.

- Unconfirmed opening: pending; never use a stale reported height.
- Missing next block: `pack pending — one more block`; no valid/invalid mint claim.
- Wrong designs, root, identity, malformed/missing mint tag, or mint not a direct
  child of the opening: `INVALID-MINT` once the pack is computable.
- Missing mint tx, unavailable ancestry, mismatched manifest, malformed chain
  data, or inconsistent block link: error (`CHECK FAILED` in UI), not acceptance.
- All API reads share the existing 429 backoff. No broadcasts, keys, or signing.

## Boundaries

WoC is the chain-data source; this is not independent header/merkle/PoW validation.
The existing prefix/tail covenant fingerprint is not a full artifact-byte proof.
The commitment reader pins the deployed scrypt-ts 1.20.0 constructor layout.
Only one tagged JSON payload per transaction is supported (not ordinal envelopes
or split card inscriptions). The genesis/current output is still the user's
locator: there is no forward spent-output discovery. Backward ancestry is capped
at 100 hops and draw work at 100,000 hashes; hitting either guard fails closed,
never returns a partial pack or changes the deterministic result. Checks are a
point-in-time view; refresh after reorgs. First vault output remains the headline
verdict, as in the original checker. Pack computation is independent of the
seal confirmation threshold; evidence states the draw block explicitly.

## Reproduce

```sh
node --test test/checker.test.js test/checker-ui.test.js
node test/vault3.test.js
python -B test/python-parity.py
node test/checker-live.js  # optional LIVE mainnet GETs, rate limited
```

Fixtures are synthetic WoC-shaped data, not signed or mined transactions.
The checker tests execute the standalone source in a browser-like VM without
`require`, Buffer, or imports. UI tests execute its actual inline script with
a minimal DOM adapter, not a real graphical browser. The 25-catalog differential
check compares the inline algorithm with the parent library; the parent library
also has its existing Python parity gate. The live test checks only legacy
Boxes A/B, not a real VAULT-0003 lifecycle.
