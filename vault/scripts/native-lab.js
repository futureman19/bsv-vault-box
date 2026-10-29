const http = require('node:http')
const fs = require('node:fs')
const path = require('node:path')
const N = require('../src/native-custody')
const f = N.fixture(), ledger = new N.LocalLedger(f.genesis)
const origin = 'http://127.0.0.1:4318'
function state() { return { localOnly: true, scope: 'single native-token wrapper prototype; NOT external NFT custody', verified: ledger.snapshot(), transactions: ledger.history.map(e => ({ action: e.action, txid: e.tx.id, bytes: e.tx.toBuffer().length })) } }
http.createServer((req, res) => {
  res.setHeader('Cache-Control', 'no-store')
  res.setHeader('X-Content-Type-Options', 'nosniff')
  if (req.headers.host !== '127.0.0.1:4318') { res.writeHead(403); return res.end('loopback only') }
  if (req.method === 'GET' && req.url === '/') { res.setHeader('Content-Type', 'text/html'); return res.end(fs.readFileSync(path.join(__dirname, '../lab/index.html'))) }
  if (req.method === 'GET' && req.url === '/api/state') { res.setHeader('Content-Type', 'application/json'); return res.end(JSON.stringify(state())) }
  if (req.method !== 'POST' || req.url !== '/api/move' || req.headers.origin !== origin || req.headers['content-type'] !== 'application/json') { res.writeHead(403); return res.end('not allowed') }
  let data = ''
  req.on('data', b => { data += b; if (data.length > 1024) req.destroy() })
  req.on('end', () => {
    res.setHeader('Content-Type', 'application/json')
    try {
      const { action, signer } = JSON.parse(data)
      if (!['alice', 'bob'].includes(signer) || !(action in N.ACTIONS) || ledger.history.length >= 100) throw Error('unsupported request or local history limit')
      const current = N.decode(ledger.tip.tx.outputs[0].script)
      const recipient = current.owner === f.alice.publicKey.toString() ? f.bob.publicKey.toString() : f.alice.publicKey.toString()
      const attempt = N.move(ledger.tip, action, f[signer], recipient)
      if (!attempt.result.success) return res.end(JSON.stringify({ ...state(), accepted: false, error: attempt.result.error }))
      ledger.accept(attempt)
      res.end(JSON.stringify({ ...state(), accepted: true }))
    } catch (e) { res.writeHead(400); res.end(JSON.stringify({ error: e.message })) }
  })
}).listen(4318, '127.0.0.1', () => console.log('Local research lab: ' + origin + ' — no funded assets, no broadcast'))
