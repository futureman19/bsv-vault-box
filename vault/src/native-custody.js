'use strict'
// LOCAL ONLY. Deliberately no provider, wallet discovery, networking or broadcast.
const S = require('scryptlib')
const { bsv } = S
const artifact = require('../artifacts/nativeVault.json')
const Contract = S.buildContractClass(artifact)
const ACTIONS = { pack: 0, remove: 1, seal: 2, transfer: 3, open: 4, withdraw: 5 }
const PHASES = ['FREE', 'PACKED', 'SEALED', 'OPENED', 'WITHDRAWN']
const FEE = 0 // LOCAL zero-fee prototype; fee sponsorship is a production blocker.
function decode(script) {
  const c = Contract.fromHex(script.toHex())
  const phase = Number(c.phase)
  const asset = c.ctorArgs().find(a => a.name === 'asset').value
  if (!PHASES[phase] || !/^[0-9a-f]{64}$/.test(asset) || !/^(02|03)[0-9a-f]{64}$/.test(c.owner)) throw Error('unsupported native NFT encoding')
  if (c.lockingScript.toHex() !== script.toHex()) throw Error('noncanonical script')
  return { asset, owner: c.owner, phase, label: PHASES[phase] }
}
function fixture(asset = '42'.repeat(32)) {
  // Public disposable test-vector scalars, NEVER fund these identities.
  const alice = new bsv.PrivateKey(new bsv.crypto.BN(1), bsv.Networks.testnet)
  const bob = new bsv.PrivateKey(new bsv.crypto.BN(2), bsv.Networks.testnet)
  const contract = new Contract(asset, 0n, alice.publicKey.toString())
  contract.phase = 0n; contract.owner = alice.publicKey.toString()
  const tx = new bsv.Transaction().addInput(new bsv.Transaction.Input({ prevTxId: '11'.repeat(32), outputIndex: 0, script: '', output: new bsv.Transaction.Output({script: bsv.Script.empty(), satoshis: 1000000}) }))
    .addOutput(new bsv.Transaction.Output({ script: contract.lockingScript, satoshis: 1000000 }))
  return { alice, bob, genesis: { tx, ancestors: [], synthetic: true } }
}
function forgeScript(source, overrides) {
  const state = { ...decode(source.tx.outputs[0].script), ...overrides }
  const c = new Contract(state.asset, BigInt(state.phase), state.owner)
  return c.getNewStateScript({ phase: BigInt(state.phase), owner: state.owner })
}
function prevouts(tx) {
  return tx.inputs.map(i => Buffer.concat([Buffer.from(i.prevTxId).reverse(), (() => { const n = Buffer.alloc(4); n.writeUInt32LE(i.outputIndex); return n })()]).toString('hex')).join('')
}
function verifySpend(parent, tx) {
  const output = parent.tx.outputs[0]
  if (tx.inputs.length !== 1 || tx.inputs[0].prevTxId.toString('hex') !== parent.tx.id || tx.inputs[0].outputIndex !== 0) return { success: false, error: 'wrong parent or sibling input' }
  const interpreter = new bsv.Script.Interpreter()
  // Post-Genesis Script VM, same flags as scryptlib, not a JavaScript state simulation.
  const success = interpreter.verify(tx.inputs[0].script, output.script, tx, 0, S.DEFAULT_FLAGS, new bsv.crypto.BN(output.satoshis))
  return { success, error: success ? '' : interpreter.errstr }
}
function move(source, action, key, recipient, mutate, proofOverride) {
  if (!(action in ACTIONS)) throw Error('unknown action')
  const output = source.tx.outputs[0]
  const state = decode(output.script)
  const c = Contract.fromHex(output.script.toHex())
  recipient = recipient || state.owner
  const nextPhase = { pack: 1, remove: 0, seal: 2, open: 3, withdraw: 4 }[action] ?? state.phase
  const nextOwner = action === 'transfer' ? recipient : state.owner
  const script = c.getNewStateScript({ phase: BigInt(nextPhase), owner: nextOwner })
  const tx = new bsv.Transaction().addInput(new bsv.Transaction.Input({ prevTxId: source.tx.id, outputIndex: 0, script: '', output }))
    .addOutput(new bsv.Transaction.Output({ script, satoshis: output.satoshis - FEE }))
  // Attack harness mutates BEFORE signing/preimage; rejection cannot be attributed
  // merely to a stale owner signature. Public local UI never supplies this hook.
  if (mutate) mutate(tx, source)
  const preimage = S.getLowSPreimage(tx, output.script, output.satoshis)
  const sig = S.signTx(tx, key, output.script, output.satoshis)
  const call = c.move(sig, BigInt(ACTIONS[action]), recipient, preimage, proofOverride ?? prevouts(tx))
  tx.inputs[0].setScript(call.toScript())
  // Direct scryptlib VM verification, including sibling-injection attacks.
  const result = call.verify({ tx, inputIndex: 0, inputSatoshis: output.satoshis })
  return { tx, result, action, ancestors: source.synthetic ? [] : [...source.ancestors, source] }
}
function verifyHistory(genesis, entries) {
  try {
    const initial = decode(genesis.tx.outputs[0].script)
    if (initial.phase !== 0) throw Error('genesis must be free')
    let parent = genesis
    const seen = new Set([genesis.tx.id])
    for (const entry of entries) {
      if (seen.has(entry.tx.id)) throw Error('duplicate transaction')
      const check = verifySpend(parent, entry.tx)
      if (!check.success) throw Error(check.error)
      const state = decode(entry.tx.outputs[0].script)
      if (state.asset !== initial.asset) throw Error('identity mismatch')
      seen.add(entry.tx.id); parent = entry
    }
    const state = decode(parent.tx.outputs[0].script)
    return { valid: true, anchor: genesis.tx.id + ':0', tip: parent.tx.id + ':0', state, inventory: state.phase >= 1 && state.phase <= 3 ? [genesis.tx.id + ':0'] : [] }
  } catch (e) { return { valid: false, error: e.message } }
}
class LocalLedger {
  constructor(genesis) { this.genesis = genesis; this.tip = genesis; this.history = [] }
  accept(entry) {
    const check = verifySpend(this.tip, entry.tx)
    if (!check.success) throw Error('spent or invalid parent: ' + check.error)
    this.history.push(entry); this.tip = entry
    return this.snapshot()
  }
  snapshot() { return verifyHistory(this.genesis, this.history) }
}
module.exports = { bsv, fixture, move, decode, forgeScript, verifySpend, verifyHistory, LocalLedger, ACTIONS, PHASES, FEE }
