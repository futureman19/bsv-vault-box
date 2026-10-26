import { Vault } from '../src/contracts/vault'
import {
    bsv,
    TestWallet,
    DefaultProvider,
    PubKey,
    Sha256,
    findSig,
    hash256,
    toByteString,
    MethodCallOptions,
    UTXO,
} from 'scrypt-ts'
import * as dotenv from 'dotenv'

dotenv.config()

const SEALED = 0n
const OPENED = 1n
const sleep = (s: number) => new Promise((r) => setTimeout(r, s * 1000))

const mkRef = (s: string) =>
    hash256(toByteString(Buffer.from(s, 'utf8').toString('hex'))) as Sha256

// Provider that tracks OUR OWN chained mempool UTXOs (WoC lags unconfirmed txs).
// Broadcast still goes through the real network via DefaultProvider.
class TrackedProvider extends DefaultProvider {
    private coins: UTXO[] = []
    private txs = new Map<string, bsv.Transaction>()

    constructor(private trackedAddr: string) {
        super({ network: bsv.Networks.mainnet })
    }

    seed(u: UTXO) {
        this.coins.push(u)
    }

    override async listUnspent(address: bsv.Address): Promise<UTXO[]> {
        return address.toString() === this.trackedAddr ? [...this.coins] : []
    }

    override async getTransaction(txHash: string): Promise<bsv.Transaction> {
        const t = this.txs.get(txHash)
        if (t) return t
        return super.getTransaction(txHash)
    }

    override async sendRawTransaction(rawTxHex: string): Promise<string> {
        const id = await super.sendRawTransaction(rawTxHex)
        this.applyTx(new bsv.Transaction(rawTxHex))
        return id
    }

    private applyTx(tx: bsv.Transaction) {
        const spent = new Set<string>()
        for (const i of tx.inputs) {
            const raw = Buffer.from(i.prevTxId)
            spent.add(raw.toString('hex') + '.' + i.outputIndex)
            spent.add(
                Buffer.from(raw).reverse().toString('hex') + '.' + i.outputIndex
            )
        }
        this.coins = this.coins.filter((c) => !spent.has(c.txId + '.' + c.outputIndex))
        const target = bsv.Script.buildPublicKeyHashOut(this.trackedAddr).toHex()
        tx.outputs.forEach((o, idx) => {
            if (o.script.toHex() === target) {
                this.coins.push({
                    address: this.trackedAddr,
                    txId: tx.id,
                    outputIndex: idx,
                    script: target,
                    satoshis: o.satoshis,
                })
            }
        })
        this.txs.set(tx.id, tx)
        console.log(
            'tracked coins: ' +
                this.coins
                    .map((c) => `${c.txId.slice(0, 8)}.${c.outputIndex}=${c.satoshis}`)
                    .join(', ')
        )
    }
}

async function withRetry<T>(label: string, fn: () => Promise<T>): Promise<T> {
    for (let i = 0; i < 6; i++) {
        try {
            return await fn()
        } catch (e) {
            console.log(
                `${label}: attempt ${i + 1} failed: ${(e as Error).message}`
            )
            await sleep(15)
        }
    }
    throw new Error(`${label}: exhausted retries`)
}

async function main() {
    const pk = bsv.PrivateKey.fromWIF(process.env.PRIVATE_KEY || '')
    const addr = pk.toAddress().toString()
    const provider = new TrackedProvider(addr)
    // Dogfood funding coin: tx 039afde2...804e3, vout 0, 2000 sats (payment is output 0 in send.ts)
    provider.seed({
        address: addr,
        txId: '039afde20c7cac9e3d2ca4a8c45589880196bbe232f1cedbd32a16367bb804e3',
        outputIndex: 0,
        script: bsv.Script.buildPublicKeyHashOut(addr).toHex(),
        satoshis: 2000,
    })
    const signer = new TestWallet(pk, provider)
    console.log('deploy address:', addr)
    await Vault.loadArtifact()

    const owner = PubKey(pk.publicKey.toByteString())
    const sigFor = (sr: any) => findSig(sr, pk.publicKey)

    // ---- BOX A: deploy SEALED, then one sealed self-transfer. Stays sealed forever.
    const boxA = new Vault(
        SEALED,
        mkRef('VAULT-0001 live box A id'),
        mkRef('VAULT-0001 live box A content'),
        owner
    )
    await boxA.connect(signer)
    const depA = await withRetry('BOX_A_DEPLOY', () => boxA.deploy(1))
    console.log('BOX_A_DEPLOY_TXID=' + depA.id)

    const aNext = boxA.next()
    aNext.owner = owner
    const callA = await withRetry('BOX_A_TRANSFER', () =>
        boxA.methods.transfer(sigFor, owner, {
            pubKeyOrAddrToSign: pk.publicKey,
            next: { instance: aNext, balance: 1 },
        } as MethodCallOptions<Vault>)
    )
    console.log('BOX_A_TRANSFER_TXID=' + callA.tx.id)

    // ---- BOX B: deploy SEALED, then open it. Proves the open transition on-chain.
    const boxB = new Vault(
        SEALED,
        mkRef('VAULT-0001 live box B id'),
        mkRef('VAULT-0001 live box B content'),
        owner
    )
    await boxB.connect(signer)
    const depB = await withRetry('BOX_B_DEPLOY', () => boxB.deploy(1))
    console.log('BOX_B_DEPLOY_TXID=' + depB.id)

    const bNext = boxB.next()
    bNext.boxState = OPENED
    const openB = await withRetry('BOX_B_OPEN', () =>
        boxB.methods.open(sigFor, {
            pubKeyOrAddrToSign: pk.publicKey,
            next: { instance: bNext, balance: 1 },
        } as MethodCallOptions<Vault>)
    )
    console.log('BOX_B_OPEN_TXID=' + openB.tx.id)

    console.log('MAINNET_CYCLE_COMPLETE')
}

main().catch((e) => {
    console.error('FAILED:', e.message)
    process.exit(1)
})
