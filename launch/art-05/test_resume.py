import unittest,json,pathlib,hashlib
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
class ReviewTests(unittest.TestCase):
 def setUp(self): self.d=json.loads((R/'review-ledger.json').read_text())
 def test_roster(self):
  self.assertEqual(len(self.d['entries']),25);self.assertEqual({e['id'] for e in self.d['entries']},set(self.d['assigned']));self.assertEqual(self.d['uncompleted_ids'],[])
 def test_no_approval_or_art_edits(self):
  self.assertTrue(all(not e['user_final_approved'] and not e['art_changed'] and e['review_complete'] for e in self.d['entries']))
 def test_holds_retained(self):
  es={e['id']:e for e in self.d['entries']}
  for s in ['azerbaijan','chile','iceland','lithuania','new-zealand','pacific-ocean','saint-kitts-and-nevis','venezuela']:self.assertEqual(es[s]['status'],'needs-decision')
  for s in ['iceland','new-zealand']:self.assertTrue(es[s]['package_holds'])
 def test_candidate_bytes(self):
  for e in self.d['entries']:
   v=e['packaging']['viewer'];b=pathlib.Path(e['source_record']['delivered_viewer']['path']).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),v['sha256']);self.assertLess(len(b),5000000)
 def test_historical_labels(self):
  self.assertIn('not rerun',self.d['technical_evidence']);self.assertIn('No fresh Blender reopening/source parity/collision sampling',self.d['limitations'])
 def test_offline_report(self):
  with sync_playwright() as pw:
   b=pw.chromium.launch(channel='msedge',headless=True)
   for w,h in [(1440,1080),(390,844)]:
    c=b.new_context(offline=True,viewport={'width':w,'height':h});p=c.new_page();errs=[];req=[];p.on('pageerror',lambda e:errs.append(str(e)));p.on('request',lambda r:req.append(r.url) if r.url.startswith(('http:','https:')) else None)
    p.goto((R/'review.html').as_uri());p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)');self.assertEqual(p.locator('section').count(),25);self.assertTrue(p.evaluate('document.documentElement.scrollWidth<=innerWidth'));self.assertFalse(errs);self.assertFalse(req);c.close()
   b.close()
if __name__=='__main__':unittest.main()
