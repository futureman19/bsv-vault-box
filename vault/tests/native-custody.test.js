const assert = require('node:assert/strict')
const N = require('../src/native-custody')
describe('BOX-NATIVE-1 actual Script VM', () => {
  it('implements the native wrapper experiment', () => assert.equal(typeof N.fixture, 'function'))
  let f, sealed, transferred, opened
  before(() => {
    f = N.fixture()
    const pack = N.move(f.genesis, 'pack', f.alice); assert.equal(pack.result.success, true)
    const remove = N.move(pack, 'remove', f.alice); assert.equal(remove.result.success, true)
    const again = N.move(remove, 'pack', f.alice); assert.equal(again.result.success, true)
    sealed = N.move(again, 'seal', f.alice); assert.equal(sealed.result.success, true)
    transferred = N.move(sealed, 'transfer', f.alice, f.bob.publicKey.toString()); assert.equal(transferred.result.success, true)
    opened = N.move(transferred, 'open', f.bob); assert.equal(opened.result.success, true)
  })
  it('full lifecycle with anchored replay', () => {
    const withdrawn = N.move(opened, 'withdraw', f.bob)
    assert.equal(withdrawn.result.success, true)
    assert.equal(N.decode(withdrawn.tx.outputs[0].script).phase, 4)
    assert.equal(N.move(withdrawn, 'transfer', f.bob, f.alice.publicKey.toString()).result.success, true)
    assert.equal(N.verifyHistory(f.genesis, [...withdrawn.ancestors, withdrawn]).valid, true)
  })
  for (const action of ['remove', 'withdraw', 'pack']) it(`sealed ${action} bypass rejected by VM`, () => assert.equal(N.move(sealed, action, f.alice).result.success, false))
  it('old owner cannot open after transfer', () => assert.equal(N.move(transferred, 'open', f.alice).result.success, false))
  it('wrong signature cannot transfer', () => assert.equal(N.move(sealed, 'transfer', f.bob, f.bob.publicKey.toString()).result.success, false))
  it('open is irreversible', () => assert.equal(N.move(opened, 'seal', f.bob).result.success, false))
  it('withdrawn wrapper cannot repack', () => assert.equal(N.move(N.move(opened, 'withdraw', f.bob), 'pack', f.bob).result.success, false))
  const attacks = {
    'asset substitution': (tx, src) => tx.outputs[0].setScript(N.forgeScript(src, { asset: 'ff'.repeat(32), phase: 2 })),
    'inventory removal': tx => { tx.outputs.length = 0 },
    'duplicate asset': tx => tx.addOutput(new N.bsv.Transaction.Output({ script: tx.outputs[0].script, satoshis: 1 })),
    'fee diversion': tx => { tx.outputs[0].satoshis -= 1 },
    'change diversion': tx => tx.addOutput(new N.bsv.Transaction.Output({ script: N.bsv.Script.buildPublicKeyHashOut(f.bob.toAddress()), satoshis: 1 })),
    'counterfeit box replacement': (tx, src) => tx.outputs[0].setScript(N.forgeScript(src, { owner: f.bob.publicKey.toString(), phase: 0 })),
    'sibling input injection': tx => tx.addInput(new N.bsv.Transaction.Input({prevTxId: '22'.repeat(32), outputIndex: 0, script: '', output: new N.bsv.Transaction.Output({script: N.bsv.Script.empty(), satoshis: 1})})),
  }
  for (const [label, mutate] of Object.entries(attacks)) it(`${label} rejected with fresh signature/preimage`, () => {
    const attempt = N.move(sealed, 'transfer', f.alice, f.alice.publicKey.toString(), mutate)
    assert.equal(attempt.result.success, false, label)
    assert.ok(attempt.result.error)
  })
  it('counterfeit standalone genesis rejected by anchored validation', () => assert.equal(N.verifyHistory(f.genesis, [N.fixture('ff'.repeat(32)).genesis]).valid, false))
  it('omitted ancestor rejected by history validator', () => assert.equal(N.verifyHistory(f.genesis, [sealed]).valid, false))
  it('forged sibling proof rejected by VM', () => assert.equal(N.move(sealed, 'transfer', f.alice, f.alice.publicKey.toString(), null, '00'.repeat(36)).result.success, false))
  it('decoder rejects unrelated scripts', () => assert.throws(() => N.decode(N.bsv.Script.buildPublicKeyHashOut(f.alice.toAddress()))))
  it('local zero-fee prototype preserves principal at minimum balance', () => {
    const tiny = N.fixture()
    tiny.genesis.tx.outputs[0].satoshis = 101
    const p = N.move(tiny.genesis, 'pack', tiny.alice)
    assert.equal(p.result.success, true)
    assert.equal(p.tx.outputs[0].satoshis, 101)
    assert.equal(N.move(p, 'remove', tiny.alice).result.success, true)
  })
  it('old owner cannot transfer or withdraw after transfer', () => {
    assert.equal(N.move(transferred, 'transfer', f.alice).result.success, false)
    assert.equal(N.move(opened, 'withdraw', f.alice).result.success, false)
  })
  it('same label on a different genesis is not the same asset', () => {
    const fake = N.fixture()
    fake.genesis.tx.outputs[0].satoshis -= 1
    assert.equal(N.decode(fake.genesis.tx.outputs[0].script).asset, N.decode(f.genesis.tx.outputs[0].script).asset)
    const branch = N.move(fake.genesis, 'pack', fake.alice)
    assert.equal(branch.result.success, true)
    assert.equal(N.verifyHistory(f.genesis, [branch]).valid, false)
  })
  it('serialized transactions replay through VM without builder result metadata', () => {
    const raw = [...opened.ancestors, opened].map(e => ({tx: new N.bsv.Transaction(e.tx.uncheckedSerialize())}))
    const root = {tx: new N.bsv.Transaction(f.genesis.tx.uncheckedSerialize())}
    assert.equal(N.verifyHistory(root, raw).valid, true)
    raw[0].tx.inputs[0].setScript(N.bsv.Script.empty())
    assert.equal(N.verifyHistory(root, raw).valid, false)
  })
  it('competing remove and seal cannot both enter local ledger', () => {
    const ledger = new N.LocalLedger(f.genesis)
    const packed = N.move(f.genesis, 'pack', f.alice); ledger.accept(packed)
    const removed = N.move(packed, 'remove', f.alice)
    const other = N.move(packed, 'seal', f.alice)
    assert.equal(other.result.success, true)
    ledger.accept(removed)
    assert.throws(() => ledger.accept(other), /spent|parent/)
  })
  it('one-satoshi principal remains spendable', () => {
    const tiny = N.fixture(); tiny.genesis.tx.outputs[0].satoshis = 1
    assert.equal(N.move(tiny.genesis, 'pack', tiny.alice).result.success, true)
  })
  it('local UTXO ledger rejects replay/double spend', () => {
    const ledger = new N.LocalLedger(f.genesis)
    const packed = N.move(f.genesis, 'pack', f.alice)
    ledger.accept(packed)
    assert.throws(() => ledger.accept(packed), /spent|parent/)
  })
})
