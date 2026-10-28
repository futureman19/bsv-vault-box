import {
    method, prop, SmartContract, assert, hash256, len,
    ByteString, PubKey, Sig, Sha256,
} from 'scrypt-ts'

/** Draft BOX-NATIVE-1. One NFT and its single-use wrapper share ONE UTXO.
 * No sibling-output claims, external NFTs, ordinals, fee inputs or change.
 * 0 free, 1 packed, 2 sealed, 3 opened, 4 withdrawn (terminal wrapper).
 */
export class NativeVault extends SmartContract {
    @prop() asset: Sha256
    @prop(true) phase: bigint
    @prop(true) owner: PubKey

    constructor(asset: Sha256, phase: bigint, owner: PubKey) {
        super(...arguments)
        this.asset = asset
        this.phase = phase
        this.owner = owner
    }

    @method()
    public move(sig: Sig, action: bigint, recipient: PubKey) {
        assert(this.checkSig(sig, this.owner), 'current owner signature required')
        assert(len(this.prevouts) == 36n, 'exactly one input; no siblings')
        assert(this.phase >= 0n && this.phase <= 4n, 'invalid phase')
        assert(len(recipient) == 33n, 'compressed recipient required')
        assert(this.ctx.utxo.value >= 1n, 'positive principal required')
        // action 0 pack, 1 remove, 2 seal, 3 transfer, 4 open, 5 withdraw
        if (action == 0n) {
            assert(this.phase == 0n, 'only free asset can pack')
            this.phase = 1n
        } else if (action == 1n) {
            assert(this.phase == 1n, 'only unsealed inventory can remove')
            this.phase = 0n
        } else if (action == 2n) {
            assert(this.phase == 1n, 'only packed inventory can seal')
            this.phase = 2n
        } else if (action == 3n) {
            this.owner = recipient
        } else if (action == 4n) {
            assert(this.phase == 2n, 'only sealed can open')
            this.phase = 3n
        } else {
            assert(action == 5n && this.phase == 3n, 'withdraw requires opened wrapper')
            this.phase = 4n
        }
        // Non-transfer calls cannot change authority. One exact continuation;
        // no fee/change destination or metadata-only inventory representation.
        const outputs: ByteString = this.buildStateOutput(this.ctx.utxo.value)
        assert(this.ctx.hashOutputs == hash256(outputs), 'exact NFT continuation required')
    }
}
