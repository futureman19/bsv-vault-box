"""Offline safety acceptance. No production keys, money or network."""
import copy
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dry_run as d


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=HERE)
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / 'sim.sqlite'
        self.config = json.loads((HERE / 'fixture-proposal.json').read_text())
        self.manifest = HERE.parent / 'assets/candidate-manifest.json'

    def init(self, config=None):
        return d.initialize(self.db, config or self.config, self.manifest)

    def op(self, key, action, **kw):
        return d.apply(self.db, {'key': key, 'action': action, **kw})

    def reserve(self, rid='r1'):
        return self.op('reserve-' + rid, 'reserve', reservation=rid)

    def pay(self, rid='r1', amount=100, receipt='receipt1'):
        return self.op(receipt, 'receipt', reservation=rid, receipt=receipt, units=amount)

    def test_initial_inventory_exact_and_locked(self):
        s = self.init()
        self.assertEqual(s['supply'], {'Country': 195, 'Ocean': 5, 'Moon': 1, 'total': 201})
        self.assertEqual(s['available'], 201)
        self.assertFalse(s['mayBroadcast'])
        self.assertFalse(s['launchReady'])
        self.assertEqual(s['proposal']['priceUnits'], 100)
        self.assertEqual(s['conditionalOdds']['perDesign'], '1/201')

    def test_all_unique_and_202nd_rejected_across_restarts(self):
        self.init()
        draws = [self.reserve('r' + str(i))['design'] for i in range(201)]
        self.assertEqual(len(set(draws)), 201)
        with self.assertRaisesRegex(ValueError, 'exhausted'):
            self.reserve('overflow')
        s = d.inspect(self.db)
        self.assertEqual(s['available'], 0)
        self.assertEqual(s['conditionalOdds']['perDesign'], '0/1')
        self.assertEqual(s['conditionalOdds']['moon'], '0/1')
        self.assertTrue(d.audit(self.db)['valid'])

    def test_idempotence_and_changed_request_fail_closed(self):
        self.init()
        first = self.reserve()
        self.assertEqual(first, self.reserve())
        with self.assertRaisesRegex(ValueError, 'idempotency'):
            self.op('reserve-r1', 'reserve', reservation='r2')
        with self.assertRaisesRegex(ValueError, 'reservation exists'):
            self.op('different-key', 'reserve', reservation='r1')
        self.assertEqual(d.inspect(self.db)['available'], 200)

    def test_fixture_payment_and_lifecycle_plan(self):
        self.init(); self.reserve()
        self.assertEqual(self.pay()['state'], 'READY')
        built = self.op('build', 'build', reservation='r1')
        self.assertEqual(built['state'], 'BUILT')
        self.assertEqual(built['plan']['profile'], 'BOXSV-LAUNCH-METADATA-1')
        self.assertEqual(built['plan']['certificate'], 'DETACHED-UNSIGNED-NOT-NFT')
        self.assertEqual(built['plan']['lifecycle'], ['Pack', 'Seal', 'Transfer', 'Open', 'Withdraw'])
        self.assertFalse(built['plan']['reusableSealsSupported'])
        self.assertEqual(self.op('send', 'simulate-send', reservation='r1', outcome='included')['state'], 'TRANSFERRED')
        self.assertEqual(self.op('open', 'simulate-open', reservation='r1')['state'], 'OPENED')
        self.assertEqual(self.op('withdraw', 'simulate-withdraw', reservation='r1')['state'], 'WITHDRAWN')
        self.assertFalse(d.inspect(self.db)['mayBroadcast'])

    def test_partial_expiry_late_payment_refund_hold_never_relist(self):
        self.init(); first = self.reserve()
        self.assertEqual(self.pay(amount=40)['state'], 'RESERVED')
        expired = self.op('expiry', 'expire', reservation='r1')
        self.assertEqual(expired['state'], 'REFUND_HOLD')
        self.assertEqual(expired['refundUnits'], 40)
        late = self.pay(amount=60, receipt='late')
        self.assertEqual(late['state'], 'REFUND_HOLD')
        self.assertEqual(late['refundUnits'], 100)
        self.assertEqual(late['design'], first['design'])
        self.assertEqual(d.inspect(self.db)['available'], 200)
        with self.assertRaisesRegex(ValueError, 'hold'):
            self.op('build', 'build', reservation='r1')

    def test_ambiguous_broadcast_never_retries_or_refunds_automatically(self):
        self.init(); self.reserve(); self.pay()
        self.op('build', 'build', reservation='r1')
        held = self.op('send', 'simulate-send', reservation='r1', outcome='ambiguous')
        self.assertEqual(held['state'], 'AMBIGUOUS_HOLD')
        for action, extra in [('simulate-send', {'outcome': 'included'}), ('expire', {}), ('build', {})]:
            with self.assertRaises(ValueError):
                self.op('again-' + action, action, reservation='r1', **extra)
        self.assertEqual(d.inspect(self.db)['reservations'][0]['plan'], held['plan'])
        self.assertEqual(d.inspect(self.db)['available'], 200)

    def test_excess_and_finality_loss_preserve_confirmed_ownership(self):
        self.init(); self.reserve(); self.pay(); self.op('b', 'build', reservation='r1')
        self.op('s', 'simulate-send', reservation='r1', outcome='included')
        self.op('o', 'simulate-open', reservation='r1')
        excess = self.pay(amount=20, receipt='extra')
        self.assertEqual(excess['state'], 'OPENED')
        self.assertEqual(excess['refundUnits'], 20)
        loss = self.op('loss', 'finality-loss', reservation='r1')
        self.assertEqual(loss['state'], 'OPENED')
        self.assertIn('FINALITY_LOST', loss['holds'])
        self.assertEqual(loss['design'], excess['design'])
        with self.assertRaisesRegex(ValueError, 'hold'):
            self.op('w', 'simulate-withdraw', reservation='r1')

    def test_receipt_reuse_and_invalid_amounts(self):
        self.init(); self.reserve(); self.reserve('r2'); self.pay()
        with self.assertRaisesRegex(ValueError, 'receipt'):
            self.op('other-key', 'receipt', reservation='r2', receipt='receipt1', units=100)
        for i, amount in enumerate([0, -1, True, 1.5, '100', 2**63]):
            with self.assertRaises(ValueError):
                self.pay(amount=amount, receipt='bad' + str(i))
        self.assertEqual(d.inspect(self.db)['reservations'][1]['paidUnits'], 0)

    def test_config_network_keys_unknowns_and_supply_rejected(self):
        for field, value in [('network', 'mainnet'), ('mode', 'live'), ('keyPath', 'do-not-read'), ('priceUnits', None), ('seed', ''), ('reserves', ['not-a-design'])]:
            cfg = {**self.config, field: value}
            with self.assertRaises(ValueError): self.init(cfg)
            self.assertFalse(self.db.exists())
        self.init()
        with self.assertRaises(ValueError):
            self.op('live', 'broadcast', reservation='r1')

    def test_manifest_exact_pin_rejects_substitution(self):
        m = json.loads(self.manifest.read_bytes())
        m['items'][0]['slug'] = m['items'][1]['slug']
        path = Path(self.tmp.name) / 'bad.json'; path.write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError, 'manifest'):
            d.initialize(self.db, self.config, path)

    def test_reserves_inside_cap_and_determinism(self):
        cfg = {**self.config, 'reserves': ['the-moon']}
        self.init(cfg)
        self.assertEqual(d.inspect(self.db)['available'], 200)
        self.assertEqual(d.inspect(self.db)['conditionalOdds']['moon'], '0/1')
        first = self.reserve()
        db2 = Path(self.tmp.name) / 'second.sqlite'
        d.initialize(db2, cfg, self.manifest)
        self.assertEqual(first, d.apply(db2, {'key': 'reserve-r1', 'action': 'reserve', 'reservation': 'r1'}))

    def test_tampered_materialized_state_and_history_rejected(self):
        self.init(); self.reserve()
        from contextlib import closing
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute("UPDATE snapshot SET body = '{}' WHERE id=1")
        with self.assertRaisesRegex(ValueError, 'integrity'):
            d.inspect(self.db)

    def test_failed_write_rolls_back_allocation(self):
        self.init()
        with patch.object(d, '_persist', side_effect=OSError('simulated disk failure')):
            with self.assertRaises(OSError): self.reserve()
        self.assertEqual(d.inspect(self.db)['available'], 201)
        self.reserve()
        self.assertEqual(d.inspect(self.db)['available'], 200)

    def test_moon_odds_track_actual_roster_slug(self):
        self.init()
        self.assertEqual(d.inspect(self.db)['conditionalOdds']['moon'], '1/201')
        for i in range(201):
            result = self.reserve('moon-check-' + str(i))
            if result['design'] == 'the-moon':
                self.assertTrue(d.inspect(self.db)['moonAllocated'])
                self.assertEqual(d.inspect(self.db)['conditionalOdds']['moon'], '0/1')
                break

    def test_parallel_reservations_and_duplicate_request(self):
        from concurrent.futures import ThreadPoolExecutor
        self.init()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(self.reserve, ['same'] * 8))
            self.assertTrue(all(r == results[0] for r in results))
            results = list(pool.map(self.reserve, ['p' + str(i) for i in range(32)]))
        self.assertEqual(len(set(r['design'] for r in results)), 32)
        self.assertEqual(d.inspect(self.db)['available'], 168)
        self.assertEqual(d.audit(self.db)['eventCount'], 34)

    def test_event_tamper_and_failed_partial_write(self):
        from contextlib import closing
        self.init()
        original = d._persist
        def fail_after_write(*args):
            original(*args)
            raise OSError('disk simulation after INSERT')
        with patch.object(d, '_persist', side_effect=fail_after_write):
            with self.assertRaises(OSError): self.reserve()
        self.assertEqual(d.inspect(self.db)['available'], 201)
        self.reserve()
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute("UPDATE events SET body='{}' WHERE seq=2")
        with self.assertRaisesRegex(ValueError, 'integrity'): d.audit(self.db)

    def test_cli_restart_and_live_action_denied(self):
        def cli(*args):
            return subprocess.run([sys.executable, str(HERE / 'dry_run.py'), *args,
                                   '--db', str(self.db)], capture_output=True, text=True)
        p = cli('init', '--config', str(HERE / 'fixture-proposal.json'), '--manifest', str(self.manifest))
        self.assertEqual(p.returncode, 0, p.stderr)
        request = Path(self.tmp.name) / 'request.json'
        request.write_text(json.dumps({'key': 'reserve-r1', 'action': 'reserve', 'reservation': 'r1'}))
        p = cli('apply', '--request', str(request))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(cli('inspect').stdout)['available'], 200)
        self.assertEqual(json.loads(cli('audit').stdout)['eventCount'], 2)
        request.write_text(json.dumps({'key': 'live', 'action': 'broadcast', 'reservation': 'r1'}))
        self.assertEqual(cli('apply', '--request', str(request)).returncode, 2)
        self.assertEqual(json.loads(cli('audit').stdout)['eventCount'], 2)
        self.assertNotEqual(cli('init', '--config', str(HERE / 'fixture-proposal.json'), '--manifest', str(self.manifest)).returncode, 0)

    def test_malformed_action_fails_controlled_without_mutation(self):
        self.init()
        for action in [[], {}, 1, None]:
            with self.assertRaises(ValueError):
                self.op('bad', action, reservation='r1')
        self.assertEqual(d.inspect(self.db)['available'], 201)

    def test_no_network_or_signing_dependencies(self):
        self.init()
        source = (HERE / 'dry_run.py').read_text()
        for forbidden in ['import requests', 'import socket', 'import urllib', 'subprocess', 'PrivateKey', 'funded-runner', 'bitcoind']:
            self.assertNotIn(forbidden, source)
        self.assertEqual(d.audit(self.db)['mode'], 'SIMULATION-ONLY')


if __name__ == '__main__':
    unittest.main(verbosity=2)
