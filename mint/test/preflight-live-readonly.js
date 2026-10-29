"use strict";
// PUBLIC DETERMINISTIC FIXTURES ONLY. Never fund these addresses.
const fs = require('node:fs'), os = require('node:os'), path = require('node:path');
const { bsv } = require('../../vault/src/ordinal-pair');
const { main } = require('../scripts/canary-preflight');
if (process.platform === 'win32' || process.argv.length !== 3 || !path.isAbsolute(process.argv[2])) throw Error('Run on Linux/WSL: node mint/test/preflight-live-readonly.js ABSOLUTE_NEW_REPORT_JSON');
const base = path.join(os.homedir(), '.cache', 'boxsv-mint-tests');
fs.mkdirSync(base, { recursive: true });
const d = fs.mkdtempSync(path.join(base, 'preflight-public-'));
const key = n => new bsv.PrivateKey(new bsv.crypto.BN(n), bsv.Networks.livenet);
const c = { inventoryKeyPath: path.join(d, 'inventory.wif'), sponsorKeyPath: path.join(d, 'sponsor.wif'), paymentXpub: bsv.HDPrivateKey.fromSeed(Buffer.alloc(32, 103), bsv.Networks.livenet).hdPublicKey.toString(), buyerPubkey: key(104).publicKey.toString() };
fs.writeFileSync(c.inventoryKeyPath, key(101).toWIF(), { mode: 0o600 });
fs.writeFileSync(c.sponsorKeyPath, key(102).toWIF(), { mode: 0o600 });
const p = path.join(d, 'config.json');
fs.writeFileSync(p, JSON.stringify(c), { mode: 0o600 });
main([p, process.argv[2]]).catch(e => { console.error(e.message); process.exitCode = 1; }).finally(() => fs.rmSync(d, { recursive: true, force: true }));
