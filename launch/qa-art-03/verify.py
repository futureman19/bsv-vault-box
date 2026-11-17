import pathlib,json,copy,hashlib,unittest
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
P=json.loads((R/'parent/review-results.json').read_text())
def validate(d):
 assert d['assigned']==P['assigned'] and len(d['entries'])==len(set(x['id'] for x in d['entries']))==25
 assert {e['id'] for e in d['entries']}==set(d['assigned']) and not d['unreviewed_ids']
 for e in d['entries']:
  p=next(x for x in P['entries'] if x['id']==e['id'])
  assert e['inherited_missing_gates']==p['inherited_missing_gates']
  assert not e['user_final_approved'] and not e['launch_ready'] and not e['art_changed']
  assert e['verdict']==('needs-user-review' if p['status']=='needs-decision' else 'candidate-with-limitations')
  assert e['viewer']==p['viewer'] and e['viewer']['bytes']<5000000
  assert len(e['fresh_browser'])==2 and all(x['result']=='pass' and x['sha256']==e['viewer']['sha256'] for x in e['fresh_browser'])
  assert e['fresh_motion']['passed']
  assert all((R/n).exists() for n in e['captures']+e['fresh_runtime_captures'])
  assert all(not a['full_historical_inventory_freshly_checked'] and all(c['matches_selected_bytes'] for c in a['selected_payload_checks']) for a in e['packaging']['archives'])
 assert 'complete-source-archive-inventory-not-verified' in next(x for x in d['entries'] if x['id']=='paraguay')['remaining_gates']
class Regression(unittest.TestCase):
 def setUp(self):self.d=json.loads((R/'reviewed-ledger.json').read_text())
 def test_valid(self):validate(self.d)
 def test_duplicate(self):self.d['entries'][-1]=copy.deepcopy(self.d['entries'][0]);self.assertRaises(AssertionError,validate,self.d)
 def test_hold_removal(self):self.d['entries'][0]['verdict']='candidate-with-limitations';self.assertRaises(AssertionError,validate,self.d)
 def test_approval(self):self.d['entries'][0]['user_final_approved']=True;self.assertRaises(AssertionError,validate,self.d)
 def test_false_fresh_inventory(self):self.d['entries'][0]['packaging']['archives'][0]['full_historical_inventory_freshly_checked']=True;self.assertRaises(AssertionError,validate,self.d)
 def test_paraguay_hold(self):next(x for x in self.d['entries'] if x['id']=='paraguay')['remaining_gates'].remove('complete-source-archive-inventory-not-verified');self.assertRaises(AssertionError,validate,self.d)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regression));assert result.wasSuccessful()
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=True)
  for w,h in [(1440,1080),(390,844)]:
   c=b.new_context(offline=True,viewport={'width':w,'height':h});p=c.new_page();errors=[];external=[]
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda q:external.append(q.url) if q.url.startswith(('http:','https:')) else None)
   p.goto((R/'review.html').as_uri());assert p.locator('article').count()==25
   assert p.evaluate('[...document.images].every(i=>i.complete&&i.naturalWidth>0)') and p.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert not errors and not external;c.close()
  b.close()
 print('PASS six ledger regressions and two offline report viewports')
