"""Bounded acceptance aggregation, exact inventory, ZIP readback + extracted HTML test."""
from pathlib import Path
import json,hashlib,zipfile,tempfile
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
sha=lambda data:hashlib.sha256(data).hexdigest()
load=lambda f:json.loads((R/f).read_text())
source=load('source-check.json');assert source['collision_samples']==81 and not source['collisions'] and source['saved_source_reopened']
assert len(load('hinge-attachment-check.json')['intersecting_attachment_pairs'])==10
parity=load('parity-check.json');assert max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
assert load('theme-check.json')['status']=='PASS' and load('extended-check.json')['status']=='PASS'
browser=load('browser-check.json');assert len(browser)==3
for b in browser[:2]:
 assert b['offline_file'] and not b['external_requests'] and not b['errors'] and b['reduced_motion'] and b['open_close'] and b['reset_mid_motion'] and not b['overflow']
 assert b['asset']['nonfinite']==b['asset']['degenerate']==0
assert browser[-1]['fallback']
assert 'fail 0' in (R/'motion-output.txt').read_text(encoding='utf8')
html=R/'canada-v1.html';glb=R/'canada.glb';assert 0<html.stat().st_size<5_000_000
required={'canada-v1.html','canada.glb','canada.blend','mechanism.blend','design-brief.md','README.md','author.py','maps.py','build.py','poster.png','poster.jpg','viewer.js','motion.mjs','template.html','THREE-LICENSE.txt','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','hinge-attachment-check.json','package.json','package-lock.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','desktop-open-rear.png','.gitattributes'}
checks=['source','hinge-attachments','parity','theme','motion','browser-desktop','browser-mobile','corrupt-GLB-fallback','no-JS-fallback','runtime-maps','poster-pixels','payload-budget']
(R/'acceptance-check.json').write_text(json.dumps(dict(status='PASS',checks_passed=checks,html_bytes=html.stat().st_size,glb_bytes=glb.stat().st_size),indent=2))
skip={'inventory.json','delivery-check.json','package-output.txt','git-verification.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(v in ['node_modules','__pycache__','delivery-probe'] for v in p.relative_to(R).parts) and p.name not in skip and p.suffix not in ['.zip','.blend1','.pyc']}
assert required<=files.keys(),required-files.keys()
inv={name:dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for name,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
archive=R/'canada-v1-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name,p in sorted(files.items()):z.write(p,name)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for name,m in inv.items():
  data=z.read(name);assert len(data)==m['bytes'] and sha(data)==m['sha256'],name
 with tempfile.TemporaryDirectory(prefix='delivery-probe-',dir=R) as d:
  target=Path(d)/html.name;target.write_bytes(z.read(html.name))
  with sync_playwright() as pw:
   b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,reduced_motion='reduce',viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();errors=[];req=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:req.append(r.url) if r.url.startswith(('http:','https:')) else None);p.goto(target.as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');assert not errors and not req;b.close()
r=dict(status='PASS',html_bytes=html.stat().st_size,glb_bytes=glb.stat().st_size,html_sha256=sha(html.read_bytes()),glb_sha256=sha(glb.read_bytes()),zip_bytes=archive.stat().st_size,zip_sha256=sha(archive.read_bytes()),inventory_sha256=sha((R/'inventory.json').read_bytes()),payload_files=len(files),zip_entries=len(files)+1,required_artifact_set_complete=True,all_archived_bytes_readback_match=True,extracted_html_offline_touch_open_reset=True,checks_passed=checks+['delivery'])
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('ALL ACCEPTANCE CHECKS PASS');print('HTML_BYTES',r['html_bytes'],'GLB_BYTES',r['glb_bytes']);print(json.dumps(r,indent=2))
