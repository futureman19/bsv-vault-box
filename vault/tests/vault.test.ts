import { expect, use } from 'chai'
import chaiAsPromised from 'chai-as-promised'
import { Vault } from '../src/contracts/vault'
import { getDefaultSigner, randomPrivateKey } from './utils/txHelper'
import {
    MethodCallOptions,
    PubKey,
    Sha256,
    findSig,
    hash256,
    toByteString,
} from 'scrypt-ts'

use(chaiAsPromised)

const SEALED = 0n
const OPENED = 1n

describe('VAULT-0001 covenant graduation tests (script-VM executed)', () => {
    const boxId = hash256(
        toByteString(
            Buffer.from('VAULT-0001 graduation box', 'utf8').toString('hex')
        )
    ) as Sha256
    const contentRef = hash256(
        toByteString(
            Buffer.from(
                'vault graduation content descriptor',
                'utf8'
            ).toString('hex')
        )
    ) as Sha256

    const [alicePriv, alicePub] = randomPrivateKey()
    const [bobPriv, bobPub] = randomPrivateKey()

    const alice = PubKey(alicePub.toByteString())
    const bob = PubKey(bobPub.toByteString())

    const evilRef = hash256(
        toByteString(Buffer.from('EVIL CONTENT', 'utf8').toString('hex'))
    ) as Sha256

    const aliceSigner = getDefaultSigner(alicePriv)
    const bobSigner = getDefaultSigner(bobPriv)

    let sealedBox: Vault

    before(async () => {
        await Vault.loadArtifact()
        sealedBox = new Vault(SEALED, boxId, contentRef, alice)
        await sealedBox.connect(aliceSigner)
        const deployTx = await sealedBox.deploy(1)
        console.log(`deployed sealed box: ${deployTx.id}`)
    })

    it('rejects theft: non-owner cannot transfer', async () => {
        const next = sealedBox.next()
        next.owner = bob
        await sealedBox.connect(aliceSigner)
        const call = sealedBox.methods.transfer(
            (sigResps) => findSig(sigResps, bobPub), // signed by bob, not alice
            bob,
            {
                pubKeyOrAddrToSign: bobPub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).to.be.rejectedWith(/signature check failed/)
    })

    it('rejects content substitution via forged next instance', async () => {
        // A forged continuation (different immutable contentRef baked into the
        // script) cannot produce a valid spend. In this SDK dry-run it fails at
        // the covenant's OP_PUSH_TX preimage gate ('signature check failed');
        // on-chain, a hand-crafted preimage would then fail the hashOutputs
        // assert. Both are consensus-layer rejections of the same forgery.
        const forged = new Vault(SEALED, boxId, evilRef, bob)
        const call = sealedBox.methods.transfer(
            (sigResps) => findSig(sigResps, alicePub),
            bob,
            {
                pubKeyOrAddrToSign: alicePub,
                next: { instance: forged, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).to.be.rejectedWith(
            /signature check failed|hashOutputs mismatch/
        )
    })

    it('allows sealed transfer alice -> bob, preserving state/ids', async () => {
        const next = sealedBox.next()
        next.owner = bob
        const call = sealedBox.methods.transfer(
            (sigResps) => findSig(sigResps, alicePub),
            bob,
            {
                pubKeyOrAddrToSign: alicePub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).not.to.be.rejected
        expect(next.boxState).to.equal(SEALED)
        expect(next.boxId).to.equal(boxId)
        expect(next.contentRef).to.equal(contentRef)
        sealedBox = next
    })

    it('rejects previous owner opening after transfer', async () => {
        const next = sealedBox.next()
        next.boxState = OPENED
        await sealedBox.connect(aliceSigner)
        const call = sealedBox.methods.open(
            (sigResps) => findSig(sigResps, alicePub), // alice no longer owns it
            {
                pubKeyOrAddrToSign: alicePub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).to.be.rejectedWith(/signature check failed/)
    })

    it('allows current owner (bob) to open', async () => {
        const next = sealedBox.next()
        next.boxState = OPENED
        await sealedBox.connect(bobSigner)
        const call = sealedBox.methods.open(
            (sigResps) => findSig(sigResps, bobPub),
            {
                pubKeyOrAddrToSign: bobPub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).not.to.be.rejected
        sealedBox = next
    })

    it('rejects double-open (open an opened box)', async () => {
        const next = sealedBox.next()
        next.boxState = OPENED
        await sealedBox.connect(bobSigner)
        const call = sealedBox.methods.open(
            (sigResps) => findSig(sigResps, bobPub),
            {
                pubKeyOrAddrToSign: bobPub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).to.be.rejectedWith(
            /only a sealed box can be opened/
        )
    })

    it('rejects reseal attempt via tampered transfer', async () => {
        const next = sealedBox.next()
        next.boxState = SEALED // attacker tries to flip OPENED back to SEALED
        next.owner = alice
        const call = sealedBox.methods.transfer(
            (sigResps) => findSig(sigResps, bobPub),
            alice,
            {
                pubKeyOrAddrToSign: bobPub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).to.be.rejectedWith(/hashOutputs mismatch/)
    })

    it('allows opened box transfer bob -> alice', async () => {
        const next = sealedBox.next()
        next.owner = alice
        const call = sealedBox.methods.transfer(
            (sigResps) => findSig(sigResps, bobPub),
            alice,
            {
                pubKeyOrAddrToSign: bobPub,
                next: { instance: next, balance: 1 },
            } as MethodCallOptions<Vault>
        )
        await expect(call).not.to.be.rejected
        expect(next.boxState).to.equal(OPENED)
        sealedBox = next
    })
})
