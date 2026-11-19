'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
test('authoritative transport exports a runnable adapter', () => {
  assert.ok(fs.existsSync(__dirname + '/adapter.js'), 'missing authoritative wallet transport');
  assert.equal(typeof require('./adapter').WalletTransport, 'function');
});
