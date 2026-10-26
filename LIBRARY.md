# VAULT-0003 pure protocol library

CommonJS, Node 20+; no install and no runtime dependencies beyond `node:crypto`.
No network, chain discovery, wallet, signing, or broadcast functionality.

## API

```js
const {buildManifest, validateManifest, canonicalSerialize, manifestRoot} = require('./manifest');
const {D, drawIndex, drawPack, drawBlockHeight, drawPackForOpen} = require('./draw');
const {verifyPack, verifyMint} = require('./verify');
const manifest = buildManifest({
  name: 'Example', pack_size: 2, allow_pack_duplicates: false,
  designs: [{id: 0, ref: 'content0', weight: 3}, {id: 1, ref: 'content1', weight: 1}]
});
const contentRef = manifestRoot(manifest);
const pack = drawPack(manifest, 'example-box', 'example-seed');
console.log(contentRef, pack.designs);
```

- `buildManifest(input)` returns a detached object, fills missing `manifest_version: 1` and main/slot `total_weight`, and validates it. Supplied totals are checked, not silently repaired. Optional `slots` keys are canonical decimal slot indices, each `{table: [{id, weight}], total_weight}`.
- `validateManifest(manifest)` returns the input or throws. IDs are unique nonnegative safe integers per table; weights are positive safe integers, totals exact and safe, refs strings. Slot IDs must exist in the catalog. Main-table unique capacity must cover its bound slots when duplicates are forbidden. Every override has its own single-slot scope and must be nonempty. No shared table aliases are defined by this baseline.
- `canonicalSerialize(value)` sorts object keys by Unicode code point, uses tight separators and Python's default ASCII escaping (including surrogate pairs and DEL). Array order is preserved. Supported values: plain JSON objects, dense arrays, strings, booleans, null, and safe integers. Fractional/unsafe numbers and non-JSON values are rejected rather than silently changed. Arbitrary Python floats/integers beyond JS's safe range are **not supported**. Use parsed JSON data, not objects with accessors.
- `manifestRoot(manifest)` hashes canonical UTF-8 bytes to lowercase SHA-256 hex. It deliberately does not validate semantics: malformed-but-serializable content can still be fingerprinted. Validate before accepting a commitment.
- `drawIndex(boxId, seed, slot, retry, totalWeight)` uses the executed Python baseline's exact UTF-8 preimage `VAULT3-DRAW|box_id|seed|slot|retry`, with decimal integers, then unsigned big-endian digest modulo weight via BigInt. Do not concatenate raw hash bytes or reverse displayed hash text. IDs/seeds are nonempty well-formed strings without `|`; simulated identifiers are accepted for baseline compatibility.
- `drawPack(manifest, boxId, seed)` validates and returns `{designs, retries, trace}`. `designs` is the ordered pack, `retries` total rejected draws; each trace row is `{slot, table, retry, design}` for the accepted draw. Dedup keys are `main` or `slotN`, not table-content identity. A rare override may repeat a main-table design. No arbitrary retry cutoff changes the protocol outcome. Extreme weight skew can be computationally expensive; enforce resource limits outside the pure algorithm without accepting incomplete packs.
- `drawBlockHeight(openHeight, delay = D)` where exported `D = 1`; explicit `0` is supported.
- `drawPackForOpen(manifest, boxId, openHeight, blockHashAtHeight, delay = D)` returns the draw result or `null` if opening height or draw hash is null/undefined. Lookup is synchronous; obtain asynchronous chain data before calling. Removing the opening height after a reorg makes the pack pending again. Heights/delays must be nonnegative safe integers.
- `verifyPack(manifest, boxId, seed, claimedDesigns)` recomputes retries and compares exact numeric design IDs in slot order; returns boolean.
- `verifyMint(manifest, boxId, openHeight, blockHashAtHeight, claimedDesigns, delay = 1)` does the same through the opening adapter; pending returns false. Invalid manifest/argument types throw; callers must treat exceptions as rejection, never acceptance.

## Integration boundary

These functions verify **pack contents**, not transaction validity. Caller must validate the opening transaction and its confirmed canonical block, resolve the correct draw block hash, check manifest root equals immutable covenant `content_ref`, validate claimed mint `manifest_root` and `box_id`, and establish mint ancestry to the opening. None of that is inferred from a supplied string or callback. No real-chain safety or unpredictability claim is made by these simulation tests.

## Reproduce

```sh
node test/vault3.test.js
python -B test/python-parity.py   # optional independent Python baseline differential
```

The Node gate checks first/reopened packs, all golden fields and regenerated JSON text (only checkout CRLF is normalized), rejection sampling in independent processes, canonical Unicode bytes, invalid manifests, ordered mint claims, per-table dedup, delay and pending behavior. The optional Python test compares 50 cases against the unmodified reference, including exact canonical bytes, roots and retry counts. It imports the reference without executing its fixture-writing main. Neither test overwrites `v3_vectors.json`.
