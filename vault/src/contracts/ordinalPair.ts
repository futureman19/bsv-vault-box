import { method, prop, SmartContract, assert, hash256, sha256, len, slice, toByteString, Utils, hash160, ByteString, PubKey, Sig } from 'scrypt-ts'

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
    public move(sig: Sig, action: bigint, recipient: PubKey, parent: ByteString,
        sponsor: PubKey, sponsorSig: Sig, fundingPrefix: ByteString,
        fundingLocktime: ByteString, fundingValue: bigint, change: bigint) {
        assert(slice(sig, len(sig) - 1n) == toByteString('41'))
        assert(this.checkSig(sig, this.owner))
        assert(len(recipient) == 33n)
        assert(len(this.prevouts) == 72n || len(this.prevouts) == 108n)
        assert(this.ctx.utxo.value == 1n)
        // txid = SHA256(SHA256(raw)); never include recursive raw witnesses.
        assert(len(parent) == 32n)
        assert(sha256(parent) == this.ctx.utxo.outpoint.txid)
        let changeOutput = toByteString('')
        if (len(this.prevouts) == 108n) {
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
            assert(slice(this.prevouts, 72n) == fundingTxid + toByteString('00000000'))
            if (change > 0n) {
                changeOutput = Utils.buildPublicKeyHashOutput(hash160(sponsor), change)
            }
        } else {
            assert(fundingValue == 0n && change == 0n)
            assert(len(fundingPrefix) == 0n && len(fundingLocktime) == 0n)
            assert(len(sponsor) == 0n && len(sponsorSig) == 0n)
        }
        const pair: ByteString = this.ctx.utxo.outpoint.txid + toByteString('00000000') + this.ctx.utxo.outpoint.txid + toByteString('01000000')
        if (this.phase == 0n) {
            assert(action == 0n)
            assert(this.ctx.utxo.outpoint.outputIndex == 0n)
            assert(slice(this.prevouts, 0n, 36n) == this.origin)
            assert(slice(this.prevouts, 36n, 72n) == this.ctx.utxo.outpoint.txid + toByteString('00000000'))
            this.phase = 1n
        } else {
            assert(slice(this.prevouts, 0n, 72n) == pair)
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
        assert(this.ctx.hashOutputs == hash256(outputs + changeOutput))
    }
}
