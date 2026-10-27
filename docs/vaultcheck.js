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

    // Compiled covenant fingerprint (vault/artifacts/vault.json, scrypt-ts 1.4.5; sCrypt compiler 1.20.0).
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

    // Inline VAULT-0003 protocol port (manifest.js/draw.js, e01d7c6).
    // JSON canonicalization matches Python's ensure_ascii and code-point sorting.
    const own = (o, k) => Object.prototype.hasOwnProperty.call(o, k)
    function integer(n, min = 0) {
        if (!Number.isSafeInteger(n) || n < min) throw new Error('Invalid integer')
        return n
    }
    function object(o) {
        if (!o || typeof o !== 'object' || Array.isArray(o)) throw new Error('Expected JSON object')
    }
    function canonicalSerialize(v) {
        const quote = s => JSON.stringify(s).replace(/[\u007f-\uffff]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'))
        if (v === null) return 'null'
        if (typeof v === 'string') return quote(v)
        if (typeof v === 'boolean') return String(v)
        if (typeof v === 'number') { if (!Number.isSafeInteger(v)) throw new Error('Unsafe JSON number'); return String(v) }
        if (Array.isArray(v)) return '[' + v.map(canonicalSerialize).join(',') + ']'
        object(v)
        const compare = (a, b) => {
            const aa = Array.from(a, c => c.codePointAt(0)), bb = Array.from(b, c => c.codePointAt(0))
            for (let i = 0; i < Math.min(aa.length, bb.length); i++) if (aa[i] !== bb[i]) return aa[i] - bb[i]
            return aa.length - bb.length
        }
        return '{' + Object.keys(v).sort(compare).map(k => quote(k) + ':' + canonicalSerialize(v[k])).join(',') + '}'
    }
    function tableWeight(table, catalog) {
        if (!Array.isArray(table) || !table.length) throw new Error('Empty weight table')
        const ids = new Set(); let total = 0
        for (const d of table) {
            object(d); integer(d.id); integer(d.weight, 1)
            if (ids.has(d.id) || (catalog && !catalog.has(d.id))) throw new Error('Invalid design id')
            ids.add(d.id); total = integer(total + d.weight, 1)
        }
        return total
    }
    function validateManifest(m) {
        object(m); canonicalSerialize(m)
        if (typeof m.name !== 'string' || m.manifest_version !== 1 || typeof m.allow_pack_duplicates !== 'boolean') throw new Error('Invalid manifest fields')
        integer(m.pack_size, 1)
        if (tableWeight(m.designs) !== m.total_weight) throw new Error('Incorrect total weight')
        for (const d of m.designs) if (typeof d.ref !== 'string') throw new Error('Missing design ref')
        const catalog = new Set(m.designs.map(d => d.id)), slots = m.slots === undefined ? {} : m.slots
        object(slots)
        for (const [key, cfg] of Object.entries(slots)) {
            if (!/^(0|[1-9][0-9]*)$/.test(key) || !Number.isSafeInteger(Number(key)) || Number(key) >= m.pack_size) throw new Error('Invalid slot')
            object(cfg)
            if (tableWeight(cfg.table, catalog) !== cfg.total_weight) throw new Error('Incorrect slot weight')
        }
        if (!m.allow_pack_duplicates && m.designs.length < m.pack_size - Object.keys(slots).length) throw new Error('Insufficient unique designs')
    }
    async function hashText(text) {
        const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text))
        return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('')
    }
    async function drawPack(manifest, boxId, seed) {
        validateManifest(manifest)
        const designs = [], trace = [], seen = new Map(); let retries = 0, work = 0
        for (let slot = 0; slot < manifest.pack_size; slot++) {
            const cfg = manifest.slots?.[String(slot)], key = cfg ? `slot${slot}` : 'main'
            const table = cfg ? cfg.table : manifest.designs, total = cfg ? cfg.total_weight : manifest.total_weight
            if (!seen.has(key)) seen.set(key, new Set())
            const used = seen.get(key); let retry = 0
            while (true) {
                // Browser resource guard: fail closed, NEVER truncate or alter the draw.
                if (++work > 100000) throw new Error('Pack computation budget exceeded; no pack verified')
                const digest = await hashText(`VAULT3-DRAW|${boxId}|${seed}|${slot}|${retry}`)
                const index = Number(BigInt('0x' + digest) % BigInt(total))
                let cumulative = 0, id
                for (const d of table) { cumulative += d.weight; if (index < cumulative) { id = d.id; break } }
                if (manifest.allow_pack_duplicates || !used.has(id)) {
                    designs.push(id); used.add(id); trace.push({slot, table: key, retry, design: id}); break
                }
                retry++; retries++
            }
        }
        return {designs, retries, trace}
    }
    function txidValue(id) {
        if (typeof id !== 'string' || !/^[0-9a-fA-F]{64}$/.test(id)) throw new Error('Invalid txid/hash')
        return id.toLowerCase()
    }
    // Pinned scrypt-ts 1.20.0 constructor layout, not a search for arbitrary 32B pushes.
    function commitments(hex) {
        if (!hex.startsWith(ARTIFACT_PREFIX) || !hex.includes(ARTIFACT_CODETAIL)) throw new Error('Unknown covenant')
        const m = hex.slice(216).match(/^000000000000000000(00|51)20([0-9a-f]{64})20([0-9a-f]{64})21((?:02|03)[0-9a-f]{64})/)
        if (!m) throw new Error('Unrecognized covenant constructor layout')
        return {boxId: m[2], contentRef: m[3], initialState: m[1] === '00' ? 0 : 1, initialOwner: m[4]}
    }
    function ancestorState(hex) {
        const state = parseStateTrailer(hex)
        if (state) return state
        // Compiler's initial-state marker: state values come from constructor.
        if (hex.endsWith(ARTIFACT_CODETAIL + '6a01010001000500000000')) {
            const c = commitments(hex)
            return {boxState: c.initialState, owner: c.initialOwner}
        }
        return null
    }
    function taggedJson(tx, tag) {
        const found = []
        for (const out of tx?.vout || []) {
            const hex = out.scriptPubKey?.hex || ''
            if (!/^(006a|6a)/.test(hex)) continue
            if (hex.length % 2 || !/^[0-9a-f]+$/i.test(hex)) throw new Error('Malformed OP_RETURN hex')
            const bytes = Uint8Array.from(hex.match(/../g), h => parseInt(h, 16))
            let p = bytes[0] === 0 ? 2 : 1
            const parts = []
            while (p < bytes.length) {
                let n = bytes[p++]
                if (n >= 76 && n <= 78) {
                    const width = 2 ** (n - 76); n = 0
                    if (p + width > bytes.length) throw new Error('Truncated OP_RETURN push')
                    for (let i = 0; i < width; i++) n += bytes[p++] * 2 ** (8 * i)
                } else if (n > 75) throw new Error('Non-push OP_RETURN')
                if (p + n > bytes.length) throw new Error('Truncated OP_RETURN data')
                parts.push(bytes.slice(p, p + n)); p += n
            }
            const decode = b => new TextDecoder('utf-8', {fatal: true, ignoreBOM: true}).decode(b)
            if (parts.length && decode(parts[0]) === tag) {
                if (parts.length !== 2) throw new Error('Expected tag and JSON pushes')
                found.push(JSON.parse(decode(parts[1])))
            }
        }
        if (found.length !== 1) throw new Error(`Expected exactly one ${tag} payload`)
        return found[0]
    }
    async function findOpening(tx, c) {
        const visited = new Set()
        for (let depth = 0; depth < 100; depth++) {
            const id = txidValue(tx.txid)
            if (visited.has(id)) throw new Error('Cyclic opening ancestry')
            visited.add(id)
            const parents = []
            for (const input of tx.vin || []) {
                if (!input.txid) continue
                const parent = await fetchJson(`${WOC}/tx/${txidValue(input.txid)}`)
                if (!parent) throw new Error('Opening ancestor unavailable')
                const hex = parent.vout?.[input.vout]?.scriptPubKey?.hex || ''
                if (!hex.startsWith(ARTIFACT_PREFIX) || !hex.includes(ARTIFACT_CODETAIL)) continue
                const pc = commitments(hex), state = ancestorState(hex)
                if (pc.boxId === c.boxId && pc.contentRef === c.contentRef && state) parents.push({parent, state})
            }
            if (parents.length !== 1) throw new Error('Opening ancestry missing or ambiguous')
            if (parents[0].state.boxState === 0) return tx
            tx = parents[0].parent
        }
        throw new Error('Opening ancestry exceeds 100 hops; no pack verified')
    }
    async function checkPack(tx, v, options, evidence) {
        if (!options.manifestTxid) {
            if (options.mintTxid) throw new Error('Manifest txid required to verify mint')
            evidence.push('Pack not checked: supply manifest txid (content_ref is a hash, not a locator)')
            return {packStatus: 'NOT-CHECKED'}
        }
        const c = commitments(v.scriptHex), manifestTxid = txidValue(options.manifestTxid)
        const manifest = taggedJson(await fetchJson(`${WOC}/tx/${manifestTxid}`), 'VAULT3-MANIFEST')
        validateManifest(manifest)
        if (await hashText(canonicalSerialize(manifest)) !== c.contentRef) throw new Error('Manifest commitment mismatch')
        const opening = await findOpening(tx, c)
        const result = {manifestTxid, openingTxid: opening.txid, packStatus: 'PENDING', mintStatus: options.mintTxid ? 'PENDING' : 'NOT-PRESENTED'}
        if (!(opening.confirmations > 0)) {
            evidence.push('pack pending — opening unconfirmed'); return result
        }
        const height = integer(opening.blockheight, 1), openingHash = txidValue(opening.blockhash)
        result.drawHeight = integer(height + 1, 1)
        const block = await fetchJson(`${WOC}/block/height/${result.drawHeight}`)
        if (!block) { evidence.push('pack pending — one more block'); return result }
        if (block.height !== result.drawHeight || block.previousblockhash !== openingHash) throw new Error('Draw block mismatch or reorg; retry')
        const seed = txidValue(block.hash)
        result.pack = await drawPack(manifest, c.boxId, seed)
        result.packStatus = 'COMPUTED'; result.drawHash = seed
        evidence.push(`manifest ${manifestTxid}: commitment verified`)
        evidence.push(`opening ${opening.txid} at ${height}; draw block ${result.drawHeight}: ${seed}`)
        evidence.push(`pack: ${result.pack.designs.join(', ')} (retries=${result.pack.retries})`)
        if (options.mintTxid) {
            const mintTxid = txidValue(options.mintTxid)
            const mint = await fetchJson(`${WOC}/tx/${mintTxid}`)
            if (!mint) throw new Error('Mint transaction unavailable; not verified')
            let claimed
            try { claimed = taggedJson(mint, 'VAULT3-MINT') } catch (_) { claimed = null }
            const valid = claimed && claimed.manifest_root === c.contentRef && claimed.box_id === c.boxId &&
                mint.vin?.some(i => i.txid === opening.txid) && Array.isArray(claimed.designs) &&
                claimed.designs.length === result.pack.designs.length && result.pack.designs.every((id, i) => own(claimed.designs, i) && claimed.designs[i] === id)
            result.mintStatus = valid ? 'VALID' : 'INVALID'; result.mintTxid = mintTxid
            evidence.push(`mint ${mintTxid}: ${result.mintStatus}`)
            if (!valid) result.verdict = 'INVALID-MINT'
        }
        return result
    }

    /**
     * checkBox(txid, K, {manifestTxid?, mintTxid?}) -> verdict object.
     * verdict: SEALED-VERIFIED | SEALED-PENDING | OPENED-VERIFIED |
     *          SPENT-UNRESOLVED | NOT-A-VAULT | TX-NOT-FOUND | UNRECOGNIZED-STATE
     */
    async function checkBox(txid, K = 3, options = {}) {
        txid = txidValue(txid)
        if (options.manifestTxid) txidValue(options.manifestTxid)
        if (options.mintTxid) txidValue(options.mintTxid)
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
            const pack = v.state.boxState === 1 ? await checkPack(tx, v, options, evidence) : {}
            results.push({ vout: v.vout, state: stateName, unspent: isUnspent, conf, verdict, ...pack })
        }
        // headline verdict = first vault output (one box per tx in v0.1)
        return { verdict: results[0].verdict, txid, confirmations: conf, outputs: results, evidence }
    }

    return { checkBox, parseStateTrailer, findVaultOutputs, ARTIFACT_PREFIX, ARTIFACT_CODETAIL }
})()

if (typeof module !== 'undefined') module.exports = VaultCheck
