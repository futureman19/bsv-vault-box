import { method, prop, SmartContract, assert, hash256, sha256, len, slice, toByteString, Utils, hash160, ByteString, PubKey, Sig } from 'scrypt-ts'

/** Offline fixed four-ordinal bundle. No sponsorship or resealing. */
export class FourOrdinal extends SmartContract {
    @prop() origins: ByteString
    @prop(true) phase: bigint
    @prop(true) owner: PubKey
    constructor(origins: ByteString, phase: bigint, owner: PubKey) {
        super(...arguments)
        this.origins = origins
        this.phase = phase
        this.owner = owner
    }
    @method()
    public move(sig: Sig, action: bigint, recipient: PubKey, parent: ByteString) {
        assert(slice(sig, len(sig) - 1n) == toByteString('41'))
        assert(this.checkSig(sig, this.owner))
        assert(len(recipient) == 33n)
        assert(len(this.origins) == 144n)
        assert(len(this.prevouts) == 180n)
        assert(this.ctx.utxo.value == 1n)
        assert(len(parent) == 32n)
        assert(sha256(parent) == this.ctx.utxo.outpoint.txid)
        const id = this.ctx.utxo.outpoint.txid
        // Every executed covenant checks its own actual UTXO index.
        assert(this.ctx.utxo.outpoint.outputIndex >= 0n && this.ctx.utxo.outpoint.outputIndex <= 4n)
        if (this.phase == 0n) {
            assert(action == 0n)
            assert(this.ctx.utxo.outpoint.outputIndex == 0n)
            assert(this.prevouts == this.origins + id + toByteString('00000000'))
            this.phase = 1n
        } else {
            const ordered = id + toByteString('00000000') + id + toByteString('01000000') + id + toByteString('02000000') + id + toByteString('03000000') + id + toByteString('04000000')
            assert(this.prevouts == ordered)
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
        let destination = toByteString('')
        if (action == 4n) {
            destination = Utils.buildPublicKeyHashOutput(hash160(this.owner), 1n)
        } else {
            destination = this.buildStateOutput(1n)
        }
        assert(this.ctx.hashOutputs == hash256(destination + destination + destination + destination + destination))
    }
}
