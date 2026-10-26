/**
 * VAULT-0001 seal checker — shared browser/Node module (zero dependencies).
 * Verifies a vault box UTXO from public chain data only (WhatsOnChain API).
 *
 * What it checks:
 *   1. The tx contains an output carrying the canonical compiled covenant
 *      (artifact fingerprint: prefix + invariant code tail).
 *   2. The covenant state trailer decodes (boxState 0=SEALED / 1=OPENED, owner pubkey).
 *   3. That exact outpoint is unspent (script-hash unspent lookup).
 *   4. Confirmation depth vs threshold K.
 *
 * Honest limitation (v0.1): forward lineage walking (genesis -> current UTXO)
 * needs an indexer that indexes vault scripts by boxId; this module verifies
 * the exact UTXO you point it at. A seller/marketplace supplies the current
 * holding txid; the checker proves its state from public data.
 */
const VaultCheck = (() => {
    const WOC = 'https://api.whatsonchain.com/v1/bsv/main'

    // Compiled covenant fingerprint (vault/artifacts/vault.json, scrypt-ts 1.20.0).
    const ARTIFACT_PREFIX =
        '0176018801a901ac2097dfd76851bf465e8f7155' // first bytes of the compiled script
    const ARTIFACT_CODETAIL =
        '776700687e5b7978aa876b6d6d6d6d6d6d6d6d6d6d6d6d6d6d6c67006868' // invariant code ending

    const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

    async function fetchJson(url, retries = 5) {
        for (let i = 0; i < retries; i++) {
            const res = await fetch(url, {
                headers: { 'User-Agent': 'vault-check/0.1' },
            })
            if (res.status === 429) {
                await sleep(3000 * (i + 1))
                continue
            }
            if (res.status === 404) return null
            if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`)
            return res.json()
        }
        throw new Error(`rate limited after ${retries} retries: ${url}`)
    }

    async function sha256hexReversed(hex) {
        const bytes = Uint8Array.from(hex.match(/../g).map((h) => parseInt(h, 16)))
        const digest = await crypto.subtle.digest('SHA-256', bytes)
        return Array.from(new Uint8Array(digest))
            .reverse()
            .map((b) => b.toString(16).padStart(2, '0'))
            .join('')
    }

    /** Parse the covenant state trailer: ... 6a 00 01 <state> 21 <33B pubkey> 25 00000000 */
    function parseStateTrailer(scriptHex) {
        const m = scriptHex.match(/6a0001(00|01)21(02|03)([0-9a-f]{64})2500000000$/)
        if (!m) return null
        return { boxState: m[1] === '00' ? 0 : 1, owner: m[2] + m[3] }
    }

    function findVaultOutputs(tx) {
        const outs = []
        tx.vout.forEach((o, i) => {
            const hex = o.scriptPubKey.hex
            if (
                hex.startsWith(ARTIFACT_PREFIX) &&
                hex.includes(ARTIFACT_CODETAIL)
            ) {
                const state = parseStateTrailer(hex)
                outs.push({
                    vout: i,
                    satoshis: Math.round(o.value * 1e8),
                    scriptHex: hex,
                    state,
                })
            }
        })
        return outs
    }

    /**
     * checkBox(txid, K) -> verdict object.
     * verdict: SEALED-VERIFIED | SEALED-PENDING | OPENED-VERIFIED |
     *          SPENT-UNRESOLVED | NOT-A-VAULT | TX-NOT-FOUND | UNRECOGNIZED-STATE
     */
    async function checkBox(txid, K = 3) {
        const tx = await fetchJson(`${WOC}/tx/${txid}`)
        if (!tx)
            return { verdict: 'TX-NOT-FOUND', txid, evidence: ['tx not indexed by WoC'] }
        const conf = tx.confirmations || 0
        const vaults = findVaultOutputs(tx)
        if (vaults.length === 0)
            return { verdict: 'NOT-A-VAULT', txid, evidence: ['no canonical covenant output found'] }
        const evidence = []
        const results = []
        for (const v of vaults) {
            if (!v.state) {
                results.push({ ...v, verdict: 'UNRECOGNIZED-STATE' })
                continue
            }
            const sh = await sha256hexReversed(v.scriptHex)
            await sleep(1200) // respect WoC rate budget
            const unspent = (await fetchJson(`${WOC}/script/${sh}/unspent`)) || []
            const isUnspent = unspent.some(
                (u) => u.tx_hash === txid && u.tx_pos === v.vout
            )
            const stateName = v.state.boxState === 0 ? 'SEALED' : 'OPENED'
            evidence.push(
                `outpoint ${txid}.${v.vout}: state=${stateName}, owner=${v.state.owner.slice(0, 12)}…, unspent=${isUnspent}, confirmations=${conf}`
            )
            let verdict
            if (isUnspent && v.state.boxState === 0)
                verdict = conf >= K ? 'SEALED-VERIFIED' : 'SEALED-PENDING'
            else if (v.state.boxState === 1)
                verdict = conf >= K ? 'OPENED-VERIFIED' : 'OPENED-PENDING'
            else verdict = 'SPENT-UNRESOLVED' // spent while sealed; forward lookup needs an indexer
            results.push({ vout: v.vout, state: stateName, unspent: isUnspent, conf, verdict })
        }
        // headline verdict = first vault output (one box per tx in v0.1)
        return { verdict: results[0].verdict, txid, confirmations: conf, outputs: results, evidence }
    }

    return { checkBox, parseStateTrailer, findVaultOutputs, ARTIFACT_PREFIX, ARTIFACT_CODETAIL }
})()

if (typeof module !== 'undefined') module.exports = VaultCheck
