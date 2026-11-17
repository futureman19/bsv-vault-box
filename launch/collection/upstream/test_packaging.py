import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent

class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((HERE / 'input-ledger.json').read_bytes())

    def api(self):
        self.assertTrue((HERE / 'packaging.py').exists(), 'packaging pipeline is not implemented')
        spec = importlib.util.spec_from_file_location('boxpack', HERE / 'packaging.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_manifest_deterministic_and_complete(self):
        p = self.api()
        a = p.make_manifest(self.ledger)
        shuffled = copy.deepcopy(self.ledger)
        shuffled['entries'].reverse()
        self.assertEqual(p.canonical(a), p.canonical(p.make_manifest(shuffled)))
        self.assertEqual(len(a['items']), 201)
        self.assertEqual(sum(i['edition_supply'] for i in a['items']), 201)
        self.assertTrue(all(i['certificate']['signature'] is None for i in a['items']))
        self.assertTrue(all(not i['launch_ready'] for i in a['items']))
        usa = next(i for i in a['items'] if i['slug'] == 'united-states')
        self.assertFalse(usa['approval']['user_final_approved'])

    def test_missing_duplicate_and_substituted_roster(self):
        p = self.api()
        for mode in ('missing', 'duplicate', 'substituted'):
            d = copy.deepcopy(self.ledger)
            if mode == 'missing': d['entries'].pop()
            elif mode == 'duplicate': d['entries'][-1] = d['entries'][0]
            else:
                d['entries'][0]['id'] = 'invented'
                d['expected_ids'][0] = 'invented'
            with self.assertRaisesRegex(ValueError, 'roster'): p.make_manifest(d)

    def test_supply_and_release_holds(self):
        p = self.api()
        for key, value in [('edition_supply', 2), ('launch_ready', True), ('missing_gates', [])]:
            d = copy.deepcopy(self.ledger)
            d['entries'][0][key] = value
            with self.assertRaises(ValueError): p.make_manifest(d)

    def test_required_recovery_roles_and_category(self):
        p = self.api()
        for key, value in [('source_archives', []), ('category', 'Moon')]:
            d = copy.deepcopy(self.ledger)
            d['entries'][0][key] = value
            with self.assertRaisesRegex(ValueError, 'archive|category'): p.make_manifest(d)

    def test_reviewed_input_guards(self):
        p = self.api()
        for mode in ('duplicate-roster', 'duplicate-archive', 'missing-notice', 'bool-supply', 'false-approval'):
            with self.subTest(mode=mode):
                d = copy.deepcopy(self.ledger)
                e = d['entries'][0]
                if mode == 'duplicate-roster': d['expected_ids'].append(d['expected_ids'][0])
                elif mode == 'duplicate-archive': e['source_archives'].append(e['source_archives'][0])
                elif mode == 'missing-notice': e['provenance']['source_readme'] = None
                elif mode == 'bool-supply': e['edition_supply'] = True
                else: e['approval']['user_final_approved'] = True
                with self.assertRaises(ValueError): p.make_manifest(d)

    def test_stable_identity_survives_art_change(self):
        p = self.api()
        a = p.make_manifest(self.ledger)
        d = copy.deepcopy(self.ledger)
        d['entries'][0]['viewer']['sha256'] = 'a' * 64
        b = p.make_manifest(d)
        self.assertEqual([i['id'] for i in a['items']], [i['id'] for i in b['items']])
        self.assertNotEqual(p.digest(p.canonical(a)), p.digest(p.canonical(b)))

    def test_full_offline_recovery_archive_and_trusted_root(self):
        p = self.api()
        d = copy.deepcopy(self.ledger)
        payloads = {}
        for e in d['entries']:
            records = [e['viewer'], e['marketing'], *e['model_sources'], *e['source_archives'], e['provenance']['source_readme']]
            if e['provenance'].get('research_brief'): records.append(e['provenance']['research_brief'])
            for r in records:
                data = ('TEST-FIXTURE:' + r['sha256']).encode()
                r['sha256'], r['bytes'] = p.digest(data), len(data)
                payloads[r['sha256']] = data
        manifest = p.make_manifest(d)
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp) / 'package'
            (root / 'blobs').mkdir(parents=True)
            for sha, data in payloads.items(): (root / 'blobs' / sha).write_bytes(data)
            (root / 'ledger.json').write_bytes(p.canonical(d))
            raw = p.canonical(manifest)
            (root / 'manifest.json').write_bytes(raw)
            expected = p.digest(raw)
            for name in ('packaging.py', 'roster.json'):
                (root / name).write_bytes((HERE / name).read_bytes())
            with self.assertRaisesRegex(ValueError, 'trusted manifest'): p.verify(root, '0' * 64)
            recovered = p.recover(root, expected, Path(tmp) / 'restored')
            self.assertEqual(recovered['items'], 201)
            self.assertFalse(recovered['website_used'])
            self.assertFalse(recovered['git_used'])
            a, b = Path(tmp) / 'a.zip', Path(tmp) / 'b.zip'
            self.assertEqual(p.archive(root, expected, a), p.archive(root, expected, b))
            (root / 'manifest.json').write_bytes(raw + b' ')
            with self.assertRaisesRegex(ValueError, 'trusted manifest'): p.verify(root, expected)

    def test_missing_tampered_payload_and_recovery_offline(self):
        p = self.api()
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp)
            data = b'offline fixture, not artwork'
            sha = p.digest(data)
            ref = {'sha256': sha, 'bytes': len(data), 'uri': 'sha256:' + sha}
            m = {'items': [{'files': [{'role': 'viewer', **ref}]}]}
            with self.assertRaisesRegex(ValueError, 'missing'): p.verify_payloads(m, root)
            target = root / 'blobs' / sha
            target.parent.mkdir()
            target.write_bytes(b'tampered')
            with self.assertRaisesRegex(ValueError, 'integrity'): p.verify_payloads(m, root)
            target.write_bytes(data)
            self.assertEqual(p.verify_payloads(m, root)['unique_blobs'], 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
