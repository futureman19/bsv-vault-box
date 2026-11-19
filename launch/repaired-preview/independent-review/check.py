import json,hashlib,zipfile,collections
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
E=Path(__file__).parent
O=ROOT/'preview/repaired-collection-v1'
D=ROOT/'launch/repaired-preview/delivery'
R=D/'recovered'
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((O/'manifest.json').read_bytes()); inv=json.loads((O/'inventory.json').read_bytes()); entries=m['entries']
b=json.loads((ROOT/'launch/repaired-preview/inputs/baseline.json').read_bytes())['entries']
assert len(entries)==201 and len({e['id'] for e in entries})==201
assert collections.Counter(e['id'] for e in entries)==collections.Counter(e['id'] for e in b)
base={e['id']:next(f['sha256'] for f in e['files'] if f['role']=='viewer') for e in b}
changed={e['id']:e['viewer']['version'] for e in entries if e['viewer']['sha256']!=base[e['id']]}
assert len(changed)==17
assert 'v10' in changed['united-states'].lower() and 'v2' in changed['bangladesh'].lower()
assert all((e['change']!='unchanged')==(e['id'] in changed) for e in entries)
expected=['cabo-verde','iceland','indonesia','lithuania','malta','morocco','mozambique','pacific-ocean','saint-vincent-and-the-grenadines','sao-tome-and-principe','united-states']
assert sorted(e['id'] for e in entries if e['disposition']=='substantive-feature-hold')==expected
assert all(not e['launch_ready'] and not e['final_user_approved'] for e in entries)
for e in entries:
 for role in ['viewer','marketing','poster']:
  f=e[role]; data=(O/f['url']).read_bytes();assert sha(data)==f['sha256'] and len(data)==f['bytes']
with zipfile.ZipFile(D/'boxsv-repaired-collection-v1-hostable.zip') as z:
 names=z.namelist();assert len(names)==len(set(names))==609
 for name in names:
  assert not name.startswith('/') and '..' not in Path(name).parts
  data=z.read(name);assert data==(R/name).read_bytes()==(O/name).read_bytes()
  if name in inv:assert sha(data)==inv[name]['sha256'] and len(data)==inv[name]['bytes']
 assert set(inv)==set(names)-{'inventory.json'}
attachment=D/'boxsv-repaired-collection-review.html'
assert attachment.read_bytes()==(R/'review.html').read_bytes()
result={'roster':201,'categories':dict(collections.Counter(e['category'] for e in entries)),'changed':changed,'change_types':dict(collections.Counter(e['change'] for e in entries)),'holds':expected,'manifest_payloads_hashed':603,'inventory_entries':len(inv),'zip_recovered_source_exact_entries':len(names),'zip_sha256':sha((D/'boxsv-repaired-collection-v1-hostable.zip').read_bytes()),'standalone_sha256':sha(attachment.read_bytes()),'cases':[]}
(E/'integrity.json').write_text(json.dumps(result,indent=2))
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for standalone in [False,True]:
  for mobile in [False,True]:
   label=('attachment' if standalone else 'recovered')+('-mobile' if mobile else '-desktop')
   ctx=browser.new_context(offline=True,viewport={'width':390 if mobile else 1440,'height':844 if mobile else 1000},is_mobile=mobile,has_touch=mobile,reduced_motion='reduce')
   page=ctx.new_page(); errors=[];external=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
   page.goto((attachment if standalone else R/'index.html').as_uri());page.wait_for_function('window.__collection?.count===201')
   assert page.locator('.card').count()==201
   page.screenshot(path=str(E/(label+'.png')))
   for cat,n in [('Country',195),('Ocean',5),('Moon',1),('All',201)]:
    page.locator('#category').select_option(cat);assert page.locator('.card').count()==n
   for scope,n in [('changed',17),('hold',11)]:
    page.locator('#scope').select_option(scope);assert page.locator('.card').count()==n
   page.locator('#reset').click()
   page.locator('#search').fill('the moon');assert page.locator('.card').count()==1 and page.locator('.card').get_attribute('data-id')=='the-moon'
   page.locator('#search').fill('no-such-box-zz');assert page.locator('#empty').is_visible();page.locator('#reset').click()
   for query in ['united states','bangladesh']:
    page.locator('#search').fill(query);assert page.locator('.card').count()==1
    card=page.locator('.card');card.tap() if mobile else card.click();page.wait_for_selector('dialog[open]')
    assert page.locator('#close').evaluate('(e)=>e===document.activeElement')
    for key in ['Tab']*12+['Shift+Tab']*12:
     page.keyboard.press(key);assert page.evaluate("document.activeElement===document.body || document.querySelector('dialog').contains(document.activeElement)")
    page.locator('#search').evaluate('(e)=>e.focus()');assert not page.locator('#search').evaluate('(e)=>e===document.activeElement')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(E/(label+'-'+query.replace(' ','-')+'-detail.png')))
    if not standalone:
     page.locator('#load-model').click()
     page.wait_for_function("document.querySelector('iframe')?.contentWindow.pilot?.ready===true",timeout=60000)
     f=page.frame_locator('#interactive iframe');f.locator('#open').tap() if mobile else f.locator('#open').click()
     page.wait_for_function("document.querySelector('iframe').contentWindow.pilot.progress===1",timeout=30000)
     page.screenshot(path=str(E/(label+'-'+query.replace(' ','-')+'-open.png')))
     f.locator('#reset').tap() if mobile else f.locator('#reset').click()
     page.wait_for_function("document.querySelector('iframe').contentWindow.pilot.progress===0")
     page.locator('#load-model').click();assert page.locator('iframe').count()==0
    else:assert page.locator('#load-model').is_hidden() and page.locator('#full-viewer').is_hidden()
    page.locator('#close').tap() if mobile else page.locator('#close').click()
    page.wait_for_selector('dialog[open]',state='hidden');assert card.evaluate('(e)=>e===document.activeElement')
    card.focus();page.keyboard.press('Enter');page.wait_for_selector('dialog[open]');page.keyboard.press('Escape');page.wait_for_selector('dialog[open]',state='hidden');assert card.evaluate('(e)=>e===document.activeElement')
   page.locator('#reset').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   decoded=page.evaluate("async()=>{let n=0;for(const e of DATA)for(const k of ['poster','marketing']){let im=new Image();im.src=e[k].url;await im.decode();n++}return n}")
   assert decoded==402 and not errors and not external,(errors,external)
   result['cases'].append({'case':label,'pass':True,'decoded_images':decoded,'errors':errors,'external_requests':external,'iframe_USA_Bangladesh_open_reset':not standalone})
   (E/'results.json').write_text(json.dumps(result,indent=2));ctx.close()
 browser.close()
print(json.dumps(result,indent=2))
