import json,pathlib,hashlib,subprocess
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
ids=json.loads((R/'assigned.json').read_text()); d=json.loads((R/'review-results.json').read_text())
assert len(ids)==len(set(ids))==25 and d['assigned']==ids and d['unreviewed']==[]
assert {e['id'] for e in d['entries']}==set(ids) and len(d['entries'])==25
assert d['counts']=={'needs-decision':12,'pass':13}
for e in d['entries']:
 assert not e['user_final_approved'] and not e['launch_ready'] and not e['model_changed'] and e['polish_iterations']==0
 assert e['viewer']['bytes']<5000000
 assert len(e['captures'])==4 and all((R/p).is_file() for p in e['captures'])
 assert len(e['browser'])==2 and all(x['result']=='pass' for x in e['browser'])
 assert e['motion']['passed']
 parent=next(x for x in json.loads((R/'launch-candidates.json').read_text())['entries'] if x['id']==e['id'])
 assert e['inherited_missing_gates']==parent['missing_gates']
assert next(e for e in d['entries'] if e['id']=='paraguay')['source_archives'] and 'unchecked' in next(e for e in d['entries'] if e['id']=='paraguay')['visual_findings']
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True)
 for w,h in [(1440,1080),(390,844)]:
  c=browser.new_context(offline=True,viewport={'width':w,'height':h});p=c.new_page();errors=[];requests=[]
  p.on('pageerror',lambda x:errors.append(str(x)));p.on('request',lambda x:requests.append(x.url) if x.url.startswith(('http:','https:')) else None)
  p.goto((R/'review.html').as_uri());assert p.locator('article').count()==25
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert p.evaluate('[...document.images].every(i=>i.complete && i.naturalWidth>0)')
  assert not errors and not requests;c.close()
 browser.close()
print('PASS: 25 roster/hold/art-immutability/capture records, 50 browser records, 25 motion records, 2 offline report sizes')
if '--staged' in __import__('sys').argv:
 inv=json.loads((R/'evidence-inventory.json').read_text())['files']
 for e in inv:
  b=subprocess.check_output(['git','show',':launch/art-03/'+e['path']]);assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
 print('PASS staged exact-byte inventory',len(inv))
