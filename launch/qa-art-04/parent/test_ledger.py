import unittest,json,pathlib,copy
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'review-results.json').read_text()); P=json.loads((R/'parent-ledger.json').read_text())
IDS=set('andorra austria belize bulgaria chad cuba ecuador fiji greece hungary israel kuwait liechtenstein malta mongolia netherlands oman peru rwanda senegal somalia suriname timor-leste uganda vatican-city'.split())
def validate(d):
 rows=d['entries'];assert len(rows)==25 and len({e['id'] for e in rows})==25 and {e['id'] for e in rows}==IDS
 parent={e['id']:e for e in P['entries']}
 for e in rows:
  assert e['viewer']==parent[e['id']]['viewer'] and e['viewer']['bytes']<5000000
  assert not e['launch_ready'] and not e['user_final_approved'] and not e['art_changed']
  assert set(parent[e['id']]['missing_gates'])<=set(e['remaining_gates'])
  assert not e['fresh_blender_reopen'] and not e['fresh_collision_sampling'] and not e['fresh_corrupt_glb_fallback']
  assert len(e['captures'])==4 and all((R/n).is_file() for n in e['captures'])
  assert len(e['browser'])==2 and {b['mode'] for b in e['browser']}=={'desktop','mobile'} and all(b['result']=='pass' for b in e['browser'])
  if e['id']=='rwanda':assert e['packaging']=='hold' and e['status']=='needs-decision' and e['visual_status']=='pass'
  if e['id']=='malta':assert e['status']=='needs-decision' and e['visual_status']=='needs-decision'
 assert not d['launch_ready'] and d['unreviewed_ids']==[]
class Ledger(unittest.TestCase):
 def test_valid(self):validate(D)
 def mutation(self,fn):
  d=copy.deepcopy(D);fn(d)
  with self.assertRaises(AssertionError):validate(d)
 def test_duplicate(self):self.mutation(lambda d:d['entries'].__setitem__(0,d['entries'][1]))
 def test_missing(self):self.mutation(lambda d:d['entries'].pop())
 def test_approval(self):self.mutation(lambda d:d['entries'][0].__setitem__('user_final_approved',True))
 def test_hold_erasure(self):self.mutation(lambda d:next(e for e in d['entries'] if e['id']=='rwanda').__setitem__('remaining_gates',[]))
 def test_fresh_claim(self):self.mutation(lambda d:d['entries'][0].__setitem__('fresh_collision_sampling',True))
 def test_malta_erasure(self):self.mutation(lambda d:next(e for e in d['entries'] if e['id']=='malta').__setitem__('status','pass'))
if __name__=='__main__':unittest.main(verbosity=2)
