"""Offline ledger contract tests, including deliberately invalid copies."""
import collections, copy, hashlib, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parent
D=json.loads((ROOT/'launch-candidates.json').read_text(encoding='utf-8'))

def validate(d):
    es=d['entries']; ids=[e['id'] for e in es]
    assert len(ids)==201 and len(set(ids))==201 and set(ids)==set(d['expected_ids'])
    assert dict(collections.Counter(e['category'] for e in es))=={'Country':195,'Ocean':5,'Moon':1}
    for e in es:
        assert e['edition_supply']==1 and not e['launch_ready'] and not e['approval']['user_final_approved']
        assert len(e['selection']['commit'])==40 and e['selection']['reachable_from_fetched_ref']
        assert e['viewer']['bytes']<5000000 and len(e['viewer']['sha256'])==64
        assert e['viewer']['sha256']==e['delivered_viewer']['sha256']
        assert e['source_archives'] and e['marketing']['matches_gallery_inventory']
        assert e['missing_gates'] and e['model_sources']
        assert {'independent-current-model-visual-review','explicit-final-user-art-approval','fresh-full-source-and-browser-acceptance','storage-and-preservation-policy','mint-and-release-authorization'} <= set(e['missing_gates'])
        assert e['qa']['fresh_runtime_execution'] is False
        for a in e['source_archives']:
            bad=not a.get('safe_unique_paths') or not all(a.get('required_payloads',{}).values()) or a.get('crc_error') is not None or 'error' in a or bool(a.get('inventory_mismatches'))
            if bad: assert 'source-archive-integrity-or-required-payload-mismatch' in e['missing_gates']
            if not a.get('inventory_checked'): assert 'complete-source-archive-inventory-not-verified' in e['missing_gates']
        assert any(x['path'].endswith('.blend') for x in e['model_sources'])
        assert any(x['path'].endswith('.glb') for x in e['model_sources'])
        assert (ROOT/e['qa']['evidence_path']).is_file() and (ROOT/e['provenance']['readme_snapshot']).is_file()
    usa=next(e for e in es if e['id']=='united-states')
    assert usa['selection']['commit']=='1e6b1712959013285769a152b1d50bbf119f7729'
    assert 'usa-full-star-to-body-continuation-unresolved' in usa['missing_gates']

class Contract(unittest.TestCase):
    def test_valid(self): validate(D)
    def test_missing(self):
        d=copy.deepcopy(D); d['entries'].pop()
        with self.assertRaises(AssertionError): validate(d)
    def test_duplicate(self):
        d=copy.deepcopy(D); d['entries'][1]=d['entries'][0]
        with self.assertRaises(AssertionError): validate(d)
    def test_tampered_digest(self):
        d=copy.deepcopy(D); d['entries'][0]['viewer']['sha256']='0'*64
        with self.assertRaises(AssertionError): validate(d)
    def test_false_approval(self):
        d=copy.deepcopy(D); d['entries'][0]['approval']['user_final_approved']=True
        with self.assertRaises(AssertionError): validate(d)
    def test_budget(self):
        d=copy.deepcopy(D); d['entries'][0]['viewer']['bytes']=5000000
        with self.assertRaises(AssertionError): validate(d)
    def test_erased_archive_gate(self):
        d=copy.deepcopy(D); e=next(e for e in d['entries'] if e['id']=='rwanda'); e['missing_gates'].remove('source-archive-integrity-or-required-payload-mismatch')
        with self.assertRaises(AssertionError): validate(d)
    def test_false_fresh_qa(self):
        d=copy.deepcopy(D); d['entries'][0]['qa']['fresh_runtime_execution']=True
        with self.assertRaises(AssertionError): validate(d)
    def test_erased_release_hold(self):
        d=copy.deepcopy(D); d['entries'][0]['missing_gates'].remove('mint-and-release-authorization')
        with self.assertRaises(AssertionError): validate(d)
    def test_fresh_local_bytes(self):
        for e in D['entries']:
            b=pathlib.Path(e['delivered_viewer']['path']).read_bytes()
            self.assertEqual(hashlib.sha256(b).hexdigest(),e['viewer']['sha256'])
    def test_smoke_coverage(self):
        rows=json.loads((ROOT/'smoke-results.json').read_text())
        self.assertEqual(len(rows),14)
        self.assertEqual(len({(r['id'],r['mode']) for r in rows}),14)
        self.assertEqual({(r['id'],r['mode']) for r in rows},{(slug,mode) for slug in ['afghanistan','arctic-ocean','iceland','japan','morocco','the-moon','united-states'] for mode in ['desktop','mobile']})
        for r in rows: self.assertEqual(r['sha256'],next(e['viewer']['sha256'] for e in D['entries'] if e['id']==r['id']))
        self.assertTrue(all(r['result']=='pass' for r in rows))

if __name__=='__main__': unittest.main(verbosity=2)
