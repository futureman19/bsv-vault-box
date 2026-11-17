import pathlib,json,unittest,hashlib
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent; d=json.loads((R/'reviewed-ledger.json').read_text()); p=json.loads((R/'parent/review-results.json').read_text())
class Ledger(unittest.TestCase):
 def test_roster(self):self.assertEqual(d['assigned'],[e['id'] for e in p['entries']]);self.assertEqual(len(set(d['assigned'])),25)
 def test_holds(self):self.assertEqual(d['visual_holds'],['malta']);self.assertEqual(d['packaging_holds'],['rwanda']);self.assertEqual(d['counts'],{'candidate-with-limitations':23,'needs-user-review':2})
 def test_approval(self):self.assertTrue(all(not e['user_final_approved'] and not e['launch_ready'] and not e['art_changed'] for e in d['entries']))
 def test_runtime(self):self.assertEqual(sum(len(e['fresh_browser']) for e in d['entries']),50);self.assertTrue(all(b['result']=='pass' for e in d['entries'] for b in e['fresh_browser']));self.assertTrue(all(e['fresh_motion']['exit_code']==0 for e in d['entries']))
 def test_gates(self):
  for e in d['entries']:
   self.assertEqual(set(e['parent_remaining_gates'])-{'independent-current-model-visual-review','independent QA-ART-04 review'},set(e['remaining_gates']))
 def test_archive(self):
  bad=[(e['id'],c) for e in d['entries'] for a in e['source_archive_audit']['archives'] for c in a['selected_payload_checks'] if not c['matches_selected_bytes']];self.assertEqual(len(bad),1);self.assertEqual(bad[0][0],'rwanda');self.assertTrue(bad[0][1]['newline_only_difference']);self.assertEqual(d['tests']['archive_inventory_members'],1344)
suite=unittest.defaultTestLoader.loadTestsFromTestCase(Ledger);result=unittest.TextTestRunner(verbosity=2).run(suite);assert result.wasSuccessful()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True)
 for w,h in [(1440,1080),(390,844)]:
  c=b.new_context(offline=True,viewport={'width':w,'height':h});page=c.new_page();errs=[];req=[];page.on('pageerror',lambda e:errs.append(str(e)));page.on('request',lambda r:req.append(r.url) if r.url.startswith(('http:','https:')) else None);page.goto((R/'review.html').as_uri());assert page.locator('article').count()==25;assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');assert not errs and not req;c.close()
 b.close()
print('PASS six ledger tests and two offline report viewports')
