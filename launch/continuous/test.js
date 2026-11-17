'use strict';
const test = require('node:test'), assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path');
const dir = path.join(__dirname, '.test-runs');
fs.mkdirSync(dir, {recursive:true});
test('one buyer/design/origin remains bound from reservation to actual withdrawn ordinal', async () => {
  const api = fs.existsSync(path.join(__dirname, 'engine.js')) ? require('./engine') : {};
  assert.equal(typeof api.createDemo, 'function', 'continuous orchestration is missing');
  const file = path.join(fs.mkdtempSync(path.join(dir, 'flow-')), 'journal.sqlite');
  const e = api.createDemo(file);
  try {
    const initial = e.inspect();
    await e.reserve('reserve-1');
    for (const action of ['Pack','Seal','Transfer','Open','Withdraw']) {
      await e.advance(action.toLowerCase());
      const s = e.inspect();
      assert.deepEqual(s.binding, initial.binding);
      assert.equal(s.history.at(-1).action, action);
      assert.equal(s.history.at(-1).vm, true);
    }
    const s=e.inspect();
    assert.equal(s.stage,'WITHDRAWN');
    assert.equal(s.history.length,5);
    assert.ok(s.provenance.originalIssuanceProvenance);
    assert.ok(s.provenance.originalManifestComplete);
    assert.ok(s.provenance.currentCustodyIntegrity);
    assert.equal(s.withdrawnOwner,s.binding.buyerPubkey);
    assert.equal(s.originalOutpoint,s.binding.origin);
  } finally { e.close(); }
});
