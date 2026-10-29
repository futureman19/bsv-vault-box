const fs = require('node:fs')
const path = require('node:path')
const assert = require('node:assert/strict')
const crypto = require('node:crypto')
const N = require('../src/native-custody')
const f = N.fixture(), ledger = new N.LocalLedger(f.genesis)
for (const [action, signer] of [['pack','alice'],['remove','alice'],['pack','alice'],['seal','alice'],['transfer','alice'],['open','bob'],['withdraw','bob']]) {
  const step = N.move(ledger.tip, action, f[signer], f.bob.publicKey.toString())
  assert.equal(step.result.success, true)
  ledger.accept(step)
}
const vector = {
  format: 'BOX-NATIVE-1 research only, synthetic genesis, zero fee',
  compiler: require('../artifacts/nativeVault.json').compilerVersion,
  codeHash: crypto.createHash('sha256').update(require('../artifacts/nativeVault.json').hex).digest('hex'),
  genesis: f.genesis.tx.uncheckedSerialize(),
  transitions: ledger.history.map(e => ({ action: e.action, txid: e.tx.id, raw: e.tx.uncheckedSerialize() })),
  final: ledger.snapshot()
}
const target = path.join(__dirname, '../fixtures/native-vectors.json')
if (process.argv.includes('--check')) {
  assert.deepEqual(vector, JSON.parse(fs.readFileSync(target)))
  // Replay byte-decoded transactions, never cached builder state/results.
  const replay = N.verifyHistory({tx: new N.bsv.Transaction(vector.genesis)}, vector.transitions.map(e=>({tx:new N.bsv.Transaction(e.raw)})))
  assert.equal(replay.valid, true)
  console.log('PASS: seven deterministic transaction vectors and serialized Script VM replay')
} else {
  fs.mkdirSync(path.dirname(target), {recursive:true})
  if (fs.existsSync(target)) throw Error('Refusing to overwrite golden fixture; review and remove explicitly')
  fs.writeFileSync(target, JSON.stringify(vector, null, 2) + '\n')
  console.log('Generated local deterministic vectors: ' + target)
}
