"""Offline allocation rehearsal. No transaction construction or live transport."""
import argparse
from collections import Counter
from contextlib import closing
import hashlib
import json
from pathlib import Path
import re
import sqlite3

MANIFEST_SHA = '307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb'
MODE = 'SIMULATION-ONLY'
SUPPLY = {'Country': 195, 'Ocean': 5, 'Moon': 1, 'total': 201}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def exact(value, keys):
    if type(value) is not dict or set(value) != set(keys.split()):
        raise ValueError('unexpected schema fields')


def identifier(value):
    if type(value) is not str or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value):
        raise ValueError('invalid identifier')


def amount(value):
    if type(value) is not int or not 0 < value <= 2**53 - 1:
        raise ValueError('invalid fictional units')


def validate_config(config, roster):
    exact(config, 'mode network allocation seed reserves priceUnits unit saleTermsApproved')
    if (config['mode'] != MODE or config['network'] != 'none'
            or config['allocation'] != 'COMMITTED-PERMUTATION-PROPOSAL-V1'
            or config['unit'] != 'FICTIONAL-UNITS-NOT-SATOSHIS'
            or config['saleTermsApproved'] is not False):
        raise ValueError('simulation only; sale approval forbidden')
    amount(config['priceUnits'])
    if type(config['seed']) is not str or not 1 <= len(config['seed']) <= 256:
        raise ValueError('fixture seed required')
    reserves = config['reserves']
    if (type(reserves) is not list or any(type(x) is not str for x in reserves)
            or len(set(reserves)) != len(reserves) or not set(reserves) <= set(roster)):
        raise ValueError('invalid reserves')


def permutation(config, roster):
    """Fisher-Yates with SHA256 counter rejection sampling, not modulo bias."""
    result = sorted(set(roster) - set(config['reserves']))
    counter = 0
    for i in range(len(result) - 1, 0, -1):
        bound = i + 1
        limit = 2**256 - (2**256 % bound)
        while True:
            n = int(digest(['boxsv-fixture-shuffle-v1', config['seed'], counter]), 16)
            counter += 1
            if n < limit:
                j = n % bound
                break
        result[i], result[j] = result[j], result[i]
    return result


def genesis(config, roster):
    validate_config(config, roster)
    counts = dict(Counter(x['category'] for x in roster.values()))
    if {**counts, 'total': len(roster)} != SUPPLY:
        raise ValueError('manifest supply invalid')
    return {'proposal': config, 'roster': roster, 'order': permutation(config, roster),
            'reservations': {}, 'receipts': [], 'requests': {}}


def transition(state, request):
    action = request.get('action') if type(request) is dict else None
    extras = {'reserve': '', 'receipt': 'receipt units', 'expire': '', 'build': '',
              'simulate-send': 'outcome', 'simulate-open': '', 'simulate-withdraw': '',
              'finality-loss': ''}
    if type(action) is not str or action not in extras:
        raise ValueError('unsupported action; live broadcast locked')
    exact(request, 'key action reservation ' + extras[action])
    identifier(request['key']); identifier(request['reservation'])
    key, rid = request['key'], request['reservation']
    if key in state['requests']:
        prior = state['requests'][key]
        if prior['request'] != request:
            raise ValueError('idempotency key reused with changed request')
        return prior['result']
    reservations = state['reservations']
    if action == 'reserve':
        if rid in reservations:
            raise ValueError('reservation exists')
        if len(reservations) >= len(state['order']):
            raise ValueError('inventory exhausted')
        r = {'reservation': rid, 'design': state['order'][len(reservations)],
             'state': 'RESERVED', 'paidUnits': 0, 'refundUnits': 0, 'holds': [], 'plan': None}
        reservations[rid] = r
    else:
        if rid not in reservations:
            raise ValueError('unknown reservation')
        r = reservations[rid]
        price = state['proposal']['priceUnits']
        if action == 'receipt':
            identifier(request['receipt']); amount(request['units'])
            if request['receipt'] in state['receipts']:
                raise ValueError('receipt already consumed')
            if r['paidUnits'] + request['units'] > 2**53 - 1:
                raise ValueError('receipt total overflow')
            state['receipts'].append(request['receipt'])
            r['paidUnits'] += request['units']
            if r['state'] in ('EXPIRED_HOLD', 'REFUND_HOLD'):
                r['state'] = 'REFUND_HOLD'
                r['refundUnits'] = r['paidUnits']
            else:
                r['refundUnits'] = max(0, r['paidUnits'] - price)
                if r['refundUnits'] and 'EXCESS_PAYMENT' not in r['holds']:
                    r['holds'].append('EXCESS_PAYMENT')
                if r['state'] == 'RESERVED' and r['paidUnits'] >= price:
                    r['state'] = 'READY'
        elif action == 'finality-loss':
            if not r['paidUnits']:
                raise ValueError('no payment to reconcile')
            if 'FINALITY_LOST' not in r['holds']:
                r['holds'].append('FINALITY_LOST')
        else:
            if r['holds'] or r['state'].endswith('_HOLD'):
                raise ValueError('reconciliation hold; no automatic retry/refund/relist')
            if action == 'expire':
                if r['state'] not in ('RESERVED', 'READY'):
                    raise ValueError('cannot expire built or transferred reservation')
                r['state'] = 'REFUND_HOLD' if r['paidUnits'] else 'EXPIRED_HOLD'
                r['refundUnits'] = r['paidUnits']
            elif action == 'build':
                if r['state'] != 'READY':
                    raise ValueError('exact fixture payment required')
                r['plan'] = {'profile': 'BOXSV-LAUNCH-METADATA-1', 'design': r['design'],
                    'candidateCommitment': state['roster'][r['design']]['commitment'],
                    'certificate': 'DETACHED-UNSIGNED-NOT-NFT',
                    'lifecycle': ['Pack', 'Seal', 'Transfer', 'Open', 'Withdraw'],
                    'reusableSealsSupported': False, 'serializedTransaction': None,
                    'custodyVerifiedByThisSimulation': False}
                r['state'] = 'BUILT'
            elif action == 'simulate-send':
                if r['state'] != 'BUILT' or request['outcome'] not in ('included', 'ambiguous'):
                    raise ValueError('invalid simulated send')
                r['state'] = 'TRANSFERRED' if request['outcome'] == 'included' else 'AMBIGUOUS_HOLD'
            elif action == 'simulate-open':
                if r['state'] != 'TRANSFERRED':
                    raise ValueError('not transferred')
                r['state'] = 'OPENED'
            elif action == 'simulate-withdraw':
                if r['state'] != 'OPENED':
                    raise ValueError('not opened')
                r['state'] = 'WITHDRAWN'
    result = json.loads(canonical(r))
    state['requests'][key] = {'request': request, 'result': result}
    return result


def _persist(conn, state, request, previous):
    body = canonical(request)
    chain = digest([previous, request])
    conn.execute('INSERT INTO events(body, hash) VALUES (?, ?)', (body, chain))
    conn.execute('INSERT OR REPLACE INTO snapshot VALUES (1, ?)', (canonical(state),))


def load(conn):
    try:
        rows = conn.execute('SELECT seq, body, hash FROM events ORDER BY seq').fetchall()
        if not rows:
            raise ValueError('empty ledger')
        previous = ''
        state = None
        for index, (seq, body, chain) in enumerate(rows):
            event = json.loads(body)
            if seq != index + 1 or chain != digest([previous, event]):
                raise ValueError('event chain changed')
            if index == 0:
                exact(event, 'config roster manifestSha')
                if event['manifestSha'] != MANIFEST_SHA:
                    raise ValueError('manifest pin changed')
                state = genesis(event['config'], event['roster'])
            else:
                transition(state, event)
            previous = chain
        snapshot = conn.execute('SELECT body FROM snapshot WHERE id=1').fetchone()
        if snapshot != (canonical(state),):
            raise ValueError('snapshot differs from replay')
        return state, previous, len(rows)
    except (ValueError, TypeError, KeyError, sqlite3.DatabaseError) as exc:
        raise ValueError('ledger integrity failure: ' + str(exc)) from exc


def connect(db):
    conn = sqlite3.connect(Path(db).resolve().as_uri() + '?mode=rw', uri=True, timeout=30)
    conn.execute('PRAGMA synchronous=FULL')
    return conn


def initialize(db, config, manifest):
    raw = Path(manifest).read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise ValueError('manifest exact-byte pin mismatch')
    items = json.loads(raw)['items']
    roster = {i['slug']: {'category': i['category'], 'commitment': i['certificate']['files_commitment']} for i in items}
    state = genesis(config, roster)
    with Path(db).open('xb'):
        pass
    with closing(connect(db)) as conn, conn:
        conn.execute('CREATE TABLE events(seq INTEGER PRIMARY KEY, body TEXT NOT NULL, hash TEXT NOT NULL)')
        conn.execute('CREATE TABLE snapshot(id INTEGER PRIMARY KEY CHECK(id=1), body TEXT NOT NULL)')
        _persist(conn, state, {'config': config, 'roster': roster, 'manifestSha': MANIFEST_SHA}, '')
    return inspect(db)


def apply(db, request):
    with closing(connect(db)) as conn, conn:
        conn.execute('BEGIN IMMEDIATE')
        state, previous, _ = load(conn)
        result = transition(state, request)
        old = conn.execute('SELECT body FROM snapshot WHERE id=1').fetchone()[0]
        if canonical(state) != old:
            _persist(conn, state, request, previous)
        return result


def inspect(db):
    with closing(connect(db)) as conn, conn:
        conn.execute('BEGIN')
        state, tip, count = load(conn)
    remaining = state['order'][len(state['reservations']):]
    n = len(remaining)
    return {'mode': MODE, 'mayBroadcast': False, 'launchReady': False,
            'supply': SUPPLY, 'proposal': state['proposal'], 'available': n,
            'conditionalOdds': {'perDesign': f'1/{n}' if n else '0/1',
                'moon': f'1/{n}' if 'the-moon' in remaining else '0/1',
                'basis': 'unallocated eligible designs only; theoretical unbiased hidden-seed proposal; fixture order PUBLIC'},
            'moonAllocated': any(r['design'] == 'the-moon' for r in state['reservations'].values()),
            'permutationCommitment': digest(state['order']), 'manifestSha': MANIFEST_SHA,
            'reservations': list(state['reservations'].values()), 'eventCount': count, 'eventTip': tip}


def audit(db):
    status = inspect(db)
    return {'valid': True, 'mode': MODE, 'eventCount': status['eventCount'],
            'eventTip': status['eventTip'], 'permutationCommitment': status['permutationCommitment'],
            'limitation': 'Local consistency replay, not authenticity, rollback protection or production fairness.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'apply', 'inspect', 'audit'])
    parser.add_argument('--db', required=True)
    parser.add_argument('--config')
    parser.add_argument('--manifest')
    parser.add_argument('--request')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            if not args.config or not args.manifest or args.request:
                raise ValueError('init requires config and manifest only')
            result = initialize(args.db, json.loads(Path(args.config).read_text()), args.manifest)
        elif args.command == 'apply':
            if not args.request or args.config or args.manifest:
                raise ValueError('apply requires request only')
            result = apply(args.db, json.loads(Path(args.request).read_text()))
        else:
            if args.config or args.manifest or args.request:
                raise ValueError('read command accepts db only')
            result = inspect(args.db) if args.command == 'inspect' else audit(args.db)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
