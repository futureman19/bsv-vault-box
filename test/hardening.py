"""Independent exact permutation oracle and encoding/budget regressions. Offline."""
import hashlib
import itertools
import json
import pathlib
import subprocess
import sys
from fractions import Fraction
from unittest.mock import patch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import v3_ref as ref

preimage = 'VAULT3-DRAW|' + '00'*32 + '|' + '11'*32 + '|2|3'
digest = 'a3ae26ffa23407ba3010b78262b0bd33b3453527012c4f34ff3e0b6658a3bdbb'
assert hashlib.sha256(preimage.encode()).hexdigest() == digest
assert ref.draw_index('00'*32, '11'*32, 2, 3, 100) == 91
for field in ('a|b', '', None, '\ud800'):
    for args in ((field, 'seed'), ('box', field)):
        try:
            ref.draw_index(*args, 0, 0, 100)
        except (ValueError, UnicodeError):
            pass
        else:
            raise AssertionError('Invalid field accepted')
for value in (-1, 1.5, True, 9007199254740992):
    try:
        ref.draw_index('box', 'seed', value, 0, 100)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid slot accepted')
m = {'pack_size': 2, 'allow_pack_duplicates': False, 'total_weight': 2,
     'designs': [{'id': 0, 'weight': 1}, {'id': 1, 'weight': 1}]}
with patch.object(ref, 'draw_index', return_value=0) as fake:
    try:
        ref.draw_pack(m, 'box', 'seed')
    except ref.DrawExhausted:
        assert fake.call_count == 10002
    else:
        raise AssertionError('Missing retry cap')

cases = []
for weights in ([99, 1], [1, 1, 1], [3, 2, 1], [2, 2, 1, 1], [9, 3, 2, 1, 1]):
    n = len(weights)
    rows = [[Fraction(0) for _ in weights] for _ in weights]
    for order in itertools.permutations(range(n)):
        probability = Fraction(1)
        remaining = sum(weights)
        for design in order:
            probability *= Fraction(weights[design], remaining)
            remaining -= weights[design]
        for slot, design in enumerate(order):
            rows[slot][design] += probability
    expected = [[{'id': i, 'probability': f'{p.numerator}/{p.denominator}'} for i, p in enumerate(row)] for row in rows]
    cases.append({'manifest': {'name': 'oracle', 'pack_size': n, 'allow_pack_duplicates': False,
                              'per_slot_odds_published': True,
                              'designs': [{'id': i, 'ref': 'x', 'weight': w} for i, w in enumerate(weights)]},
                  'expected': expected})
script = """
const assert=require('node:assert/strict'),fs=require('node:fs');
const {buildManifest}=require('./manifest');
for(const c of JSON.parse(fs.readFileSync(0,'utf8')))assert.deepEqual(buildManifest(c.manifest).slot_odds,c.expected);
"""
subprocess.run(['node', '-e', script], input=json.dumps(cases), text=True,
               cwd=pathlib.Path(__file__).resolve().parents[1], check=True)
print('PASS Python encoding/input/cap tests and 5 independent exact permutation odds oracles')
