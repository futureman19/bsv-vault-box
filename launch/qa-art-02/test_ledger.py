import unittest,json,pathlib,copy
R=pathlib.Path(__file__).resolve().parent
L=json.loads((R/'reviewed-ledger.json').read_text())
P=json.loads((R/'parent/review-results.json').read_text())
def validate(d):
    assert len(d['entries'])==25 and {e['id'] for e in d['entries']}=={e['id'] for e in P['entries']}
    assert not d['launch_ready'] and not d['final_user_approvals_granted'] and not d['changed_art']
    assert all(not e['approval']['user_final_approved'] and not e['launch_ready'] for e in d['entries'])
    assert set(P['needs_decision'])<=set(d['needs_user_review'])
    assert all(e['visual_verdict']=='needs-user-review' for e in d['entries'] if e['id'] in P['needs_decision'])
    assert 'sampled mechanism collisions' in d['historical_only']
    assert d['fresh_checks']['offline_browser_cases']==50
class LedgerTests(unittest.TestCase):
    def test_valid(self): validate(L)
    def test_missing_id_rejected(self):
        x=copy.deepcopy(L);x['entries'].pop()
        with self.assertRaises(AssertionError):validate(x)
    def test_dropped_hold_rejected(self):
        x=copy.deepcopy(L);x['needs_user_review'].pop()
        with self.assertRaises(AssertionError):validate(x)
    def test_hidden_hold_rejected(self):
        x=copy.deepcopy(L);next(e for e in x['entries'] if e['id']=='brazil')['visual_verdict']='candidate-with-limitations'
        with self.assertRaises(AssertionError):validate(x)
    def test_fake_approval_rejected(self):
        x=copy.deepcopy(L);x['entries'][0]['approval']['user_final_approved']=True
        with self.assertRaises(AssertionError):validate(x)
    def test_collision_claim_rejected(self):
        x=copy.deepcopy(L);x['historical_only'].remove('sampled mechanism collisions')
        with self.assertRaises(AssertionError):validate(x)
if __name__=='__main__':unittest.main(verbosity=2)
