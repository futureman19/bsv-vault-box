# Regtest sponsor pool (phase 1)

**Not a production wallet. No mainnet/testnet broadcasting, no VPS changes.**
`SponsorPool` checks `getblockchaininfo.chain === 'regtest'` before every public asynchronous operation. Only compressed testnet-prefix WIF files are accepted; a testnet prefix alone is not treated as permission to contact testnet.

## Run

Install the existing pinned dependency tree with `cd vault && npm ci --ignore-scripts`. This package deliberately reuses `vault/src/ordinal-pair.js` and its dependency versions; it does not modify or compile the contracts.

From the repository root:

```sh
node mint/test/run.js
node mint/scripts/regtest-pool.js
```

Linux/WSL, Node >=22, curl, tar and GNU timeout are required. Windows entrypoints invoke WSL's login-shell Node. The test runner uses a Linux filesystem scratch directory so POSIX file permissions are actually checked, not simulated by Windows mode bits. Direct `node --test mint/test/*.test.js` also works on Linux. Native Windows tests skip POSIX pool tests; use the supplied runner for the full gate.

The integration downloads the official 1.2.3 Linux archive, verifies its pinned SHA-256, creates a new nondefault datadir under `~/.cache/boxsv-mint-regtest`, and launches **through the unchanged `vault/scripts/bitcoind-guard.sh`** with explicit `-regtest`, `-datadir`, wallet disabled, no P2P, loopback cookie RPC and a 180-second guard timeout. No bare version/help invocation. The recorded RPC network version identifies the running node. Only a public scalar-1 fixture is used; its WIF is written to an owned 0600 file and removed on shutdown. Do not fund fixture keys on any real network.

Default evidence destination is `evidence/mint-pool-regtest/`. Existing evidence is never overwritten; repeat with a new absolute destination argument. Logs include raw public transactions, not cookies/authorization headers/WIF. The independent signature on the downloaded release is not authenticated; archive bytes are pinned to the same digest as the existing harness.

## API

```js
const { SponsorPool } = require('./mint/pool')
const { createRpc } = require('./mint/node-rpc')
const rpc = createRpc({ url: 'http://127.0.0.1:19483', cookiePath: '/owned/regtest/.cookie' })
const pool = new SponsorPool({
  keyPath: '/owned/sponsor.key', // absolute path; POSIX regular owned file, 0600
  ledgerPath: '/owned/pool.jsonl',
  rpc,
  depth: 5,           // K, minimum 1
  capSats: 1000000,   // bounds held reservations plus next input amount
  prepFee: 500,      // default; integer 1..10000, no automatic fee escalation
})
// parent is a bsv.Transaction, index identifies a sponsor-owned P2PKH UTXO.
const prep = await pool.prepare(parent, index)
const statuses = await pool.refresh()
const fundingParent = await pool.dispense() // bsv.Transaction or null
pool.close()
```

Call `prepare` to replenish from explicitly supplied source outpoints. It validates the source against `gettxout`, signs one input to one output at index zero, and checks the exact BOX-ORDINAL-SPONSOR-1 §3 byte grammar. The prep fee is separate from the later custody-transition fee; existing covenant enforcement of the latter remains unchanged (1..10000 sat; fixtures use 500).

`dispense` rechecks depth, script, amount and unspentness, then returns the oldest **eligible** parent in insertion order. An unconfirmed/spent/reorged older entry does not block eligible later entries. Each handoff is persisted before returning it, so it is never reissued after restart. Confirmation is not a guarantee against a subsequent reorg or an external conflicting spend; the future transfer worker must revalidate before use.

## Ledger and failure model

JSONL events are append-only:
- `prepared`: source outpoint, raw signed parent/txid, input sats, output amount, prep fee. Written and fsynced **before** broadcasting.
- `dispensed`: txid. Written and fsynced before handing the parent to a caller.

`totals()` returns `inputSats`, `prepFeeSats`, `preparedSats`, `dispensedSats`, `heldSats`. Identities: input = prep fee + prepared; prepared = dispensed + held. These are reservation totals, not an assertion that every broadcast succeeded. An ambiguous/rejected broadcast remains reserved and counted against the cap; `refresh` can discover subsequent inclusion. There is deliberately no automatic release/rebroadcast or stale-lock deletion. Stop the writer and reconcile against the chain before recovery. A crash between durable dispense and delivery sacrifices availability rather than reissuing funding.

An exclusive `.lock` file prevents concurrent processes; simultaneous async operations fail busy rather than race. `close()` is synchronous and throws `Pool busy` while an operation is active, retaining both descriptors and the lock; await that operation (including rejection) and retry close. Idle close is idempotent. Closed pools reject prepare/refresh/dispense and ledger appends without RPC or writes. A synchronous ledger failure poisons and closes the writer before the operation rejects, preventing broadcast or delivery from that failed operation. Truncated/corrupt ledgers fail closed. Use one canonical ledger path in an operator-owned directory on a local filesystem, not symlink aliases/network filesystems, and never edit events or share the sponsor key with another spender. The phase-1 pool is not a distributed coordinator, scheduler, root-UTXO finder, or full crash-recovery service. The cap covers undistributed funding reservations, not funds already handed to downstream workers or unrelated key UTXOs. Manual top-ups and caller-driven replenishment are intentional.

## Evidence boundary

The integration matures a coinbase, splits a sponsor root, admits three real preparations to the mempool, mines all three to depth 5, dispenses FIFO, and compares ledger fees/amounts with node-decoded input/output values. Root splitting has its own separately reported 500-sat fee. The evidence does not establish mainnet miner policy, real-wallet compatibility, production security or a sale-loop implementation.
