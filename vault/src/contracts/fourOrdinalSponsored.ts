import { method, prop, SmartContract, assert, hash256, sha256, len, slice, toByteString, Utils, hash160, ByteString, PubKey, Sig } from 'scrypt-ts'

/** Fixed four-ordinal bundle with mandatory bounded sponsorship. No resealing. */
export class FourOrdinalSponsored extends SmartContract {
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
    public move(sig: Sig, action: bigint, recipient: PubKey, parent: ByteString,
        sponsor: PubKey, sponsorSig: Sig, fundingPrefix: ByteString,
        fundingLocktime: ByteString, fundingValue: bigint, change: bigint) {
        assert(slice(sig, len(sig) - 1n) == toByteString('41'))
        assert(this.checkSig(sig, this.owner))
        assert(len(recipient) == 33n)
        assert(len(this.origins) == 144n)
        assert(len(this.prevouts) == 216n)
        assert(this.ctx.utxo.value == 1n)
        assert(len(parent) == 32n)
        assert(sha256(parent) == this.ctx.utxo.outpoint.txid)
        let changeOutput = toByteString('')
            assert(len(sponsor) == 33n)
            assert(slice(sponsorSig, len(sponsorSig) - 1n) == toByteString('41'))
            assert(this.checkSig(sponsorSig, sponsor))
            // Canonical one-input, one-output funding parent, short scriptSig.
            // Parse its boundaries, not a purported unparsed output suffix.
            assert(len(fundingPrefix) >= 47n && len(fundingPrefix) <= 155n)
            assert(slice(fundingPrefix, 4n, 5n) == toByteString('01'))
            const unlockSize = Utils.fromLEUnsigned(slice(fundingPrefix, 41n, 42n))
            assert(unlockSize <= 108n)
            assert(len(fundingPrefix) == 47n + unlockSize)
            assert(slice(fundingPrefix, 46n + unlockSize) == toByteString('01'))
            assert(len(fundingLocktime) == 4n)
            assert(fundingValue > 0n && fundingValue <= 2100000000000000n)
            assert(change >= 0n && change < fundingValue)
            assert(fundingValue - change <= 10000n)
            const fundingOutput = Utils.buildPublicKeyHashOutput(hash160(sponsor), fundingValue)
            const fundingTxid = hash256(fundingPrefix + fundingOutput + fundingLocktime)
            assert(slice(this.prevouts, 180n) == fundingTxid + toByteString('00000000'))
            if (change > 0n) {
                changeOutput = Utils.buildPublicKeyHashOutput(hash160(sponsor), change)
            }
        const id = this.ctx.utxo.outpoint.txid
        // Every executed covenant checks its own actual UTXO index.
        assert(this.ctx.utxo.outpoint.outputIndex >= 0n && this.ctx.utxo.outpoint.outputIndex <= 4n)
        if (this.phase == 0n) {
            assert(action == 0n)
            assert(this.ctx.utxo.outpoint.outputIndex == 0n)
            assert(slice(this.prevouts, 0n, 180n) == this.origins + id + toByteString('00000000'))
            this.phase = 1n
        } else {
            const ordered = id + toByteString('00000000') + id + toByteString('01000000') + id + toByteString('02000000') + id + toByteString('03000000') + id + toByteString('04000000')
            assert(slice(this.prevouts, 0n, 180n) == ordered)
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
        assert(this.ctx.hashOutputs == hash256(destination + destination + destination + destination + destination + changeOutput))
    }
}
