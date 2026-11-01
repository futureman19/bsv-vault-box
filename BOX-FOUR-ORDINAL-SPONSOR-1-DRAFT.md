# BOX-FOUR-ORDINAL-SPONSOR-1 — bounded sponsorship and isolated regtest

## Result

Separate `FourOrdinalSponsored` compiled contract, artifact, builder, tests and node runner. Existing four-ordinal offline fixtures, single-ordinal implementation, artifacts and website are unchanged. The public site remains a fictional demo. Local feature-branch work only; no push or public-chain transaction.

**Executed gate:** compiler 1 passing / 0 failing; TypeScript exit 0; **129 VM tests passing (original 95 + new 34)**; four existing deterministic fixture checks unchanged. Bitcoin SV **1.2.3** independently admitted and confirmed **16 non-coinbase transactions**, rejected **20 security alternatives** with RPC -26 mandatory Script failures, reached height **126**, and returned `verifychain(4,0) = true`. Every attack's actual inputs were queried unspent before and after submission, before the valid competing spend. Invalid alternatives were never mined. Offline replay of the stored node bytes independently passes all 16 valid and rejects all 20 invalid transactions in the VM, and computes **8500 sats** total actual fees.

Evidence: `evidence/four-ordinal-sponsored/`; full node: `regtest-run-1/`. Includes raw transactions, generated non-secret config, full RPC request/result journal, exact argv, installed binary hash, node logs, block confirmation evidence, final UTXOs, process snapshots and shutdown status. Cookie contents and existing wallet/config files are not captured or read.

## Enforced construction

Mandatory exactly six ordered inputs: four original one-sat text inscriptions, one control sat, then one sponsor input. Every covenant validates its actual one-sat value, parent digest, own output index, ordered principal vector, sponsor prevout and exact entire outputs. Pack uses the four immutable original outpoints and separate initial control; subsequent operations require outputs 0..4 of the same authenticated parent. The owner and sponsor each authorize the whole transaction with SIGHASH_ALL|FORKID (`41`), and the funding input independently executes its P2PKH authorization. All input sequences/preimages stabilize before **any** signatures.

Outputs 0..4 are exactly one sat, identical next-state covenants until withdrawal, then five current-owner P2PKH outputs. Sponsor change, if positive, is only output 5 to HASH160(sponsor). No additional outputs. Let authenticated funding value be V and change C: `0 < V <= 2100000000000000`, `0 <= C < V`, and `1 <= V-C <= 10000` sat. No-change funding emits only the five principals. Transfer changes all covenant owners; old-owner open/withdraw and withdrawal while sealed fail compiled Script.

This reuses the restrictive **one-input, one-output-index-zero canonical funding-parent grammar** from BOX-ORDINAL-SPONSOR-1: prefix `version[4] || 01 || prevout[36] || N[1] || scriptSig[N] || sequence[4] || 01`, N <= 108, prefix length exactly 47+N; reconstructed output `amount[8] || 19 || P2PKH(sponsor)[25]`; four-byte locktime. Script validates boundaries and hashes the reconstructed transaction against input 5. Arbitrary wallet UTXOs, multiple inputs/outputs, extended scriptSig lengths and direct reuse of lifecycle change are not accepted. Prepare a qualifying parent first; its fee is separate.

Foreign asset one-sat admission is still a client/actual-UTXO base case, not sibling-amount introspection. Subsequent preservation follows enforced exact outputs and ordered ancestry. A 32-byte inner parent digest prevents recursive witness growth but is not generic sibling-script introspection. Script does not verify certificate provenance. The node runner creates an explicit scalar-3 issuer signature naming the three genuine original outpoints, then inscribes its canonical envelope SHA256 as 64 ASCII hex characters in the fourth, certificate record. It retains the detached envelope and ordered outer manifest, with explicit fixture trusted-issuer policy. All content remains tiny one-push text/plain, not images, arbitrary NFTs, or production certificates.

## Real regtest ancestry and fees

No synthetic roots are sent to the node. Mine 110 blocks to public disposable Alice scalar 1, spend a matured coinbase into ten funding outputs and change, mint four independent inscriptions and separate EMPTY control, prepare five bounded P2PKH sponsor parents paying public Bob scalar 2, and execute pack → seal → transfer → open → withdraw. Never fund these public fixture keys elsewhere.

Each lifecycle consumes 999500 sponsor sats, returns 999000 and pays **500 sats**; all five principal sats survive. Lifecycle fees: **2500**. Five sponsor preparations: **2500** separately. Funding split: **1000**. Four inscriptions plus initial control: **2500**. Total mined non-coinbase fees: **8500**, independently computed from captured input/output values. Invalid alternatives pay no mined fee and reuse a still-unspent preparation until the valid lifecycle step spends it.

| Lifecycle | Serialized bytes |
|---|---:|
| Pack | 24054 |
| Seal | 41740 |
| Transfer | 41736 |
| Open | 41742 |
| Withdraw | 23201 |

Final transaction: `4cd43d140973d410b212f58216a3c9abaed6df35ac8a2cd3a38c7950503f1661`. Its outputs 0..4 are confirmed one-sat Bob P2PKH UTXOs in this exact order:

| Role | Original transaction (output 0) | Final output |
|---|---|---:|
| Collectible Box | `75ea6ef6cae46f0a67bbb7cf853cde4841c5108b9ddf88153083bc535c41f3cd` | 0 |
| Certificate | `e938d9113d186ead8d70d1f6aca2acce022fc36ebe86344e38738656ddc3dd90` | 1 |
| Object one | `badbf6642847d1bc0cd1c3f2e424f95e0db315e8d58e580bafabf70953c0c31f` | 2 |
| Object two | `f3864ef3b780cdaf0c5d2b77ffc1c098f07738bf8eb56b79b41f9d201861b751` | 3 |
| Control | `990beb9f0c0787ef4706f9f76826179de1c11bd032776a24dac34b16de2b7c51` | 4 |

## Security tests and TDD evidence

Tests were written before new contract/builder code. `red.txt` records a meaningful baseline failure: the old four-item builder returns five inputs, not the required six. `red-distinct.txt` records a second real failure: the initial sponsor fixture reused one funding parent across lifecycle steps; fixed by deriving distinct synthetic fixture roots. New production Script was not written before the first RED. The remaining adversarial cases were specified before implementation but were **not each independently observed RED**.

34 new VM tests include full lifecycle, distinct funding parents, fee boundaries and no-change, zero/negative/excess fees, every principal diversion, missing/reordered sponsor, change omission/diversion/extra outputs, parent boundaries/amount/locktime, missing and genuinely wrong sponsor authorization, wrong sighash types, independent P2PKH authorization, old-owner attacks and sealed withdrawal. All five covenants independently reject changed output commitments.

20 native-node failures cover missing/wrong sponsor authorization; three malformed parent witnesses; reordered sponsor; zero/negative fee witnesses and actual excess-fee transaction; change diversion and extra output; each of five principal diversions; missing funding P2PKH authorization; sealed withdrawal; old-owner open/withdraw. Zero/negative node cases alter the authenticated change witness while keeping a funded transaction, so ledger overspend cannot mask Script fee-bound enforcement. Actual zero/negative-fee output constructions and missing sponsor input are additionally tested in VM, not claimed as separate native-node acceptance-path tests.

## Isolation and exact reproduction

Only installed `/home/futureman19/bitcoin-sv-1.2.3/bin/bitcoind` was executed, SHA256 `70b36ab04b1bdd5712e58cf43957e21f6d02dd890f0cce6d0acae16e97783610`. No version/help invocation. Version comes from the owned node RPC. The historical fullnode runner contains a bare version probe and was **not executed**; its read/accept helpers were adapted into the separate safe runner.

Fresh datadir: `/mnt/c/Users/futur/.hermes/profiles/telegram2/cache/scratch/box4-sponsored/box4-regtest-e6dkcv`. Owned PID **641**, clean exit 0, `/proc/641` absent at shutdown. Process inventories before/after retained; no pre-existing node was stopped. P2P connection counts 0 at both endpoints. Explicit argv: fresh datadir/config, `-regtest -disablewallet -listen=0 -connect=0 -dnsseed=0 -dns=0 -discover=0 -upnp=0 -rpcbind=127.0.0.1 -rpcallowip=127.0.0.1 -rpcport=33813`. Generated config additionally enables server/txindex, assumevalid=0, Genesis height 1, Chronicle height 2, 100MB excessive block/consensus stack, 10MB construction, 32MB coins cache/16MB DB cache, minminingtxfee=0.00000001, acceptnonstdtxn=0, acceptnonstdoutputs=1. Uses only its fresh cookie. Local policy is not a commercial miner quote.

Commands from `vault/` (on this host executed through Python `subprocess.run([shutil.which('node'), ...], check=True)` to bypass the Windows Node shim):

```sh
node node_modules/scrypt-cli/src/bin/index.js compile -i src/contracts/fourOrdinalSponsored.ts
node node_modules/mocha/bin/mocha.js --no-config tests/ordinal-pair.test.js tests/ordinal-sponsored.test.js tests/four-ordinal.test.js tests/four-ordinal-sponsored.test.js
node node_modules/typescript/bin/tsc --noEmit
node scripts/ordinal-pair-vectors.js
node scripts/ordinal-sponsored-vectors.js
node scripts/four-ordinal-vectors.js
node scripts/native-vectors.js --check
node scripts/four-ordinal-regtest-replay.js ../evidence/four-ordinal-sponsored/regtest-run-1
```

Actual node command from Windows Bash:

```sh
wsl.exe -d Ubuntu-24.04 -- bash -lc 'node /mnt/c/Users/futur/Desktop/bsv-vault-box/vault/scripts/four-ordinal-regtest.js /home/futureman19/bitcoin-sv-1.2.3/bin/bitcoind /mnt/c/Users/futur/.hermes/profiles/telegram2/cache/scratch/box4-sponsored /mnt/c/Users/futur/Desktop/bsv-vault-box/evidence/four-ordinal-sponsored/regtest-run-1'
```

For reruns select a new evidence directory; the runner refuses overwrite and creates a new datadir. Read the full-node skill safety rules first. Only exact owned-child PID fallback signals are permitted.

## Failures and limits

First node run passed; no node retry or alternate install required. WSL emitted benign terminal-dimension warnings. A first inline offline-replay command failed due to nested Python/JS newline quoting (plus Node Windows shutdown assertion); preserved in `independent-replay.txt`. The dedicated replay script then passed (`stored-replay.txt`). One tool refused a full-file overwrite; targeted patch preserved existing content. Earlier GREEN log (33 tests) precedes the distinct-parent test/fix; final `tests.txt` is authoritative at 129.

This closes only the bounded local-regtest gate, not miner/public-chain policy, wallet/indexer compatibility, independent security audit, invalid-block rejection, reorg testing, arbitrary NFTs, asset storage durability, reuse/resealing or production readiness. Ordinal mapping is positional ancestry checked by the harness, not native node awareness of NFT identity. The new module does not export the old five-input history verifier or old fixture generator as though they supported this six-input protocol. Existing fixture evidence remains unchanged. No website, UI, accessories, images or deployment work.
