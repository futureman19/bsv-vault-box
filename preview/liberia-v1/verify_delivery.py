from pathlib import Path
import json,hashlib,io,struct
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
b=(R/'liberia.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);raw=b[28+n:];maps=[]
for im in g['images']:
 v=g['bufferViews'][im['bufferView']];data=raw[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];img=Image.open(io.BytesIO(data));ext=img.convert('RGB').getextrema();assert max(c[1]-c[0] for c in ext)>0;maps.append({'name':im.get('name'),'size':img.size,'extrema':ext})
with sync_playwright() as p:
 browser=p.chromium.launch(channel='msedge',headless=True)
 c=browser.new_context(java_script_enabled=False,offline=True);page=c.new_page();page.goto((R/'liberia-v1.html').as_uri());assert page.locator('#fallback').is_visible();assert page.locator('#open').is_disabled();browser.close()
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
cases=json.loads((R/'browser-check.json').read_text());assert len(cases)==3
assert (R/'liberia-v1.html').stat().st_size<5000000
required=['liberia-v1.html','liberia.glb','liberia.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','mechanism.blend','source-check.json','parity-check.json','browser-check.json','theme-check.json']
assert all((R/f).is_file() for f in required)
files=[p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['inventory.json','delivery-check.json','delivery-output.txt'] and not p.name.endswith('.blend1')]
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
for f,x in json.loads((R/'inventory.json').read_text()).items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==x['sha256']
r={'status':'PASS','html_bytes':(R/'liberia-v1.html').stat().st_size,'glb_bytes':len(b),'decoded_maps':maps,'no_js_fallback':True,'required_artifacts':required,'inventory_files':len(inventory),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'exclusions':['inventory.json and delivery-check.json avoid recursive self hashes'],'scope':'Local file delivery, no archive/upload/mint/deployment'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',r['html_bytes'],r['glb_bytes'],len(inventory))
