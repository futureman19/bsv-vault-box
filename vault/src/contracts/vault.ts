import {
    method,
    prop,
    SmartContract,
    hash256,
    assert,
    ByteString,
    PubKey,
    Sig,
    Sha256,
} from 'scrypt-ts'

/**
 * VAULT-0001 sealed vault box covenant.
 * States: 0 = SEALED, 1 = OPENED. boxId and contentRef are immutable.
 * Legal transitions: transfer (boxState preserved), open (SEALED->OPENED only).
 * Everything else is impossible: hashOutputs must match the rebuilt boxState output.
 */
export class Vault extends SmartContract {
    @prop(true)
    boxState: bigint // 0n = SEALED, 1n = OPENED

    @prop()
    boxId: Sha256 // immutable box identity

    @prop()
    contentRef: Sha256 // immutable content commitment

    @prop(true)
    owner: PubKey

    constructor(boxState: bigint, boxId: Sha256, contentRef: Sha256, owner: PubKey) {
        super(...arguments)
        this.boxState = boxState
        this.boxId = boxId
        this.contentRef = contentRef
        this.owner = owner
    }

    @method()
    public transfer(sig: Sig, nextOwner: PubKey) {
        assert(this.checkSig(sig, this.owner), 'owner signature required')
        assert(this.boxState == 0n || this.boxState == 1n, 'invalid boxState byte')
        // boxState and contentRef untouched -> preserved in the rebuilt output
        this.owner = nextOwner
        const amount: bigint = this.ctx.utxo.value
        const outputs: ByteString =
            this.buildStateOutput(amount) + this.buildChangeOutput()
        assert(this.ctx.hashOutputs == hash256(outputs), 'hashOutputs mismatch')
    }

    @method()
    public open(sig: Sig) {
        assert(this.checkSig(sig, this.owner), 'owner signature required')
        assert(this.boxState == 0n, 'only a sealed box can be opened')
        this.boxState = 1n // SEALED -> OPENED, irreversible: no method clears it
        const amount: bigint = this.ctx.utxo.value
        const outputs: ByteString =
            this.buildStateOutput(amount) + this.buildChangeOutput()
        assert(this.ctx.hashOutputs == hash256(outputs), 'hashOutputs mismatch')
    }
}
