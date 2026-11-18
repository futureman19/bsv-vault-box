from pathlib import Path
import json,subprocess,hashlib
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;REPO=R.parents[1]
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for ident,ref in [('cabo-verde','4ba628e8aee53db399067ebe1e82f3d8d2b15feb'),('saint-vincent-and-the-grenadines','b9010bff23da564a81a1d98efba5f6821b5b62b0')]:
  folder=REPO/'preview'/f'{ident}-view-v2';proof=[]
  for n in [ident+'.glb',ident+'.blend','motion.mjs']:
   old=subprocess.check_output(['git','show',ref+':preview/'+ident+'-v1/'+n]);current=(folder/n).read_bytes();assert current==old
   proof.append({'file':n,'sha256':hashlib.sha256(current).hexdigest(),'exact_baseline':True})
  c=b.new_context(offline=True,viewport={'width':390,'height':844},reduced_motion='reduce');p=c.new_page();panels=[]
  for version,path in [('Before',folder/'historical-v1'/f'{ident}-v1.html'),('Camera trial',folder/f'{ident}-view-v2.html')]:
   p.goto(path.as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(150);dest=folder/('compare-'+version.split()[0].lower()+'.png');p.screenshot(path=str(dest),full_page=True);panels.append(Image.open(dest).convert('RGB'))
  board=Image.new('RGB',(780,884),(16,21,26));d=ImageDraw.Draw(board)
  for i,im in enumerate(panels):board.paste(im,(i*390,40));d.text((i*390+15,12),['Original camera','Raised camera; SAME geometry'][i],fill='white')
  board.save(folder/'camera-comparison.jpg',quality=92)
  c.close();rows.append({'id':ident,'unchanged_payloads':proof,'camera_only':True,'visual_result':'Partial only; crater remains weak at normal mobile size. Owner hold retained.'})
 # Exact extracted canonical viewers from all six repaired packages.
 report=json.loads((R/'packages-02/report.json').read_text())
 for e in report['packages']:
  folder=R/'packages-02'/(e['id']+'-recovered');inv=json.loads((folder/'inventory.json').read_text());name=next(n for n in inv['required'] if n.endswith('.html'))
  c=b.new_context(offline=True,viewport={'width':390,'height':844},has_touch=True,is_mobile=True,reduced_motion='reduce');p=c.new_page();errors=[];network=[]
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
  p.goto((folder/name).as_uri());p.wait_for_function('pilot.ready',timeout=90000);p.locator('#open').tap();p.wait_for_function('pilot.progress===1');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.screenshot(path=str(R/(e['id']+'-recovered-open.png')),full_page=True)
  p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');assert not errors and not network;c.close()
  rows.append({'id':e['id'],'canonical_recovered_viewer':name,'offline_mobile_open_reset':True,'errors':errors,'external_requests':network})
 b.close()
(R/'recovery-browser.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
