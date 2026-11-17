import unittest,json,pathlib,hashlib
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
class ReviewTests(unittest.TestCase):
 def setUp(self):self.d=json.loads((R/'review-ledger.json').read_text());self.rows=self.d['entries']
 def test_exact_roster(self):
  ids=json.loads((R/'assigned.json').read_text());self.assertEqual(len(self.rows),25);self.assertEqual(len({x['id'] for x in self.rows}),25);self.assertEqual(set(ids),{x['id'] for x in self.rows})
 def test_holds(self):
  self.assertEqual({x['id'] for x in self.rows if x['verdict']=='needs-decision'},set('arctic-ocean bolivia cabo-verde indian-ocean mozambique saint-vincent-and-the-grenadines sierra-leone'.split()))
 def test_parent_hold_preservation(self):
  p={x['id']:x for x in json.loads((R/'parent-ledger.json').read_text())['entries']}
  for x in self.rows:self.assertEqual(x['inherited_missing_gates'],p[x['id']]['missing_gates']);self.assertFalse(x['final_approval']);self.assertFalse(x['art_changed']);self.assertFalse(x['launch_ready'])
 def test_capture_identity(self):
  for x in self.rows:
   self.assertEqual(len(x['captures']),4)
   for c in x['captures']:self.assertEqual(hashlib.sha256((R/c['path']).read_bytes()).hexdigest(),c['sha256']);self.assertEqual(c['viewer_sha256'],x['viewer']['sha256'])
 def test_measured_runtime(self):
  for x in self.rows:
   self.assertLess(x['viewer']['bytes'],5000000);self.assertEqual(len(x['browser']),2);self.assertTrue(all(y['result']=='pass' for y in x['browser']));self.assertTrue(x['motion']['passed']);self.assertTrue(x['extended']['no_js_poster']);self.assertFalse(x['fresh_source_reopen_parity_collision']);self.assertFalse(x['fresh_corrupt_glb_fallback'])
 def test_report_offline(self):
  with sync_playwright() as pw:
   b=pw.chromium.launch(channel='msedge',headless=True)
   for w,h in [(1440,1080),(390,844)]:
    c=b.new_context(offline=True,viewport={'width':w,'height':h});p=c.new_page();errors=[];req=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:req.append(r.url) if r.url.startswith(('http:','https:')) else None);p.goto((R/'review.html').as_uri());self.assertEqual(p.locator('section').count(),25);self.assertTrue(p.evaluate('Array.from(document.images).every(x=>x.complete&&x.naturalWidth>0)'));self.assertTrue(p.evaluate('document.documentElement.scrollWidth<=innerWidth'));self.assertEqual(errors,[]);self.assertEqual(req,[]);c.close()
   b.close()
if __name__=='__main__':unittest.main(verbosity=2)
