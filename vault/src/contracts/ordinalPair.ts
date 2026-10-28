import { method, prop, SmartContract, assert, hash256, len, slice, toByteString, Utils, hash160, ByteString, PubKey, Sig } from 'scrypt-ts'

/** LOCAL DRAFT: external ordinal at input/output zero; control at one. */
export class OrdinalPair extends SmartContract {
    @prop() origin: ByteString
    @prop(true) phase: bigint
    @prop(true) owner: PubKey
    constructor(origin: ByteString, phase: bigint, owner: PubKey) {
        super(...arguments)
        this.origin = origin
        this.phase = phase
        this.owner = owner
    }
    @method()
    public move(sig: Sig, action: bigint, recipient: PubKey, parent: ByteString) {
        assert(this.checkSig(sig, this.owner))
        assert(len(recipient) == 33n)
        assert(len(this.prevouts) == 72n)
        assert(this.ctx.utxo.value == 1n)
        assert(hash256(parent) == this.ctx.utxo.outpoint.txid)
        const pair: ByteString = this.ctx.utxo.outpoint.txid + toByteString('00000000') + this.ctx.utxo.outpoint.txid + toByteString('01000000')
        if (this.phase == 0n) {
            assert(action == 0n)
            assert(this.ctx.utxo.outpoint.outputIndex == 0n)
            assert(slice(this.prevouts, 0n, 36n) == this.origin)
            assert(slice(this.prevouts, 36n) == this.ctx.utxo.outpoint.txid + toByteString('00000000'))
            this.phase = 1n
        } else {
            assert(this.prevouts == pair)
            assert(this.ctx.utxo.outpoint.outputIndex <= 1n)
            if (action == 1n) {
                assert(this.phase == 1n)
                this.phase = 2n
            } else if (action == 2n) {
                assert(this.phase == 2n)
                this.owner = recipient
            } else if (action == 3n) {
                assert(this.phase == 2n)
                this.phase = 3n
            } else {
                assert(action == 4n && this.phase == 3n)
            }
        }
        let outputs: ByteString = toByteString('')
        if (action == 4n) {
            const pay: ByteString = Utils.buildPublicKeyHashOutput(hash160(this.owner), 1n)
            outputs = pay + pay
        } else {
            const continuation: ByteString = this.buildStateOutput(1n)
            outputs = continuation + continuation
        }
        assert(this.ctx.hashOutputs == hash256(outputs))
    }
}
