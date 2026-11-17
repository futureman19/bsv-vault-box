import unittest,json,pathlib,copy
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'reviewed-ledger.json').read_text());P=json.loads((R/'parent/review-results.json').read_text())
def validate(d):
 es=d['entries'];ids=[e['id'] for e in es]
 assert len(ids)==len(set(ids))==25 and set(ids)=={e['id'] for e in P['entries']}
 assert set(P['visual_holds'])<=set(d['visual_holds'])
 assert all(e['verdict']=='needs-user-review' for e in es if e['id'] in P['visual_holds'])
 assert [e['id'] for e in es if e['packaging_hold']]==['morocco']
 assert not d['launch_ready'] and d['final_approvals']==0
 for e in es:
  assert not any(e[k] for k in ['art_changed','user_final_approved','launch_ready','fresh_blender_reopen','fresh_collision_sampling','fresh_corrupt_glb_fallback','fresh_nojs'])
  assert e['viewer']==next(p['viewer'] for p in P['entries'] if p['id']==e['id'])
  assert len(e['fresh_browser'])==2 and all(b['result']=='pass' for b in e['fresh_browser'])
  assert all((R/p).is_file() for p in e['original_capture_paths'])
class QA(unittest.TestCase):
 def test_valid(self):validate(D)
 def reject(self,fn):
  d=copy.deepcopy(D);fn(d)
  with self.assertRaises(AssertionError):validate(d)
 def test_duplicate(self):self.reject(lambda d:d['entries'].__setitem__(0,d['entries'][1]))
 def test_lost_hold(self):self.reject(lambda d:d['visual_holds'].remove('morocco'))
 def test_approval(self):self.reject(lambda d:d.__setitem__('final_approvals',1))
 def test_freshness(self):self.reject(lambda d:d['entries'][0].__setitem__('fresh_collision_sampling',True))
 def test_packaging(self):self.reject(lambda d:next(e for e in d['entries'] if e['id']=='morocco').__setitem__('packaging_hold',False))
if __name__=='__main__':unittest.main()
