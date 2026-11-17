import unittest,json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
L=json.loads((R/'reviewed-ledger.json').read_text());P=json.loads((R/'parent/review-ledger.json').read_text());A=json.loads((R/'audit-results.json').read_text())
class Review(unittest.TestCase):
 def test_exact_roster(self):
  ids=[x['id'] for x in L['entries']];self.assertEqual(len(ids),25);self.assertEqual(len(set(ids)),25);self.assertEqual(set(ids),{x['id'] for x in P['entries']});self.assertEqual(L['unreviewed_ids'],[])
 def test_holds(self):
  self.assertEqual({x['id'] for x in L['entries'] if x['verdict']=='needs-user-review'},{x['id'] for x in P['entries'] if x['verdict']=='needs-decision'})
 def test_not_approval(self):
  for e in L['entries']:self.assertFalse(e['final_approval']);self.assertFalse(e['launch_ready']);self.assertFalse(e['art_changed']);self.assertIn('explicit-final-user-art-approval',e['missing_gates'])
 def test_historical_separation(self):
  for e in L['entries']:
   for k in ['runtime','motion','blender_parity_collision','fallback','full_inner_archive_inventories']:self.assertFalse(e['fresh_checks'][k])
   self.assertEqual(e['historical_runtime']['parent_commit'],L['parent_commit'])
 def test_payloads_and_captures(self):
  self.assertEqual(len(A['source_checks']),25);self.assertEqual(A['parent_evidence_hashes'],302);self.assertEqual(len(A['parent_zips']),3)
  for e in L['entries']:
   self.assertLess(e['viewer']['bytes'],5000000);self.assertEqual(len(e['captures']),4)
   for c in e['captures']:self.assertEqual(hashlib.sha256((R/'parent'/c['path']).read_bytes()).hexdigest(),c['sha256']);self.assertEqual(c['viewer_sha256'],e['viewer']['sha256'])
 def test_report_offline(self):
  from playwright.sync_api import sync_playwright
  results=[]
  with sync_playwright() as p:
   b=p.chromium.launch(channel='msedge',headless=True)
   for w,h in [(1440,1080),(390,844)]:
    c=b.new_context(offline=True,viewport={'width':w,'height':h});page=c.new_page();errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((R/'review.html').as_uri());self.assertEqual(page.locator('article').count(),25);self.assertTrue(page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'));self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'));self.assertEqual(errors,[]);self.assertEqual(requests,[]);page.screenshot(path=str(R/('report-'+str(w)+'.png')));results.append({'width':w,'height':h,'articles':25,'images_loaded':25,'errors':errors,'external_requests':requests,'overflow':False});c.close()
   b.close()
  (R/'report-browser.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':unittest.main()
