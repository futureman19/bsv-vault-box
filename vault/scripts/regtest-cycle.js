'use strict';
// RPC-only transport: no DefaultProvider, public endpoints, dotenv or persisted keys.
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const { bsv, Provider, TestWallet, PubKey, Sha256, findSig } = require('scrypt-ts');
const { Vault } = require('../dist/contracts/vault');
const { buildManifest, canonicalSerialize, manifestRoot } = require('../../manifest');
const { drawPackForOpen } = require('../../draw');
const { verifyMint } = require('../../verify');
const port = process.env.REGTEST_RPC_PORT || '18443';
assert(['18443', '18445'].includes(port), 'Only dedicated local regtest ports allowed');
const endpoint = `http://127.0.0.1:${port}`;
async function rpc(method, params = []) {
    const auth = process.env.REGTEST_RPC_AUTH;
    assert(auth, 'Set REGTEST_RPC_AUTH to local regtest user:password');
    const response = await fetch(endpoint, { method: 'POST', redirect: 'error',
        signal: AbortSignal.timeout(30000), headers: { Authorization: 'Basic ' + Buffer.from(auth).toString('base64') },
        body: JSON.stringify({ jsonrpc: '1.0', id: 1, method, params }) });
    const data = await response.json();
    if (data.error) throw new Error(`${method}: ${data.error.code} ${data.error.message}`);
    assert(response.ok); return data.result;
}
async function guard() { assert.equal((await rpc('getblockchaininfo')).chain, 'regtest'); }
async function mutate(method, params) { await guard(); return rpc(method, params); }
async function mine() {
    const address = await rpc('getnewaddress');
    await mutate('generatetoaddress', [1, address]);
}
class LocalProvider extends Provider {
    constructor(key) { super(); this.key = key; this.address = key.toAddress().toString(); this.coins = []; }
    isConnected() { return true; }
    async connect() { await guard(); return this; }
    updateNetwork(network) { assert.equal(network.name, 'testnet'); }
    getNetwork() { return bsv.Networks.testnet; } // Address encoding only; transport is regtest-only.
    async getFeePerKb() { return 500; }
    async getTransaction(id) { return new bsv.Transaction(await rpc('getrawtransaction', [id])); }
    async getBalance() { return { confirmed: (await this.listUnspent()).reduce((s, c) => s + c.satoshis, 0), unconfirmed: 0 }; }
    async listUnspent(address) {
        if (address && address.toString() !== this.address) return [];
        const result = [];
        for (const c of this.coins) if (await rpc('gettxout', [c.txId, c.outputIndex, true])) result.push(c);
        this.coins = result; return [...result];
    }
    track(tx) {
        const target = bsv.Script.buildPublicKeyHashOut(this.address).toHex();
        tx.outputs.forEach((o, outputIndex) => { if (o.script.toHex() === target)
            this.coins.push({ txId: tx.id, outputIndex, script: target, satoshis: o.satoshis, address: this.address }); });
    }
    async sendRawTransaction(raw) {
        const tx = new bsv.Transaction(raw);
        const id = await mutate('sendrawtransaction', [raw]);
        assert.equal(id, tx.id);
        assert.equal(await rpc('getrawtransaction', [id]), raw);
        this.track(tx); return id;
    }
    async fund() {
        const id = await mutate('sendtoaddress', [this.address, 0.01]);
        await mine(); this.track(await this.getTransaction(id));
        return id;
    }
    async publish(outputs) {
        const tx = new bsv.Transaction().from(await this.listUnspent());
        outputs.forEach(o => tx.addOutput(new bsv.Transaction.Output(o)));
        // Explicit conservative fee, checked against raw input/output values.
        const fee = tx.toBuffer().length + tx.inputs.length * 180 + 100;
        tx.fee(fee).change(this.address).sign(this.key);
        console.log('FEE_CHECK', fee, tx.getFee(), tx.inputs.map(i => i.output.satoshis), tx.outputs.map(o => o.satoshis));
        assert.equal(tx.inputs.reduce((n, i) => n + i.output.satoshis, 0) - tx.outputs.reduce((n, o) => n + o.satoshis, 0), fee);
        await this.sendRawTransaction(tx.serialize()); return tx;
    }
}
function dataScript(tag, payload) {
    return new bsv.Script().add('OP_FALSE').add('OP_RETURN').add(Buffer.from(tag)).add(Buffer.from(canonicalSerialize(payload)));
}
function inscription(address, payload) {
    return new bsv.Script().add('OP_FALSE').add('OP_IF').add(Buffer.from('ord')).add('OP_1')
        .add(Buffer.from('application/vnd.vault3-mint+json')).add('OP_0')
        .add(Buffer.from(canonicalSerialize(payload))).add('OP_ENDIF')
        .add(bsv.Script.buildPublicKeyHashOut(address));
}
function newProvider() { return new LocalProvider(bsv.PrivateKey.fromRandom(bsv.Networks.testnet)); }
function wallet(provider) {
    const signer = new TestWallet(provider.key, provider);
    signer.enableSplitFeeTx(false); // Preserve sufficient opening change for the mint child.
    return signer;
}
async function confirmed(id) {
    const tx = await rpc('getrawtransaction', [id, true]);
    assert(tx.confirmations > 0); const header = await rpc('getblockheader', [tx.blockhash]);
    assert.equal(await rpc('getblockhash', [header.height]), tx.blockhash);
    return { tx, height: header.height };
}
async function publicPack(manifestTxId, openTxId) {
    const manifestTx = await confirmed(manifestTxId);
    const script = bsv.Script.fromHex(manifestTx.tx.vout[0].scriptPubKey.hex);
    assert.equal(script.chunks[2].buf.toString(), 'VAULT3-MANIFEST');
    const manifest = JSON.parse(script.chunks[3].buf.toString());
    const opening = await confirmed(openTxId);
    assert(manifestTx.height < opening.height);
    const vault = Vault.fromLockingScript(opening.tx.vout[0].scriptPubKey.hex);
    assert.equal(vault.boxState, 1n); assert.equal(vault.contentRef, manifestRoot(manifest));
    // Node-confirmed input-zero covenant transition; compare predecessor fields too.
    const previous = await rpc('getrawtransaction', [opening.tx.vin[0].txid, true]);
    const prior = Vault.fromLockingScript(previous.vout[opening.tx.vin[0].vout].scriptPubKey.hex);
    assert.equal(prior.boxState, 0n); assert.equal(prior.boxId, vault.boxId);
    assert.equal(prior.contentRef, vault.contentRef);
    const drawHeight = opening.height + 1;
    const seed = (await rpc('getblockcount')) >= drawHeight ? await rpc('getblockhash', [drawHeight]) : null;
    const lookup = height => { assert.equal(height, drawHeight); return seed; };
    return { manifest, boxId: vault.boxId, root: vault.contentRef, openHeight: opening.height, seed,
        pack: drawPackForOpen(manifest, vault.boxId, opening.height, lookup), lookup };
}
async function checkMint(manifestId, openId, mintId, outputIndex) {
    const data = await publicPack(manifestId, openId);
    const { tx } = await confirmed(mintId);
    assert(tx.vin.some(i => i.txid === openId && i.vout !== 0), 'mint must directly spend opening change, not vault');
    const chunks = bsv.Script.fromHex(tx.vout[outputIndex].scriptPubKey.hex).chunks;
    assert.equal(chunks[2].buf.toString(), 'ord');
    const claim = JSON.parse(chunks[6].buf.toString());
    assert.equal(claim.protocol, 'VAULT3-MINT');
    assert.equal(claim.box_id, data.boxId); assert.equal(claim.manifest_root, data.root);
    return verifyMint(data.manifest, data.boxId, data.openHeight, data.lookup, claim.designs);
}
async function main() {
    await guard(); Vault.loadArtifact(require('../artifacts/vault.json'));
    if (process.argv[2] === '--replay') {
        const data = await publicPack(process.argv[3], process.argv[4]);
        console.log(JSON.stringify({ boxId: data.boxId, seed: data.seed, pack: data.pack })); return;
    }
    if ((await rpc('getblockcount')) < 101) {
        await mutate('generatetoaddress', [101, await rpc('getnewaddress')]);
    }
    const manifest = buildManifest({ name: 'VAULT-0003 local regtest', pack_size: 10,
        allow_pack_duplicates: false,
        designs: Array.from({ length: 1000 }, (_, id) => ({ id, ref: `design:${id}`, weight: id < 900 ? 100 : id < 990 ? 10 : 1 })),
        slots: { 9: { table: Array.from({ length: 10 }, (_, i) => ({ id: 990 + i, weight: 1 })) } } });
    const publisher = newProvider(); await publisher.fund();
    const manifestTx = await publisher.publish([{ satoshis: 0, script: dataScript('VAULT3-MANIFEST', manifest) }]);
    await mine(); console.log('MANIFEST', manifestTx.id, manifestRoot(manifest));
    const boxes = [];
    for (let i = 0; i < 3; i++) {
        const provider = newProvider(); const funding = await provider.fund();
        const signer = wallet(provider);
        // Existing v0.1 covenant requires an ID before its own txid exists.
        // Commit a public funding outpoint anchor; do not claim v0.2 self-outpoint binding.
        const coin = (await provider.listUnspent())[0];
        const anchor = Buffer.concat([Buffer.from(funding, 'hex').reverse(), Buffer.alloc(4)]);
        anchor.writeUInt32LE(coin.outputIndex, 32);
        const id = bsv.crypto.Hash.sha256sha256(anchor).toString('hex');
        let box = new Vault(0n, Sha256(id), Sha256(manifestRoot(manifest)), PubKey(provider.key.publicKey.toByteString()));
        await box.connect(signer); const deployed = await box.deploy(1); await mine();
        console.log('BOX', i, 'DEPLOY', deployed.id, 'ID', id, 'ANCHOR', `${funding}:${coin.outputIndex}`);
        assert.equal(Vault.fromLockingScript((await confirmed(deployed.id)).tx.vout[0].scriptPubKey.hex).contentRef, manifestRoot(manifest));
        boxes.push({ provider, signer, box, deployed: deployed.id });
    }
    // Real ownership change while SEALED; transfer recipient is ephemeral too.
    const first = boxes[0]; const recipient = newProvider(); await recipient.fund();
    const next = first.box.next(); next.owner = PubKey(recipient.key.publicKey.toByteString());
    const transfer = await first.box.methods.transfer(sr => findSig(sr, first.provider.key.publicKey), next.owner,
        { pubKeyOrAddrToSign: first.provider.key.publicKey, next: { instance: next, balance: 1 } });
    await mine();
    const transferred = Vault.fromLockingScript((await confirmed(transfer.tx.id)).tx.vout[0].scriptPubKey.hex);
    assert.equal(transferred.boxState, 0n); assert.equal(transferred.owner, next.owner);
    assert.equal(transferred.boxId, first.box.boxId); assert.equal(transferred.contentRef, manifestRoot(manifest));
    console.log('SEALED_TRANSFER', transfer.tx.id);
    await next.connect(wallet(recipient));
    boxes[0] = { ...first, box: next, provider: recipient };
    for (let i = 0; i < 2; i++) {
        const { box, provider } = boxes[i]; const opened = box.next(); opened.boxState = 1n;
        const result = await box.methods.open(sr => findSig(sr, provider.key.publicKey),
            { pubKeyOrAddrToSign: provider.key.publicKey, next: { instance: opened, balance: 1 } });
        await mine(); const openId = result.tx.id;
        const pending = await publicPack(manifestTx.id, openId); assert.equal(pending.pack, null);
        console.log('PASS pending draw', openId, 'height', pending.openHeight);
        await mine(); const data = await publicPack(manifestTx.id, openId);
        const replay = () => execFileSync(process.execPath, [__filename, '--replay', manifestTx.id, openId], { encoding: 'utf8' }).trim();
        const a = replay(), b = replay(); assert.equal(a, b); assert.deepEqual(JSON.parse(a).pack, data.pack);
        assert.equal(new Set(data.pack.designs.slice(0, 9)).size, 9); assert(data.pack.designs[9] >= 990);
        console.log('PASS independent public RPC replay / unique main / legendary slot', a);
        const claim = { protocol: 'VAULT3-MINT', manifest_root: data.root, box_id: data.boxId, designs: data.pack.designs };
        // Only spend this opening's change so mint ancestry is explicit.
        provider.coins = (await provider.listUnspent()).filter(c => c.txId === openId);
        assert(provider.coins.length > 0);
        const outputs = [{ satoshis: 1, script: inscription(provider.address, claim) }];
        if (i === 1) outputs.push({ satoshis: 1, script: inscription(provider.address,
            { ...claim, designs: [1000, ...claim.designs.slice(1)] }) });
        const mint = await provider.publish(outputs); await mine();
        assert.equal(await checkMint(manifestTx.id, openId, mint.id, 0), true);
        console.log('PASS valid mint', mint.id, 'output 0', 'open', openId);
        if (i === 1) {
            assert.equal(await checkMint(manifestTx.id, openId, mint.id, 1), false);
            console.log('PASS forged on-chain mint rejected', mint.id, 'output 1');
        }
        assert(await rpc('gettxout', [openId, 0]), 'opened box remains independent unspent collectible');
    }
    assert(await rpc('gettxout', [boxes[2].deployed, 0]));
    console.log('REGTEST_CYCLE_COMPLETE: all five acceptance checks passed; third box remains sealed');
}
main().catch(error => { console.error('FAILED:', error.message); process.exitCode = 1; });
