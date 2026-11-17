import json,pathlib,unittest
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
class QA(unittest.TestCase):
 def setUp(self):self.d=json.loads((R/'reviewed-ledger.json').read_text())
 def test_roster(self):
  self.assertEqual(len(self.d['entries']),25);self.assertEqual(len(set(self.d['assigned'])),25);self.assertEqual(set(self.d['assigned']),{e['id'] for e in self.d['entries']})
 def test_no_approval(self):self.assertTrue(all(not e['user_final_approved'] and not e['launch_ready'] and not e['art_changed'] for e in self.d['entries']))
 def test_holds(self):
  self.assertEqual(self.d['needs_user_review'],['azerbaijan','chile','iceland','lithuania','new-zealand','pacific-ocean','saint-kitts-and-nevis','venezuela'])
  for e in self.d['entries']:
   if e['id'] in ['iceland','new-zealand']:self.assertTrue(e['package_holds'])
 def test_capture_coverage(self):self.assertEqual(sum(len(e['inspected_images']) for e in self.d['entries']),125)
 def test_historical_labels(self):self.assertTrue(all(e['historical_runtime_only'] for e in self.d['entries']))
 def test_report_offline(self):
  with sync_playwright() as pw:
   b=pw.chromium.launch(channel='msedge',headless=True)
   for w,h in [(1440,1080),(390,844)]:
    c=b.new_context(offline=True,viewport={'width':w,'height':h});p=c.new_page();errors=[];requests=[]
    p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
    p.goto((R/'review.html').as_uri());p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
    self.assertEqual(p.locator('article').count(),25);self.assertFalse(errors);self.assertFalse(requests);self.assertTrue(p.evaluate('document.documentElement.scrollWidth<=innerWidth'));c.close()
   b.close()
if __name__=='__main__':unittest.main()
